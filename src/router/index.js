import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import WeatherForecast from '../views/WeatherForecast.vue';
import History from '../views/History.vue';
import HistoryDetail from '../views/HistoryDetail.vue';
import LifeIndex from '../views/LifeIndex.vue';
import DisasterWarning from '../views/DisasterWarning.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/weather', component: WeatherForecast },
  { path: '/history', component: History },
  { path: '/history/:url', component: HistoryDetail, props: true }, 
  { path: '/life-index', component: LifeIndex },
  {path: '/disaster-warning', component: DisasterWarning},
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
