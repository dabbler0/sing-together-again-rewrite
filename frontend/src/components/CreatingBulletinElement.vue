<template>
    <div>
      <b-container>
        <b-form-row>
          <b-col cols="3">
            <select v-model="value.song" class="form-control">
              <option value="-1">No song</option>
              <option v-for="song in songs"
                      v-bind:key="song.id"
                      v-bind:value="song.id"> {{ song.name }} </option>
            </select>
          </b-col>
          <b-col cols="9">
            <input v-model="value.title" class="form-control"/>
          </b-col>
        </b-form-row>

        <b-form-row>
          <textarea v-model="value.description" class="form-control"/>
        </b-form-row>
      </b-container>
    </div>
</template>

<script>
export default {
  name: 'CreatingBulletinElement',
  props: ['value', 'songs'],
  watch: {
    value () {
      this.$emit('input', this.value)
    }
  },
  data () {
    return {}
  },
  created () {
    console.log(this.value)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
