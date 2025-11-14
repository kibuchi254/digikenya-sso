import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      const res = await api.post('/auth/login', credentials, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      this.accessToken = res.data.access_token
      this.refreshToken = res.data.refresh_token
      localStorage.setItem('access_token', this.accessToken)
      localStorage.setItem('refresh_token', this.refreshToken)
      await this.fetchUser()
      return res
    },

    async register(userData) {
      return await api.post('/users/', userData)
    },

    async fetchUser() {
      const res = await api.get('/users/me')
      this.user = res.data
    },

    async refreshAccessToken() {
      const res = await api.post('/auth/refresh', { refresh_token: this.refreshToken })
      this.accessToken = res.data.access_token
      localStorage.setItem('access_token', this.accessToken)
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.clear()
    }
  }
})