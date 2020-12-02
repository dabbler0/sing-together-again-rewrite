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
                          <v-list-item-group v-model="index">
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

export default {
  name: 'Sing',
  props: ['context'],
  data () {
    return {
      'bulletin': [],
      'users': [],

      'roomId': this.$route.params.room,
      'name': decodeURIComponent(this.$route.params.user),

      'roomSinging': false,
      'schedulers': {},

      'songs': {},

      'advanceMessage': 'Begin service',

      'index': -1,
      'playingIndex': -1,
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
    }
  },
  created () {
    window.setLatency = (latency) => {
      this.$store.commit('setLatency', latency)
    }
    // Asynchronously also get songs

    audio.getMediaStream().then((stream) => {
      // Populate the bulletin
      brq.get('/api/get-bulletin', {
        'room_id': this.roomId
      }, true).then((response) => {
        this.bulletin = response
      })

      // Join the relevant room
      brq.get('/api/join-room', {
        'room_id': this.roomId,
        'name': this.name
      }, true).then((response) => {
        this.userId = response.user_id

        heartbeat()
      })

      const backupResponses = {}

      // Singing scheduler
      const scheduleNext = async (index, parity, time) => {
        this.schedulers[index] = true

        // Nothing to do if we are not actually singing anything
        if ((!this.singing && parity === 0) ||
          index < 0 || this.bulletin[index].song < 0) return

        if (!(index in backupResponses)) backupResponses[index] = {}

        const response = await brq.get('/api/get-mixed', {
          room_id: this.roomId,
          user_id: this.userId,
          hearme: this.$store.state.hearme,
          index: index,
          parity: parity
        }, true, () => this.context.currentTime + 1000 > time, backupResponses[index][parity])

        backupResponses[index][parity] = response

        const range = response.range
        const buffer = await this.context.decodeAudioData(response.audio.buffer)

        // Kick off the next schedule and also play the next
        // sound
        setTimeout(() => {
          if (parity === 0 || (index === this.index && this.singing)) {
            scheduleNext(index,
              (parity + 1) % 2,
              time + buffer.duration)
          } else {
            this.schedulers[index] = false
          }
        }, (time + buffer.duration -
          this.context.currentTime) * 1000 / 2)

        // Assume everyone will have submitted by
        // about halfway to the next beat.
        this.playingIndex = index

        audio.playAudioBuffer(this.context, buffer, time)

        if (this.$store.state.headphones) {
          let [buffer, offset] = await audio.recordAtTime(this.context, stream, time + range[0] / 1000, time + range[1] / 1000)

          offset += this.$store.state.latency

          return brq.post('/api/submit-audio', {
            'user_id': this.userId,
            'index': index,
            'parity': parity
          }, {
            'audio': buffer,
            'offset': Math.round(offset * 1000)
          }, true)
        }
      }

      // Heartbeat our presence to the server
      // every 3 seconds
      const heartbeat = () => {
        brq.get('/api/heartbeat', {
          'user_id': this.userId,
          'name': this.name,
          'room_id': this.roomId,
          'current_index': this.playingIndex
        }, true).then(({ heart, room_data: roomData }) => {
          this.userId = heart['user_id']
          this.singing = roomData.singing
          this.index = roomData.index
          this.users = roomData.users

          if (this.singing) {
            this.advanceMessage = 'Stop singing'
          } else if (this.index + 1 < this.bulletin.length) {
            console.log(this.index + 1, this.bulletin, this.bulletin[this.index + 1])
            this.advanceMessage = 'Start ' + this.bulletin[this.index + 1].title
          }

          // If we are not singing the song that
          // everyone else is singing, start doing so.
          if (!this.schedulers[this.index]) {
            scheduleNext(this.index, 0, this.context.currentTime + 1.5)
          }

          setTimeout(heartbeat, 3000)
        })
      }
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
