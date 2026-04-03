import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/key-points', name: 'KeyPoints', component: () => import('../views/KeyPoints.vue') },
  { path: '/workbench', name: 'Workbench', component: () => import('../views/Workbench.vue') },
  { path: '/score-publish', name: 'ScorePublish', component: () => import('../views/ScorePublish.vue') },
  { path: '/style', name: 'StyleManage', component: () => import('../views/StyleManage.vue') },
  { path: '/settings', name: 'Settings', component: () => import('../views/Settings.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
