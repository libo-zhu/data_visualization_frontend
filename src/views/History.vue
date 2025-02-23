<template>
    <div class="history-page">
      <h1>历史天气数据</h1>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else>
        <div v-if="error" class="error">{{ error }}</div>
        <div v-else>
          <div v-for="(cities, letter) in groupedCities" :key="letter" class="letter-group">
            <h2>{{ letter.toUpperCase() }}</h2>
            <ul>
              <li v-for="city in citiesToShow(letter)" :key="city.url">
                <router-link :to="`/history/${city.url}`">{{ city.cityName }}</router-link>
              </li>
            </ul>
            <button v-if="cities.length > getDisplayLimit(letter)" @click="showMore(letter)">
              展开更多
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref } from 'vue';
  
  export default {
    name: 'History',
    setup() {
      const cities = ref([]);
      const groupedCities = ref({});
      const displayLimits = ref({});
      const loading = ref(true);
      const error = ref(null);
      const INITIAL_DISPLAY_LIMIT = 5;
  
      const fetchCities = async () => {
        try {
          console.log('Fetching cities...');
          const response = await axios.get('http://localhost:8080/api/history_cities');
          console.log('Cities fetched:', response.data);
          cities.value = response.data;
          groupCities();
          initializeDisplayLimits();
        } catch (err) {
          console.error('Error fetching cities:', err);
          error.value = '获取城市数据失败';
        } finally {
          loading.value = false;
        }
      };
  
      const groupCities = () => {
        const groups = {};
        cities.value.forEach(city => {
          const firstLetter = city.url.charAt(0).toLowerCase();
          if (!groups[firstLetter]) {
            groups[firstLetter] = [];
          }
          groups[firstLetter].push(city);
        });
        // Sort the groups by letter
        const sortedGroups = {};
        Object.keys(groups).sort().forEach(letter => {
          sortedGroups[letter] = groups[letter].sort((a, b) => a.cityName.localeCompare(b.cityName));
        });
        groupedCities.value = sortedGroups;
        console.log('Grouped cities:', groupedCities.value);
      };
  
      const initializeDisplayLimits = () => {
        const limits = {};
        Object.keys(groupedCities.value).forEach(letter => {
          limits[letter] = INITIAL_DISPLAY_LIMIT;
        });
        displayLimits.value = limits;
        console.log('Display limits initialized:', displayLimits.value);
      };
  
      const getDisplayLimit = (letter) => {
        return displayLimits.value[letter] || INITIAL_DISPLAY_LIMIT;
      };
  
      const citiesToShow = (letter) => {
        const limit = getDisplayLimit(letter);
        return groupedCities.value[letter].slice(0, limit);
      };
  
      const showMore = (letter) => {
        displayLimits.value[letter] = groupedCities.value[letter].length;
        console.log(`Display limit for ${letter.toUpperCase()} set to ${displayLimits.value[letter]}`);
      };
  
      // Fetch cities on mount
      fetchCities();
  
      return {
        groupedCities,
        showMore,
        citiesToShow,
        loading,
        error,
        getDisplayLimit,
      };
    },
  };
  </script>
  
  <style scoped>
  .history-page {
    padding: 20px;
    color: #fff;
  }
  
  .loading {
    text-align: center;
    font-size: 1.5rem;
    color: #3498db;
  }
  
  .error {
    text-align: center;
    color: #e74c3c;
    font-size: 1.2rem;
  }
  
  .letter-group {
    margin-bottom: 30px;
  }
  
  .letter-group h2 {
    color: #3498db;
    margin-bottom: 10px;
    text-transform: uppercase;
  }
  
  .letter-group ul {
    list-style: none;
    padding: 0;
  }
  
  .letter-group ul li {
    margin-bottom: 5px;
  }
  
  .letter-group ul li a {
    color: #ecf0f1;
    text-decoration: none;
    font-size: 1.1rem;
  }
  
  .letter-group ul li a:hover {
    text-decoration: underline;
  }
  
  button {
    background-color: #2980b9;
    color: #fff;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  button:hover {
    background-color: #1c5980;
  }
  </style>
  