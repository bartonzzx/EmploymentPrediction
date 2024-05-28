<template>
  <el-table
    :data="filteredData"
    stripe
    style="width: 100%;"
    :default-sort="{ prop: 'coursename', order: 'ascending' }"
    :row-class-name="rowClassName"
  >
    <el-table-column prop="coursename" label="课程名" min-width="150"></el-table-column>
    <el-table-column prop="re1" label="工程知识" min-width="100"></el-table-column>
    <el-table-column prop="re2" label="问题分析" min-width="100"></el-table-column>
    <el-table-column prop="re3" label="设计/开发解决方案" min-width="100"></el-table-column>
    <el-table-column prop="re4" label="研究" min-width="100"></el-table-column>
    <el-table-column prop="re5" label="使用现代工具" min-width="100"></el-table-column>
    <el-table-column prop="re6" label="工程与社会" min-width="100"></el-table-column>
    <el-table-column prop="re7" label="环境和可持续发展" min-width="100"></el-table-column>
    <el-table-column prop="re8" label="职业规范" min-width="100"></el-table-column>
    <el-table-column prop="re9" label="个人和团队" min-width="100"></el-table-column>
    <el-table-column prop="re10" label="沟通" min-width="100"></el-table-column>
    <el-table-column prop="re11" label="项目管理" min-width="100"></el-table-column>
    <el-table-column prop="re12" label="终身学习" min-width="100"></el-table-column>
    <el-table-column prop="score" label="考试成绩" min-width  ="100"></el-table-column>
    <!-- <el-table-column align="right">
      <template v-slot:header>
        <el-input v-model="search" size="mini" placeholder="输入关键字搜索" @input="handleSearch"/>
      </template>
    </el-table-column> -->
  </el-table>
</template>

<script setup lang="ts">
import api from '@/api'
import { ref } from 'vue'
import useUserStore from '@/store/modules/user'
defineOptions({
  name: 'CourseManagementCourse',
})

const tableData = ref([]);
const filteredData = ref([]);
const search = ref('');
const userStore = useUserStore()

api.post('/course_management/course',{
  stu_id: userStore.stu_id
})
  .then((res) => {
    console.log(res.data)
    tableData.value = res.data;
    filteredData.value = res.data; // 初始化过滤数据
  })
  .catch((error) => {
    console.error('Error fetching data:', error)
  })
  const handleSearch = () => {
  if (search.value) {
    filteredData.value = tableData.value.filter((item) => {
      return Object.values(item).some(val => String(val).includes(search.value));
    });
  } else {
    filteredData.value = tableData.value;
  }
}

const rowClassName = ({ row }) => {
  console.log("Row Score:", row.score); // 添加调试语句
  return Number(row.score) < 60 ? 'row-red' : '';
}
</script>

