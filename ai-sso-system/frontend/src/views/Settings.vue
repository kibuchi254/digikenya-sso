<template>
  <ProtectedPage>
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">Settings</h1>
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-2xl font-bold mb-6">Profile Information</h2>
        <div class="space-y-4">
          <div><strong>Email:</strong> {{ authStore.currentUser?.email }}</div>
          <div><strong>Name:</strong> {{ authStore.currentUser?.first_name }} {{ authStore.currentUser?.last_name }}</div>
          <div><strong>Status:</strong> <span class="text-green-600 font-bold">Active</span></div>
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