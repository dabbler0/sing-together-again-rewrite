from flask import Flask, Response, url_for, request, render_template
from . import encoding
from .import pydub_helpers
from .model import *

app = Flask(__name__,
    static_folder = '../dist/static',
    template_folder = '../dist'
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/song-list')
def list_songs():
    song_pks = list(Song.collection())
    return encoding.encode(
        [Song(pk.decode('utf-8')).metadata() for pk in song_pks]
    )

@app.route('/api/new-song', methods=['POST'])
def submit_new_song():
    payload = encoding.decode(request.data)

    # Interpret the audio clip as requested
    segment = pydub_helpers.read_arbitrary(payload['audio'], format=payload['format'])
    segment = segment[payload['start-time']:payload['end-time']]

    print('start time', payload['start-time'], 'end time', payload['end-time'])
    print(len(segment))

    # Create a new song entry
    song = Song()

    song.name.set(payload['name'])
    song.credits.set(payload['credits'])
    song.first_half.set(pydub_helpers.as_mp3(segment[:len(segment) // 2]))
    song.second_half.set(pydub_helpers.as_mp3(segment[len(segment) // 2:]))

    return encoding.encode({'success': True, 'id': song.pk.get()})

@app.route('/api/create-room', methods=['POST'])
def create_room():
    bulletin = encoding.decode(request.data)

    room = Room()

    room.bulletin.set(encoding.encode(bulletin))

    for i, item in enumerate(bulletin):
        room.program.hset(i, item['song'])

    return encoding.encode({'room_id': room.pk.get()})


@app.route('/api/get-bulletin')
def get_bulletin():
    room_id = request.args['room_id']

    room = Room(room_id)

    return room.bulletin.get().decode('utf-8')

@app.route('/api/start-song')
def set_index():
    room_id = request.args['room_id']
    index = int(request.args['index'])

    room = Room(room_id)

    room.set_index(index)
    room.start_singing()

    return encoding.encode({'success': True})

@app.route('/api/join-room')
def join_room():
    room_id = request.args['room_id']
    name = request.args['name']

    room = Room(room_id)

    return encoding.encode({
        'user_id': room.new_user(name)
    })

@app.route('/api/get-mixed')
def get_mixed():
    room_id = request.args['room_id']
    user_id = request.args['user_id']
    index = int(request.args['index'])
    parity = int(request.args['parity'])

    room = Room(room_id)

    return encoding.encode({
        'audio': pydub_helpers.as_mp3(room.mix(index, parity, user_id))
    })

@app.route('/api/submit-audio', methods=['POST'])
def submit_audio():
    user_id = request.args['user_id']
    index = int(request.args['index'])
    parity = int(request.args['parity'])
    payload = encoding.decode(request.data)

    user = User(user_id)
    user.update_audio(index, parity,
            pydub_helpers.read_opus(payload['audio']), payload['offset'])

    return encoding.encode({'success': True})

@app.route('/api/heartbeat')
def heartbeat():
    user_id = request.args['user_id']

    user = User(user_id)
    user.heartbeat()

    room_id = user.room.get().decode('utf-8')
    room = Room(room_id)

    # TODO potentially handle cleanup at a different time,
    # or different parts of cleanup at different times?
    room.cleanup()

    print('responding with', room.get_state())

    return encoding.encode(room.get_state())

@app.route('/api/stop-song')
def stop_song():
    room_id = request.args['room_id']

    room = Room(room_id)

    room.stop_singing()

    return encoding.encode({'success': True})

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

    return Response(as_mp3(segment_0 + segment_1), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
