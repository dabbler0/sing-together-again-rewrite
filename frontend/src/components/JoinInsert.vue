<template>
  <v-card class="elevation-12" align="center">
    <v-card-title class="indigo white--text">Join Room</v-card-title>

    <v-spacer></v-spacer>

    <v-card-text>
      <v-form>
        <v-text-field
          label="Room ID"
          name="Room ID"
          v-model="roomId"
          type="text">
        </v-text-field>
        <v-text-field
          label="Your Name"
          name="Your Name"
          v-model="name"
          type="text">
        </v-text-field>

        <v-checkbox
          v-model="hearSelf"
          label="Hear myself"
          type="text"></v-checkbox>

        <v-checkbox
          v-model="leader"
          label="Join with leader controls"
          type="text"></v-checkbox>
      </v-form>
    </v-card-text>

    <v-card-actions class="justify-center">
      <v-btn v-on:click="$emit('cancel')" large>Back</v-btn>
      <v-btn color="primary" v-on:click="$emit('submit', roomId, name, { hearSelf, leader })" large>Join</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'JoinInsert',
  data () {
    return {
      roomId: (this.$route.params.hasOwnProperty('prefill') ? this.$route.params.prefill : ''),
      name: '',
      hearSelf: false,
      leader: false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
