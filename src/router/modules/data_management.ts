import type { RouteRecordRaw } from 'vue-router'

function Layout() {
  return import('@/layouts/index.vue')
}

const routes: RouteRecordRaw = {
  path: '/data_management',
  component: Layout,
  redirect: '/data_management/data',
  name: 'data',
  meta: {
    title: '数据管理',
    icon: 'heroicons:arrow-up-tray-16-solid',
  },
  children: [
    {
      path: 'data',
      name: 'data',
      component: () => import('@/views/data_management/data.vue'),
      meta: {
        title: '数据上传',
        menu: false,
        breadcrumb: false,
        activeMenu: '/data_management',
      },
    },
  ],
}

export default routes
