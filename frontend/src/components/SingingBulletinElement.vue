<template>
    <div>
      <div>
        {{ item.title }}
      </div>
      <div>
        {{ item.description }}
      </div>
    </div>
</template>

<script>
export default {
  name: 'Welcome',
  props: ['item'],
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
