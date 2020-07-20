<template>
  <v-content>
    <v-card fluid class="mx-auto text-center pb-10">
      <div class="central-title d-flex justify-center align-center mb-4 pt-10">
        <div>
          <img src="@/assets/prototype-logo.svg"/>
        </div>
        <h1 class="text--primary ml-2">
          Contribute
        </h1>
      </div>

      <v-card-text style="text-align:left">
        If you are a developer with time, this project is on Github at <a href="https://github.com/dabbler0/sing-together-again-rewrite">sing-together-again-rewrite</a>. As of right now I am still actively maintaining it and am open to Github issues or pull requests.
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
