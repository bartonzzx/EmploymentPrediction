<route lang="yaml">
meta:
  title: 数据管理
</route>

<script setup lang="ts">
import { Delete, Edit, Search, Share, Upload } from '@element-plus/icons-vue'
import type { UploadInstance } from 'element-plus'
import { ref } from 'vue'
import Reload from '@/views/reload.vue';
import { nextTick } from 'vue';
import { defineComponent } from 'vue';

defineOptions({
  name: 'DataManagementData',
})

const uploadRef0 = ref<UploadInstance>()
const uploadRef1 = ref<UploadInstance>()
const uploadRef2 = ref<UploadInstance>()

const submitUpload0 = () => {
  uploadRef0.value!.submit()
}
const submitUpload1 = () => {
  uploadRef1.value!.submit()
}
const submitUpload2 = () => {
  uploadRef2.value!.submit()
}
</script>

<template>
  <div>
    <PageHeader>
      <template #title>
        <div class="flex items-center gap-4">
          数据上传
        </div>
      </template>
      <template #content>
        <div class="text-sm/6">
          <div>
            需要上传的数据有：成绩列表，毕业生去向表，课程与毕业能力对应矩阵（培养方案）
          </div>
          <div>
            成绩列表：从教务系统导出的学生成绩列表。
          </div>
          <div>
            毕业生去向表：从教务系统导出的毕业生去向信息表。
          </div>
          <div>
            课程与毕业能力对应矩阵（培养方案）：由培养方案得到的课程与毕业能力对应矩阵，存在格式要求。使用“H”表示强支撑，“M”表示中等支撑，“L”表示弱支撑。
          </div>
          <div>
            <el-image style="width: 800px; height: 100px;" src='public\upload_course_preview.jpg' fit="contain" />
          </div>
        </div>
      </template>
      <el-upload
        ref="uploadRef0"
        accept=""
        class="upload-demo"
        header=""
        action="http://172.16.194.137:3000/employment_management/realtime_evaluation_prediction"
        :auto-upload="false">
        <template #trigger>
          <el-button type="primary">选择成绩列表</el-button>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload0">
          上传
        </el-button>

        <template #tip>
          <div class="el-upload__tip">
            请上传从教务系统导出的成绩列表
          </div>
        </template>
    </el-upload>

    <el-upload
        ref="uploadRef1"
        accept=""
        class="upload-demo"
        header=""
        action="http://172.16.194.137:3000/employment_management/realtime_evaluation_prediction"
        :auto-upload="false">
        <template #trigger>
          <el-button type="primary">选择毕业生去向表</el-button>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload1">
          上传
        </el-button>

        <template #tip>
          <div class="el-upload__tip">
            请上传从教务系统导出的毕业生去向表
          </div>
        </template>
    </el-upload>
    <el-upload
        ref="uploadRef2"
        accept=".xls, .xlsx"
        class="upload-demo"
        header=""
        action="http://172.16.194.137:3000/employment_management/realtime_evaluation_prediction"
        :auto-upload="false">
        <template #trigger>
          <el-button type="primary">选择课程与毕业能力对应矩阵</el-button>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload2">
          上传
        </el-button>

        <template #tip>
          <div class="el-upload__tip">
            请上传课程与毕业能力对应矩阵
          </div>
        </template>
    </el-upload>
    <el-button-group class="ml-4">
        <el-button type="primary">
          进行数据处理
        <el-icon class="el-icon--right"><Upload /></el-icon>
        </el-button>
        <el-button type="primary" :icon="Delete">删除所有数据</el-button>
      </el-button-group>
    </PageHeader>

  </div>
</template>

<style lang="scss" scoped>
// 样式
</style>
