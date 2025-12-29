<script setup>
import AppNavbar from './components/AppNavbar.vue';
import AppFooter from './components/AppFooter.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="app-container" style="padding-top: 75px;">
    <AppNavbar />
    <RouterView />
    <AppFooter />
  </div>
</template>
