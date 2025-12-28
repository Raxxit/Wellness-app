<script setup>
import { onMounted } from 'vue';
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation, Pagination, Autoplay } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import slide1 from '@/assets/img/1.jpg';
import slide2 from '@/assets/img/3.jpg';

import { WOW } from 'wowjs';

const modules = [Navigation, Pagination, Autoplay];

const services = [
    { title: 'Personal Training', desc: 'Get trained by expert coaches dedicated to your success.' },
    { title: 'Nutrition Plans', desc: 'Healthy eating made simple with custom diet programs.' },
    { title: 'Workout Programs', desc: 'Follow structured workout routines for every level.' }
];

onMounted(() => {
    new WOW().init();
});
</script>

<template>
    <div class="home">

        <div class="slider-container mb-5">
            <swiper :modules="modules" :slides-per-view="1" navigation :pagination="{ clickable: true }"
                :autoplay="{ delay: 5000 }" class="my-swiper">
                <swiper-slide>
                    <div class="slide-content" :style="{ backgroundImage: `url(${slide1})` }">
                        <div class="overlay wow fadeInDown" data-wow-delay="0.2s">
                            <h2>It is health that is real wealth and not pieces of gold and silver</h2>
                        </div>
                    </div>
                </swiper-slide>
                <swiper-slide>
                    <div class="slide-content" :style="{ backgroundImage: `url(${slide2})` }">
                        <div class="overlay wow fadeInDown" data-wow-delay="0.2s">
                            <h2>Happiness is nothing more than good health and a bad memory</h2>
                        </div>
                    </div>
                </swiper-slide>
            </swiper>
        </div>

        <section class="hero-banner bg-primary text-white text-center py-5 mb-5">
            <div class="container wow fadeInUp" data-wow-delay="0.3s">
                <h1 class="display-4 font-weight-bold">Welcome to Fitness</h1>
                <p class="lead">Your journey to a healthier life begins here.</p>
                <button class="btn btn-light btn-lg mt-3">Join Now</button>
            </div>
        </section>

        <section class="services-section py-5">
            <div class="container">
                <div class="row">
                    <div class="col-md-4 text-center mb-4 wow fadeInLeft" data-wow-delay="0.4s"
                        v-for="service in services" :key="service.title">
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