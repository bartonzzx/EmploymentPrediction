import MultilevelMenuExample from './modules/multilevel.menu.example'
// import employment_management from './modules/employment_management'

import type { Menu } from '#/global'

const menu: Menu.recordMainRaw[] = [
  {
    meta: {
      title: '主导航',
      icon: 'uim:box',
    },
    children: [
      MultilevelMenuExample,
      // employment_management,
    ],
  },
]

export default menu
