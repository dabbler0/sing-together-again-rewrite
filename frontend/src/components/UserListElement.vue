<template>
    <div>
      {{ name }}
    </div>
</template>

<script>
export default {
  name: 'Welcome',
  props: ['name', 'isme'],
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
