import type { RouteRecordRaw } from 'vue-router'

function Layout() {
  return import('@/layouts/index.vue')
}

const routes: RouteRecordRaw = {
  path: '/data_upload',
  component: Layout,
  redirect: '/data_upload/upload',
  name: 'upload',
  meta: {
    title: '数据上传',
    icon: 'heroicons:arrow-up-tray-16-solid',
  },
  children: [
    {
      path: 'upload',
      name: 'upload',
      component: () => import('@/views/data_upload/upload.vue'),
      meta: {
        title: '数据上传',
        menu: false,
        breadcrumb: false,
        activeMenu: '/data_upload',
      },
    },
  ],
}

export default routes
