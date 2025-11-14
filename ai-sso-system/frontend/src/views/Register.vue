<template>
  <div class="flex min-h-screen items-center justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-xl p-8">
      <h2 class="text-3xl font-bold text-center mb-8">Create Account</h2>
      <form @submit.prevent="register">
        <input v-model="form.email" type="email" placeholder="Email" required class="w-full mb-4 px-4 py-3 border rounded-lg" />
        <input v-model="form.first_name" type="text" placeholder="First Name" class="w-full mb-4 px-4 py-3 border rounded-lg" />
        <input v-model="form.last_name" type="text" placeholder="Last Name" class="w-full mb-4 px-4 py-3 border rounded-lg" />
        <input v-model="form.password" type="password" placeholder="Password" required class="w-full mb-6 px-4 py-3 border rounded-lg" />
        <button type="submit" :disabled="loading"
          class="w-full bg-green-600 text-white font-bold py-3 rounded-lg hover:bg-green-700">
          {{ loading ? 'Creating...' : 'Register' }}
        </button>
      </form>
      <p class="mt-4 text-center text-sm text-gray-600">
        Already have an account? <router-link to="/login" class="text-indigo-600 font-bold">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const form = ref({
  email: '', password: '', first_name: '', last_name: ''
})
const loading = ref(false)
const router = useRouter()

const register = async () => {
  loading.value = true
  try {
    await api.post('/users/', form.value)
    alert('Registration successful! Please check your email to activate.')
    router.push('/login')
  } catch (err) {
    alert('Error: ' + (err.response?.data?.detail || 'Registration failed'))
  } finally {
    loading.value = false
  }
}
</script>