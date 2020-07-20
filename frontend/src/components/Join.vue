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
        <JoinInsert @submit="(roomId, name) => join(roomId, name)" @cancel="$router.push('/')"></JoinInsert>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import JoinInsert from '@/components/JoinInsert'

export default {
  name: 'Welcome',
  data () {
    return {
      roomId: (this.$route.params.hasOwnProperty('prefill') ? this.$route.params.prefill : ''),
      name: ''
    }
  },
  components: {JoinInsert},
  methods: {
    join (roomId, name) {
      this.$router.push(
        '/calibrate/' + roomId + '/' + encodeURIComponent(name)
      )
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
