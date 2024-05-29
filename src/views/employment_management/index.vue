<route lang="yaml">
meta:
  title: 页面标题
</route>

<script setup lang="ts">
defineOptions({
  name: 'EmploymentManagementIndex',
})
</script>

<template #content>
 <div>
    <PageHeader>
      <template #title>
        <div class="flex items-center gap-4">
          就业管理功能
        </div>
      </template>
      <template #content>
        <div class="text-sm/6">
          <div>
            就业管理功能分为：就业能力评估，就业去向预测，实时评估和预测。
          </div>
          <div>
            就业能力评估：展示评估得到的用户能力。能力为百分制。
          </div>
          <div>
            就业去向预测：展示预测得到的用户就业去向及各去向对应的概率。
          </div>
          <div>
            实时评估和预测：通过上传成绩单进行实时评估和预测。
          </div>
        </div>
      </template>
    </PageHeader>
    <div class="w-full flex flex-col gap-4 px-4 xl:flex-row">
    </div>
  </div>
</template>

<style lang="scss" scoped>
// 样式
</style>
