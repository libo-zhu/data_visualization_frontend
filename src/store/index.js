import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null, // 当前用户信息
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
  },
  actions: {
    login({ commit }, userData) {
      commit('setUser', userData);
    },
    logout({ commit }) {
      commit('setUser', null);
    },
  },
});
