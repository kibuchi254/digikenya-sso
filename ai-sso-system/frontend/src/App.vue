<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar v-if="$route.path !== '/login' && $route.path !== '/register'" />
    <router-view class="container mx-auto px-4 py-8" />
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>