import type { RouteRecordRaw } from 'vue-router'

function Layout() {
  return import('@/layouts/index.vue')
}

const routes: RouteRecordRaw = {
  path: '/employment_management',
  component: Layout,
  redirect: '/employment_management/index',
  name: 'index',
  meta: {
    title: '就业管理',
    icon: 'i-heroicons-solid:menu-alt-3',
  },
  children: [
    {
      path: 'index',
      name: 'index',
      component: () => import('@/views/employment_management/index.vue'),
      meta: {
        title: '简介',
        activeMenu: '/employment_management',
      },
    },
    {
      path: 'ability_evaluation',
      name: 'ability',
      component: () => import('@/views/employment_management/ability_evaluation/ability.vue'),
      meta: {
        title: '就业能力评估',
        activeMenu: '/employment_management',
      },
    },
    {
      path: 'employment_prediction',
      name: 'employment',
      component: () => import('@/views/employment_management/employment_prediction/employment.vue'),
      meta: {
        title: '就业去向预测',
        activeMenu: '/employment_management',
      },
    },
    {
      path: 'realtime_evaluation_prediction',
      name: 'realtime',
      component: () => import('@/views/employment_management/realtime_evaluation_prediction/realtime.vue'),
      meta: {
        title: '实时评估和预测',
        activeMenu: '/employment_management',
      },
    },
  ],
}

export default routes
