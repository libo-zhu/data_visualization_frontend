<template>
    <div class="history-detail">
      <h1>{{ cityName }} 历史天气数据</h1>
      
      <!-- 筛选选项 -->
      <div class="filters">
        <div class="filter-group">
          <label for="displayMode">显示模式:</label>
          <select v-model="displayMode" id="displayMode">
            <option value="all">全部</option>
            <option value="year">按年</option>
            <option value="quarter">按季度</option>
          </select>
        </div>
  
        <div v-if="displayMode === 'year'" class="filter-group">
          <label for="yearSelect">选择年份:</label>
          <select v-model="selectedYear" id="yearSelect">
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
          </select>
        </div>
  
        <div v-if="displayMode === 'quarter'" class="filter-group">
          <label for="yearSelectQuarter">选择年份:</label>
          <select v-model="selectedYear" id="yearSelectQuarter">
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
          </select>
  
          <label for="quarterSelect">选择季度:</label>
          <select v-model="selectedQuarter" id="quarterSelect">
            <option v-for="q in availableQuarters" :key="q" :value="q">{{ q }}</option>
          </select>
        </div>
      </div>
  
      <!-- 加载和错误状态 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="error" class="error">{{ error }}</div>
  
      <!-- 图表展示 -->
      <div v-if="!loading && !error">
        <!-- 温度趋势图 -->
        <div ref="temperatureChart" class="chart-container"></div>
        <!-- 天气分布图 -->
        <div ref="weatherChart" class="chart-container"></div>
        <!-- 风向与风力热力图 -->
        <div ref="windHeatmapChart" class="chart-container"></div>
      </div>
    </div>
  </template>
  
  <script>
  /**
   * 使用 ECharts 5.6.0 的按需加载方式：
   * 如果你想使用全量包，可改为：
   *   import * as echarts from 'echarts'
   */
  import { ref, onMounted, watch, computed, nextTick } from 'vue';
  import axios from 'axios';
  
  // ECharts 5.x 按需加载
  import * as echarts from 'echarts/core';
  import { LineChart, PieChart, HeatmapChart } from 'echarts/charts';
  import { 
    TitleComponent, 
    LegendComponent, 
    TooltipComponent, 
    VisualMapComponent, 
    GridComponent 
  } from 'echarts/components';
  import { CanvasRenderer } from 'echarts/renderers';
  
  // 注册需要的图表和组件
  echarts.use([
    LineChart,
    PieChart,
    HeatmapChart,
    TitleComponent,
    LegendComponent,
    TooltipComponent,
    VisualMapComponent,
    GridComponent, // 确保 GridComponent 已注册
    CanvasRenderer
  ]);
  
  export default {
    name: 'HistoryDetail',
    props: ['url'],
    setup(props) {
      const cityName = ref('');
      const temperatureChart = ref(null);
      const weatherChart = ref(null);
      const windHeatmapChart = ref(null);
  
      // 存放 ECharts 实例
      const temperatureChartInstance = ref(null);
      const weatherChartInstance = ref(null);
      const windHeatmapChartInstance = ref(null);
  
      const loading = ref(true);
      const error = ref(null);
  
      // 筛选相关的状态
      const displayMode = ref('all'); // 'all', 'year', 'quarter'
      const selectedYear = ref(null);
      const selectedQuarter = ref(null);
  
      // 存储所有数据
      const allData = ref([]);
  
      // 可用的年份和季度
      const availableYears = ref([]);
      const availableQuarters = computed(() => ['第一季度', '第二季度', '第三季度', '第四季度']);
  
      // 检查 ECharts 是否正确初始化
      const isEchartsAvailable = () => {
        return echarts && typeof echarts.init === 'function';
      };
  
      // 数据获取和处理
      const fetchHistoryData = async () => {
        try {
          console.log(`Fetching history data for URL: ${props.url}`);
          const response = await axios.get(`http://localhost:8080/api/history/${props.url}`);
          console.log('History data fetched:', response.data);
  
          if (response.data.length === 0) {
            throw new Error('没有找到该城市的历史数据');
          }
  
          cityName.value = response.data[0].city;
          allData.value = response.data;
  
          // 提取可用的年份
          availableYears.value = Array.from(
            new Set(response.data.map(entry => new Date(entry.date).getFullYear()))
          ).sort((a, b) => a - b);
  
          // 默认选择最新的年份
          if (availableYears.value.length > 0) {
            selectedYear.value = availableYears.value[availableYears.value.length - 1];
          }
  
        } catch (err) {
          console.error('Error fetching history data:', err);
          error.value = err.message || '获取历史数据失败';
        } finally {
          loading.value = false;
          if (!error.value) {
            await nextTick(); 
            await updateCharts(); 
          }
        }
      };
  
      // 根据选择过滤数据
      const filteredData = computed(() => {
        if (displayMode.value === 'all') {
          return allData.value;
        } else if (displayMode.value === 'year') {
          return allData.value.filter(
            entry => new Date(entry.date).getFullYear() === selectedYear.value
          );
        } else if (displayMode.value === 'quarter') {
          if (!selectedYear.value || !selectedQuarter.value) return [];
          const quarterMonthMap = {
            '第一季度': [1, 2, 3],
            '第二季度': [4, 5, 6],
            '第三季度': [7, 8, 9],
            '第四季度': [10, 11, 12],
          };
          const months = quarterMonthMap[selectedQuarter.value];
          return allData.value.filter(entry => {
            const date = new Date(entry.date);
            return (
              date.getFullYear() === selectedYear.value &&
              months.includes(date.getMonth() + 1)
            );
          });
        }
        return allData.value;
      });
  
      // 更新图表
      const updateCharts = async () => {
        const data = filteredData.value;
  
        if (data.length === 0) {
          // 如果没有数据，清空图表
          clearCharts();
          return;
        }
  
        // 处理温度趋势数据
        const temperatureData = processTemperatureData(data);
        console.log('Temperature Data:', temperatureData);
  
        // 处理天气分布数据
        const weatherData = processWeatherData(data);
        console.log('Weather Data:', weatherData);
  
        // 处理风向与风力数据
        const windHeatmapData = processWindHeatmapData(data);
        console.log('Wind Heatmap Data:', windHeatmapData);
  
        // 绘制图表
        console.log('Drawing Temperature Chart');
        drawTemperatureChart(temperatureData);
  
        console.log('Drawing Weather Chart');
        drawWeatherChart(weatherData);
  
        console.log('Drawing Wind Heatmap Chart');
        drawWindHeatmapChart(windHeatmapData);
      };
  
      // 清空图表
      const clearCharts = () => {
        if (temperatureChartInstance.value) {
          temperatureChartInstance.value.clear();
        }
        if (weatherChartInstance.value) {
          weatherChartInstance.value.clear();
        }
        if (windHeatmapChartInstance.value) {
          windHeatmapChartInstance.value.clear();
        }
      };
  
      // 处理温度数据
      const processTemperatureData = (data) => {
        if (displayMode.value === 'all') {
          const tempByYear = {};
  
          data.forEach(entry => {
            const year = new Date(entry.date).getFullYear();
            if (!tempByYear[year]) {
              tempByYear[year] = { min: [], max: [] };
            }
            const minTemp = parseInt(entry.minTemperature.replace('℃', ''));
            const maxTemp = parseInt(entry.maxTemperature.replace('℃', ''));
            tempByYear[year].min.push(minTemp);
            tempByYear[year].max.push(maxTemp);
          });
  
          // 计算每年的最低和最高温度
          const years = Object.keys(tempByYear).sort((a, b) => a - b);
          const minTemps = years.map(year => Math.min(...tempByYear[year].min));
          const maxTemps = years.map(year => Math.max(...tempByYear[year].max));
  
          return { categories: years, minTemps, maxTemps };
        } else if (displayMode.value === 'year') {
          const tempByMonth = Array.from({ length: 12 }, () => ({ min: [], max: [] }));
  
          data.forEach(entry => {
            const month = new Date(entry.date).getMonth(); // 0-11
            const minTemp = parseInt(entry.minTemperature.replace('℃', ''));
            const maxTemp = parseInt(entry.maxTemperature.replace('℃', ''));
            tempByMonth[month].min.push(minTemp);
            tempByMonth[month].max.push(maxTemp);
          });
  
          const categories = Array.from({ length: 12 }, (_, i) => `${i + 1}月`);
          const minTemps = tempByMonth.map(m => (m.min.length ? Math.min(...m.min) : null));
          const maxTemps = tempByMonth.map(m => (m.max.length ? Math.max(...m.max) : null));
  
          return { categories, minTemps, maxTemps };
        } else if (displayMode.value === 'quarter') {
          const quarterMonthMap = {
            '第一季度': [1, 2, 3],
            '第二季度': [4, 5, 6],
            '第三季度': [7, 8, 9],
            '第四季度': [10, 11, 12],
          };
          const months = quarterMonthMap[selectedQuarter.value];
          const tempByMonth = months.map(() => ({ min: [], max: [] }));
  
          data.forEach(entry => {
            const month = new Date(entry.date).getMonth(); // 0-11
            const index = months.indexOf(month + 1);
            if (index !== -1) {
              const minTemp = parseInt(entry.minTemperature.replace('℃', ''));
              const maxTemp = parseInt(entry.maxTemperature.replace('℃', ''));
              tempByMonth[index].min.push(minTemp);
              tempByMonth[index].max.push(maxTemp);
            }
          });
  
          const categories = months.map(m => `${m}月`);
          const minTemps = tempByMonth.map(m => (m.min.length ? Math.min(...m.min) : null));
          const maxTemps = tempByMonth.map(m => (m.max.length ? Math.max(...m.max) : null));
  
          return { categories, minTemps, maxTemps };
        }
  
        return { categories: [], minTemps: [], maxTemps: [] };
      };
  
      // 处理天气数据，限制前30
      const processWeatherData = (data) => {
        const weatherCount = {};
  
        data.forEach(entry => {
          const weather = entry.weather;
          if (weatherCount[weather]) {
            weatherCount[weather]++;
          } else {
            weatherCount[weather] = 1;
          }
        });
  
        // 转换为数组并排序，取前30
        const sortedWeather = Object.entries(weatherCount)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 30);
  
        const weatherTypes = sortedWeather.map(item => item[0]);
        const counts = sortedWeather.map(item => item[1]);
  
        return { weatherTypes, counts };
      };
  
      // 处理风向与风力数据，生成热力图所需数据，限制前20
      const processWindHeatmapData = (data) => {
        const windHeatmapMatrix = {};
  
        data.forEach(entry => {
          const wind = entry.wind;
          // 简单分割，可能需要根据实际风向/风力格式进行更灵活处理
          const windParts = wind.split('~');
          const directions = windParts
            .filter(part => part.includes('风') && !/\d/.test(part))
            .map(part => part.trim());
          const strengths = windParts
            .filter(part => !part.includes('风') && /\d/.test(part))
            .map(part => part.trim());
  
          directions.forEach(direction => {
            strengths.forEach(strength => {
              if (!windHeatmapMatrix[direction]) {
                windHeatmapMatrix[direction] = {};
              }
              windHeatmapMatrix[direction][strength] =
                (windHeatmapMatrix[direction][strength] || 0) + 1;
            });
          });
        });
  
        // 统计每个风向与风力组合的频率
        const directionCounts = {};
        const strengthCounts = {};
  
        Object.keys(windHeatmapMatrix).forEach(direction => {
          Object.keys(windHeatmapMatrix[direction]).forEach(strength => {
            directionCounts[direction] =
              (directionCounts[direction] || 0) + windHeatmapMatrix[direction][strength];
            strengthCounts[strength] =
              (strengthCounts[strength] || 0) + windHeatmapMatrix[direction][strength];
          });
        });
  
        // 获取top 20风向和top 20风力
        const topDirections = Object.entries(directionCounts)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 20)
          .map(item => item[0]);
  
        const topStrengths = Object.entries(strengthCounts)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 20)
          .map(item => item[0]);
  
        // 构建热力图数据，仅包含top 20风向和风力
        const heatmapData = [];
        topDirections.forEach(direction => {
          topStrengths.forEach(strength => {
            const value =
              windHeatmapMatrix[direction] && windHeatmapMatrix[direction][strength]
                ? windHeatmapMatrix[direction][strength]
                : 0;
            heatmapData.push([direction, strength, value]);
          });
        });
  
        console.log('Processed Wind Heatmap Data:', { heatmapData, directions: topDirections, strengths: topStrengths });
  
        return {
          heatmapData,
          directions: topDirections,
          strengths: topStrengths,
        };
      };
  
      // 绘制温度趋势图
      const drawTemperatureChart = ({ categories, minTemps, maxTemps }) => {
        if (!temperatureChart.value) {
          console.error('Temperature chart container is not available.');
          return;
        }
        if (!isEchartsAvailable()) {
          console.error('ECharts is not available.');
          return;
        }
  
        // 初始化或获取现有的 ECharts 实例
        if (!temperatureChartInstance.value) {
          temperatureChartInstance.value = echarts.init(temperatureChart.value);
        }
  
        const option = {
          title: {
            text: `${cityName.value} 温度趋势`,
            left: 'center',
            textStyle: {
              color: '#fff',
              fontSize: 18,
            }
          },
          tooltip: {
            trigger: 'axis',
          },
          legend: {
            data: ['最低温度', '最高温度'],
            top: 30,
            textStyle: {
              color: '#fff'
            }
          },
          grid: {
            left: '10%',
            right: '10%',
            bottom: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: categories,
            axisLabel: {
              color: '#fff',
              fontSize: 12
            },
            axisLine: {
              lineStyle: {
                color: '#fff'
              }
            }
          },
          yAxis: {
            type: 'value',
            name: '温度 (℃)',
            axisLabel: {
              color: '#fff',
              fontSize: 12
            },
            axisLine: {
              lineStyle: {
                color: '#fff'
              }
            },
            splitLine: {
              lineStyle: {
                color: '#444'
              }
            }
          },
          series: [
            {
              name: '最低温度',
              type: 'line',
              data: minTemps,
              smooth: true,
              itemStyle: {
                color: '#00bfff',
              },
              lineStyle: {
                width: 3,
              },
              connectNulls: true, // 连接空数据
            },
            {
              name: '最高温度',
              type: 'line',
              data: maxTemps,
              smooth: true,
              itemStyle: {
                color: '#ff4500',
              },
              lineStyle: {
                width: 3,
              },
              connectNulls: true, // 连接空数据
            },
          ],
          backgroundColor: 'rgba(44, 62, 80, 0.7)',
        };
  
        // 调试日志
        console.log('Temperature chart option.series:', option.series);
  
        try {
          temperatureChartInstance.value.setOption(option, { notMerge: true });
          temperatureChartInstance.value.resize();
        } catch (e) {
          console.error('Error setting Temperature chart option:', e);
        }
      };
  
      // 绘制天气分布图（饼图）
      const drawWeatherChart = ({ weatherTypes, counts }) => {
        if (!weatherChart.value) {
          console.error('Weather chart container is not available.');
          return;
        }
        if (!isEchartsAvailable()) {
          console.error('ECharts is not available.');
          return;
        }
  
        // 初始化或获取现有的 ECharts 实例
        if (!weatherChartInstance.value) {
          weatherChartInstance.value = echarts.init(weatherChart.value);
        }
  
        // 检查 weatherTypes 和 counts 是否有效
        if (!weatherTypes.length || !counts.length || weatherTypes.length !== counts.length) {
          console.error('Invalid weather data:', { weatherTypes, counts });
          return;
        }
  
        const data = weatherTypes.map((type, index) => ({
          name: type,
          value: counts[index],
        }));
  
        const option = {
          title: {
            text: `${cityName.value} 天气分布`,
            left: 'center',
            textStyle: {
              color: '#fff',
              fontSize: 18,
            }
          },
          tooltip: {
            trigger: 'item',
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            textStyle: {
              color: '#fff'
            }
          },
          series: [
            {
              name: '天气类型',
              type: 'pie',
              radius: '50%',
              data,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)',
                },
              },
              label: {
                color: '#fff',
                fontSize: 12,
              },
            },
          ],
          backgroundColor: 'rgba(44, 62, 80, 0.7)',
        };
  
        // 调试日志
        console.log('Weather chart option.series:', option.series);
  
        try {
          weatherChartInstance.value.setOption(option, { notMerge: true });
          weatherChartInstance.value.resize();
        } catch (e) {
          console.error('Error setting Weather chart option:', e);
        }
      };
  
      // 绘制风向与风力热力图
      const drawWindHeatmapChart = ({ heatmapData, directions, strengths }) => {
        if (!windHeatmapChart.value) {
          console.error('Wind Heatmap chart container is not available.');
          return;
        }
        if (!isEchartsAvailable()) {
          console.error('ECharts is not available.');
          return;
        }
  
        // 初始化或获取现有的 ECharts 实例
        if (!windHeatmapChartInstance.value) {
          windHeatmapChartInstance.value = echarts.init(windHeatmapChart.value);
        }
  
        // 检查 heatmapData, directions, strengths 是否有效
        if (!heatmapData.length || !directions.length || !strengths.length) {
          console.error('Invalid wind heatmap data:', { heatmapData, directions, strengths });
          return;
        }
  
        const maxFrequency = Math.max(...heatmapData.map(item => item[2]));
        console.log('Max Frequency for Wind Heatmap:', maxFrequency);
  
        const option = {
          title: {
            text: `${cityName.value} 风向与风力热力图`,
            left: 'center',
            textStyle: {
              color: '#fff',
              fontSize: 18,
            }
          },
          tooltip: {
            position: 'top',
            formatter: function (params) {
              return `风向: ${params.data[0]}<br/>风力: ${params.data[1]}<br/>频率: ${params.data[2]}`;
            }
          },
          grid: {
            height: '70%',
            top: '15%'
          },
          xAxis: {
            type: 'category',
            data: directions,
            splitArea: {
              show: true
            },
            axisLabel: {
              color: '#fff',
              fontSize: 12,
              interval: 0,
              rotate: 30
            },
            axisLine: {
              lineStyle: {
                color: '#fff'
              }
            }
          },
          yAxis: {
            type: 'category',
            data: strengths,
            splitArea: {
              show: true
            },
            axisLabel: {
              color: '#fff',
              fontSize: 12
            },
            axisLine: {
              lineStyle: {
                color: '#fff'
              }
            }
          },
          visualMap: {
            type: 'continuous', // 明确指定类型
            min: 0,
            max: maxFrequency,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '5%',
            textStyle: {
              color: '#fff'
            },
            inRange: {
              color: ['#e0ffff', '#006edd']
            },
            dimension: 2, // 指定 value 的维度
          },
          series: [
            {
              name: '频率',
              type: 'heatmap',
              data: heatmapData,
              label: {
                show: true,
                formatter: '{c}',
                color: '#fff',
                fontSize: 12
              },
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ],
          backgroundColor: 'rgba(44, 62, 80, 0.7)',
        };
  
        // 调试日志
        console.log('Wind Heatmap chart option.series:', option.series);
        console.log('Wind Heatmap chart option.visualMap:', option.visualMap);
  
        try {
          windHeatmapChartInstance.value.setOption(option, { notMerge: true });
          windHeatmapChartInstance.value.resize();
        } catch (e) {
          console.error('Error setting Wind Heatmap chart option:', e);
        }
      };
  
      onMounted(async () => {
        await fetchHistoryData();
  
        // 添加窗口 resize 监听器
        window.addEventListener('resize', () => {
          if (temperatureChartInstance.value) temperatureChartInstance.value.resize();
          if (weatherChartInstance.value) weatherChartInstance.value.resize();
          if (windHeatmapChartInstance.value) windHeatmapChartInstance.value.resize();
        });
      });
  
      watch(
        () => props.url,
        async (newUrl, oldUrl) => {
          console.log(`URL changed from ${oldUrl} to ${newUrl}`);
          // 重新销毁图表实例
          if (temperatureChartInstance.value) {
            echarts.dispose(temperatureChart.value);
            temperatureChartInstance.value = null;
          }
          if (weatherChartInstance.value) {
            echarts.dispose(weatherChart.value);
            weatherChartInstance.value = null;
          }
          if (windHeatmapChartInstance.value) {
            echarts.dispose(windHeatmapChart.value);
            windHeatmapChartInstance.value = null;
          }
          // 重新获取数据
          await fetchHistoryData();
        }
      );
  
      // 监听筛选选项的变化，更新图表
      watch([displayMode, selectedYear, selectedQuarter], async () => {
        await updateCharts();
      });
  
      return {
        cityName,
        temperatureChart,
        weatherChart,
        windHeatmapChart,
        loading,
        error,
        displayMode,
        selectedYear,
        selectedQuarter,
        availableYears,
        availableQuarters,
      };
    },
  };
  </script>
  
  <style scoped>
  .history-detail {
    padding: 20px;
    color: #ecf0f1;
    background-color: #000; /* 深色背景以增强专业感 */
    min-height: 100vh; /* 确保背景覆盖整个页面 */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 30px;
    font-size: 2.5rem;
    color: #ecf0f1;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  }
  
  .filters {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-bottom: 30px;
    background-color: #34495e;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  }
  
  .filter-group {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  label {
    font-size: 1.1rem;
    color: #ecf0f1;
  }
  
  select {
    padding: 8px 16px;
    border-radius: 6px;
    border: none;
    outline: none;
    font-size: 1rem;
    background-color: #ecf0f1;
    color: #2c3e50;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  select:hover {
    background-color: #bdc3c7;
    transform: translateY(-2px);
  }
  
  .loading {
    text-align: center;
    font-size: 1.5rem;
    color: #3498db;
    margin-top: 50px;
  }
  
  .error {
    text-align: center;
    color: #e74c3c;
    font-size: 1.2rem;
    margin-top: 50px;
  }
  
  .chart-container {
    width: 100%;
    max-width: 1200px;
    height: 500px;
    margin: 40px auto;
    background-color: rgba(44, 62, 80, 0.8);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .chart-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
  }
  
  @media (max-width: 768px) {
    .filters {
      flex-direction: column;
      align-items: center;
    }
  
    .chart-container {
      height: 400px;
    }
  }
  </style>
  