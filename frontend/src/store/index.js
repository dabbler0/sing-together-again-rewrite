import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    latency: 0
  },
  mutations: {
    setLatency (state, latency) {
      state.latency = latency
    }
  },
  actions: {
  },
  getters: {
  }
})
