<route lang="yaml">
meta:
  title: 能力评估
</route>

<script setup lang="ts">
import api from '@/api'
import useUserStore from '@/store/modules/user'
defineOptions({
  name: 'EmploymentManagementAbilityEvaluationAbility',
})

const userStore = useUserStore()

api.post('/employment_management/ability_evaluation/personal_ability',{
  stu_id: userStore.stu_id
}).then((res) => {
    console.log(res.data)
  })
  .catch((error) => {
    console.error('Error fetching data:', error)
  })

let year_data=[0,2014,2015,2016,2017,2018]

for(let i=0;i<year_data.length;i++){
  api.post('/employment_management/ability_evaluation/yearly_ability',{
  year: year_data[i]
}).then((res) => {
    console.log(res.data)
  })
  .catch((error) => {
    console.error('Error fetching data:', error)
  })

}

</script>

<template>
  <div>
    <!-- 布局 -->
    <p>ability.vue</p>
  </div>
</template>

<style lang="scss" scoped>
// 样式
</style>
