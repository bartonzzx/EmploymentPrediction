import type { RouteRecordRaw } from 'vue-router'

function Layout() {
  return import('@/layouts/index.vue')
}

const routes: RouteRecordRaw = {
  path: '/employment_management',
  component: Layout,
  name: 'index',
  meta: {
    title: '就业管理',
    icon: 'ep:avatar',
    breadcrumb: false,
  },
  children: [
    {
      path: 'index',
      name: 'index',
      component: () => import('@/views/employment_management/index.vue'),
      meta: {
        title: '简介',
        icon: 'line-md:text-box-to-text-box-multiple-transition',
      },
    },
    {
      path: 'ability_evaluation',
      name: 'ability',
      component: () => import('@/views/employment_management/ability_evaluation/ability.vue'),
      meta: {
        title: '就业能力评估',
        icon: 'line-md:speedometer-loop',
      },
    },
    {
      path: 'employment_prediction',
      name: 'employment',
      component: () => import('@/views/employment_management/employment_prediction/employment.vue'),
      meta: {
        title: '就业去向预测',
        icon: 'line-md:uploading-loop',
      },
    },
    {
      path: 'realtime_evaluation_prediction',
      name: 'realtime',
      component: () => import('@/views/employment_management/realtime_evaluation_prediction/realtime.vue'),
      meta: {
        title: '实时评估和预测',
        icon: 'line-md:loading-loop',
      },
    },
  ],
}

export default routes
