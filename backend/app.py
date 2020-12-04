from flask import Flask, Response, url_for, request, render_template
from flask_talisman import Talisman
from . import encoding
from .import pydub_helpers
from .model import *
from flask_socketio import SocketIO
import os
import redis

app = Flask(__name__,
    static_folder = '../dist/static',
    template_folder = '../dist'
)

# Open up websockets
socketio = SocketIO(app)
redis = redis.from_url(os.environ['REDIS_URL'])

#Talisman(app)

@app.route('/')
def index():
    return render_template('index.html')

def create_new_song(payload):
    print([key for key in payload])
    # Interpret the audio clip as requested
    segment = pydub_helpers.read_arbitrary(payload['audio'], format=payload['format'])
    segment = segment[payload['time'][0]:payload['time'][1]]

    repeat = (
        payload['repeat'][0] - payload['time'][0],
        payload['repeat'][1] - payload['time'][0]
    )

    # Create a new song entry
    song = Song()

    song.name.set(payload['name'])
    song.credits.set(payload['credits'])

    mid = len(segment) // 2

    song.first_range_start.set(
        min(repeat[0], mid)
    )
    song.first_range_end.set(
        min(repeat[1], mid)
    )

    song.second_range_start.set(
        max(repeat[0], mid) - mid
    )
    song.second_range_end.set(
        max(repeat[1], mid) - mid
    )

    song.repeat_start.set(payload['repeat'][0])
    song.repeat_end.set(payload['repeat'][1])

    song.first_half.set(pydub_helpers.as_mp3(segment[:len(segment) // 2]))
    song.second_half.set(pydub_helpers.as_mp3(segment[len(segment) // 2:]))

    return song

@app.route('/api/create-room', methods=['POST'])
def create_room():
    payload = encoding.decode(request.data)

    room = Room()

    room.expiration.set(payload['expiration'])

    room.title.set(payload['title'])
    # room.password.set(payload['password']) # TODO any real password system

    bulletin = []

    for item in payload['bulletin']:
        bulletin_item = {
            'title': item['title'],
            'description': item['description']
        }
        if 'accompaniment' in item:
            song = create_new_song(item['accompaniment'])
            bulletin_item['accompaniment'] = {
                'name': item['accompaniment']['name'],
                'credits': item['accompaniment']['credits'],
                'repeat': item['accompaniment']['repeat'],
                'id': song.pk.get()
            }
        bulletin.append(bulletin_item)

    room.bulletin.set(encoding.encode(bulletin))

    for i, item in enumerate(bulletin):
        room.program.hset(i,
            -1 if 'accompaniment' not in item else item['accompaniment']['id']
        )

    return encoding.encode({'room_id': room.pk.get()})

@app.route('/api/get-bulletin')
def get_bulletin():
    room_id = request.args['room_id']

    room = Room(room_id)

    return room.bulletin.get()

@app.route('/api/get-mixed')
def get_mixed():
    room_id = request.args['room_id']
    user_id = request.args['user_id']
    hearme = (request.args['hearme'] == 'true')
    index = int(request.args['index'])
    parity = int(request.args['parity'])

    room = Room(room_id)

    song_pk = room.program.hget(index).decode('utf-8')
    song = Song(song_pk)

    return encoding.encode({
        'audio': pydub_helpers.as_mp3(room.mix(index, parity, (-1 if hearme else user_id))),
        'range': [
            int(song.first_range_start.get()),
            int(song.first_range_end.get())
        ] if parity == 0 else [
            int(song.second_range_start.get()),
            int(song.second_range_end.get())
        ]
    })

@app.route('/api/submit-audio', methods=['POST'])
def submit_audio():
    user_id = request.args['user_id']
    index = int(request.args['index'])
    parity = int(request.args['parity'])
    payload = encoding.decode(request.data)

    try:
        user = User(user_id)
        user.update_audio(index, parity,
                pydub_helpers.read_opus(payload['audio']), payload['offset'])

        return encoding.encode({'success': True})

    except Exception as e:
        return encoding.encode({'success': False})


@app.route('/api/heartbeat')

@app.route('/api/download-audio')
def download_audio():
    song_id = request.args['song_id']

    song = Song(song_id)

    segment_0 = pydub_helpers.read_mp3(
        song.first_half.get()
    )
    segment_1 = pydub_helpers.read_mp3(
        song.second_half.get()
    )

    return Response(pydub_helpers.as_mp3(segment_0 + segment_1), mimetype='audio/mpeg')

# Socket.io for presence and start/stop commands
sid_uid = {}
sid_room = {}
# New socket => new user
@socketio.on('register')
def register(json):
    room_pk = json['rid']
    name = json['name']

    try:
        room = Room(room_pk)

        join_room(room_pk)

        user_pk = room.new_user(name)

        sid_uid[request.sid] = user_pk
        sid_rid[request.sid] = room_pk

        socket.emit('uid', user_pk)

    except limpyd.exceptions.DoesNotExist:
        pass

@socketio.on('stop-song')
def stop_song(json):
    room_pk = sid_room[request.sid]
    room = Room(room_pk)

    room.stop_singing()

    update_status(room_pk)

@socketio.on('start-song')
def set_index(json):
    room_id = request.args['room_id']
    index = int(request.args['index'])

    room = Room(room_id)

    room.set_index(json['index'])
    room.start_singing()

    update_status(room_pk)

# Disconnect => remove previous user
@socketio.on('disconnect')
def disconnect():
    if request.sid in sid_uid:
        room_pk = sid_room[request.sid]

        user = User(sid_uid[request.sid])
        user.remove_self_and_close()

        update_status(room_pk)

def update_status(room_pk):
    room = Room(room_pk)
    socketio.emit(
        'update',
        room.get_state(),
        broadcast=True,
        room=room_pk
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
