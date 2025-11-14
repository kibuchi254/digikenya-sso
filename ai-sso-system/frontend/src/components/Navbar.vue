<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <h1 class="text-2xl font-bold text-indigo-600">AI SSO</h1>
        </div>
        <div class="flex items-center space-x-4">
          <router-link to="/dashboard" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md">Dashboard</router-link>
          <router-link to="/settings" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md">Settings</router-link>
          <button @click="logout" class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700">
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>