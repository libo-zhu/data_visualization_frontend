<template>
  <div class="weather-page">
    <h1>天气预报查询</h1>
    <div class="input-container">
      <input
        v-model="inputCity"
        @keyup.enter="handleSearch"
        type="text"
        placeholder="请输入城市名称"
        class="city-input"
      />
      <button @click="handleSearch" class="search-button">查询</button>
    </div>

    <!-- 新增城市快捷按钮 -->
    <div class="city-buttons-container">
      <button 
        v-for="city in defaultCities" 
        :key="city" 
        @click="handleCityClick(city)"
        class="city-button"
      >
        {{ city }}
      </button>
    </div>

    <div class="map-container">
      <img :src="mapUrl" 
          alt="城市地图" 
          class="city-map"
          @load="handleMapLoad"
          @error="handleMapError">
    </div>

    <div v-if="weatherData" class="weather-info">
      <h2>{{ weatherData.city }} 当前天气</h2>
      <div v-if="isLiveData" class="current-weather">
        <div class="charts">
          <div ref="temperatureChart" class="chart"></div>
          <div ref="humidityChart" class="chart" v-if="weatherData.humidity !== undefined"></div>
          <div ref="windChart" class="chart"></div>
        </div>
      </div>
      <div v-else class="forecast-weather">
        <h2>天气预报（未来{{ weatherData.forecasts.length }}天）</h2>
        <div class="charts">
          <div ref="temperatureForecastChart" class="chart"></div>
          <div ref="weatherConditionChart" class="chart"></div>
          <div ref="windForecastChart" class="chart"></div>
        </div>
      </div>
    </div>
    <div v-if="error" class="error-message">{{ error }}</div>


  </div>
</template>

<script>
import axios from 'axios';
import * as XLSX from 'xlsx';
import * as echarts from 'echarts';

export default {
  name: 'WeatherPage',
  data() {
    return {
      inputCity: '',
      adcodeMap: {}, // 城市名称到 adcode 的映射
      weatherData: null, // 天气数据
      error: '', // 错误信息
      isLiveData: true, // 是否为实时数据
      temperatureForecastChartInstance: null,
      weatherConditionChartInstance: null,
      windForecastChartInstance: null,
      defaultCities: ['北京', '上海', '广州', '深圳', '杭州', '成都', '南京', '武汉', '西安', '重庆'],
      mapLocation: '116.397428,39.90923', // 默认北京坐标
      mapZoom: 2, // 默认缩放级别
      mapLng: 116.397428,
      mapLat: 39.90923,
    };
  },
  computed: {
  mapUrl() {
    const markers = `mid,,A:${this.mapLocation}`;
    return `https://restapi.amap.com/v3/staticmap?key=e2fecd966bfc670623846d9722065fb6&location=${this.mapLocation}&zoom=${this.mapZoom}&size=700*350&scale=1&markers=${markers}`;
  }
  },
  mounted() {
    this.loadAdcodeMapping();
  },
  methods: {
    handleCityClick(city) {
      this.inputCity = city;
      this.handleSearch();
    },
    async handleSearch() {
      this.error = '';
      this.weatherData = null;
      const city = this.inputCity.trim();

      if (!city) {
        this.error = '请输入城市名称。';
        return;
      }

      try {
        // 获取城市坐标
        const geoResponse = await axios.get(
          `https://restapi.amap.com/v3/geocode/geo?address=${encodeURIComponent(city)}&key=e2fecd966bfc670623846d9722065fb6`
        );

        if (geoResponse.data.status === '1' && geoResponse.data.geocodes.length > 0) {
          const geocode = geoResponse.data.geocodes[0];
          [this.mapLng, this.mapLat] = geocode.location.split(',').map(Number);
          this.mapLocation = `${this.mapLng},${this.mapLat}`;
          this.mapZoom = geocode.level === '省' ? 8 : 12; // 根据行政级别动态缩放
          
          // 获取天气数据
          this.fetchWeatherData(geocode.adcode);
        } else {
          this.error = '未找到该城市的位置信息。';
        }
      } catch (error) {
        console.error('获取地理信息失败:', error);
        this.error = '获取城市信息失败，请稍后重试。';
      }
    },
    // 加载 Excel 文件并解析 adcode 映射
    handleCityClick(city) {
      this.inputCity = city;
      this.handleSearch();
    },
    async loadAdcodeMapping() {
      try {
        const filePath = '/adcode.xlsx'; // Excel 文件路径
        const response = await axios.get(filePath, { responseType: 'arraybuffer' });
        const data = new Uint8Array(response.data);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        // 假设第一行为标题
        const headers = jsonData[0];
        const nameIndex = headers.indexOf('中文名');
        const adcodeIndex = headers.indexOf('adcode');

        if (nameIndex === -1 || adcodeIndex === -1) {
          throw new Error('Excel 文件缺少 "中文名" 或 "adcode" 列');
        }

        jsonData.slice(1).forEach((row) => {
          const cityName = row[nameIndex] ? row[nameIndex].trim() : '';
          const adcode = row[adcodeIndex] ? row[adcodeIndex].toString().trim() : '';
          if (cityName && adcode) {
            this.adcodeMap[cityName] = adcode;
          }
        });

        console.log('adcodeMap:', this.adcodeMap); // 调试信息
      } catch (error) {
        console.error('加载 adcode 映射失败:', error);
        this.error = '加载城市映射数据失败，请稍后重试。';
      }
    },
    handleMapLoad() {
    console.log('地图加载成功');
    this.$nextTick(() => {
      // 触发图表重绘适配地图布局
      [this.temperatureChart, this.humidityChart, this.windChart].forEach(chart => {
        chart?.resize();
      });
    });
  },
  handleMapError() {
    this.error = '地图加载失败，请检查网络连接';
  },
    // // 处理搜索事件
    // handleSearch() {
    //   this.error = '';
    //   this.weatherData = null;
    //   this.isLiveData = true;
    //   const city = this.inputCity.trim();

    //   if (!city) {
    //     this.error = '请输入城市名称。';
    //     return;
    //   }

    //   // 尝试直接匹配
    //   let adcode = this.adcodeMap[city];

    //   // 如果直接匹配失败，尝试添加或移除“市”字后再次匹配
    //   if (!adcode) {
    //     if (city.endsWith('市')) {
    //       adcode = this.adcodeMap[city.slice(0, -1)];
    //     } else {
    //       adcode = this.adcodeMap[`${city}市`];
    //     }
    //   }

    //   if (!adcode) {
    //     this.error = '未找到该城市的编码，请检查输入是否正确。';
    //     return;
    //   }

    //   this.fetchWeatherData(adcode);
    // },
    // 获取天气数据
    async fetchWeatherData(adcode) {
      const apiKey = 'e2fecd966bfc670623846d9722065fb6'; // 替换为您的 API Key
      const apiUrl = `https://restapi.amap.com/v3/weather/weatherInfo?city=${adcode}&key=${apiKey}&extensions=all&output=json`;

      try {
        const response = await axios.get(apiUrl);
        if (response.data.status === '1') {
          if (response.data.lives && response.data.lives.length > 0) {
            // 处理 lives 数据（区级编码）
            const live = response.data.lives[0];
            this.weatherData = {
              province: live.province,
              city: live.city,
              adcode: live.adcode,
              weather: live.weather,
              temperature: parseInt(live.temperature),
              winddirection: live.winddirection,
              windpower: parseInt(live.windpower),
              humidity: parseFloat(live.humidity),
              reporttime: live.reporttime,
            };
            this.isLiveData = true;
            this.renderCurrentWeatherCharts();
          } else if (response.data.forecasts && response.data.forecasts.length > 0) {
            // 处理 forecasts 数据（市级编码）
            const forecast = response.data.forecasts[0];
            const casts = forecast.casts;
            this.weatherData = {
              province: forecast.province,
              city: forecast.city,
              adcode: forecast.adcode,
              reporttime: forecast.reporttime,
              forecasts: casts.map(cast => ({
                date: cast.date,
                week: cast.week,
                dayweather: cast.dayweather,
                nightweather: cast.nightweather,
                daytemp: parseInt(cast.daytemp),
                nighttemp: parseInt(cast.nighttemp),
                daywind: cast.daywind,
                nightwind: cast.nightwind,
                daypower: parseInt(cast.daypower.split('-')[0]), // 取风力等级的起始值
                nightpower: parseInt(cast.nightpower.split('-')[0]),
                daytemp_float: parseFloat(cast.daytemp_float),
                nighttemp_float: parseFloat(cast.nighttemp_float),
              })),
            };
            this.isLiveData = false;
            this.renderForecastWeatherCharts();
          } else {
            this.error = '未获取到天气数据，请稍后重试。';
            this.weatherData = null;
            return;
          }
        } else {
          this.error = `API 错误信息：${response.data.info}`;
          this.weatherData = null;
        }
      } catch (error) {
        console.error('获取天气数据失败:', error);
        this.error = '获取天气数据失败，请检查网络或稍后重试。';
        this.weatherData = null;
      }
    },
    // 渲染当前天气图表
    renderCurrentWeatherCharts() {
      this.$nextTick(() => {
        // 温度图表
        const tempChart = echarts.init(this.$refs.temperatureChart);
        const tempOption = {
          title: {
            text: '温度',
            left: 'center',
            textStyle: { color: '#333' },
          },
          tooltip: {
            formatter: '{a} <br/>{b} : {c}°C',
          },
          series: [
            {
              name: '温度',
              type: 'gauge',
              detail: { formatter: '{value}°C', fontSize: 16 },
              data: [{ value: this.weatherData.temperature, name: '温度' }],
              axisLine: {
                lineStyle: {
                  width: 10,
                  color: [
                    [0.3, '#67e0e3'],
                    [0.7, '#37a2da'],
                    [1, '#fd666d'],
                  ],
                },
              },
              title: {
                fontSize: 14,
              },
            },
          ],
        };
        tempChart.setOption(tempOption);

        // 湿度图表
        if (this.weatherData.humidity !== undefined) {
          const humidityChart = echarts.init(this.$refs.humidityChart);
          const humidityOption = {
            title: {
              text: '湿度',
              left: 'center',
              textStyle: { color: '#333' },
            },
            tooltip: {
              formatter: '{a} <br/>{b} : {c}%',
            },
            series: [
              {
                name: '湿度',
                type: 'gauge',
                detail: { formatter: '{value}%', fontSize: 16 },
                data: [{ value: this.weatherData.humidity, name: '湿度' }],
                axisLine: {
                  lineStyle: {
                    width: 10,
                    color: [
                      [0.3, '#a1c4fd'],
                      [0.7, '#c2e9fb'],
                      [1, '#ff9a9e'],
                    ],
                  },
                },
                title: {
                  fontSize: 14,
                },
              },
            ],
          };
          humidityChart.setOption(humidityOption);
        }

        // 风速图表
        const windChart = echarts.init(this.$refs.windChart);
        const windOption = {
          title: {
            text: '风速',
            left: 'center',
            textStyle: { color: '#333' },
          },
          tooltip: {
            formatter: '{a} <br/>{b} : {c} km/h',
          },
          series: [
            {
              name: '风速',
              type: 'gauge',
              detail: { formatter: '{value} km/h', fontSize: 16 },
              data: [{ value: this.weatherData.windpower, name: '风速' }],
              axisLine: {
                lineStyle: {
                  width: 10,
                  color: [
                    [0.3, '#cfd9df'],
                    [0.7, '#e2ebf0'],
                    [1, '#f1f2f6'],
                  ],
                },
              },
              title: {
                fontSize: 14,
              },
            },
          ],
        };
        windChart.setOption(windOption);
      });
    },
    // 渲染天气预报图表
    renderForecastWeatherCharts() {
      this.$nextTick(() => {
        const forecasts = this.weatherData.forecasts;

        // 准备数据
        const dates = forecasts.map(f => f.date);
        const dayTemps = forecasts.map(f => f.daytemp);
        const nightTemps = forecasts.map(f => f.nighttemp);
        const weatherConditions = forecasts.map(f => f.dayweather);
        const windPowers = forecasts.map(f => f.daypower);

        // 温度折线图
        const tempForecastChart = echarts.init(this.$refs.temperatureForecastChart);
        this.temperatureForecastChartInstance = tempForecastChart;
        const tempForecastOption = {
          title: {
            text: '未来温度变化',
            left: 'center',
            textStyle: { color: '#333' },
          },
          tooltip: {
            trigger: 'axis',
          },
          legend: {
            data: ['白天温度', '夜晚温度'],
            top: '10%',
            textStyle: { color: '#333' },
          },
          xAxis: {
            type: 'category',
            data: dates,
            boundaryGap: false,
          },
          yAxis: {
            type: 'value',
            name: '温度 (°C)',
          },
          series: [
            {
              name: '白天温度',
              type: 'line',
              data: dayTemps,
              smooth: true,
              lineStyle: { color: '#ff7f50' },
              areaStyle: { opacity: 0.1 },
            },
            {
              name: '夜晚温度',
              type: 'line',
              data: nightTemps,
              smooth: true,
              lineStyle: { color: '#87cefa' },
              areaStyle: { opacity: 0.1 },
            },
          ],
        };
        tempForecastChart.setOption(tempForecastOption);

        // 天气状况柱状图
        const weatherConditionChart = echarts.init(this.$refs.weatherConditionChart);
        this.weatherConditionChartInstance = weatherConditionChart;
        const weatherConditionOption = {
          title: {
            text: '未来天气状况',
            left: 'center',
            textStyle: { color: '#333' },
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
          },
          xAxis: {
            type: 'category',
            data: dates,
          },
          yAxis: {
            type: 'value',
            name: '次数',
            minInterval: 1,
          },
          series: [
            {
              name: '天气次数',
              type: 'bar',
              data: weatherConditions.map(condition => {
                // 统计不同天气状况的次数
                return 1; // 每天一个天气状况
              }),
              itemStyle: {
                color: '#ffa07a',
              },
              label: {
                show: true,
                position: 'top',
                formatter: params => weatherConditions[params.dataIndex],
              },
            },
          ],
        };
        weatherConditionChart.setOption(weatherConditionOption);

        // 风速折线图
        const windForecastChart = echarts.init(this.$refs.windForecastChart);
        this.windForecastChartInstance = windForecastChart;
        const windForecastOption = {
          title: {
            text: '未来风速变化',
            left: 'center',
            textStyle: { color: '#333' },
          },
          tooltip: {
            trigger: 'axis',
          },
          xAxis: {
            type: 'category',
            data: dates,
            boundaryGap: false,
          },
          yAxis: {
            type: 'value',
            name: '风力等级',
            min: 0,
            max: 12,
          },
          series: [
            {
              name: '白天风力',
              type: 'line',
              data: windPowers,
              smooth: true,
              lineStyle: { color: '#32cd32' },
              areaStyle: { opacity: 0.1 },
            },
          ],
        };
        windForecastChart.setOption(windForecastOption);
      });
    },
  },
};
</script>

<style scoped>
/* 新增城市按钮样式 */
.city-buttons-container {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 30px;
  max-width: 800px;
  animation: fadeIn 1s ease-in-out;
}

.city-button {
  padding: 8px 16px;
  background-color: #666;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.city-button:hover {
  background-color: #555;
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0,0,0,0.2);
}

.city-button:active {
  transform: translateY(0);
}

.weather-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #ece9e6, #ffffff);
  min-height: 100vh;
  animation: fadeIn 1s ease-in-out;
}

h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 30px;
  animation: slideDown 1s ease-out;
}

.input-container {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  animation: fadeIn 1s ease-in-out;
}

.city-input {
  padding: 10px 20px;
  font-size: 1rem;
  border: 2px solid #4c90f2;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s;
  width: 200px;
}

.city-input:focus {
  border-color: #3878d4;
}

.search-button {
  padding: 10px 20px;
  background-color: #4c90f2;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.3s;
}

.search-button:hover {
  background-color: #3878d4;
  transform: translateY(-2px);
}

.weather-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1000px;
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 1s ease-out;
}

.weather-info h2 {
  font-size: 2rem;
  color: #4c90f2;
  margin-bottom: 20px;
}

.charts {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.chart {
  width: 300px;
  height: 300px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.error-message {
  margin-top: 20px;
  color: #ff4d4f;
  font-weight: bold;
  animation: shake 0.5s;
}

/* 新增地图样式 */
.map-container {
  margin: 20px 0;
  width: 100%;
  max-width: 800px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 1s ease-out;
}

.city-map {
  width: 100%;
  height: 300px;
  object-fit: cover;
}


/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideDown {
  from {
    transform: translateY(-20px);
  }
  to {
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shake {
  0% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  50% {
    transform: translateX(5px);
  }
  75% {
    transform: translateX(-5px);
  }
  100% {
    transform: translateX(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .charts {
    flex-direction: column;
    align-items: center;
  }

  .chart {
    width: 90%;
    height: 250px;
  }
}
</style>