import { defaultsDeep } from 'lodash-es'
import type { RecursiveRequired, Settings } from '#/global'
import settingsDefault from '@/settings.default'

const globalSettings: Settings.all = {
  // 请在此处编写或粘贴配置代码
  app: {
    colorScheme: '',
    enableDynamicTitle: true,
  },
  menu: {
    menuMode: 'single',
  },
  toolbar: {
    colorScheme: true,
    pageReload: true,
  },
  tabbar: {
    enable: true,
    enableIcon: true,
  },
}

export default defaultsDeep(globalSettings, settingsDefault) as RecursiveRequired<Settings.all>
