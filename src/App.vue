<template>
  <div id="app" class="app-container">
    <aside class="sidebar">
      <h2>医学数据可视化</h2>
      <nav>
        <ul>
          <li @click="selectChart('chart1')">血压变化</li>
          <li @click="selectChart('chart2')">心率分布</li>
          <li @click="selectChart('chart3')">年龄统计</li>
        </ul>
      </nav>
    </aside>
    <main class="main-content">
      <DataChart :chart-type="selectedChart" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DataChart from './components/DataChart.vue';

const selectedChart = ref('chart1');

const selectChart = (chart) => {
  selectedChart.value = chart;
};
</script>

<style>
.app-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
}

.sidebar h2 {
  font-size: 20px;
  margin-bottom: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin: 10px 0;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.sidebar li:hover {
  background-color: #34495e;
}

.main-content {
  flex: 1;
  padding: 20px;
  background-color: #f4f6f9;
}
</style>
