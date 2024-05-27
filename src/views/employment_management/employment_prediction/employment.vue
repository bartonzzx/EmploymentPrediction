<route lang="yaml">
meta:
  title: 就业去向预测
</route>

<script setup lang="ts">
import api from '@/api'
import useUserStore from '@/store/modules/user'

defineOptions({
  name: 'EmploymentManagementEmploymentPredictionEmployment',
})

const userStore = useUserStore()

api.post('/employment_management/employment_prediction/employment',{
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
    <p>employment_prediction.vue</p>
  </div>
</template>

<style lang="scss" scoped>
// 样式
</style>
