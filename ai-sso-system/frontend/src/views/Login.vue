<template>
  <div class="flex min-h-screen items-center justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-xl p-8">
      <h2 class="text-3xl font-bold text-center mb-8">Welcome Back</h2>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input v-model="form.username" type="email" required
            class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:border-indigo-500" />
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input v-model="form.password" type="password" required
            class="w-full px-4 py-3 border rounded-lg focus:outline-none focus:border-indigo-500" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full bg-indigo-600 text-white font-bold py-3 rounded-lg hover:bg-indigo-700 transition">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <div class="mt-6 text-center">
        <router-link to="/register" class="text-indigo-600 hover:underline">Create an account</router-link>
      </div>
      <div class="mt-4 text-center">
        <a href="/auth/oauth/google" class="inline-block bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700">
          Sign in with Google
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const form = ref({ username: '', password: '' })
const loading = ref(false)
const router = useRouter()
const authStore = useAuthStore()

const login = async () => {
  loading.value = true
  try {
    const data = new URLSearchParams()
    data.append('username', form.value.username)
    data.append('password', form.value.password)

    await authStore.login(data)
    router.push('/dashboard')
  } catch (err) {
    alert('Login failed: ' + (err.response?.data?.detail || err.message))
  } finally {
    loading.value = false
  }
}
</script>