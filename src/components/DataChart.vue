<template>
    <div ref="chartRef" class="chart-container"></div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted, onUnmounted } from 'vue';
  import * as echarts from 'echarts';
  
  const props = defineProps({
    chartType: String,
  });
  
  const chartRef = ref(null);
  let chartInstance = null;
  
  const initChart = () => {
    if (chartInstance) {
      chartInstance.dispose();
    }
    chartInstance = echarts.init(chartRef.value);
  
    const options = getChartOptions(props.chartType);
    chartInstance.setOption(options);
  };
  
  const getChartOptions = (type) => {
    switch (type) {
      case 'chart1':
        return {
          title: { text: '血压变化趋势' },
          xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
          yAxis: { type: 'value' },
          series: [{ data: [120, 130, 115, 140, 150, 135, 145], type: 'line' }],
        };
      case 'chart2':
        return {
          title: { text: '心率分布' },
          xAxis: { type: 'category', data: ['60-70', '70-80', '80-90', '90-100', '100-110'] },
          yAxis: { type: 'value' },
          series: [{ data: [50, 80, 90, 60, 30], type: 'bar' }],
        };
      case 'chart3':
        return {
          title: { text: '年龄统计' },
          series: [
            {
              type: 'pie',
              data: [
                { value: 40, name: '20-30岁' },
                { value: 30, name: '30-40岁' },
                { value: 20, name: '40-50岁' },
                { value: 10, name: '50-60岁' },
              ],
            },
          ],
        };
      default:
        return {};
    }
  };
  
  watch(() => props.chartType, initChart);
  
  onMounted(() => {
    initChart();
    window.addEventListener('resize', () => chartInstance?.resize());
  });
  
  onUnmounted(() => {
    chartInstance?.dispose();
  });
  </script>
  
  <style>
  .chart-container {
    width: 100%;
    height: 100%;
    min-height: 400px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 10px;
  }
  </style>
  