import type { RouteRecordRaw } from 'vue-router'

function Layout() {
  return import('@/layouts/index.vue')
}

const routes: RouteRecordRaw = {
  path: '/course_management',
  component: Layout,
  redirect: '/course_management/course',
  name: 'course',
  meta: {
    title: '课程管理',
    icon: 'bxs:book-content',
  },
  children: [
    {
      path: 'course',
      name: 'course',
      component: () => import('@/views/course_management/course.vue'),
      meta: {
        title: '课程管理',
        menu: false,
        breadcrumb: false,
        activeMenu: '/course_management',
      },
    },
  ],
}

export default routes
