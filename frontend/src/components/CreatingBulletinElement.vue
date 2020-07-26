<template>
      <v-form>
        <v-file-input
            @change="(file) => processAccompaniment(file)"
            label="Upload different accompaniment"
            style="display: inline-block"
            prepend-icon="mdi-music-note-plus"
            hide-input
            ></v-file-input>Change accompaniment ({{(value.accompaniment ? value.accompaniment.name : 'None')}})
          <v-text-field
            v-model="value.title"
            label="Section Title"
            name="Section Title"
            type="text"
            ></v-text-field>
          <v-textarea
            v-model="value.description"
            label="Additional text for this section"
            name="Additional text for this section"
            type="text"></v-textarea>

          <v-divider class="pb-5"></v-divider>
      </v-form>
</template>

<script>
import encoding from '@/encoding'

export default {
  name: 'CreatingBulletinElement',
  props: ['value'],
  watch: {
    value () {
      this.$emit('input', this.value)
    }
  },
  data () {
    return {
    }
  },
  methods: {
    processAccompaniment (file) {
      file.arrayBuffer().then((buffer) => {
        this.value.accompaniment = encoding.decode(new Uint8Array(buffer))
        if (this.value.title === '') {
          this.value.title = this.value.accompaniment.name
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
