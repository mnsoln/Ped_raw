import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Books from '../components/Books.vue'
import Pedigree from '../components/Pedigree.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Books',
      component: Books,
    },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
    {
      path: '/ped',
      name: 'Pedigree',
      component: Pedigree
    },
  ]
})

export default router