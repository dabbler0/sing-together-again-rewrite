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
          <v-card class="elevation-12" align="center">
            <v-card-title class="indigo white--text">Sing Together Again</v-card-title>

            <v-spacer></v-spacer>

            <v-card-text>
              Sing repeated songs together in harmony online. Everyone hears everyone else's previous repetition.
            </v-card-text>

            <v-card-actions class="justify-center">
              <v-btn to="join" color="primary" large>Join Room</v-btn>
              <v-btn to="create" large>Create Room</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
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
