<script setup>

import { onMounted } from 'vue';
import { WOW } from 'wowjs';


import aboutImage from '@/assets/img/1.jpg';

onMounted(() => {
    new WOW().init();
})


</script>

<template>
    <div class="about-page">

        <header class="py-5 bg-light border-bottom">
            <div class="container text-center">
                <h1 class="display-4 fw-bold text-primary wow fadeInUp" data-wow-delay="0.1s">About Us</h1>
                <p class="lead text-secondary wow fadeInUp" data-wow-delay="0.2s">
                    Empowering your journey to a healthier, happier life.
                </p>
            </div>
        </header>

        <section class="py-5">
            <div class="container">
                <div class="row align-items-center">

                    <div class="col-12 col-md-6 mb-4 mb-md-0 wow fadeInLeft" data-wow-delay="0.3s">
                        <div class="image-wrapper shadow rounded overflow-hidden">
                            <img :src="aboutImage" alt="About our gym" class="img-fluid">
                        </div>
                    </div>

                    <div class="col-12 col-md-6 wow fadeInRight" data-wow-delay="0.4s">
                        <h2 class="fw-bold mb-3">Our Mission</h2>
                        <p class="text-muted">
                            Founded in 2024, WellnessApp was created with a simple belief:
                            <strong>Fitness should be accessible to everyone.</strong>
                        </p>
                        <p class="text-muted">
                            We don't just focus on lifting weights; we focus on lifting spirits.
                            Our community is built on support, expert knowledge, and the drive to see you succeed.
                        </p>

                        <ul class="list-unstyled mt-4">
                            <li class="mb-2 d-flex align-items-center">
                                <i class="fa fa-check-circle text-primary me-2"></i>
                                Expert Personal Trainers
                            </li>
                            <li class="mb-2 d-flex align-items-center">
                                <i class="fa fa-check-circle text-primary me-2"></i>
                                Custom Nutrition Plans
                            </li>
                            <li class="mb-2 d-flex align-items-center">
                                <i class="fa fa-check-circle text-primary me-2"></i>
                                Supportive Community
                            </li>
                        </ul>

                        <button class="btn btn-primary rounded-pill px-4 mt-3 shadow-sm">
                            Meet Our Team
                        </button>
                    </div>

                </div>
            </div>
        </section>

    </div>
</template>

<style scoped>
/* Custom tweaks specific to this page only */

.image-wrapper img {
    width: 100%;
    height: auto;
    object-fit: cover;
    /* Ensures image doesn't stretch weirdly */
    transition: transform 0.3s ease;
}

/* Hover Effect: Zoom image slightly */
.image-wrapper:hover img {
    transform: scale(1.05);
}
</style>