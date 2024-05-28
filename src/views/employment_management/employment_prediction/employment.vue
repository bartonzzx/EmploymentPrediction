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
    title: {
      text: '就业预测结果:各类去向的概率'
    },
    legend: {
      padding: 25,
      data: ['概率'],
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        var str = params[0].name + '<br>'
        for (const item of params) {
          str += '概率' + ' : ' + item.value + '%<br>'
        }
        return str
      }
    },
    grid: {
      containLabel: true,
      left: 20
    },
    yAxis: {
      data: ['三资企业', '其他企业', '升学', '国有企业', '待就业', '自由职业'],
      inverse: true,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        margin: 30,
        fontSize: 14
      },
      axisPointer: {
        label: {
          show: true,
          margin: 30
        }
      }
    },
    xAxis: {
      splitLine: { show: true },
      axisLabel: { show: true },
      axisTick: { show: true },
      axisLine: { show: true }
    },
    animationDurationUpdate: 500,
    series: [
      {
        name: '概率',
        id: 'bar1',
        // label: this.labelSetting,
        label: {
          normal: {
            show: true,
            formatter: function(params) { // 标签内容
              return params.value + '%'
            },
            position: 'right',
            fontSize: 16,
            color: '#cdcdcd'
          }
        },
        symbolRepeat: true,
        symbolSize: ['80%', '60%'],
        barCategoryGap: '40%',
        universalTransition: {
          enabled: true,
          delay: function(idx, total) {
            return (idx / total) * 1000
          }
        },
        data: [44.04, 56.44, 87.48, 61.07, 33.91, 13.17]
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

