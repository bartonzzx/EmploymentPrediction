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
  import * as Echarts from 'echarts'

const chart3Ref = ref()
let chart3: any

onMounted(() => {
  initChart3()
  window.addEventListener('resize', () => {
    chart3.resize()
  })
})

function initChart3() {
  chart3 = Echarts.init(chart3Ref.value)
  // 配置数据
  const option = {
    titile:{
      text:'就业预测结果:各类去向的概率'
    },
    tooltip:{
      trigger:'axis',
      axisPointer:{
        type:'shadow'
      }
    },
    legend:{
      data:['2011','2012']
    },
    grid: {
      left: 0,
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      boundaryGap: [0, 0.01]
    },
    yAxis: {
      type: 'category',
      data: ['Brazil', 'Indonesia', 'USA', 'India', 'China', 'World']
    },
    series: [
      {
        name: '2011',
        type: 'bar',
        data: [18203, 23489, 29034, 104970, 131744, 630230]
      },
      {
        name: '2012',
        type: 'bar',
        data: [19325, 23438, 31000, 121594, 134141, 681807]
      }
    ]
  }
  // 传入数据
  chart3.setOption(option)
}

function open(url: string) {
  window.open(url, '_blank')
}
</script>

<template>
  <div>
    <PageHeader title="ECharts">
      <template #content>
        <p>不建议使用第三方封装的组件（如：vue-echarts），因为 ECharts 本身文档和演示 demo 已经很完善且方便了，再使用第三方的组件在使用体验上反而会束手束脚。</p>
        <p style="margin-bottom: 0;">
          安装命令：<ElTag>pnpm add echarts</ElTag>
        </p>
      </template>
      <ElButton @click="open('https://github.com/apache/echarts')">
        <template #icon>
          <SvgIcon name="i-ep:link" />
        </template>
        访问 echarts
      </ElButton>
    </PageHeader>
    <ElRow :gutter="20" style="margin: 0 10px;">
      <ElCol :md="32">
        <PageMain title="第三个线图" style="margin: 10px 0;">
          <div ref="chart3Ref" style="width: 100%; height: 400px;" />
        </PageMain>
      </ElCol>
    </ElRow>
  </div>
</template>

