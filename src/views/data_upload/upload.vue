<route lang="yaml">
meta:
  title: 数据上传
</route>

<script setup lang="ts">
defineOptions({
  name: 'DataUploadUpload',
})
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
            <el-image style="width: 1500px; height: 600px;" src='public\upload_course_preview.jpg' fit="contain" />
          </div>
        </div>
      </template>
    </PageHeader>
  </div>
</template>

<style lang="scss" scoped>
// 样式
</style>
