<script setup>
import { onMounted } from "vue";
import WOW from "wowjs";
</script>

<template>
  <div class="error-page">
    <!-- Header -->
    <header class="page-header">
      <div class="container text-center">
        <h1 class="error-code wow zoomIn">400</h1>
        <p class="error-title wow fadeInUp" data-wow-delay="0.2s">
          Bad Request
        </p>
      </div>
    </header>

    <!-- Content -->
    <section class="py-5">
      <div class="container text-center">
        <div class="card error-card wow fadeInUp" data-wow-delay="0.4s">
          <h2 class="mb-3">Something went wrong</h2>
          <p class="text-muted mb-4">
            The request could not be processed. Please check your input and try
            again.
          </p>

          <router-link to="/" class="btn btn-primary mt-3">
            Go Back
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Page background */
.error-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #eef4ff, #ffffff);
  display: flex;
  flex-direction: column;
}

/* Header */
.page-header {
  padding: 4rem 0;
  background: white;
  border-bottom: 1px solid #e5e5e5;
}

/* Animated number */
.error-code {
  font-size: 5rem;
  font-weight: 800;
  color: #0d6efd;
  animation: float 3s ease-in-out infinite;
}

.error-title {
  font-size: 1.2rem;
  color: #6c757d;
}

/* Card */
.error-card {
  border: none;
  border-radius: 14px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(13, 110, 253, 0.08);
  animation: slideUp 0.8s ease forwards;
}

/* Button animation */
.animated-btn {
  border-radius: 50px;
  padding: 0.75rem 2rem;
  transition: all 0.3s ease;
}

.animated-btn:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 10px 25px rgba(13, 110, 253, 0.35);
}

/* Keyframes */
@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
