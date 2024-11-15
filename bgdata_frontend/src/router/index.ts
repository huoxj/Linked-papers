import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
      meta: {
        title: 'Home'
      },
    }, {
      path: '/search',
      name: 'search',
      component: () => import('../views/Search.vue'),
      meta: {
        title: 'Search'
      },
    }
  ],
})

export default router
