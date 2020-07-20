<template>
  <v-content>
    <v-card fluid class="mx-auto text-center pb-10">
      <div class="central-title d-flex justify-center align-center mb-4 pt-10">
        <div>
          <img src="@/assets/prototype-logo.svg"/>
        </div>
        <h1 class="text--primary ml-2">
          Sing Together Again
        </h1>
      </div>

      <v-card-text>
        <h3 class="headline">Sing repeated songs together in harmony online. Everyone hears everyone else's previous repetition.</h3>
      </v-card-text>

      <v-card-actions class="pt-10 pb-10 justify-center">
          <v-dialog width="500px" v-model="joinDialogShown">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                v-bind="attrs"
                v-on="on"
                large
              >
                Join Room
              </v-btn>
            </template>
            <JoinInsert @submit="(roomId, name) => join(roomId, name)" @cancel="joinDialogShown=false"></JoinInsert>
        </v-dialog>
        <v-btn to="create" class="ml-5" large>Create Room</v-btn>
      </v-card-actions>
    </v-card>
  </v-content>
</template>

<script>
import JoinInsert from '@/components/JoinInsert'

export default {
  name: 'Welcome',
  components: {JoinInsert},
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      joinDialogShown: false
    }
  },
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
