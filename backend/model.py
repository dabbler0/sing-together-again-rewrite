from limpyd import model
import time
from . import encoding
from . import pydub_helpers
from urllib.parse import urlparse
import math
import os

url = os.environ.get('REDIS_URL')
parsed = urlparse(url)

database = model.RedisDatabase(
    host = parsed.hostname,
    username = parsed.username,
    password = parsed.password,
    port = parsed.port,
    decode_responses = False
)

class Room(model.RedisModel):
    database = database

    title = model.StringField()
    expiration = model.StringField()

    program = model.HashField()
    bulletin = model.StringField()

    index = model.StringField(default=-1)
    singing = model.StringField(default=0)
    users = model.SetField()

    def get_users(self):
        result = self.users.smembers()
        if result is None:
            return []
        return [
            User(user_pk.decode('utf-8')).metadata()
            for user_pk in result
        ]

    def new_user(self, name):
        '''
        Add a new user to this room, returning
        their user id.

        returns: str
        '''

        user = User()

        user.name.set(name)
        user.room.set(self.pk.get())
        user.last_active.set(int(time.time() * 1000))

        print('Created user and set last active')

        user_pk = user.pk.get()

        self.users.sadd(user_pk)

        return user_pk

    def mix(self, index, parity, exclude_user_pk):
        '''
        Get mixed audio for a given service element
        and given parity, excluding audio from a certain user. Takes:

        index: int
        parity: int
        exclude_user_pk: str

        returns: AudioSegment
        '''

        song_pk = self.program.hget(index).decode('utf-8')
        song = Song(song_pk)

        repeat_range = [
            int(song.first_range_start.get()),
            int(song.first_range_end.get()),
        ] if parity == 0 else [
            int(song.second_range_start.get()),
            int(song.second_range_end.get()),
        ]

        repeat_length = repeat_range[1] - repeat_range[0]

        if parity == 0:
            result = pydub_helpers.read_mp3(song.first_half.get())
        else:
            result = pydub_helpers.read_mp3(song.second_half.get())

        # Count how many things we will overlay
        overlays = 1
        for user_pk in self.users.smembers():
            user_pk = user_pk.decode('utf-8')

            if user_pk == exclude_user_pk:
                continue

            user = User(user_pk)

            attempt = user.get_audio(index, parity)

            if attempt is not None:
                overlays += 1

        # Turn down the volume by an appropriate amount
        gain = -math.log(overlays, 10 ** 0.1)
        print('Applying gain', gain)

        # Overlay them, with a gain
        for user_pk in self.users.smembers():
            user_pk = user_pk.decode('utf-8')
            print('processing user', user_pk)

            if user_pk == exclude_user_pk:
                continue

            user = User(user_pk)

            attempt = user.get_audio(index, parity)

            if attempt is not None:
                audio, offset = attempt
                audio = audio[:repeat_length - offset].apply_gain(gain)
                result = result.overlay(audio, offset + repeat_range[0])

        return result

    def cleanup(self, thresh = 5000):
        '''
        Check to see whether any users should be removed from the room,
        and if any indices are now complete.
        '''
        wanted_indices = set()

        for user_pk in self.users.smembers():
            user_pk = user_pk.decode('utf-8')

            user = User(user_pk)
            
            # Remove any users who have not checked in within threshold time
            if time.time() * 1000 - int(user.last_active.get()) > thresh:
                self.users.srem(user_pk)
                user.close()
                user.delete()

            # For still-active users, see what index they want
            else:
                wants_index = user.wants_index.get()

                if wants_index is not None:
                    wanted_indices.add(int(wants_index))

        # Now tell everyone they can delete any indices that are
        # not in their wanted indices
        for user_pk in self.users.smembers():
            user_pk = user_pk.decode('utf-8')

            user = User(user_pk)

            for key in user.clips.hkeys():
                key = key.decode('utf-8')

                index = int(key.split('-')[0])

                if index not in wanted_indices:
                    sfile = File(user.clips.hget(key).decode('utf-8'))
                    sfile.delete()

                    user.clips.hdel(key)

    def get_bulletin(self):
        return encoding.decode(
            self.bulletin.get()
        )

    def get_state(self):
        return {
            'singing': self.singing.get().decode('utf-8') == '1',
            'index': int(self.index.get().decode('utf-8')),
            'users': self.get_users()

        }

    def stop_singing(self):
        self.singing.set(0)

    def start_singing(self):
        self.singing.set(1)

    def set_index(self, index):
        self.index.set(index)

    def close(self):
        for user_pk in self.users.smembers():
            user_pk = user_pk.decode('utf-8')

            user = User(user_pk)
            user.close()
            user.delete()

class Song(model.RedisModel):
    database = database

    name = model.StringField()
    credits = model.StringField()

    first_range_start = model.StringField()
    first_range_end = model.StringField()
    second_range_start = model.StringField()
    second_range_end = model.StringField()

    repeat_start = model.StringField()
    repeat_end = model.StringField()

    first_half = model.StringField()
    second_half = model.StringField()

    def metadata(self):
        return {
            'id': self.pk.get(),
            'name': self.name.get().decode('utf-8'),
            'credits': self.credits.get().decode('utf-8')
        }

class User(model.RedisModel):
    database = database

    name = model.StringField()

    room = model.StringField()
    clips = model.HashField()

    last_active = model.StringField()
    wants_index = model.StringField()

    def metadata(self):
        return {
            'id': self.pk.get(),
            'name': self.name.get().decode('utf-8')
        }

    def heartbeat(self, current_index):
        '''
        Indicate that this user has been active recently.
        '''
        self.last_active.set(int(time.time() * 1000))
        self.wants_index.set(current_index)

    def update_audio(self, index, parity, audio, offset):
        '''
        Update this user's audio for service element (index)
        and rotation pairty (parity). Parameters:

        index: int
        parity: int
        audio: AudioSegment
        offset: int

        returns: None
        '''

        print('UPDATING AUDIO', index, parity, len(audio), offset)

        key = '%d-%d' % (index, parity)
        if self.clips.hexists(key):
            sfile = File(self.clips.hget(key).decode('utf-8'))

        else:
            sfile = File()

            self.clips.hset(key, sfile.pk.get())
            print('CREATED KEY', key, 'VALUE IS', sfile.pk.get())

        # If offset is positive, that means
        # recording started BEFORE the true beginning.
        # Thus, truncate the recording by the appropriate amount.
        if offset > 0:
            audio = audio[offset:]
            offset = 0

        # If offset was negative, make it positive
        offset = abs(offset)

        sfile.data.set(encoding.encode({
            'offset': offset,
            'audio': pydub_helpers.as_mp3(audio)
        }))
    
    def get_audio(self, index, parity):
        '''
        Get this user's audio for service element (index)
        and rotation parity (parity), with its recording offset.

        returns: (AudioSegment, int)
        '''
        key = '%d-%d' % (index, parity)

        if not self.clips.hexists(key):
            print('NO KEY', key)
            return None
        
        sfile = File(self.clips.hget(key).decode('utf-8'))

        result = encoding.decode(
            sfile.data.get()
        )

        return (
            pydub_helpers.read_mp3(result['audio']),
            result['offset']
        )

    def close(self):
        for key in self.clips.hkeys():
            sfile_pk = self.clips.hget(key).decode('utf-8')
            sfile = File(sfile_pk)

            sfile.close()
            sfile.delete()

class File(model.RedisModel):
    database = database

    data = model.StringField()

    def close(self):
        return
