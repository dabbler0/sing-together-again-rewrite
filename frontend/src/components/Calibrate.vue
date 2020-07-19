<template>
    <v-container
      class="fill-height"
      fluid
    >
      <v-row
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
          sm="8"
          md="4"
        >
          <v-card class="elevation-12" align="center">
            <v-card-title class="indigo white--text">Calibrate audio latency</v-card-title>
            <v-spacer></v-spacer>
            <v-card-text>
              <div v-if="!finished">
              Hold your headphones up to your microphone and click "calibrate". This will take about 15 seconds.
              </div>
              <div v-if="finished">
              We estimate your audio latency to be around {{$store.state.latency.toPrecision(3)}} seconds. Click "continue", or, if something went wrong, hold your headphones up to your micrphone and click "recalibrate".
              </div>
              <v-spacer></v-spacer>
              <v-btn v-on:click="calibrate()" color="primary" large>{{(finished? 'Recalibrate' : 'Calibrate')}}</v-btn>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn to="/join" large>Back</v-btn>
              <v-btn
                :disabled="!finished"
                v-bind:to="'/sing/' + room + '/' + user"
                color="success" large>Continue</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import audio from '@/audio'

export default {
  name: 'Calibrate',
  props: ['context'],
  data () {
    return {
      'measurements': [],
      'room': this.$route.params.room,
      'user': this.$route.params.user,
      'finished': false
    }
  },
  methods: {
    calibrate () {
      this.measurements = []
      let p = Promise.resolve(-1)
      for (let i = 0; i < 9; i++) {
        p = p.then((data) => {
          if (data > 0) this.measurements.push(data)
          return audio.measureLatency(this.context)
        })
      }
      p.then((data) => {
        this.measurements.push(data)
        this.$store.commit('setLatency', this.measurements.sort()[4])
        this.finished = true
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
