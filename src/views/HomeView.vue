<script setup>
import { onMounted } from "vue";
import { Swiper, SwiperSlide } from "swiper/vue";
import { Navigation, Pagination, Autoplay, EffectFade } from "swiper/modules";

// --- AOS Imports ---
import AOS from "aos";
import "aos/dist/aos.css";

// Import Swiper styles
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/effect-fade";

import slide1 from "@/assets/img/sl1.jpg";
import slide2 from "@/assets/img/sl2.png";

const modules = [Navigation, Pagination, Autoplay, EffectFade];

const services = [
  {
    title: "Stress Management",
    desc: "Learn effective techniques to manage stress and maintain emotional balance in daily life.",
    icon: "bi-lungs-fill",
    color: "text-primary"
  },
  {
    title: "Mindfulness",
    desc: "Practice mindfulness and self-care strategies to improve mental clarity and inner calm.",
    icon: "bi-flower1",
    color: "text-success"
  },
  {
    title: "Emotional Support",
    desc: "Access professional guidance and community resources to support your well-being.",
    icon: "bi-heart-pulse-fill",
    color: "text-danger"
  },
];

onMounted(() => {
  // Initialize AOS
  AOS.init({
    duration: 1000,
    once: true,
  });
});
</script>

<template>
  <div class="home">

    <div class="slider-wrapper">
      <swiper :modules="modules" :slides-per-view="1" :effect="'fade'" :pagination="{ clickable: true }"
        :autoplay="{ delay: 6000, disableOnInteraction: false }" class="hero-swiper">
        <swiper-slide>
          <div class="slide-background" :style="{ backgroundImage: `url(${slide1})` }">
            <div class="overlay-gradient">
              <div
                class="container h-100 d-flex flex-column justify-content-center align-items-center text-center text-white">
                <h1 class="display-3 fw-bold mb-3" data-aos="fade-down">Find Your Inner Peace</h1>
                <p class="lead mb-4" data-aos="fade-up" data-aos-delay="200">
                  Your journey to emotional balance and clarity begins here.
                </p>
                <router-link to="Register" class="btn btn-primary btn-lg rounded-pill px-5 shadow-lg" data-aos="fade-up"
                  data-aos-delay="400">
                  Start Journey
                </router-link>
              </div>
            </div>
          </div>
        </swiper-slide>

        <swiper-slide>
          <div class="slide-background" :style="{ backgroundImage: `url(${slide2})` }">
            <div class="overlay-gradient">
              <div
                class="container h-100 d-flex flex-column justify-content-center align-items-center text-center text-white">
                <h1 class="display-3 fw-bold mb-3">You Are Not Alone</h1>
                <p class="lead mb-4">Join a community dedicated to mental strength and happiness.</p>
                <button class="btn btn-light btn-lg rounded-pill px-5 shadow-lg text-primary fw-bold">Join
                  Community</button>
              </div>
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>

    <section class="services-section py-5 bg-light">
      <div class="container py-4">

        <div class="text-center mb-5" data-aos="fade-up">
          <h2 class="fw-bold display-6 text-dark">Our Approach</h2>
          <div class="divider mx-auto bg-primary"></div>
          <p class="text-muted mt-3 max-w-600 mx-auto">We use evidence-based practices to help you navigate life's
            challenges.</p>
        </div>

        <div class="row g-4">
          <div class="col-md-4" v-for="(service, index) in services" :key="service.title" data-aos="fade-up"
            :data-aos-delay="index * 200">
            <div class="service-card p-4 h-100 bg-white text-center position-relative overflow-hidden">
              <div
                class="icon-wrapper mb-4 mx-auto shadow-sm rounded-circle d-flex align-items-center justify-content-center">
                <i :class="['bi fs-2', service.icon, service.color]"></i>
              </div>
              <h4 class="mb-3 fw-bold text-dark">{{ service.title }}</h4>
              <p class="text-muted mb-4">{{ service.desc }}</p>
              <router-link to="/resources"
                class="stretched-link text-decoration-none fw-bold small text-uppercase letter-spacing-1">
                Learn More <i class="bi bi-arrow-right ms-1"></i>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-5 bg-white text-center border-top">
      <div class="container" data-aos="fade-up">
        <h2 class="fw-bold mb-3">Ready to prioritize your mental health?</h2>
        <p class="text-muted mb-4">Take the first step towards a happier, healthier you today.</p>
        <router-link to="/register" class="btn btn-outline-primary btn-lg rounded-pill px-5">Get Started Free</router-link>
      </div>
    </section>

  </div>
</template>

<style scoped>
/* --- HERO / SLIDER STYLES --- */
.hero-swiper {
  width: 100%;
  height: 85vh;
  min-height: 500px;
}

.slide-background {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
}

.overlay-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.6));
  display: flex;
  align-items: center;
}

/* --- TYPOGRAPHY & UTILS --- */
.divider {
  width: 60px;
  height: 4px;
  border-radius: 2px;
}

.max-w-600 {
  max-width: 600px;
}

.letter-spacing-1 {
  letter-spacing: 1px;
}

/* --- SERVICE CARDS --- */
.service-card {
  border-radius: 15px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  background: #f8f9fa;
  transition: background 0.3s ease;
}

.service-card:hover .icon-wrapper {
  background: #e9ecef;
}

:deep(.swiper-pagination-bullet) {
  background: white;
  opacity: 0.6;
}

:deep(.swiper-pagination-bullet-active) {
  background: white;
  opacity: 1;
  transform: scale(1.2);
}
</style>
