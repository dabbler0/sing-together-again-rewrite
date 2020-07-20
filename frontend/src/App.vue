<template>
  <v-app id="inspire">
    <!--<v-app-bar
      app
      color="indigo"
      dark
    >
      <v-toolbar-title>Sing Together Again</v-toolbar-title>
    </v-app-bar>-->

    <v-main style="position:absolute; top:0; bottom: 32px; left: 0; right: 0">
      <router-view/>
    </v-main>

    <v-footer absolute style="height:32px" class="justify-center">
      <router-link to="/">Sing Together Again</router-link>
      <router-link to="/about" class="ml-5 mr-5">About</router-link>
      <router-link to="/contributing">Contribute</router-link>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  text-align: center;
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
}

#header {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 60px;
  background: #EEE;
}

#footer {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 60px;
  background: #EEE;
}
#contents {
  position: absolute;
  top: 60px; bottom: 60px;
  left: 0; right: 0;
  overflow: auto;
}
</style>
