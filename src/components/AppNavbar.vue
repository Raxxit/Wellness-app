<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterLink, useRoute } from 'vue-router';

const route = useRoute();
const isScrolled = ref(false);
const isNavOpen = ref(false);

const handleScroll = () => {
  if (window.scrollY > 50) {
    isScrolled.value = true;
  } else {
    isScrolled.value = false;
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <nav class="navbar navbar-expand-lg fixed-top transition-all" :class="{
    'navbar-scrolled': isScrolled,
    'navbar-transparent': !isScrolled && !isNavOpen,
    'bg-white shadow-sm': isScrolled || isNavOpen
  }">
    <div class="container">

      <RouterLink class="navbar-brand fw-bold" to="/">
        Wellness<span class="text-primary">App</span>
      </RouterLink>

      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav"
        aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation" @click="isNavOpen = !isNavOpen">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="mainNav">
        <ul class="navbar-nav ms-auto align-items-center">

          <li class="nav-item" v-for="item in ['Home', 'Community', 'About', 'Questionnaire']" :key="item">
            <RouterLink class="nav-link custom-link" :to="item === 'Home' ? '/' : `/${item.toLowerCase()}`">
              {{ item }}
            </RouterLink>
          </li>

          <li class="nav-item dropdown ms-lg-3">
            <a class="btn nav-link custom-link" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Account
            </a>
            <ul class="dropdown-menu dropdown-menu-end shadow border-0 mt-2">
              <li>
                <RouterLink class="dropdown-item" to="/login">Login</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/register">Register</RouterLink>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/profile">Profile</RouterLink>
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/report">Report</RouterLink>
              </li>
            </ul>
          </li>

          <li class="nav-item ms-lg-3 mt-3 mt-lg-0">
            <RouterLink to="/register" class="btn btn-primary px-4 rounded-pill shadow-sm">
              Get Started
            </RouterLink>
          </li>

        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* --- 1. NAVBAR TRANSITIONS --- */
.navbar {
  padding-top: 25px;
  padding-bottom: 25px;
  transition: all 0.4s ease-in-out;
}

.navbar-scrolled {
  padding-top: 10px;
  padding-bottom: 10px;
  background-color: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
}

/* --- 2. LINK ANIMATIONS --- */
.custom-link {
  font-weight: 500;
  color: #636262;
  margin: 0 10px;
  position: relative;
  transition: color 0.3s ease;
}

.custom-link::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 50%;
  background-color: #0d6efd;
  transition: all 0.3s ease-in-out;
  transform: translateX(-50%);
}

.custom-link:hover {
  color: #0d6efd;
}

.custom-link:hover::after {
  width: 100%;
}

.router-link-active:not(.btn) {
  color: #0d6efd;
  font-weight: 600;
}

.router-link-active:not(.btn)::after {
  width: 100%;
}

/* --- 3. DROPDOWN ANIMATION (DESKTOP ONLY) --- */
/* We wrap this in a Media Query so it DOES NOT affect mobile */
@media (min-width: 992px) {
  .dropdown-menu {
    display: block;
    /* Only force block on desktop for animation */
    opacity: 0;
    visibility: hidden;
    transform: translateY(10px);
    transition: all 0.3s ease;
  }

  /* Show on Hover (Desktop) */
  .nav-item.dropdown:hover .dropdown-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
}

/* --- 4. MOBILE ADJUSTMENTS --- */
@media (max-width: 991px) {
  .navbar-collapse {
    background: white;
    padding: 20px;
    margin-top: 15px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }

  .navbar {
    background-color: white !important;
    padding: 15px 0;
  }

  /* On mobile, we fix the dropdown spacing */
  .dropdown-menu {
    border: none;
    box-shadow: none;
    padding-left: 20px;
    /* Indent sub-items */
    margin-top: 0;
  }
}
</style>