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

  //个人数据
  api.post('/employment_management/ability_evaluation/personal_ability',{
    stu_id: userStore.stu_id
  }).then((res) => {
      console.log(res.data)

    })
    .catch((error) => {
      console.error('Error fetching data:', error)
    })

  //年级平均
  api.post('/employment_management/ability_evaluation/yearly_avg_ability',{
    year: userStore.stu_id.substring(0,4)
  }).then((res) => {
      console.log(res.data)
    })
    .catch((error) => {
      console.error('Error fetching data:', error)
    })
  //历史平均
  api.post('/employment_management/ability_evaluation/yearly_avg_ability',{
    year: 0
  }).then((res) => {
      console.log(res.data)
    })
    .catch((error) => {
      console.error('Error fetching data:', error)
    })


  // 线图数据
let year_data = [2014, 2015, 2016, 2017, 2018]
let promises = []

for (let i = 0; i < year_data.length; i++) {
  promises.push(api.post('/employment_management/ability_evaluation/yearly_ability', {
    year: year_data[i]
  }))
}

Promise.all(promises)
  .then((responses) => {
    // console.log(responses[0].data)
    // 处理每个年份的数据，例如：
    const data2014 = responses[0].data.map(obj => Object.values(obj))
    console.log(data2014)
    const data2015=responses[1].data.map(obj => Object.values(obj))
    console.log(data2015)
    const data2016=responses[2].data.map(obj => Object.values(obj))
    console.log(data2016)
    const data2017=responses[3].data.map(obj => Object.values(obj))
    console.log(data2017)
    const data2018=responses[4].data.map(obj => Object.values(obj))
    console.log(data2018)
    initChart3(data2014,data2015,data2016,data2017,data2018)
  })
  .catch((error) => {
    console.error('Error fetching data:', error)
  })




  import * as Echarts from 'echarts'
import echarts from 'echarts/types/dist/echarts.js';
import { min } from 'lodash-es';

  const chart1Ref = ref()
  const chart2Ref = ref()
  const chart3Ref = ref()
  let chart1: any
  let chart2: any
  let chart3: any

  var schema = [
  { name: '工程知识', index: 0},
  { name: '问题分析', index: 1},
  { name: '设计/开发解决方案', index: 2},
  { name: '研究', index: 3},
  { name: '使用现代工具', index: 4},
  { name: '工程与社会', index: 5},
  { name: '环境和可持续发展', index: 6},
  { name: '职业规范', index: 7},
  { name: '个人和团队', index: 8},
  { name: '沟通', index: 9 },
  { name: '项目管理', index: 10},
  { name: '终身学习', index: 11}
];
  // var lineStyle = {
    //  width: 0.5,
    //  opacity: 2
  //  }

  onMounted(() => {
    initChart1()
    initChart2()
    // initChart3()
    window.addEventListener('resize', () => {
      chart1.resize()
      chart2.resize()
      chart3.resize()
    })
  })

  function initChart1() {
    chart1 = Echarts.init(chart1Ref.value)
    // 配置数据
    const option = {
      backgroundColor: '#F5F5F5',
        tooltip:{
          trigger:'axis'
        },
        // title: {
        //   text: '能力图'
        // },
        legend: {
          data: ['本人', '同级平均','历史平均']
        },
        radar: {
          shape: 'circle',
          raduys: 120,
          startAngle: 90,
          splitNumber: 4,
          axisName:{
            color:'#428BD4'
          },
          splitArea:{
            areaStyle:{
              color:['#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
              shadowColor:'rgba(0,0,0,0.2)',
              shadowBlur:10
            }
          },
          axisLine:{
            lineStyle:{
              color:'rgb(17,12,12)'
            }
          },
          splitLine:{
            lineStyle:{
              color:'rgb(17,12,12)'
            }
          },
          indicator: [
            { name: '工程知识', max: 6500 },
            { name: '问题分析', max: 16000 },
            { name: '设计/解决问题', max: 30000 },
            { name: '研究', max: 38000 },
            { name: '使用现代工具', max: 52000 },
            { name: '工程与社会', max: 25000 }
          ]
        },
        series: [
          {
            name: '本人 vs 同级平均 vs 历史平均',
            type: 'radar',
            tooltip:{
              trigger:'item'
            },
            data: [
              {
                value: [4200, 3000, 20000, 35000, 50000, 18000],
                name: '本人',
                Symbol: 'rect',
                lineStyle:{
                  color: 'red'
                }
              },
              {
                value: [5000, 14000, 28000, 26000, 42000, 21000],
                name: '同级平均'
              },
              {
                value: [4000, 2800, 26000, 42000, 21000,5000],
                name: '历史平均'
              }
            ]
          }
        ]
    }
    // 传入数据
    chart1.setOption(option)
  }
  function initChart2() {
    chart2 = Echarts.init(chart2Ref.value)
    // 配置数据
    const option = {
      backgroundColor: '#F5F5F5',
        tooltip:{
          trigger:'axis'
        },
        // title: {
        //   text: '能力图'
        // },
        legend: {
          data: ['本人', '同级平均','历史平均']
        },
        radar: {
          shape: 'circle',
          raduys: 120,
          startAngle: 90,
          splitNumber: 4,
          axisName:{
            color:'#428BD4'
          },
          splitArea:{
            areaStyle:{
              color:['#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
              shadowColor:'rgba(0,0,0,0.2)',
              shadowBlur:10
            }
          },
          axisLine:{
            lineStyle:{
              color:'rgb(17,12,12)'
            }
          },
          splitLine:{
            lineStyle:{
              color:'rgb(17,12,12)'
            }
          },
          indicator: [
            { name: '1', max: 6500 },
            { name: '2', max: 16000 },
            { name: '3', max: 30000 },
            { name: '4', max: 38000 },
            { name: '5', max: 52000 },
            { name: '6', max: 25000 }
          ]
        },
        series: [
          {
            name: '本人 vs 同级平均 vs 历史平均',
            type: 'radar',
            tooltip:{
              trigger:'item'
            },
            data: [
              {
                value: [4200, 3000, 20000, 35000, 50000, 18000],
                name: '本人',
                Symbol: 'rect',
                lineStyle:{
                  color: 'red'
                }
              },
              {
                value: [5000, 14000, 28000, 26000, 42000, 21000],
                name: '同级平均'
              },
              {
                value: [4000, 2800, 26000, 42000, 21000,5000],
                name: '历史平均'
              }
            ]
          }
        ]
    }
    // 传入数据
    chart2.setOption(option)
  }



  function initChart3(data2014:number [],data2015:number [],data2016:number [],data2017:number [],data2018:number []) {
    chart3 = Echarts.init(chart3Ref.value)
    // 配置数据
    // const indices = {
    //   name: 0,
    //   group: 1,
    //   id: 16
    // };
    const option = {
      backgroundColor: '#F5F5F5',
      tooltip: {
        padding: 10,
        backgroundColor: '#000',
        borderColor: '#777',
        borderWidth: 1
      },
      title: [
        {
          // text: '就业能力统计',
          left: 0,
          textStyle: {
            color: '#fff',
            fontSize: 20,
            padding: 25
          }
        }
      ],
      legend: {
        bottom:30,
        data: ['2014', '2015', '2016', '2017', '2018'],
        itemGap: 20,
        textStyle: {
          color: '#000',
          // color: '#fff',
          fontSize: 14
        }
      },
      parallelAxis: [
      { dim: 0, name: schema[0].name, min:0, max:100 },
      { dim: 1, name: schema[1].name, min:0, max:100 },
      { dim: 2, name: schema[2].name, min:0, max:100 },
      { dim: 3, name: schema[3].name, min:0, max:100 },
      { dim: 4, name: schema[4].name, min:0, max:100 },
      { dim: 5, name: schema[5].name, min:0, max:100 },
      { dim: 6, name: schema[6].name, min:0, max:100 },
      { dim: 7, name: schema[7].name, min:0, max:100 },
      { dim: 8, name: schema[8].name, min:0, max:100 },
      { dim: 9, name: schema[9].name, min:0, max:100 },
      { dim: 10, name: schema[10].name, min:0, max:100 },
      { dim: 11, name: schema[11].name, min:0, max:100 }
      ],
      parallel: {
        left: '2%',
        right: '5%',
        // top: 150,
        // height: 300,
        bottom: 100,
        // layout: 'vertical',
        parallelAxisDefault: {
          nameGap: 20,
          nameTextStyle: {
            color: '#101010',
            fontSize: 14
          },
          axisLine: {
            lineStyle: {
              color: '#aaa'
            }
          },
          axisTick: {
            lineStyle: {
              color: '#777'
            }
          },
          splitLine: {
            show: false,
            color: '#000'
          },
          axisLabel: {
            color: '#000'
          },
          realtime: false
        }
      },
      animation:false,
      series: [
        {
          smooth:true,
          data: data2014,
          name: '2014',
          Symbol: 'rect',
          type: 'parallel',
          lineStyle:{
            color: 'red',
            width: 0.5,
            opacity: 2,
          }
        },
        {
          smooth:true,
          data: data2015,
          name: '2015',
          Symbol: 'rect',
          type: 'parallel',
          lineStyle:{
            color: 'orange',
            width: 0.5,
            opacity: 2,
          }
        },
        {
          smooth:true,
          data: data2016,
          name: '2016',
          Symbol: 'rect',
          type: 'parallel',
          lineStyle:{
            width: 0.5,
            opacity: 2,
            color: 'yellow'
          }
        },
        {
          smooth:true,
          data: data2017,
          name: '2017',
          Symbol: 'rect',
          type: 'parallel',
          lineStyle:{
            width: 0.5,
            opacity: 2,
            color: 'yellow'
          }
        },
        {
          smooth:true,
          data: data2018,
          name: '2018',
          Symbol: 'rect',
          type: 'parallel',
          lineStyle:{
            width: 0.5,
            opacity: 2,
            color: 'green'
          }
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
      <Alert />
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
      <ElRow  :gutter="20" style="margin: -10px 10px;">
        <ElCol :md="12">
          <PageMain title="能力图" style="margin: 10px 0;">
            <div ref="chart1Ref" style="width: 100%; height: 400px;" />
          </PageMain>
        </ElCol>
        <ElCol :md="12">
          <PageMain title="能力图" style="margin: 10px 0;">
            <div ref="chart2Ref" style="width: 100%; height: 400px;" />
          </PageMain>
        </ElCol>
      </ElRow>
      <ElRow :gutter="20" style="margin: 0 10px;">
        <ElCol :md="32">
          <PageMain title="就业能力统计" style="margin: 10px 0;">
            <div ref="chart3Ref" style="width: 100%; height: 400px;" />
          </PageMain>
        </ElCol>
        <!-- <ElCol :md="12">
          <PageMain title="雷达图" style="margin: 10px 0;">
            <div ref="chart4Ref" style="width: 100%; height: 400px;" />
          </PageMain>
        </ElCol> -->
      </ElRow>
    </div>
  </template>
