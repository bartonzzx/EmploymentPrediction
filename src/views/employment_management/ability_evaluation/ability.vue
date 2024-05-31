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

let promises_ability = []

promises_ability.push(api.post('/employment_management/ability_evaluation/personal_ability',{
    stu_id: userStore.stu_id
  }))
  promises_ability.push(api.post('/employment_management/ability_evaluation/yearly_avg_ability',{
    year: userStore.stu_id.substring(0,4)
  }))
  promises_ability.push(api.post('/employment_management/ability_evaluation/yearly_avg_ability',{
    year: 0
  }))

Promise.all(promises_ability)
  .then((responses) => {
    // console.log(responses[0].data)
    // 处理每个年份的数据，例如：
    let temp = responses[0].data.map(obj => Object.values(obj))
    const personal_ability = temp[0]
    console.log(personal_ability)
    temp=responses[1].data.map(obj => Object.values(obj))
    const yearly_ability = temp[0]
    console.log(yearly_ability)
    temp=responses[2].data.map(obj => Object.values(obj))
    const history_ability = temp[0]
    console.log(history_ability)
    initChart1(personal_ability,yearly_ability,history_ability)
    initChart2(personal_ability,yearly_ability,history_ability)
  })
  .catch((error) => {
    console.error('Error fetching data:', error)
  })

  // 线图数据
let year_data = [2014, 2015, 2016, 2017, 2018]
let promises_line = []

for (let i = 0; i < year_data.length; i++) {
  promises_line.push(api.post('/employment_management/ability_evaluation/yearly_ability', {
    year: year_data[i]
  }))
}

Promise.all(promises_line)
  .then((responses) => {
    // console.log(responses[0].data)
    // 处理每个年份的数据，例如：
    const data2014 = responses[0].data.map(obj => Object.values(obj))
    // console.log(data2014)
    const data2015=responses[1].data.map(obj => Object.values(obj))
    // console.log(data2015)
    const data2016=responses[2].data.map(obj => Object.values(obj))
    // console.log(data2016)
    const data2017=responses[3].data.map(obj => Object.values(obj))
    // console.log(data2017)
    const data2018=responses[4].data.map(obj => Object.values(obj))
    // console.log(data2018)
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
    // initChart1()
    // initChart2()
    // initChart3()
    window.addEventListener('resize', () => {
      chart1.resize()
      chart2.resize()
      chart3.resize()
    })
  })

  function initChart1(personal_ability:number [],yearly_ability:number [],history_ability:number []) {
    chart1 = Echarts.init(chart1Ref.value)
    // 配置数据
    const option = {
      backgroundColor: '#FFFFFF',
        tooltip:{
          trigger:'axis'
        },
        // title: {
        //   text: '能力图'
        // },
        color: [
          '#F5F5F7',
          // '#56A3F1',
          'rgba(255, 145, 124)',
          '#FFE434'
        ],
        legend: {
          data: ['本人', '同级平均','历史平均']
        },
        radar: {
          // shape: 'circle',
          splitNumber: 5,
          axisName:{
            color:'#000000'
          },
          splitArea:{
            areaStyle:{
              color:['#bda29a', '#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
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
            { name: '工程知识', max: 100, min: 20 },
            { name: '问题分析', max: 100, min: 20 },
            { name: '设计/解决问题', max: 100, min: 20 },
            { name: '研究', max: 100, min: 20 },
            { name: '使用现代工具', max: 100, min: 20 },
            { name: '工程与社会', max: 100, min: 20 }
          ]
        },
        series: [
          {
            name: '本人 vs 同级平均 vs 历史平均',
            type: 'radar',
            emphasis: {
              lineStyle: {
                width: 4
              }
            },
            tooltip:{
              trigger:'item'
            },
            data: [
              {
                value: personal_ability.slice(0,6),
                name: '本人',
                symbol: 'rect',
                symbolSize: 12,
                lineStyle: {
                  type: 'dashed'
                },
                label: {
                  show: true,
                  formatter: function(params) {
                    return params.value
                  }
                }
              },
              {
                value: yearly_ability.slice(0,6),
                name: '同级平均',
              },
              {
                value: history_ability.slice(0,6),
                name: '历史平均'
              }
            ]
          }
        ]
    }
    // 传入数据
    chart1.setOption(option)
  }
  function initChart2(personal_ability:number [],yearly_ability:number [],history_ability:number []) {
    chart2 = Echarts.init(chart2Ref.value)
    // 配置数据
    const option = {
      backgroundColor: '#FFFFFF',
        tooltip:{
          trigger:'axis'
        },
        // title: {
        //   text: '能力图'
        // },
        legend: {
          data: ['本人', '同级平均','历史平均']
        },
        color: [
          '#F5F5F7',
          // '#56A3F1',
          'rgba(255, 145, 124)',
          '#FFE434'
        ],
        radar: {
          // shape: 'circle',
          splitNumber: 5,
          axisName:{
            color:'#000000'
          },
          splitArea:{
            areaStyle:{
              color:['#bda29a', '#77EADF', '#26C3BE', '#64AFE9', '#428BD4'],
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
            { name: '环境和可持续发展', max: 100, min: 20 },
            { name: '职业规范', max: 100, min: 20 },
            { name: '个人和团队', max: 100, min: 20 },
            { name: '沟通', max: 100, min: 20 },
            { name: '项目管理', max: 100, min: 20 },
            { name: '终身学习', max: 100, min: 20 }
          ]
        },
        series: [
          {
            name: '本人 vs 同级平均 vs 历史平均',
            type: 'radar',
            emphasis: {
              lineStyle: {
                width: 4
              }
            },
            tooltip:{
              trigger:'item'
            },
            data: [
              {
                value: personal_ability.slice(6,12),
                name: '本人',
                symbol: 'rect',
                symbolSize: 12,
                lineStyle: {
                  type: 'dashed'
                },
                label: {
                  show: true,
                  formatter: function(params) {
                    return params.value
                  }
                }
              },
              {
                value: yearly_ability.slice(6,12),
                name: '同级平均'
              },
              {
                value: history_ability.slice(6,12),
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
      backgroundColor: '#FFFFFF',
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
            fontSize: 22,
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
          fontSize: 16
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
            fontSize: 16
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
      <PageHeader title="就业能力评估">
        <template #content>
          <p>综合考虑用户成绩、专业培养方案、课程重要性和考试性质，对用户就业能力进行评估。评估结果为百分制。</p>
          <p>就业能力分为：工程知识能力，问题分析能力，设计/开发解决方案能力，研究能力，使用现代工具能力，工程与社会，环境和可持续发展，职业规范，个人和团队，沟通能力，项目管理能力，终身学习能力。详情请见专业培养方案。</p>
          <p>专业培养方案:</p>
          <p><a href="https://jwxy.xtu.edu.cn/info/1016/1126.htm">2021年计算机科学与技术专业本科人才培养方案</a></p>
          <p><a href="https://jwxy.xtu.edu.cn/info/1016/1125.htm">2021年网络空间安全专业本科人才培养方案</a></p>
          <p><a href="https://jwxy.xtu.edu.cn/info/1016/1124.htm">2021年软件工程专业本科人才培养方案</a></p>
          <p><a href="https://jwxy.xtu.edu.cn/info/1016/1119.htm">历年人才培养方案</a></p>
          <!-- <p style="margin-bottom: 0;"> -->
            <!-- Star：<ElTag>test</ElTag> -->
          <!-- </p> -->
        </template>
      </PageHeader>
      <ElRow  :gutter="20" style="margin: -10px 10px;">
        <ElCol :md="12">
          <PageMain title="能力图(1)" style="margin: 10px 0;">
            <div ref="chart1Ref" style="width: 100%; height: 400px;" />
          </PageMain>
        </ElCol>
        <ElCol :md="12">
          <PageMain title="能力图(2)" style="margin: 10px 0;">
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
      </ElRow>
    </div>
  </template>
