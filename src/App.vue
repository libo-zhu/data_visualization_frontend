<template>
  <div id="app">

        <!-- 动态背景容器 -->
    <div class="global-background">
      <canvas class="particles-canvas"></canvas>
      <div class="gradient-overlay"></div>
    </div>
    <!-- 顶部标题栏 -->
    <header class="header">
      <div class="header-left">
        <button @click="toggleSidebar" class="toggle-btn">
          <i :class="isSidebarCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
        </button>
        <div class="logo">
          <i class="fas fa-cloud-sun-rain"></i> 气象数据分析平台
        </div>
      </div>
      <div class="auth-buttons">
        <template v-if="!isLoggedIn">
          <router-link to="/login" class="auth-btn"><i class="fas fa-sign-in-alt"></i> 登录</router-link>
          <router-link to="/register" class="auth-btn"><i class="fas fa-user-plus"></i> 注册</router-link>
        </template>
        <template v-else>
          <button @click="handleLogout" class="auth-btn"><i class="fas fa-sign-out-alt"></i> 退出</button>
        </template>
      </div>
    </header>

    <!-- 退出成功消息 -->
    <transition name="fade">
      <div v-if="logoutMessage" class="logout-message">
        已成功退出
      </div>
    </transition>

    <div class="main-content">
      <!-- 左侧导航栏 -->
      <aside :class="['sidebar', { collapsed: isSidebarCollapsed }]">
        <ul>
          <li>
            <router-link to="/">
              <i class="fas fa-home"></i>
              <span v-if="!isSidebarCollapsed">首页</span>
            </router-link>
          </li>
          <li>
            <router-link to="/weather">
              <i class="fas fa-sun"></i>
              <span v-if="!isSidebarCollapsed">天气预报</span>
            </router-link>
          </li>
          <li>
            <router-link to="/history">
              <i class="fas fa-history"></i>
              <span v-if="!isSidebarCollapsed">历史天气数据</span>
            </router-link>
          </li>
          <li>
            <router-link to="/life-index">
              <i class="fas fa-bed"></i>
              <span v-if="!isSidebarCollapsed">生活指数</span>
            </router-link>
          </li>
          <li>
            <router-link to="/disaster-warning">
              <i class="fas fa-exclamation-triangle"></i>
              <span v-if="!isSidebarCollapsed">气象灾害预警</span>
            </router-link>
          </li>
        </ul>
      </aside>

      <!-- 主体内容 -->
      <main class="content">
        <router-view></router-view> <!-- 路由视图, 动态加载不同页面 -->
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      isSidebarCollapsed: false, // 控制侧边栏折叠状态
      logoutMessage: false, // 控制退出消息显示
    };
  },
  created() {
    this.isLoggedIn = !!localStorage.getItem('token'); // 假设登录后存储token
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.logoutMessage = true; // 显示退出消息
      this.$router.push('/'); // 返回首页

      // 3秒后隐藏退出消息
      setTimeout(() => {
        this.logoutMessage = false;
      }, 3000);
    },
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
  },
};
</script>

<style scoped>

.global-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  overflow: hidden;
}

.particles-canvas {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #000;
}

.gradient-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    45deg,
    rgba(76, 144, 242, 0.1) 0%,
    transparent 60%
  );
}
/* 基础布局 */
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #000; /* 全局背景设为黑色 */

}

/* 顶部标题栏 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50;
  color: white;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  margin-right: 15px;
  transition: transform 0.3s ease;
}

.toggle-btn:hover {
  color: #3498db;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.logo i {
  margin-right: 10px;
  color: #3498db;
}

.auth-buttons {
  display: flex;
  gap: 15px;
}

.auth-btn {
  color: #fff;
  text-decoration: none;
  padding: 8px 16px;
  background-color: #3498db;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.auth-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

/* 退出成功消息 */
.logout-message {
  position: fixed;
  top: 70px;
  right: 20px;
  background-color: #2ecc71;
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

/* 主内容布局 */
.main-content {
  display: flex;
  flex: 1;
  background-color: #000; /* 全局背景黑色 */
  
}

/* 侧边栏 */
.sidebar {
  width: 220px;
  background-color: #34495e;
  padding-top: 20px;
  transition: width 0.3s ease, border-radius 0.3s ease;
  overflow: hidden;
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar ul li {
  margin: 20px 0;
}

.sidebar ul li a {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 1rem;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s ease, padding-left 0.3s ease, border-radius 0.3s ease;
  border-radius: 6px;
}

.sidebar.collapsed ul li a {
  justify-content: center;
  padding: 10px 0;
}

.sidebar ul li a i {
  margin-right: 15px;
  min-width: 20px;
  text-align: center;
}

.sidebar ul li a:hover {
  background-color: #2980b9;
  border-radius: 6px;
}

.sidebar.collapsed ul li a span {
  display: none;
}

/* 主体内容 */
.content {
  flex: 1;
  background-color: #000; /* 主体内容背景黑色 */
  color: #ecf0f1;
  padding: 20px;
  overflow-y: auto;
  transition: padding 0.3s ease, background-color 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    z-index: 1000;
    height: 100%;
    left: -220px;
    border-radius: 0;
  }

  .sidebar.collapsed {
    left: 0;
    width: 220px;
  }

  .main-content {
    flex-direction: column;
  }

  .content {
    padding: 15px;
  }
}
</style>