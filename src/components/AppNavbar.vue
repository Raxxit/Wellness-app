<script setup>
import { ref, onMounted, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

const router = useRouter();

const isNavOpen = ref(false);
const isLoggedIn = ref(false);
const userName = ref('');

const checkAuthStatus = () => {
  const token = localStorage.getItem('token');
  const user = localStorage.getItem('user');

  isLoggedIn.value = !!token;

  if (user && isLoggedIn.value) {
    try {
      const parsedUser = JSON.parse(user);
      userName.value = parsedUser.username || 'User';
    } catch (e) {
      userName.value = 'User';
    }
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  isLoggedIn.value = false;
  userName.value = '';
  router.push('/login');
};

onMounted(() => {
  checkAuthStatus();
});

watch(() => route.fullPath, () => {
  checkAuthStatus();
  isNavOpen.value = false; 
});
</script>

<template>
  <nav class="navbar navbar-expand-lg fixed-top bg-white shadow-sm">
    <div class="container">

      <RouterLink class="navbar-brand fw-bold d-flex align-items-center" to="/">
        <span class="brand-icon me-2">🍃</span>
        Wellness<span class="text-primary">App</span>
      </RouterLink>

      <button class="navbar-toggler border-0 p-0" type="button" @click="isNavOpen = !isNavOpen" aria-controls="mainNav"
        :aria-expanded="isNavOpen" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" :class="{ 'show': isNavOpen }" id="mainNav">
        <ul class="navbar-nav ms-auto align-items-center">

          <li class="nav-item" v-for="item in ['Home', 'Community', 'About']" :key="item">
            <RouterLink class="nav-link custom-link" :to="item === 'Home' ? '/' : `/${item.toLowerCase()}`">
              {{ item }}
            </RouterLink>
          </li>

          <li class="nav-item dropdown ms-lg-3">
            <a class="nav-link custom-link dropdown-toggle d-flex align-items-center gap-2" href="#" role="button"
              data-bs-toggle="dropdown" aria-expanded="false">

              <div class="user-avatar-bg">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>

              <span class="fw-medium">{{ isLoggedIn ? userName : 'Account' }}</span>
            </a>

            <ul class="dropdown-menu dropdown-menu-end shadow-lg border-0 mt-3 p-2 rounded-3 animate-slide">

              <template v-if="!isLoggedIn">
                <li>
                  <RouterLink class="dropdown-item rounded-2" to="/login">Login</RouterLink>
                </li>
                <li>
                  <RouterLink class="dropdown-item rounded-2" to="/register">Register</RouterLink>
                </li>
              </template>

              <template v-else>
                <li>
                  <div class="px-3 py-2 text-muted small text-uppercase fw-bold">Menu</div>
                </li>
                <li>
                  <RouterLink class="dropdown-item rounded-2 d-flex align-items-center gap-2" to="/profile">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                    My Profile
                  </RouterLink>
                </li>
                <li>
                  <RouterLink class="dropdown-item rounded-2 d-flex align-items-center gap-2" to="/report">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                      <line x1="16" y1="13" x2="8" y2="13"></line>
                      <line x1="16" y1="17" x2="8" y2="17"></line>
                      <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    My Reports
                  </RouterLink>
                </li>
                <li>
                  <RouterLink class="dropdown-item rounded-2 d-flex align-items-center gap-2" to="/questionnaire">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round">
                      <polygon
                        points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2">
                      </polygon>
                    </svg>
                    Questionnaire
                  </RouterLink>
                </li>
                <li>
                  <hr class="dropdown-divider my-2">
                </li>
                <li>
                  <button class="dropdown-item rounded-2 text-danger d-flex align-items-center gap-2"
                    @click="handleLogout">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                      <polyline points="16 17 21 12 16 7"></polyline>
                      <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                    Logout
                  </button>
                </li>
              </template>
            </ul>
          </li>

          <li class="nav-item ms-lg-3 mt-3 mt-lg-0" v-if="!isLoggedIn">
            <RouterLink to="/register" class="btn btn-primary px-4 py-2 rounded-pill shadow-sm fw-semibold">
              Get Started
            </RouterLink>
          </li>

        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  padding: 12px 0;
  transition: all 0.3s ease;
}

.brand-icon {
  font-size: 1.2rem;
}

/* Custom Link Styling */
.custom-link {
  font-weight: 500;
  color: #555;
  margin: 0 5px;
  padding: 8px 12px !important;
  border-radius: 8px;
  transition: all 0.2s ease;
  position: relative;
}

.custom-link:hover,
.router-link-active {
  color: #0d6efd;
  background-color: rgba(13, 110, 253, 0.05);
}

/* User Avatar Styling */
.user-avatar-bg {
  width: 32px;
  height: 32px;
  background-color: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0d6efd;
  transition: all 0.2s;
}

.nav-link:hover .user-avatar-bg {
  background-color: #0d6efd;
  color: white;
}

/* Dropdown Menu Polish */
.dropdown-menu {
  border-radius: 12px;
  min-width: 220px;
  padding: 8px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.dropdown-item {
  padding: 8px 12px;
  font-size: 0.95rem;
  color: #4b5563;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  color: #0d6efd;
  transform: translateX(3px);
}

.dropdown-item.text-danger:hover {
  background-color: #fef2f2;
  color: #dc3545;
}

/* Animation for Dropdown (Desktop) */
@media (min-width: 992px) {
  .animate-slide {
    display: block;
    opacity: 0;
    visibility: hidden;
    transform: translateY(10px);
    transition: all 0.2s cubic-bezier(0.165, 0.84, 0.44, 1);
  }

  .nav-item.dropdown:hover .animate-slide {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
}

/* Mobile Styling */
@media (max-width: 991px) {
  .navbar-collapse {
    background: white;
    padding: 20px;
    margin-top: 15px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  }

  .dropdown-menu {
    border: none;
    box-shadow: none;
    padding-left: 10px;
    margin-top: 5px;
    background-color: #f8f9fa;
  }

  .nav-item {
    margin-bottom: 5px;
  }
}
</style>