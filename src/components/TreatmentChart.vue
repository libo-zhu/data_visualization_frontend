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
      title: { text: '治疗方式分布' },
      series: [
        {
          type: 'pie',
          data: data.treatmentData,
        },
      ],
    });
  });
  </script>
  