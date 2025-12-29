<script setup>
import AppNavbar from './components/AppNavbar.vue';
import AppFooter from './components/AppFooter.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="app-container pt-5">
    <AppNavbar />
    <RouterView />
    <AppFooter />
  </div>
</template>
