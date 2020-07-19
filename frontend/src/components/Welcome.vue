<template>
    <div>
        <router-link to="join" class="btn btn-success">Join</router-link>

        <router-link to="create" class="btn btn-primary">Create</router-link>

    </div>
</template>

<script>
export default {
  name: 'Welcome',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
