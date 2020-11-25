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
                Hold your headphones up to your microphone and click "calibrate". This will take somewhere between 5 and 20 seconds.<br/><br/>
                Or, if you've done this before (with these same headphones and computer) and remember a previous audio latency value that worked well, you can enter it manually.
              </div>
              <div v-if="finished">
              We estimate your audio latency to be around {{$store.state.latency.toPrecision(3)}} seconds. Click "continue", or, if something went wrong, hold your headphones up to your microphone and click "recalibrate".
              </div>

              <br/><br/>
              <v-spacer></v-spacer>

              <div v-if="manualSet">
                <div>
                  <v-text-field
                    label="Audio latency"
                    v-model="manualValue"
                    type="text"
                  >
                  </v-text-field>
                </div>
                <v-btn v-on:click="cancelManualEntry()" large>Cancel</v-btn>
                <v-btn
                    v-on:click="finishManualEntry()"
                    color="primary"
                    :disabled="!(manualValue.length > 0)"
                    large>Continue</v-btn>
              </div>
              <div v-if="!manualSet">
                <v-btn v-on:click="calibrate()" color="primary" large>{{(finished? 'Recalibrate' : 'Calibrate')}}</v-btn>
                <v-btn v-on:click="manualEntry()" large>Enter Manually</v-btn>
              </div>
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

function median (arr) {
  return arr.sort()[Math.floor(arr.length / 2)]
}

export default {
  name: 'Calibrate',
  props: ['context'],
  data () {
    return {
      'measurements': [],
      'room': this.$route.params.room,
      'user': this.$route.params.user,
      'finished': false,
      'manualValue': '',
      'manualSet': false
    }
  },
  // Skip calibration if no headphones
  created () {
    if (!this.$store.state.headphones) {
      this.$router.push('/sing/' + this.room + '/' + this.user)
    }
  },
  methods: {
    async calibrate () {
      this.measurements = []
      for (let i = 0; i < 20; i++) {
        this.measurements.push(await audio.measureLatency(this.context))

        const medianMeasurement = median(this.measurements)

        // If at least 5 samples are approximately equal to each other and the median,
        // we can stop immediately. Otherwise, continue.
        if (this.measurements.filter((x) => Math.abs(x -
            medianMeasurement) < 0.015).length >= 5) {
          break
        }
      }

      this.$store.commit('setLatency', median(this.measurements))
      this.finished = true
    },

    manualEntry () {
      this.manualSet = true
    },

    cancelManualEntry () {
      this.manualSet = false
    },

    finishManualEntry () {
      this.$store.commit('setLatency', Number(this.manualValue))
      this.$router.push('/sing/' + this.room + '/' + this.user)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
