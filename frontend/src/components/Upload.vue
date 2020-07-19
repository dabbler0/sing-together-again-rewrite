<template>
    <div>
      Upload an accompaniment:
      <input ref="input" type="file" class="form-control-file" v-on:change="processFile()"/>
      <div v-if="hasSound">
        <div>Cut and finish:</div>
        (TODO start/end sliders)
        <input v-model="name" placeholder="Name" class="form-control"/>
        <textarea v-model="credits" placeholder="Credits" class="form-control"></textarea>
        <button v-on:click="submit()">Submit</button>
      </div>
    </div>
</template>

<script>
import brq from '@/binaryRequests'

export default {
  name: 'Welcome',
  props: ['context'],
  data () {
    return {
      hasSound: false,
      name: '',
      credits: '',
      file: null,
      fileFormat: null,
      sourceNode: null,
      startTime: 0,
      endTime: 0
    }
  },
  methods: {
    submit () {
      this.sourceNode.stop()

      new Response(this.file).arrayBuffer().then((buffer) => {
        brq.post('/api/new-song', {}, {
          'audio': buffer,
          'format': this.fileFormat,
          'name': this.name,
          'credits': this.credits,
          'start-time': Math.round(this.startTime * 1000),
          'end-time': Math.round(this.endTime * 1000)
        }).then(() => {
          this.$router.push('/create')
        })
      })
    },

    processFile () {
      console.log(this.$refs.input.files)
      const file = this.$refs.input.files[0]
      const fileName = this.$refs.input.value
      const fileFormat = fileName.substr(fileName.indexOf('.') + 1)

      this.file = file
      this.fileFormat = fileFormat

      new Response(file).arrayBuffer().then((buffer) => {
        this.context.decodeAudioData(buffer, (audioBuffer) => {
          // TODO cutting UI

          this.sourceNode = this.context.createBufferSource()
          this.sourceNode.buffer = audioBuffer
          this.sourceNode.loop = true
          this.sourceNode.loopStart = 0
          this.sourceNode.loopEnd = audioBuffer.duration
          this.sourceNode.connect(this.context.destination)
          this.sourceNode.start()

          this.startTime = 0
          this.endTime = audioBuffer.duration

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
