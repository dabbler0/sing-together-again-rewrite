<template>
  <v-content>
    <v-card fluid class="mx-auto text-center pb-10">
      <div class="central-title d-flex justify-center align-center mb-4 pt-10">
        <div>
          <img src="@/assets/prototype-logo.svg"/>
        </div>
        <h1 class="text--primary ml-2">
          About
        </h1>
      </div>

      <v-card-text style="text-align: left">
        <p>Sing Together Again was originally written by Anthony Bau in an effort to find a way for Taize at MIT to sing together again during the COVID-19 lockdown in 2020. It is built with congregational singing in mind, but can be used for any situation where a group of people want to sing something in harmony repeatedly.</p>

        <p>If a group wants to sing together with Sing Together Again, they'll first need to get, in advance, some accompaniment or leading voice to record one playthrough of each song they will sing. This will serve to ground the rhythm of the group and ensure everyone remains in time. Then one person will create a room and load these recordings into the order of service. They'll then distribute the room ID so everyone else can join.</p>

        <p>When singing, everyone will first hear just the recorded accompaniment/leader, and should begin singing along to it immediately. After one full playthrough, everyone will begin to hear everyone else's voices in harmony; these voices are taken from the previous repetition.</p>
      </v-card-text>
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
