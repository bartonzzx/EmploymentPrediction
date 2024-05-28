<!-- <template>
  <el-table
    :data="filteredData"
    stripe
    style="width: 100%;"
    :default-sort="{ prop: 'date', order: 'descending' }"
  >
    <el-table-column prop="coursename" label="课程名" width="310"></el-table-column>
    <el-table-column prop="natureofexam" label="考试性质" width="300"></el-table-column>
    <el-table-column prop="credit" label="学分" sortable width="200"></el-table-column>
    <el-table-column prop="score" label="考试成绩" sortable width="200"></el-table-column>
    <el-table-column align="right">
      <template v-slot:header>
        <el-input v-model="search" size="mini" placeholder="输入关键字搜索" @input="handleSearch"/>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import useUserStore from '@/store/modules/user'

defineOptions({
  name: 'ScoreManagementScore',
})

const tableData = ref([]);
const filteredData = ref([]);
const search = ref('');
const userStore = useUserStore()

api.post('/score_management/score', {
  stu_id: userStore.stu_id
}).then((res) => {
  console.log(res.data)
  tableData.value = res.data;
  filteredData.value = res.data; // 初始化过滤数据
}).catch((error) => {
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
</script>

<style lang="scss" scoped>
// 样式
</style> -->

<template>
  <el-table
    :data="tableData"
    style="width: 100%;"
    :default-sort="{ prop: 'coursename', order: 'ascending' }"
    :row-class-name="rowClassName"
  >
    <el-table-column prop="coursename" label="课程名" min-width="100"></el-table-column>
    <el-table-column prop="natureofexam" label="考试性质" min-width="100"></el-table-column>
    <el-table-column prop="credit" label="学分" sortable min-width="100"></el-table-column>
    <el-table-column prop="score" label="考试成绩" sortable min-width="100"></el-table-column>
    <el-table-column align="right">
      <template v-slot:header>
        <el-input v-model="search" size="mini" placeholder="输入关键字搜索" @input="handleSearch"/>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'
import useUserStore from '@/store/modules/user'

defineOptions({
  name: 'ScoreManagementScore',
})

const tableData = ref([]);
const filteredData = ref([]);
const search = ref('');
const userStore = useUserStore()

api.post('/score_management/score', {
  stu_id: userStore.stu_id
}).then((res) => {
  console.log(res.data)
  tableData.value = res.data;
  filteredData.value = res.data; // 初始化过滤数据
}).catch((error) => {
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

const rowClassName = ({ row , rowIndex }) => {
  // console.log("Row Score:", row.score); // 添加调试语句
  // return Number(row.score) < 60 ? 'row-red' : '';
  if(Number(row.score) < 60) return 'unaccept';
  else if(Number(row.score >= 80)) return 'accept';
  else return 'warning';
}
</script>

<style>
.el-table .unaccept {
  background-color: rgb(253 232 230);
}

.el-table .warning {
  background-color: oldlace;
}

.el-table .accept {
  background-color: #f0f9eb;
}
</style>




