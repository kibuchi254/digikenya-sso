<template>
  <ProtectedPage>
    <div class="bg-white rounded-lg shadow p-8">
      <h1 class="text-4xl font-bold mb-6">Welcome, {{ authStore.currentUser?.first_name || 'User' }}!</h1>
      <p class="text-gray-600 text-lg">You are successfully logged into the AI SSO System.</p>
      <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-blue-100 p-6 rounded-lg">
          <h3 class="font-bold text-xl">Tenant</h3>
          <p>Default Organization</p>
        </div>
        <div class="bg-green-100 p-6 rounded-lg">
          <h3 class="font-bold text-xl">Status</h3>
          <p class="text-green-700 font-bold">Active</p>
        </div>
        <div class="bg-purple-100 p-6 rounded-lg">
          <h3 class="font-bold text-xl">Role</h3>
          <p>Admin (coming soon)</p>
        </div>
      </div>
    </div>
  </ProtectedPage>
</template>

<script setup>
import ProtectedPage from '@/components/ProtectedPage.vue'
import { useAuthStore } from '@/store/auth'
const authStore = useAuthStore()
</script>