import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import Router from 'vue-router'
import Welcome from '@/components/Welcome'
import Join from '@/components/Join'
import Create from '@/components/Create'
import Sing from '@/components/Sing'
import Upload from '@/components/Upload'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(Router)
Vue.use(BootstrapVue)

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
      component: Create
    },
    {
      path: '/sing/:room/:user',
      name: 'Sing',
      props: {context},
      component: Sing
    },
    {
      path: '/upload',
      name: 'Upload',
      props: {context},
      component: Upload
    }
  ]
})
