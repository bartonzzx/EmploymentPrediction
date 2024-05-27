import type { Menu } from '#/global'

const menus: Menu.recordRaw = {
  meta: {
    title: '就业管理',
    icon: 'ep:avatar',
  },
  children: [
    {
      path: '/employment_management/index.vue',
      meta: {
        title: '简介',
        icon: 'line-md:text-box-to-text-box-multiple-transition',
      },
    },
    {
      path: '/employment_management/ability_evaluation/ability.vue',
      meta: {
        title: '就业能力评估',
        icon: 'line-md:speedometer-loop',
      },
    },
  ],
}
export default menus
