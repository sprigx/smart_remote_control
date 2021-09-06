import { createRouter, createWebHashHistory } from 'vue-router'
import App from '../views/App.vue'

const routes = [
  {
    path: '/',
    name: 'Control',
    component: App,
    meta: { title: 'Smart Remote Controller' }
  }
]

const DEFAULT_TITLE = 'default title'

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.afterEach((to) => {
  document.title = to.meta.title || DEFAULT_TITLE
})

export default router
