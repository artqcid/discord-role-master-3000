import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import RolesView from '../views/RolesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/roles',
      name: 'roles',
      component: RolesView
    },
    {
      path: '/channels',
      name: 'channels',
      component: () => import('../views/ChannelsView.vue')
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/CategoriesView.vue')
    }
  ]
})

export default router
