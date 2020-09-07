<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row
    >
      <v-col>
        <h1>Record or Import Accompaniment</h1>
        <v-form>
          Record a new accompaniment right now:
          <br/>

          <v-btn color="primary ml-5 mt-5 mb-5" @click="record()">Start Recording</v-btn>

          <br/>

          Or upload a sound file or <code>.accompaniment</code> file for editing:
          <v-file-input color="primary" ref="input" v-on:change="(file) => processFile(file)" label="Upload"></v-file-input>
        </v-form>

        <div v-if="hasFile">
          <h1>Edit Accompaniment</h1>
          <v-form>

            <audio :src="audioSrc" controls style="width:100%"></audio>

            Clip to range: {{ timeRange[0] }} - {{ timeRange[1] }}
              <v-range-slider
                thumb-label
                v-model="timeRange"
                v-on:change="reclip()"
                step="0.01"
                min="0"
                :max="fullDuration"></v-range-slider>

            Sing together during range: {{ repeatRange[0] }} - {{ repeatRange[1] }}
              <v-range-slider
                thumb-label
                v-model="repeatRange"
                step="0.01"
                min="0"
                :max="fullDuration"></v-range-slider>
              <v-text-field v-model="name" label="Name of song"></v-text-field>
              <v-textarea v-model="credits" label="Credits"></v-textarea>
              <!--<v-btn color="primary" large>Add to Service</v-btn>-->

            <v-btn @click="togglePreview()" large>
              <span v-if="previewing">Stop&nbsp;</span> Preview</v-btn>
            <v-btn color="success" @click="download()" class="ml-5" large>Download</v-btn>
          </v-form>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import audio from '@/audio'
import encoding from '@/encoding'

export default {
  data () {
    return {
      name: '',
      credits: '',
      timeRange: [0, 0],
      lastReclippedStartTime: 0,
      lastReclippedEndTime: 0,
      repeatRange: [0, 0],
      fullDuration: 0,
      audioData: null,
      audioBuffer: null,
      audioSrc: '',
      previewing: false,
      hasFile: false,
      fileFormat: ''
    }
  },
  props: ['context'],
  created () {
    window.encoding = encoding
  },
  methods: {
    processFile (file) {
      const fileName = file.name
      const fileFormat = fileName.substr(fileName.indexOf('.') + 1)

      if (fileFormat === 'accompaniment') {
        file.arrayBuffer().then((buffer) => {
          const accompaniment = encoding.decode(new Uint8Array(buffer))

          this.name = accompaniment.name
          this.credits = accompaniment.credits
          this.format = accompaniment.format
          this.timeRange = accompaniment.time.map((x) => x / 1000)
          this.repeatRange = accompaniment.repeat.map((x) => x / 1000)

          this.audioData = accompaniment.audio.buffer.slice(
            accompaniment.audio.byteOffset,
            accompaniment.audio.byteOffset + accompaniment.audio.byteLength
          )
          this.audioSrc = URL.createObjectURL(new Blob([
            this.audioData
          ]))

          this.context.decodeAudioData(this.audioData.slice(0)).then((audioBuffer) => {
            this.fullDuration = audioBuffer.duration
            this.audioBuffer = audioBuffer

            this.hasFile = true
          })
        })
      } else {
        this.audioSrc = URL.createObjectURL(file)

        this.format = fileFormat

        file.arrayBuffer().then((buffer) => {
          this.audioData = buffer.slice(0)
          return this.context.decodeAudioData(buffer)
        }).then((audioBuffer) => {
          this.audioBuffer = audioBuffer
          this.timeRange = [0, audioBuffer.duration]
          this.lastReclippedEndTIme = audioBuffer.duration
          this.repeatRange = [0, audioBuffer.duration]
          this.fullDuration = audioBuffer.duration
          this.hasFile = true
        })
      }
    },

    reclip () {
      if (this.repeatRange[0] === this.lastReclippedStartTime) {
        this.repeatRange[0] = this.timeRange[0]
      }

      this.repeatRange[0] = Math.max(this.repeatRange[0], this.timeRange[0])

      if (this.repeatRange[1] === this.lastReclippedEndTime) {
        this.repeatRange[1] = this.timeRange[1]
      }

      this.repeatRange[1] = Math.min(this.repeatRange[1], this.timeRange[1])

      this.$set(this.repeatRange, 0, this.repeatRange[0])
      this.$set(this.repeatRange, 1, this.repeatRange[1])

      this.lastReclippedStartTime = this.timeRange[0]
      this.lastReclippedEndTime = this.timeRange[1]
    },

    togglePreview () {
      if (this.previewing) {
        this.sourceNode.stop()
        this.previewing = false
      } else {
        this.sourceNode = this.context.createBufferSource()
        this.sourceNode.buffer = this.audioBuffer
        this.sourceNode.loop = true
        this.sourceNode.loopStart = this.timeRange[0]
        this.sourceNode.loopEnd = this.timeRange[1]
        this.sourceNode.connect(this.context.destination)
        this.sourceNode.start(0, this.timeRange[0])
        this.previewing = true
      }
    },

    record () {
      alert('Not implemented yet.')
    },

    download () {
      const resultBuffer = encoding.encode({
        name: this.name,
        format: this.format,
        credits: this.credits,
        time: this.timeRange.map((x) => Math.round(x * 1000)),
        repeat: this.repeatRange.map((x) => Math.round(x * 1000)),
        audio: this.audioData
      })

      const blobURL = URL.createObjectURL(new Blob([resultBuffer.buffer]))

      const link = document.createElement('a')
      link.href = blobURL
      link.download = this.name + '.accompaniment'

      document.body.appendChild(link)

      link.dispatchEvent(
        new MouseEvent('click', {
          bubbles: true,
          cancelable: true,
          view: window
        })
      )

      document.body.removeChild(link)
    }
  }
}
</script>
