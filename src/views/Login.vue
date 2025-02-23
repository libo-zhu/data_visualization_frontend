<template>
  <div class="auth-container">
    <div class="auth-box">
      <button class="close-btn" @click="closePage">&times;</button> <!-- 关闭按钮 -->
      <h2 class="auth-title">登录</h2>
      <form @submit.prevent="handleLogin">
        <input v-model="username" type="text" placeholder="用户名" class="input" />
        <input v-model="password" type="password" placeholder="密码" class="input" />
        <button type="submit" class="btn">登录</button>
      </form>
      <div class="register-link">
        <span>没有账号？</span>
        <router-link to="/register">注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Login',
  setup() {
    const username = ref('');
    const password = ref('');
    const router = useRouter();

    const handleLogin = async () => {
      try {
        const response = await axios.post('http://localhost:8080/api/auth/login', {
          username: username.value,
          password: password.value,
        });
        localStorage.setItem('token', response.data.token); // 假设返回token
        router.push('/');
        alert("登录成功!");
      } catch (error) {
        alert('登录失败，用户名或密码错误');
      }
    };

    const closePage = () => {
      router.push('/');
    };

    return {
      username,
      password,
      handleLogin,
      closePage,
    };
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  /* background-color: #2c3e50; */
  height: 100vh;
}

.auth-box {
  position: relative; /* 相对定位以便关闭按钮 */
  background-color: #34495e;
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #fff;
  cursor: pointer;
}

.close-btn:hover {
  color: #e74c3c;
}

.auth-title {
  font-size: 2rem;
  color: #fff;
  margin-bottom: 20px;
}

.input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #ecf0f1;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1rem;
  cursor: pointer;
}

.btn:hover {
  background-color: #2980b9;
}

.register-link {
  text-align: center;
  margin-top: 10px;
}

.register-link a {
  color: #ecf0f1;
}
</style>
