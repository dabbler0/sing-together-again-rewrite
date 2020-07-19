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
        <v-card class="elevation-12" height="100%" align="center" style="position:relative">
            <v-card-title class="indigo white--text" dark flat ref="header" style="position:absolute;top:0;left:0;right:0">
              Create the Order of Service
            </v-card-title>

            <v-card-text style="position:absolute;top:64px;bottom:64px;padding:10px;overflow: auto">
              <CreatingBulletinElement
                  v-for="(item, i) in bulletin"
                  :key="i"
                  :context="context"
                  v-bind:songs="knownSongs"
                  v-on:upload="refetchSongs()"
                  v-model="bulletin[i]"></CreatingBulletinElement>
              <v-btn v-on:click="addSection()" large>Add section</v-btn>
            </v-card-text>

            <v-card-actions class="justify-center indigo white--text" ref="footer" style="position:absolute;bottom:0;left:0;right:0">
                <v-btn to="/" large>Cancel</v-btn>
                <v-btn v-on:click="submit()" large color="primary">Done</v-btn>
            </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CreatingBulletinElement from '@/components/CreatingBulletinElement'
import brq from '@/binaryRequests'
// import encoding from '@/encoding'

export default {
  name: 'Sing',
  props: ['context'],
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
    },

    refetchSongs () {
      brq.get('/api/song-list', {}).then((songs) => {
        this.knownSongs = songs
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
