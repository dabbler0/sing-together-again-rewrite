<template>
    <v-container
      class="fill-height"
      fluid
    >
      <v-row
        class="fill-height"
        align="center"
        justify="center"
      >
        <v-col
          class="fill-height"
          cols="10"
          sm="10"
          md="10"
        >
        <v-card class="elevation-12 fill-height" align="center">
          <v-card-title class="indigo white--text" style="position: absolute; top:0; left: 0; right: 0">Room {{$route.params.room}}</v-card-title>
            <v-spacer></v-spacer>

            <v-card-text style="position: absolute; top: 64px; bottom: 64px;">
              <v-container class="fill-height">
                <v-row class="fill-height">
                  <v-col cols="3" class="fill-height">
                    <v-card class="fill-height">
                      <v-card-title light flat>Participants</v-card-title>
                      <v-divider></v-divider>
                      <v-card-text>
                        <v-list disabled>
                          <v-list-item-group v-model="userId">
                             <v-list-item
                              v-for="user in users"
                              :key="user.id"
                            >
                              <v-list-item-icon>
                                <v-icon>mdi-account</v-icon>
                              </v-list-item-icon>

                              <v-list-item-content>
                                <v-list-item-title v-text="user.name"></v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                          </v-list-item-group>
                        </v-list>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="9" class="fill-height">
                    <v-card class="fill-height overflow-y-auto">
                      <v-card-title>Bulletin</v-card-title>

                      <v-divider></v-divider>

                      <v-card-text>
                        <v-list disabled>
                          <v-list-item-group v-model="nextIndex">
                             <v-list-item
                              v-for="(item, i) in bulletin"
                              :key="i"
                            >
                              <v-list-item-content>
                                <v-list-item-title v-text="(i + 1) + '. ' + item.title"></v-list-item-title>
                                <div class="justify-left">{{item.description}}</div>
                              </v-list-item-content>
                            </v-list-item>
                          </v-list-item-group>
                        </v-list>
                      </v-card-text>
                    </v-card>

                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions class="justify-center indigo white--text" style="position: absolute; bottom:0; left: 0; right: 0">
              <div v-if="$store.state.leader">
                <v-btn v-on:click="advance()">{{advanceMessage}}</v-btn>
              </div>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import brq from '@/binaryRequests'
import audio from '@/audio'
import io from 'socket.io-client'

export default {
  name: 'Sing',
  props: ['context'],
  data () {
    return {
      'bulletin': [],
      'users': [],

      'roomId': this.$route.params.room,
      'name': decodeURIComponent(this.$route.params.user),

      'fetchedAudio': {},

      'roomSinging': false,
      'schedulers': {},

      'songs': {},

      'advanceMessage': 'Begin service',

      'nextIndex': -1,
      'nextParity': 0,
      'nextTime': 0,
      'nextSinging': false,
      'updateIndex': -1,
      'updateSinging': false,
      'userId': ''
    }
  },
  methods: {
    advance () {
      if (this.singing) {
        brq.get('/api/stop-song', {room_id: this.roomId})
      } else {
        brq.get('/api/start-song', {room_id: this.roomId, index: this.index + 1})
      }
    },

    async fetchFor (index, parity) {
      if (!(index in this.fetchedAudio)) {
        this.fetchedAudio[index] = {}
      }
      const response = await brq.get('/api/get-mixed', {
        room_id: this.roomId,
        user_id: this.userId,
        hearme: this.$store.state.hearme,
        index,
        parity
      })
      this.fetchedAudio[index][parity] = {
        range: response.range,
        buffer: await this.context.decodeAudioData(response.audio.buffer)
      }
    },

    async getMostRecentAudio (index, parity) {
      if (!(index in this.fetchedAudio) || !(parity in this.fetchedAudio[index])) {
        await this.fetchFor(index, parity)
      }
      return this.fetchedAudio[index][parity]
    },

    async playLoop () {
      this.nextSinging = true

      // Any time we finish a loop through,
      // receive any updates the remote has for us.
      if (this.nextParity === 0) {
        // If we need to stop singing now, stop.
        if (!this.updateSinging) {
          this.nextSinging = false
          return
        } else if (this.updateIndex !== this.nextIndex) {
          this.nextIndex = this.updateIndex
        }
      }

      // Since this is an async function we want to make sure
      // these values don't change in the middle of execution
      const { nextIndex: index, nextParity: parity, nextTime: time } = this

      // Note: this function should be the ONLY one to modify
      // nextTime and nextParity

      // Get audio for this next audio and play it.
      const { buffer, range } = await this.getMostRecentAudio(index, parity)
      audio.playAudioBuffer(this.context, buffer, time)
      this.nextParity = (parity + 1) % 2
      this.nextTime = time + buffer.duration

      // Request a fetch for the opposite parity of this song
      // about halfway through this next buffer.
      setTimeout(
        () => this.fetchFor(index, (parity + 1) % 2),
        (this.nextTime - buffer.duration / 2) * 1000
      )

      // If we're recording for this user, record
      // and submit. Don't block the play loop for this,
      // just schedule it.
      if (this.$store.state.headphones) {
        // Record...
        audio.recordAtTime(
          this.context,
          this.stream,
          time + range[0] / 1000,
          time + range[1] / 1000
        ).then(([recordedBuffer, recordedOffset]) => {
          // ...and submit.
          brq.post('/api/submit-audio', {
            'user_id': this.userId,
            index,
            parity
          }, {
            'audio': recordedBuffer,
            'offset': Math.round(
              (recordedOffset + this.$store.state.latency) * 1000
            )
          }, true)
        })
      }

      // Schedule the next play registration
      // some amount of time before the buffer must
      // actually play.
      setTimeout(
        () => this.playLoop(),
        (this.nextTime - buffer.duration / 4) * 1000
      )
    },
    async register () {
      this.socket.emit('register', { rid: this.roomId, name: this.name })
    }
  },

  async created () {
    // DEBUGGING
    window.setLatency = (latency) => {
      this.$store.commit('setLatency', latency)
    }

    // Open a socket connection and register
    this.socket = io()

    // Whenever we connect or reconnect,
    // reregister
    this.socket.on('connect', () => this.register())
    this.socket.on('reconnect', () => this.register())

    // Whenever we are informed of our uid, update it
    this.socket.on('uid', (uid) => { this.userId = uid })

    // Whenever we get info on the room status, update ours to reflect it
    this.socket.on('update', ({ singing, index, users }) => {
      this.users = users
      this.updateIndex = index
      this.updateSinging = singing

      if (!this.nextSinging && this.updateSinging) {
        this.playLoop()
      }

      this.singing = singing
    })

    // Wait until the first time we get our uid
    await new Promise((resolve) => this.socket.on('uid', resolve))

    // Now we can begin. Get recording stream
    this.stream = await audio.getMediaStream()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
