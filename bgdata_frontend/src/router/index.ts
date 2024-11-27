import {createRouter, createWebHistory} from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
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
    }, {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    }, {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
    }, {
      path: '/paper/:id',
      name: 'paper',
      component: () => import('../views/Paper.vue'),
    }
  ],
})

export default router
