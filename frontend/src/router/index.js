import Vue from 'vue'
import Router from 'vue-router'
import Welcome from '@/components/Welcome'
import Join from '@/components/Join'
import Create from '@/components/Create'
import Sing from '@/components/Sing'
import Calibrate from '@/components/Calibrate'

Vue.use(Router)

// The one audiocontext everone will use
const context = new AudioContext()

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: Welcome
    },
    {
      path: '/join',
      name: 'Join',
      component: Join
    },
    {
      path: '/join/:prefill',
      name: 'JoinPrefilled',
      component: Join
    },
    {
      path: '/create',
      name: 'Create',
      props: {context},
      component: Create
    },
    {
      path: '/sing/:room/:user',
      name: 'Sing',
      props: {context},
      component: Sing
    },
    {
      path: '/calibrate/:room/:user',
      name: 'Calibrate',
      props: {context},
      component: Calibrate
    }
  ]
})
