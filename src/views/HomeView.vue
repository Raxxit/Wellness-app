<script setup>
import { onMounted } from "vue";
import { Swiper, SwiperSlide } from "swiper/vue";
import { Navigation, Pagination, Autoplay } from "swiper/modules";

import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

import slide1 from "@/assets/img/1.jpg";
import slide2 from "@/assets/img/3.webp";

import { WOW } from "wowjs";

const modules = [Navigation, Pagination, Autoplay];

const services = [
  {
    title: "Stress Management",
    desc: "Learn effective techniques to manage stress and maintain emotional balance.",
  },
  {
    title: "Mindfulness & Self-Care",
    desc: "Practice mindfulness and self-care strategies to improve mental clarity and calm.",
  },
  {
    title: "Emotional Support",
    desc: "Access guidance and resources to support your emotional well-being.",
  },
];

onMounted(() => {
  new WOW().init();
});
</script>

<template>
  <div class="home">
    <div class="slider-container mb-5">
      <swiper
        :modules="modules"
        :slides-per-view="1"
        navigation
        :pagination="{ clickable: true }"
        :autoplay="{ delay: 5000 }"
        class="my-swiper"
      >
        <swiper-slide>
          <div
            class="slide-content"
            :style="{ backgroundImage: `url(${slide1})` }"
          >
            <div class="overlay wow fadeInDown" data-wow-delay="0.2s">
              <h2>
                Mental health is not a destination, but a process of growth and
                self-care.
              </h2>
            </div>
          </div>
        </swiper-slide>
        <swiper-slide>
          <div
            class="slide-content"
            :style="{ backgroundImage: `url(${slide2})` }"
          >
            <div class="overlay wow fadeInDown" data-wow-delay="0.2s">
              <h2>
                Taking care of your mind is just as important as taking care of
                your body.
              </h2>
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>

    <section class="hero-banner bg-primary text-white text-center py-5 mb-5">
      <div class="container wow fadeInUp" data-wow-delay="0.3s">
        <h1 class="display-4 font-weight-bold">Welcome to Mental Wellness</h1>
        <p class="lead">
          Your journey to emotional balance, clarity, and peace begins here.
        </p>
        <button class="btn btn-light btn-lg mt-3">Join Now</button>
      </div>
    </section>

    <section class="services-section py-5">
      <div class="container">
        <div class="row">
          <div
            class="col-md-4 text-center mb-4 wow fadeInLeft"
            data-wow-delay="0.4s"
            v-for="service in services"
            :key="service.title"
          >
            <div class="p-4 border rounded shadow-sm h-100 bg-white">
              <h3>{{ service.title }}</h3>
              <p>{{ service.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.my-swiper {
  width: 100%;
  /* Default for Mobile */
  height: 50vh;
  min-height: 400px;
}

/* For Desktop */
@media (min-width: 768px) {
  .my-swiper {
    height: 70vh;
    /* Taller on desktop */
  }
}

/* Make text readable */
.overlay {
  background: rgba(0, 0, 0, 0.5);
  /* Slightly darker for better contrast */
  padding: 2rem;
  color: white;
  border-radius: 10px;
  backdrop-filter: blur(5px);
  /* Adds a modern "frosted glass" effect */
}

.slide-content {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
</style>
