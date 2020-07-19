<template>
    <div>
      <h3>{{ $route.params.room }}</h3>
      <b-container>
        <b-row>
          <b-col cols="3">
            <h3>Users</h3>

            <UserListElement
              v-for="user in users"
              v-bind:key="user.id"
              v-bind:name="user.name"
              />

          </b-col>
          <b-col cols="9">
            <h3>Bulletin</h3>

            <SingingBulletinElement
              v-for="item in bulletin"
              v-bind:key="item.index"
              v-bind:item="item"
              />

          </b-col>
        </b-row>
      </b-container>
    </div>
</template>

<script>
import UserListElement from '@/components/UserListElement'
import SingingBulletinElement from '@/components/SingingBulletinElement'
import brq from '@/binaryRequests'
import audio from '@/audio'

export default {
  name: 'Welcome',
  props: ['context'],
  data () {
    return {
      'bulletin': [],
      'users': [],

      'roomId': this.$route.params.room,
      'name': this.$route.params.user,
      'calibration': this.$route.params.calibration,

      'roomSinging': false,
      'schedulers': {},

      'index': 0,
      'userId': ''
    }
  },
  components: {
    UserListElement,
    SingingBulletinElement
  },
  created () {
    audio.getMediaStream().then((stream) => {
      // Populate the bulletin
      brq.get('/api/get-bulletin', {
        'room_id': this.roomId
      }).then((response) => {
        this.bulletin = response
      })

      // Join the relevant room
      brq.get('/api/join-room', {
        'room_id': this.roomId,
        'name': this.name
      }).then((response) => {
        this.userId = response.user_id

        heartbeat()
      })

      // Singing scheduler
      const scheduleNext = (index, parity, time) => {
        this.schedulers[index] = true

        // Nothing to do if we are not actually singing anything
        if (index < 0 || this.bulletin[index].song < 0) return

        brq.get('/api/get-mixed', {
          room_id: this.roomId,
          user_id: this.userId,
          index: index,
          parity: parity
        }).then((response) => {
          return this.context.decodeAudioData(response.audio.buffer)
        }).then((buffer) => {
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
            this.context.currentTime) * 1000 - 2000)

          audio.playAudioBuffer(this.context, buffer, time)
          return audio.recordAtTime(this.context, stream, time, time + buffer.duration)
        }).then(([buffer, offset]) => {
          offset += this.calibration

          return brq.post('/api/submit-audio', {
            'user_id': this.userId,
            'index': index,
            'parity': parity
          }, {
            'audio': buffer,
            'offset': offset
          })
        })
      }

      // Heartbeat our presence to the server
      // every 1.5 seconds
      const heartbeat = () => {
        brq.get('/api/heartbeat', {
          'user_id': this.userId
        }).then((response) => {
          this.singing = response.singing
          this.index = response.index
          this.users = response.users

          // If we are not singing the song that
          // everyone else is singing, start doing so.
          if (!this.schedulers[this.index]) {
            scheduleNext(this.index, 0, this.context.currentTime)
          }

          setTimeout(heartbeat, 1500)
        })
      }
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
