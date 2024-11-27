<template>
    <div ref="chartRef" class="chart-container"></div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue';
  import * as echarts from 'echarts';
  import data from '../data';
  
  const chartRef = ref(null);
  
  onMounted(() => {
    const chart = echarts.init(chartRef.value);
    chart.setOption({
      title: { text: '不同年龄段的风险概率' },
      xAxis: { type: 'category', data: data.ageProbabilityData.xAxis },
      yAxis: { type: 'value' },
      series: [{ data: data.ageProbabilityData.yAxis, type: 'bar' }],
    });
  });
  </script>
  
  <style>
  .chart-container {
    width: 100%;
    height: 400px;
  }
  </style>
  