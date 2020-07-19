<template>
    <div>
      <div class="creating-body">
        <CreatingBulletinElement
          v-for="(item, i) in bulletin"
          v-bind:key="i"

          v-bind:songs="knownSongs"
          v-model="bulletin[i]"
          />

        <div class="list-group-item list-group-item-action"
            v-on:click="addSection()">
          add new section
        </div>
      </div>

      <div class="creating-buttons">
        <button class="btn btn-primary" v-on:click="submit()">Create</button>
      </div>
    </div>
</template>

<script>
import CreatingBulletinElement from '@/components/CreatingBulletinElement'
import brq from '@/binaryRequests'
// import encoding from '@/encoding'

export default {
  name: 'Sing',
  components: {
    'CreatingBulletinElement': CreatingBulletinElement
  },
  data () {
    return {
      bulletin: [],
      knownSongs: []
    }
  },
  methods: {
    addSection () {
      this.bulletin.push({
        'title': '',
        'song': -1,
        'description': ''
      })
    },

    submit () {
      brq.post('/api/create-room', {}, this.bulletin).then((response) => {
        this.$router.push('/join/' + response.room_id)
      })
    }
  },

  created () {
    brq.get('/api/song-list', {}).then((songs) => {
      this.knownSongs = songs
    })
  }
}
</script>

<style scoped>
</style>
