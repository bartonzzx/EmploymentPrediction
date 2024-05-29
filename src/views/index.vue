<route lang="yaml">
name: home
meta:
  title: 主页
  icon: ant-design:home-twotone
</route>

<script setup lang="ts">
const fantasticStartkitInfo = ref({
  feature: [
    '支持 TypeScript',
    '默认集成 vue-router 和 pinia',
    '支持基于文件系统的路由',
    '全局组件自动引入',
    '全局 SCSS 资源引入',
    '支持 Unocss',
    '支持 SVG 文件图标、Iconify 图标、UnoCSS 图标',
    '支持 mock 数据，可脱离后端束缚独立开发',
    '支持 gzip / brotli 优化项目体积，提高加载速度',
    '结合 IDE 插件、ESlint 、stylelint 、Git 钩子，轻松实现团队代码规范',
  ],
})

const fantasticAdminInfo = ref({
  imageVisible: false,
  index: 0,
  data: [
    'https://fantastic-admin.github.io/preview1.png',
    'https://fantastic-admin.github.io/preview2.png',
    'https://fantastic-admin.github.io/preview3.png',
    'https://fantastic-admin.github.io/preview4.png',
    'https://fantastic-admin.github.io/preview5.png',
    'https://fantastic-admin.github.io/preview6.png',
  ],
})

const oneStepAdminInfo = ref({
  imageVisible: false,
  index: 0,
  data: [
    'https://one-step-admin.github.io/preview1.png',
    'https://one-step-admin.github.io/preview2.png',
    'https://one-step-admin.github.io/preview3.png',
    'https://one-step-admin.github.io/preview4.png',
    'https://one-step-admin.github.io/preview5.png',
    'https://one-step-admin.github.io/preview6.png',
  ],
})

function open(url: string) {
  window.open(url, '_blank')
}
</script>

<template>
  <div>
    <PageHeader>
      <template #title>
        <div class="flex items-center gap-4">
          欢迎使用 就业预测系统
        </div>
      </template>
      <template #content>
        <div class="text-sm/6">
          <div>
            这是一个<b class="text-emphasis">就业预测系统</b>，整个系统分为：成绩管理，课程管理，就业管理。
          </div>
          <div>
            成绩管理：展示用户成绩。成绩高低用不同颜色区分。
          </div>
          <div>
            课程管理：展示用户所修的全部课程。展示了课程与毕业能力的对应情况，同时显示用户对应的成绩。
          </div>
          <div>
            就业管理：展示根据成绩评估出的用户就业能力和就业预测去向，同时提供通过上传成绩单进行实时评估和预测的功能。
          </div>
        </div>
      </template>
        <HButton class="ml-2" @click="open('https://github.com/bartonzzx/EmploymentPrediction')">
          <SvgIcon name="i-ri:code-s-slash-line" />
          代码仓库
        </HButton>
    </PageHeader>
    <div class="w-full flex flex-col gap-4 px-4 xl:flex-row">
    </div>
  </div>
</template>

<style lang="scss" scoped>
.text-emphasis {
  text-emphasis-style: "❤";
}

.ecology {
  --at-apply: flex-1 m-0;

  :deep(.title-container) {
    --at-apply: flex items-center justify-between flex-wrap gap-4;

    .title-info {
      --at-apply: flex items-center gap-4;

      img {
        --at-apply: block w-12 h-12;
      }

      h1 {
        --at-apply: m-0 text-2xl;
      }

      h2 {
        --at-apply: m-0 text-base text-stone-5 font-normal;
      }
    }
  }
}
</style>
