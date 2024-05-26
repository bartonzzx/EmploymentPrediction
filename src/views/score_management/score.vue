<route lang="yaml">
meta:
  title: 成绩管理
</route>

<script setup lang="ts">
import api from '@/api'

defineOptions({
  name: 'ScoreManagementScore',
})

api.get('/score_management/score')
  .then((res) => {
    console.log(res)
  })
  .catch((error) => {
    console.error('Error fetching data:', error)
  })
</script>

<template>
  <div>
    <!-- 布局 -->
    <p>score.vue</p>
  </div>
</template>

<style lang="scss" scoped>
// 样式
</style>
