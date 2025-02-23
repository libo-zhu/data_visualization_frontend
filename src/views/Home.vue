<template>
  <div class="home" @mousemove="handleMouseMove">
    <!-- 动态粒子背景 -->
    <canvas ref="canvas" class="particles"></canvas>
    
    <!-- 视差效果图层 -->
    <div 
      v-for="(layer, index) in parallaxLayers" 
      :key="index"
      class="parallax-layer"
      :style="{
        transform: `translate(${layer.x}px, ${layer.y}px)`,
        opacity: layer.opacity
      }"
    ></div>

    <!-- 主内容区 -->
    <div class="content">
      <h1 class="title">气象数据分析平台</h1>
      <p class="description">
        本平台提供全面的气象数据分析，包括实时天气信息与历史天气数据，帮助您更好地了解气候变化趋势。
      </p>
    </div>
    
    <div class="weather-icons">
    <font-awesome-icon :icon="['fas', 'sun']" />
    <font-awesome-icon :icon="['fas', 'cloud']" />
    <font-awesome-icon :icon="['fas', 'cloud-rain']" />
  </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

export default {
  
  name: 'Home',
  data() {
    return {
      mouseX: 0,
      mouseY: 0,
      parallaxLayers: [
        { sensitivity: 0.03, opacity: 0.2 },
        { sensitivity: 0.05, opacity: 0.4 },
        { sensitivity: 0.08, opacity: 0.3 }
      ]
    }
  },
  mounted() {
    this.initParticles();
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleMouseMove(e) {
      this.mouseX = (e.clientX - window.innerWidth/2) * 0.5;
      this.mouseY = (e.clientY - window.innerHeight/2) * 0.5;
      
      this.parallaxLayers = this.parallaxLayers.map(layer => ({
        ...layer,
        x: this.mouseX * layer.sensitivity,
        y: this.mouseY * layer.sensitivity
      }));
    },
    initParticles() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');
      let particles = [];

      // 粒子系统初始化（
      class Particle {
        constructor() {
          this.x = Math.random() * canvas.width;
          this.y = Math.random() * canvas.height;
          this.size = Math.random() * 2 + 1;
          this.speedX = Math.random() * 3 - 1.5;
          this.speedY = Math.random() * 3 - 1.5;
        }
        update() {
          this.x += this.speedX;
          this.y += this.speedY;
          if(this.x > canvas.width) this.x = 0;
          if(this.x < 0) this.x = canvas.width;
          if(this.y > canvas.height) this.y = 0;
          if(this.y < 0) this.y = canvas.height;
        }
        draw() {
          ctx.fillStyle = 'rgba(255,255,255,0.8)';
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
          ctx.fill();
        }
      }

      // 粒子动画循环
      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(particle => {
          particle.update();
          particle.draw();
        });
        requestAnimationFrame(animate);
      }

      // 初始化粒子数组
      for(let i=0; i<50; i++) {
        particles.push(new Particle());
      }
      animate();
    },
    handleResize() {
      const canvas = this.$refs.canvas;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
  }
}
</script>

<style scoped>
.home {
  position: relative;
  height: 100vh;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d4059 100%);
  overflow: hidden;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.parallax-layer {
  position: absolute;
  width: 150%;
  height: 150%;
  background: 
    radial-gradient(circle at 50% 50%, 
      rgba(76, 144, 242, 0.1) 0%, 
      transparent 60%),
    repeating-linear-gradient(
      45deg,
      rgba(255,255,255,0.05) 0px,
      rgba(255,255,255,0.05) 2px,
      transparent 2px,
      transparent 8px
    );
  transition: transform 0.3s ease-out;
  pointer-events: none;
}

.content {
  position: relative;
  text-align: center;
  color: #fff;
  z-index: 2;
  padding: 20px;
  animation: contentEntrance 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.title {
  font-size: 3.5rem;
  font-weight: 800;
  text-shadow: 0 4px 15px rgba(0,0,0,0.3);
  margin-top: 130px;
  margin-bottom: 25px;
  background: linear-gradient(45deg, #fff 30%, #4c90f2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.description {
  font-size: 1.3rem;
  max-width: 700px;
  margin: 0 auto 50px;
  line-height: 1.6;
  opacity: 0.9;
}

.weather-icons {
  position: absolute;
  bottom: 10%;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 40px;
  z-index: 1;
}

.weather-icons i {
  font-size: 2.5rem;
  opacity: 0.6;
  animation: float 3s ease-in-out infinite;
}

@keyframes contentEntrance {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* 响应式优化 */
@media (max-width: 768px) {
  .title {
    font-size: 2.5rem;
  }
  .description {
    font-size: 1.1rem;
    padding: 0 15px;
  }
  .weather-icons {
    gap: 20px;
    bottom: 5%;
  }
}
</style>