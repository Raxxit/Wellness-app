<script setup>
import { onMounted } from 'vue';
import * as wowModule from "wowjs";

// defineProps is the bridge to your future database. 
// When you fetch data from Flask/Axios, you'll pass it here.
const props = defineProps({
  report: {
    type: Object,
    default: () => ({
      user_name: '',
      generated_at: '',
      score: 0,
      status_label: '', // e.g., "Excellent", "Improving"
      metrics: [],      // array of { name, value, icon, color }
      insights: []      // array of strings
    })
  }
});

onMounted(() => {
  const WOW = wowModule.WOW || wowModule.default.WOW;
  new WOW().init();
});
</script>

<template>
  <div class="report-view py-5">
    <div class="container">
      
      <div class="row mb-5 wow fadeIn">
        <div class="col-md-8">
          <h1 class="display-5 fw-bold text-dark">{{ report.user_name }}'s Wellness Analysis</h1>
          <p class="text-muted">
            <i class="fa fa-clock me-2"></i>Report Generated: {{ report.generated_at }}
          </p>
        </div>
        <div class="col-md-4 text-md-end">
          <button class="btn btn-outline-primary rounded-pill px-4 me-2">
            <i class="fa fa-print"></i>
          </button>
          <button class="btn btn-primary rounded-pill px-4 shadow-sm">
            Refresh Data
          </button>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-lg-4 wow fadeInLeft" data-wow-delay="0.2s">
          <div class="card border-0 shadow-sm rounded-4 h-100 text-center">
            <div class="card-body d-flex flex-column justify-content-center p-5">
              <h5 class="text-secondary fw-bold mb-4">Overall Score</h5>
              <div class="position-relative d-inline-block mx-auto mb-4">
                <svg width="150" height="150" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" fill="none" stroke="#eee" stroke-width="8" />
                  <circle cx="50" cy="50" r="45" fill="none" stroke="var(--bs-primary)" 
                    stroke-width="8" stroke-dasharray="283" 
                    :stroke-dashoffset="283 - (283 * report.score) / 100" 
                    stroke-linecap="round" style="transition: stroke-dashoffset 1s ease-out" />
                </svg>
                <div class="position-absolute top-50 start-50 translate-middle">
                  <span class="h1 fw-bold mb-0">{{ report.score }}</span>
                </div>
              </div>
              <h4 class="text-primary fw-bold">{{ report.status_label }}</h4>
            </div>
          </div>
        </div>

        <div class="col-lg-8 wow fadeInRight" data-wow-delay="0.4s">
          <div class="card border-0 shadow-sm rounded-4 h-100 p-4">
            <h5 class="fw-bold mb-4">Detailed Breakdown</h5>
            <div class="row g-4">
              <div v-for="(metric, index) in report.metrics" :key="index" class="col-md-6">
                <div class="p-3 border rounded-3 bg-light-subtle">
                  <div class="d-flex justify-content-between mb-2">
                    <span class="small fw-bold text-muted text-uppercase">
                      <i :class="['fa me-2', metric.icon]"></i>{{ metric.name }}
                    </span>
                    <span class="small fw-bold">{{ metric.value }}%</span>
                  </div>
                  <div class="progress" style="height: 6px;">
                    <div class="progress-bar rounded-pill" :class="'bg-' + metric.color" 
                         :style="{ width: metric.value + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 wow fadeInUp" data-wow-delay="0.6s">
          <div class="card border-0 shadow-sm rounded-4 bg-dark text-white p-4 p-md-5">
            <div class="d-flex align-items-center mb-4">
              <div class="bg-primary p-3 rounded-circle me-3">
                <i class="fa fa-robot fa-lg"></i>
              </div>
              <h4 class="fw-bold mb-0">Personalized Insights</h4>
            </div>
            <div class="row">
              <div v-for="(insight, idx) in report.insights" :key="idx" class="col-md-4 mb-3">
                <div class="d-flex align-items-start">
                  <i class="fa fa-check text-success me-3 mt-1"></i>
                  <p class="mb-0 opacity-75 small">{{ insight }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.rounded-4 {
  border-radius: 1.5rem !important;
}

.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.bg-light-subtle {
  background-color: #f8f9fa;
}

/* SVG Progress Styling */
circle {
  transition: stroke-dashoffset 1s ease-in-out;
}
</style>