<template>
  <div id="app" class="app-container">
    <aside class="sidebar">
      <h2>艾兹海默症数据可视化</h2>
      <nav>
        <ul>
          <li @click="selectChart('brainAnalysis')">脑部分析</li>
          <li @click="selectChart('risk')">风险概率分布</li>
          <li @click="selectChart('symptoms')">症状数据统计</li>
          <li @click="selectChart('treatment')">治疗方式与分布</li>
        </ul>
      </nav>
    </aside>
    <main class="main-content">
      <component :is="currentComponent" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import BrainAnalysis from './components/BrainAnalysis.vue';
import RiskDistribution from './components/RiskDistribution.vue';
import SymptomsChart from './components/SymptomsChart.vue';
import TreatmentChart from './components/TreatmentChart.vue';

const components = {
  brainAnalysis: BrainAnalysis,
  risk: RiskDistribution,
  symptoms: SymptomsChart,
  treatment: TreatmentChart,
};

const currentComponent = ref(components.brainAnalysis);

const selectChart = (chartKey) => {
  currentComponent.value = components[chartKey];
};
</script>

<style>
.app-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 220px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
}

.sidebar h2 {
  font-size: 18px;
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
