<template>
    <v-card>
      <v-card-title>Upload an accompaniment</v-card-title>

      <v-card-text>
        <v-form>
          <v-file-input ref="input" v-on:change="(files) => processFile(files)"></v-file-input>
          <div v-if="hasSound">
            <div>Cut and finish:</div>
            <v-range-slider
              thumb-label="always"
              v-model="timeRange"
              v-on:end="reclip()"
              step="0.01"
              min="0"
              :max="fullDuration"></v-range-slider>
            <v-text-field v-model="name" label="Name of song"></v-text-field>
            <v-textarea v-model="credits" label="Credits"></v-textarea>
            <v-btn v-on:click="$emit('cancel')">Cancel</v-btn>
            <v-btn v-on:click="submit()" color="primary">Submit</v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
</template>

<script>
import brq from '@/binaryRequests'

export default {
  name: 'Upload',
  props: ['context'],
  data () {
    return {
      hasSound: false,
      name: '',
      credits: '',
      file: null,
      fileFormat: null,
      sourceNode: null,
      timeRange: [0, 0],
      fullDuration: 0
    }
  },
  methods: {
    reclip () {
      this.sourceNode.loopStart = this.timeRange[0]
      this.sourceNode.loopEnd = this.timeRange[1]
    },

    submit () {
      this.sourceNode.stop()

      this.file.arrayBuffer().then((buffer) => {
        brq.post('/api/new-song', {}, {
          'audio': buffer,
          'format': this.fileFormat,
          'name': this.name,
          'credits': this.credits,
          'start-time': Math.round(this.timeRange[0] * 1000),
          'end-time': Math.round(this.timeRange[1] * 1000)
        }).then(() => {
          console.log('finishing submission')
          this.$emit('submit')
        })
      })
    },

    processFile (file) {
      const fileName = file.name
      const fileFormat = fileName.substr(fileName.indexOf('.') + 1)

      this.file = file
      this.fileFormat = fileFormat

      file.arrayBuffer().then((buffer) => {
        this.context.decodeAudioData(buffer, (audioBuffer) => {
          // TODO cutting UI

          this.sourceNode = this.context.createBufferSource()
          this.sourceNode.buffer = audioBuffer
          this.sourceNode.loop = true
          this.sourceNode.loopStart = 0
          this.sourceNode.loopEnd = audioBuffer.duration
          this.sourceNode.connect(this.context.destination)
          this.sourceNode.start()

          this.timeRange = [0, audioBuffer.duration]
          this.fullDuration = audioBuffer.duration

          this.hasSound = true
        })
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
