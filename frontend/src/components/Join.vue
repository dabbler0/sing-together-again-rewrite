<template>
    <div>
        <input v-model="roomId"
        class="form-control" placeholder="Room ID"/>
        <input v-model="name"
        class="form-control" placeholder="Your Name"/>
        <router-link class="btn btn-secondary" to="/">Back</router-link>
        <button class="btn btn-success" v-on:click="join()">Join</button>
    </div>
</template>

<script>
export default {
  name: 'Welcome',
  data () {
    return {
      roomId: (this.$route.params.hasOwnProperty('prefill') ? this.$route.params.prefill : ''),
      name: ''
    }
  },
  methods: {
    join () {
      this.$router.push(
        '/sing/' + this.roomId + '/' + encodeURIComponent(this.name)
      )
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
