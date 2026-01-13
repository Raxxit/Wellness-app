<script setup>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { authState } from '/src/authStore'; // Ensure this path matches your file location

const router = useRouter();
const isNavOpen = ref(false);

// Logout function using the shared state
const handleLogout = () => {
  authState.logout();
  router.push('/'); // Redirect to home without a full page refresh
};
</script>

<template>
  <nav class="navbar navbar-expand-lg fixed-top bg-white shadow-sm">
    <div class="container">
      <RouterLink class="navbar-brand fw-bold" to="/">
        Wellness<span class="text-primary">App</span>
      </RouterLink>

      <button 
        class="navbar-toggler border-0" 
        type="button" 
        @click="isNavOpen = !isNavOpen"
        data-bs-toggle="collapse" 
        data-bs-target="#mainNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" :class="{ 'show': isNavOpen }" id="mainNav">
        <ul class="navbar-nav ms-auto align-items-center">
          
          <li class="nav-item" v-for="item in ['Home', 'Community', 'About', 'Questionnaire']" :key="item">
            <RouterLink class="nav-link custom-link" :to="item === 'Home' ? '/' : `/${item.toLowerCase()}`">
              {{ item }}
            </RouterLink>
          </li>

          <template v-if="!authState.user">
            <li class="nav-item dropdown ms-lg-3">
              <a class="btn nav-link custom-link" href="#" role="button" data-bs-toggle="dropdown">
                Account
              </a>
              <ul class="dropdown-menu dropdown-menu-end shadow border-0 mt-2">
                <li><RouterLink class="dropdown-item" to="/login">Login</RouterLink></li>
                <li><RouterLink class="dropdown-item" to="/register">Register</RouterLink></li>
                <li><hr class="dropdown-divider"></li>
                <li><RouterLink class="dropdown-item" to="/profile">Profile</RouterLink></li>
                                <li><RouterLink class="dropdown-item" to="/report">Report</RouterLink></li>
              </ul>
            </li>

            <li class="nav-item ms-lg-3 mt-3 mt-lg-0">
              <RouterLink to="/register" class="btn btn-primary px-4 rounded-pill shadow-sm">
                Get Started
              </RouterLink>
            </li>
          </template>

          <template v-else>
            <li class="nav-item ms-lg-3">
<div class="user-name">
  Welcome, {{ authState.user.name || authState.user.email?.split('@')[0] || 'User' }}
</div> 
            </li>
            
            <li class="nav-item ms-lg-3 mt-3 mt-lg-0">
              <button @click="handleLogout" class="btn btn-outline-primary px-4 rounded-pill">
                Logout
              </button>
            </li>
          </template>

        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  padding-top: 15px;
  padding-bottom: 15px;
}

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

@media (min-width: 992px) {
  .dropdown-menu {
    display: block;
    opacity: 0;
    visibility: hidden;
    transform: translateY(10px);
    transition: all 0.3s ease;
  }

  .nav-item.dropdown:hover .dropdown-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
}

.user-name {
  font-weight: 600;
  color: #0d6efd;
  padding: 8px 16px;
  border-radius: 20px;
  background-color: #f8f9fa;
}

@media (max-width: 991px) {
  .navbar-collapse {
    background: white;
    padding: 20px;
    margin-top: 15px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }

  .user-name {
    margin-top: 10px;
    text-align: center;
  }
}
</style>