<route lang="yaml">
meta:
  title: 成绩管理
</route>

<script setup lang="ts">
import api from '@/api'
import useUserStore from '@/store/modules/user'

defineOptions({
  name: 'ScoreManagementScore',
})

const userStore = useUserStore()

api.post('/score_management/score',{
  stu_id: userStore.stu_id
}).then((res) => {
    console.log(res.data)
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
