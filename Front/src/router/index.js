import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Books from '../components/Books.vue'
import Pedigree from '../components/Pedigree.vue'
import Documentation from '../components/Documentation.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/doc',
      name: 'Documentation',
      component: Documentation,
    },
    {
      path: '/ping',
      name: 'ping',
      component: Ping
    },
    {
      path: '/',
      name: 'Pedigree',
      component: Pedigree
    },
  ]
})

export default router