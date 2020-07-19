<template>
  <div id="app">
    <div id="header">
      <h1>Sing together again</h1>
    </div>

    <div id="contents">
        <router-view/>
    </div>

    <div id="footer">
        By Anthony Bau. MIT License.
    </div>
  </div>
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
