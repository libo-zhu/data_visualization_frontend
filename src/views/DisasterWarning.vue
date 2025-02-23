<template> 
  <div class="disaster-warning">
    <h1>气象灾害预警</h1>
    <div class="search-box">
      <input
        v-model="province"
        type="text"
        placeholder="输入你要查询的省份"
        @keyup.enter="fetchDisasterWarning"
        class="search-input"
      />
      <button @click="fetchDisasterWarning" class="search-button">查询</button>
    </div>

    <!-- 省份快捷按钮 -->
    <div class="province-buttons-container">
      <button 
        v-for="province in defaultProvinces" 
        :key="province" 
        @click="handleProvinceClick(province)"
        class="province-button"
      >
        {{ province }}
      </button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="warnings.length > 0" class="warning-list">
      <div v-for="warning in warnings" :key="warning.cityid" class="warning-item">
        <h2>{{ warning.alarm_title }}</h2>
        <p><strong>地区:</strong> {{ warning.area }}, {{ warning.city }}, {{ warning.province }}</p>
        <p><strong>预警类型:</strong> {{ warning.alarm_type }}</p>
        <div class="warning-level">
          <strong>预警等级:</strong>
          <div class="gauge-container" :ref="`gauge-${warning.cityid}`"></div>
          <span class="level-text">{{ warning.alarm_level }}</span>
        </div>
        <p><strong>预警内容:</strong> {{ warning.alarm_content }}</p>
      </div>
    </div>

    <div v-else-if="!loading && !error" class="no-warnings">
      当前没有气象灾害预警信息。
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'DisasterWarning',
  data() {
    return {
      province: '',
      warnings: [],
      loading: false,
      error: '',
      defaultProvinces: ['北京', '上海', '广东', '浙江', '江苏', '四川', '湖北', '陕西', '重庆', '山东'],
      charts: []
    };
  },
  methods: {
    handleProvinceClick(province) {
      this.province = province;
      this.fetchDisasterWarning();
    },
    async fetchDisasterWarning() {
      if (!this.province) {
        this.error = '请输入省份名称';
        return;
      }

      this.loading = true;
      this.error = '';
      this.charts.forEach(chart => chart.dispose());
      this.charts = [];

      try {
        const response = await fetch(
          `http://gfeljm.tianqiapi.com/api?version=v71&appid=74973365&appsecret=xI3DmtIf&province=${this.province}`
        );
        const data = await response.json();

        if (data.errcode === 0) {
          this.warnings = data.list;
          this.$nextTick(() => {
            this.initGauges();
          });
        } else {
          this.error = data.errmsg || '获取数据失败';
        }
      } catch (err) {
        this.error = '网络错误，请稍后重试';
      } finally {
        this.loading = false;
      }
    },
    initGauges() {
      this.warnings.forEach(warning => {
        const container = this.$refs[`gauge-${warning.cityid}`];
        if (container) {
          const chart = echarts.init(container[0]);
          this.charts.push(chart);
          const option = this.getGaugeOption(warning.alarm_level);
          chart.setOption(option);
        }
      });
    },
    getGaugeOption(level) {
      const valueMap = { 
        '蓝色': 22.5,   // 对应0-45度的中间值
        '黄色': 67.5,   // 对应45-90度的中间值
        '橙色': 157.5,  // 对应135-180度的中间值
        '红色': 202.5   // 对应180-225度的中间值
      };
      
      return {
        animationDuration: 2000,
        animationEasing: 'cubicOut',
        series: [{
          type: 'gauge',
          startAngle: 220,
          endAngle: -40,
          min: 0,
          max: 270,
          radius: '100%',
          pointer: {
            show: true,
            length: '75%',
            width: 8,
            itemStyle: {
              color: '#fff',
              shadowBlur: 10,
              shadowColor: 'rgba(255,255,255,0.3)'
            }
          },
          progress: {
            show: false
          },
          axisLine: {
            lineStyle: {
              width: 20,
              color: [
                [0.166, '#3498db'],
                [0.333, '#f1c40f'],
                [0.666, '#e67e22'],
                [1, '#e74c3c']
              ]
            }
          },
          axisTick: {
            show: false
          },
          splitLine: {
            distance: -20,
            length: 14,
            lineStyle: {
              width: 2,
              color: '#fff'
            }
          },
          axisLabel: {
            distance: 10,
            color: '#fff',
            fontSize: 14,
            formatter: (value) => {
              if (value === 0) return '蓝';
              if (value === 90) return '黄';
              if (value === 180) return '橙';
              if (value === 270) return '红';
              return '';
            }
          },
          detail: {
            show: false
          },
          data: [{
            value: valueMap[level] || 0,
            name: level
          }]
        }]
      };
    },
    getLevelColor(level) {
      const colorMap = {
        '蓝色': '#3498db',
        '黄色': '#f1c40f',
        '橙色': '#e67e22',
        '红色': '#e74c3c',
      };
      return colorMap[level] || '#3498db';
    }
  },
  beforeDestroy() {
    this.charts.forEach(chart => chart.dispose());
  }
};
</script>
  
  <style scoped>
  /* 新增省份按钮样式 */
  .province-buttons-container {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 1rem 0;
    max-width: 800px;
  }

  .province-button {
    padding: 8px 16px;
    background-color: #34495e;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.3s;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }

  .province-button:hover {
    background-color: #2980b9;
    transform: translateY(-1px);
  }

  .province-button:active {
    transform: translateY(0);
  }
  .disaster-warning {
    padding: 20px;
    color: #ecf0f1;
    max-width: 800px;
    margin: 0 auto;
  }
  
  h1 {
    font-size: 2rem;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .search-box {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    justify-content: center;
  }
  
  .search-input {
    padding: 10px;
    border: 1px solid #3498db;
    border-radius: 6px;
    background-color: #34495e;
    color: #ecf0f1;
    width: 300px;
  }
  
  .search-button {
    padding: 10px 20px;
    background-color: #3498db;
    border: none;
    border-radius: 6px;
    color: #ecf0f1;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .search-button:hover {
    background-color: #2980b9;
  }
  
  .loading,
  .error,
  .no-warnings {
    text-align: center;
    margin-top: 20px;
    font-size: 1.2rem;
  }
  
  .error {
    color: #e74c3c;
  }
  
  .warning-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .gauge-container {
  width: 180px;
  height: 140px;
  margin: 10px 0;
}

.warning-level {
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 15px 0;
  min-height: 140px; /* 保证统一高度 */
}

  .level-text {
    font-size: 18px;
    font-weight: bold;
    min-width: 40px;
  }

  .warning-item {
    background-color: #34495e;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  }

  .warning-item h2 {
    color: #3498db;
    margin-bottom: 15px;
  }
  
  .warning-item p {
    margin: 5px 0;
  }
  
  .warning-level {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .level-axis {
    position: relative;
    width: 100px;
    height: 10px;
    background-color: #2c3e50;
    border-radius: 5px;
  }
  
  .level-marker {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transform: translateX(-50%);
  }
  
  .level-text {
    font-weight: bold;
  }
  </style>