# 🌦️ 气象数据可视化分析平台 - 前端

[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![ECharts](https://img.shields.io/badge/ECharts-AA344D?logo=apache-echarts&logoColor=white)](https://echarts.apache.org/)
[![高德地图API](https://img.shields.io/badge/高德地图-0089D6?logo=amap&logoColor=white)](https://lbs.amap.com/)

> 基于Vue.js的气象数据可视化平台，集成多维度天气数据分析与预警功能

## 📌 功能亮点
1. **实时天气预报**  
   - 地图可视化（高德地图API）展示全国地图
   - 折线图/柱状图（ECharts）呈现温度、湿度趋势
2. **历史天气分析**  
   - 热力图展示风力风向关系
   - 饼图分析天气类型分布（晴/雨/雪等）
3. **生活指数可视化**  
   - 动态数轴展示紫外线、穿衣、运动等指数等级
4. **灾害预警系统**  
   - 仪表盘实时显示台风/暴雨预警等级
5. **用户认证**  
   - 登录/注册功能（JWT鉴权）
   - 防CSRF/XSS攻击机制

## 🛠️ 技术栈
- **框架**: Vue 3 + Vue Router + Pinia
- **可视化**: ECharts 5 + 高德地图JavaScript API v2.0
- **爬虫工具**: Requests + BeautifulSoup4 + Selenium（历史数据采集）
- **安全防护**: Axios拦截器 + 请求频率限制
- **构建工具**: Vite 4 + TypeScript

## 🚀 快速启动
```bash
# 安装依赖
npm install

# 配置环境变量（创建.env文件）
VITE_AMAP_KEY=your_amap_api_key
VITE_API_BASE_URL=http://your-backend-domain.com

# 启动开发服务器
npm run dev
```

## 🔧 配置说明

1. **高德地图API**
   在`.env`文件中配置`VITE_AMAP_KEY`（申请地址)
2. **后端接口**
   修改`VITE_API_BASE_URL`指向您的SpringBoot服务地址

## 📸 界面预览

|    实时天气地图     |     历史数据热力图      |
| :-----------------: | :---------------------: |
| screenshots/map.png | screenshots/heatmap.png |

## 📚 相关文档

- ECharts配置指南
- 高德地图API文档
