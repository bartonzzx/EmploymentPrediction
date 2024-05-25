import type { RouteRecordRaw } from 'vue-router'

function Layout() {
  return import('@/layouts/index.vue')
}

const routes: RouteRecordRaw = {
  path: '/score_management',
  component: Layout,
  redirect: '/score_management/score',
  name: 'score',
  meta: {
    title: '成绩管理',
    icon: 'heroicons-outline:academic-cap',
  },
  children: [
    {
      path: 'score',
      name: 'score',
      component: () => import('@/views/score_management/score.vue'),
      meta: {
        title: '成绩管理',
        menu: false,
        breadcrumb: false,
        activeMenu: '/score_management',
      },
    },
  ],
}

export default routes
