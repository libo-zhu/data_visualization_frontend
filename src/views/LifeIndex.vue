<template>
  <div class="life-index">
    <h2 class="title">🌤️ 城市生活指数查询</h2>

    <div class="form">
      <input 
        v-model="city" 
        class="city-input"
        type="text" 
        placeholder="输入城市名称..."
        @keyup.enter="fetchLifeIndex"
      >
      <button @click="fetchLifeIndex" class="search-btn">
        <span class="icon">🔍</span> 立即查询
      </button>
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

    <transition name="fade">
      <div v-if="lifeIndexData" class="index-grid">
        <div 
          v-for="(item, index) in filteredIndexData" 
          :key="index" 
          class="index-card"
          :style="{borderColor: getLevelColor(item.level)}"
        >
          <div class="card-header">
            <h3 class="index-name">{{ item.name }}</h3>
            <div class="level-tag" :style="{backgroundColor: getLevelColor(item.level)}">
              {{ item.level }}
            </div>
          </div>
          <p class="index-desc">{{ item.desc }}</p>
          <div class="status-visual">
            <div 
              class="status-dot"
              :style="{backgroundColor: getLevelColor(item.level)}"
            ></div>
            <div class="status-bar" :style="{width: getLevelWidth(item.level)}"></div>
          </div>
        </div>
      </div>
    </transition>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-if="!lifeIndexData && !loading" class="empty-state">
      <div class="prompt-box">
        <span class="emoji">🤔</span>
        <p>请输入城市名称，点击查询！</p>
      </div>
    </div>
  </div>
</template>

<script>
const LEVEL_CONFIG = {
  '极不易发': { level: 1, color: '#27ae60' },
  '较少开启': { level: 1, color: '#27ae60' },
  '无需戴口罩': { level: 1, color: '#27ae60' },
  '较冷': { level: 2, color: '#f1c40f' },
  '较适宜': { level: 2, color: '#f1c40f' },
  '较弱': { level: 2, color: '#f1c40f' },
  '适宜': { level: 3, color: '#e67e22' },
  '必要': { level: 3, color: '#e67e22' },
  '很不舒适': { level: 4, color: '#e74c3c' },
  '凉': { level: 4, color: '#e74c3c' },
};

export default {
  data() {
    return {
      city: '',
      lifeIndexData: null,
      loading: false,
      importantIndexes: [
        'chuanyi', 'shushidu', 'ziwaixian', 'ganmao', 
        'kongtiao', 'yusan', 'jiaotong', 'lvyou'
      ],
       // 新增默认城市列表
       defaultCities: ['北京', '上海', '广州', '深圳', '杭州', '成都', '南京', '武汉', '西安', '重庆']
    };
  },
  computed: {
    filteredIndexData() {
      if (!this.lifeIndexData) return [];
      return this.lifeIndexData.filter(item => 
        this.importantIndexes.includes(item.key)
      );
    }
  },
  methods: {
    handleCityClick(city) {
      this.city = city;
      this.fetchLifeIndex();
    },

    getLevelColor(level) {
      return LEVEL_CONFIG[level]?.color || '#95a5a6';
    },

    getLevelWidth(level) {
      const baseWidth = LEVEL_CONFIG[level]?.level || 1;
      return `${baseWidth * 25}%`;
    },

    fetchLifeIndex() {
      if (!this.city) return;

      this.loading = true;
      this.lifeIndexData = null;

      const apiUrl = `http://v1.yiketianqi.com/life/lifepro?appid=74973365&appsecret=xI3DmtIf&city=${this.city}`;

      fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
          this.loading = false;
          if (data.data) {
            // 添加原始key用于过滤
            this.lifeIndexData = Object.entries(data.data).map(([key, value]) => ({
              ...value,
              key
            }));
          }
        })
        .catch(() => {
          this.loading = false;
          this.lifeIndexData = null;
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
  margin: 1rem 0;
  max-width: 800px;
}

.city-button {
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

.city-button:hover {
  background-color: #2980b9;
  transform: translateY(-1px);
}

.city-button:active {
  transform: translateY(0);
}

.life-index {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
  background: #2c3e50; /* 深色背景 */
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
}

.title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  text-align: center;
}

.form {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.city-input {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 2px solid #7f8c8d;
  background: #34495e;
  color: white;
  width: 250px;
}

.search-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
}

.search-btn:hover {
  background: #2980b9;
}

.index-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  width: 100%;
}

.index-card {
  background: #34495e;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.index-name {
  font-size: 1.2rem;
  font-weight: bold;
}

.level-tag {
  color: white;
  background-color: #e74c3c;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
}

.index-desc {
  font-size: 1rem;
  margin-top: 1rem;
  color: #bdc3c7;
}

.status-visual {
  margin-top: 1rem;
  height: 6px;
  background: #95a5a6;
  border-radius: 3px;
  position: relative;
}

.status-bar {
  height: 100%;
  border-radius: 3px;
  background-color: #3498db;
  transition: width 0.5s ease;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #3498db;
  position: absolute;
  right: -6px;
  top: -4px;
}

.loading {
  text-align: center;
  margin-top: 2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 4rem;
}

.prompt-box {
  background: #34495e;
  padding: 2rem;
  border-radius: 15px;
}

.emoji {
  font-size: 3rem;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
