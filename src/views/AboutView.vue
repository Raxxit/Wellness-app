<script setup>
import { onMounted } from "vue";
import aboutImage from "@/assets/img/4.jpg";

// --- AOS Imports ---
import AOS from "aos";
import "aos/dist/aos.css";

onMounted(() => {
  AOS.init({
    duration: 1000, // Animation speed
    once: true,     // Animate only once per scroll
  });
});
</script>

<template>
  <div class="about-page">
    <header class="py-5 bg-light border-bottom">
      <div class="container text-center">
        <h1 class="display-4 fw-bold text-primary" data-aos="fade-up" data-aos-delay="100">
          About Us
        </h1>
        <p class="lead text-secondary" data-aos="fade-up" data-aos-delay="200">
          Empowering your journey to a healthier, happier life.
        </p>
      </div>
    </header>

    <section class="py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-12 col-md-6 mb-4 mb-md-0" data-aos="fade-right" data-aos-delay="300">
            <div class="image-wrapper shadow rounded overflow-hidden">
              <img :src="aboutImage" alt="About our mental wellness platform" class="img-fluid" />
            </div>
          </div>

          <div class="col-12 col-md-6" data-aos="fade-left" data-aos-delay="400">
            <p class="text-muted">
              Founded in 2024, WellnessApp was created with a simple belief:
              <strong>Mental well-being should be accessible to everyone.</strong>
            </p>

            <p class="text-muted">
              We focus on nurturing the mind as much as caring for the body. Our
              platform promotes emotional resilience, stress management, and a
              supportive environment where individuals can grow and heal.
            </p>

            <ul class="list-unstyled mt-4">
              <li class="mb-2 d-flex align-items-center">
                <i class="bi bi-check-circle-fill text-primary me-2"></i>
                Qualified Psychological Doctors
              </li>
              <li class="mb-2 d-flex align-items-center">
                <i class="bi bi-check-circle-fill text-primary me-2"></i>
                Mental Health Awareness & Education
              </li>
              <li class="mb-2 d-flex align-items-center">
                <i class="bi bi-check-circle-fill text-primary me-2"></i>
                Supportive Community
              </li>
            </ul>

            <button class="btn btn-primary rounded-pill px-4 mt-3 shadow-sm">
              Learn More About Our Approach
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.image-wrapper img {
  width: 100%;
  height: auto;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-wrapper:hover img {
  transform: scale(1.05);
}
</style>