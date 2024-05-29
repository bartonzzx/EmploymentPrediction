<route lang="yaml">
  meta:
    title: 就业去向预测
  </route>

  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import api from '@/api'
  import useUserStore from '@/store/modules/user'
  import * as Echarts from 'echarts'

  const userStore = useUserStore()
  const chartRef = ref()
  let chart: any

  api.post('/employment_management/employment_prediction/employment',{
    stu_id: userStore.stu_id
  }).then((res) => {
      console.log(res.data)
      const data = res.data
      console.log(data[0].possibility)
      initChart(data)
    })
    .catch((error) => {
      console.error('Error fetching data:', error)
    })

  onMounted(() => {
    window.addEventListener('resize', () => {
      chart.resize()
    })
  })

  function initChart(data: number[]) {
    chart = Echarts.init(chartRef.value)
    const option = {
      title: {
        text: '各类去向的概率'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['概率']
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
        data: ['三资企业', '其他企业', '升学', '国有企业', '待就业', '自由职业']
      },
      series: [
        {
          name: '概率',
          type: 'bar',
          data: [
            data[0].possibility,
            data[1].possibility,
            data[2].possibility,
            data[3].possibility,
            data[4].possibility,
            data[5].possibility
          ]
        }
      ]
    }
    chart.setOption(option)
  }

  function open(url: string) {
    window.open(url, '_blank')
  }
  </script>

  <template>
    <div>
      <PageHeader title="就业去向预测">
        <template #content>
          <p>根据评估得到的就业能力，和2014年——2018年共五年的学生成绩数据，我们训练了一个算法模型。利用该模型进行就业去向的预测。</p>
          <!-- <p style="margin-bottom: 0;"> -->
            <!-- Star：<ElTag>test</ElTag> -->
          <!-- </p> -->
        </template>
      </PageHeader>
      <ElRow :gutter="20" style="margin: 0 10px;">
        <ElCol :md="32">
          <PageMain title="就业去向预测结果" style="margin: 10px 0;">
            <div ref="chartRef" style="width: 100%; height: 400px;" />
          </PageMain>
        </ElCol>
      </ElRow>
    </div>
  </template>

