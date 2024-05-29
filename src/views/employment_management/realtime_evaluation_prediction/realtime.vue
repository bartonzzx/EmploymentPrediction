<route lang="yaml">
meta:
  title: 实时评估和预测
</route>

<script setup lang="ts">
import api from '@/api'
import useUserStore from '@/store/modules/user'
defineOptions({
  name: 'EmploymentManagementAbilityEvaluationAbility',
})
let history_ability: any[] = []

api.post('/employment_management/ability_evaluation/yearly_avg_ability',{
    year: 0
}).then((response)=>{
  history_ability = response.data.map(obj=>Object.values(obj))
  console.log(history_ability)
})

import * as Echarts from 'echarts'
import { ref } from 'vue'
import type { UploadInstance } from 'element-plus'
import Reload from '@/views/reload.vue';
import { nextTick } from 'vue';
import { defineComponent } from 'vue';


const uploadRef = ref<UploadInstance>()
const submitUpload = () => {
  uploadRef.value!.submit()
}
var fileUploaded : boolean = false;
const handleSuccess = (response: any, file: any, fileList: any) => {
    fileUploaded = true;

      initChart1([response.data.re1,response.data.re2,response.data.re3,response.data.re4,response.data.re5,response.data.re6,response.data.re7,response.data.re8,response.data.re9,response.data.re10,response.data.re11,response.data.re12],history_ability[0])
      initChart2([response.data.re1,response.data.re2,response.data.re3,response.data.re4,response.data.re5,response.data.re6,response.data.re7,response.data.re8,response.data.re9,response.data.re10,response.data.re11,response.data.re12],history_ability[0])
      initChart3([response.data.result0,response.data.result1,response.data.result2,response.data.result3,response.data.result4,response.data.result5])
      console.log(fileUploaded)
      console.log('文件上传成功！:', response.data);
      // 处理上传成功后的逻辑，例如刷新界面
}

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

  onMounted(() => {
    window.addEventListener('resize', () => {
      chart1.resize()
      chart2.resize()
      chart3.resize()
    })
  })

  function initChart1(realtime:number [],history_ability:number []) {
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
        color: [
          '#F5F5F7',
          // '#56A3F1',
          'rgba(255, 145, 124)',
          '#FFE434'
        ],
        legend: {
          data: ['本人', '历史平均']
        },
        radar: {
          shape: 'circle',
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
            name: '本人 vs 历史平均',
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
                value: realtime.slice(0,6),
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
  function initChart2(realtime:number [],history_ability:number []) {
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
          data: ['本人', '历史平均']
        },
        color: [
          '#F5F5F7',
          // '#56A3F1',
          'rgba(255, 145, 124)',
          '#FFE434'
        ],
        radar: {
          shape: 'circle',
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
            name: '本人 vs 历史平均',
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
                value: realtime.slice(6,12),
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
  function initChart3(data: number[]) {
    chart3 = Echarts.init(chart3Ref.value)
    const option = {
      title: {
        text: '就业预测结果:各类去向的概率'
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
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5]
          ]
        }
      ]
    }
    chart3.setOption(option)
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
      <el-upload
        ref="uploadRef"
        accept=".pdf"
        limit=1
        class="upload-demo"
        header=""
        action="http://172.16.194.137:3000/employment_management/realtime_evaluation_prediction"
        :auto-upload="false"
        :on-success="handleSuccess">
        <template #trigger>
          <el-button type="primary">选择文件</el-button>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload">
          上传
        </el-button>

        <template #tip>
          <div class="el-upload__tip">
            请上传从教务系统导出的成绩单.pdf
          </div>
        </template>
    </el-upload>
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
        <ElCol :md="32">
          <PageMain title="就业去向预测" style="margin: 10px 0;">
            <div ref="chart3Ref" style="width: 100%; height: 400px;" />
          </PageMain>
        </ElCol>
      </ElRow>
  </div>
</template>
