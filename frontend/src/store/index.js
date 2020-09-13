import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    latency: 0,
    hearme: false,
    leader: false
  },
  mutations: {
    setLatency (state, latency) {
      state.latency = latency
    },
    setHearme (state, hearme) {
      state.hearme = hearme
    },
    setLeader (state, leader) {
      state.leader = leader
    }
  },
  actions: {
  },
  getters: {
  }
})
