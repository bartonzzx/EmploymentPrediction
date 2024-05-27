<route lang="yaml">
  meta:
    title: 课程管理
  </route>

<script setup lang="ts">
import api from '@/api'

defineOptions({
  name: 'CourseManagementCourse',
})

api.get('/course_management/course')
  .then((res) => {
    console.log(res.data)
  })
  .catch((error) => {
    console.error('Error fetching data:', error)
  })
</script>

<template>
  <div>
    <!-- 布局 -->
    <p>course.vue</p>
  </div>
</template>

  <style lang="scss" scoped>
  // 样式
  </style>
