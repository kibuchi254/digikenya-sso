<template>
  <div v-if="authStore.isAuthenticated">
    <slot />
  </div>
  <div v-else class="text-center py-20">
    <h1 class="text-2xl">Access Denied</h1>
    <router-link to="/login" class="text-indigo-600 underline">Please login first</router-link>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
const authStore = useAuthStore()
</script>