<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import * as wowModule from "wowjs";
import "wowjs/css/libs/animate.css";
import axios from 'axios';

import registrationBg from '@/assets/img/3.png';

const router = useRouter();

const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  gender: '',
});

// Alert/Message state
const alert = ref({
  show: false,
  type: '', // 'success' or 'error'
  message: ''
});

// Show alert message
const showAlert = (type, message) => {
  alert.value.show = true;
  alert.value.type = type;
  alert.value.message = message;

  // Scroll to top so user can see the error
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });

  // Auto-hide after 5 seconds
  setTimeout(() => {
    alert.value.show = false;
  }, 5000);
};

// Close alert manually
const closeAlert = () => {
  alert.value.show = false;
};

// Validation functions
const validateEmail = (email) => {
  // Check if email contains @ and has text after @
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const validateAge = (age) => {
  // Age should be a number between 18 and 100
  const ageNum = parseInt(age);
  return !isNaN(ageNum) && ageNum >= 18 && ageNum <= 100;
};

const validatePassword = (password) => {
  // Password should be at least 8 characters
  return password.length >= 8;
};

// Sanitize input - remove dangerous characters
const sanitizeInput = (input) => {
  // Remove < > to prevent script injection
  return input.replace(/[<>]/g, '');
};

const handleSubmit = async () => {
  // 1. CHECK FOR EMPTY FIELDS
  if (!formData.value.username.trim()) {
    showAlert('error', 'Please enter your username');
    return;
  }
  if (!formData.value.email.trim()) {
    showAlert('error', 'Please enter your email');
    return;
  }
  if (!formData.value.age) {
    showAlert('error', 'Please enter your age');
    return;
  }
  if (!formData.value.gender) {
    showAlert('error', 'Please select your gender');
    return;
  }
  if (!formData.value.password) {
    showAlert('error', 'Please enter a password');
    return;
  }
  if (!formData.value.confirmPassword) {
    showAlert('error', 'Please confirm your password');
    return;
  }

  // 2. VALIDATE EMAIL FORMAT
  if (!validateEmail(formData.value.email)) {
    showAlert('error', 'Please enter a valid email (e.g., user@example.com)');
    return;
  }

  // 3. VALIDATE AGE (18-100)
  if (!validateAge(formData.value.age)) {
    showAlert('error', 'Age must be between 18 and 100');
    return;
  }

  // 4. VALIDATE PASSWORD LENGTH
  if (!validatePassword(formData.value.password)) {
    showAlert('error', 'Password must be at least 8 characters long');
    return;
  }

  // 5. CHECK IF PASSWORDS MATCH
  if (formData.value.password !== formData.value.confirmPassword) {
    showAlert('error', 'Passwords do not match');
    return;
  }

  // 6. SANITIZE ALL INPUTS
  const sanitizedData = {
    username: sanitizeInput(formData.value.username.trim()),
    email: sanitizeInput(formData.value.email.trim()),
    age: parseInt(formData.value.age),
    gender: formData.value.gender,
    password: formData.value.password // Don't sanitize password, it needs special chars
  };

  // Create FormData for API (matching your DB fields: username, email, age, gender, password)
  const data = new FormData();
  data.append('username', sanitizedData.username);
  data.append('email', sanitizedData.email);
  data.append('age', sanitizedData.age);
  data.append('gender', sanitizedData.gender);
  data.append('password', sanitizedData.password);

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/register', data);

    if (response.status === 200 || response.status === 201) {
      showAlert('success', 'Registration successful! Redirecting to login...');
      
      // Clear form after successful registration
      formData.value = {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        age: '',
        gender: '',
      };

      // Redirect to login page after 2 seconds
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    }
  } catch (error) {
    console.error('Registration error:', error);
    
    // Check for email uniqueness error (status 409 or specific message)
    if (error.response && error.response.status === 409) {
      showAlert('error', 'This email is already registered. Please use a different email or login.');
    } 
    // Show specific error message from server if available
    else if (error.response && error.response.data && error.response.data.message) {
      showAlert('error', error.response.data.message);
    } 
    else if (error.response && error.response.data && error.response.data.error) {
      showAlert('error', error.response.data.error);
    } 
    else {
      showAlert('error', 'Registration failed. Please check if the backend server is running.');
    }
  }
};

onMounted(() => {
  const WOW = wowModule.WOW || wowModule.default.WOW;
  new WOW().init();
});

</script>


<template>
  <div class="registration-page">

    <!-- Header Section -->
    <header class="py-5 bg-light border-bottom">
      <div class="container text-center">
        <h1 class="display-4 fw-bold text-primary wow fadeInUp" data-wow-delay="0.1s">Begin Your Wellness Journey</h1>
        <p class="lead text-secondary wow fadeInUp" data-wow-delay="0.2s">
          Take the first step towards better mental health and emotional well-being.
        </p>
      </div>
    </header>

    <!-- Registration Form Section -->
    <section class="py-5">
      <div class="container">
        <div class="row align-items-center">

          <!-- Left Side: Benefits -->
          <div class="col-12 col-md-6 mb-4 mb-md-0 wow fadeInLeft" data-wow-delay="0.3s">
            <div class="image-wrapper shadow rounded overflow-hidden">
              <img :src="registrationBg" alt="Mental wellness journey" class="img-fluid">
            </div>
            <div class="mt-4 p-4 bg-light rounded">
              <h3 class="fw-bold mb-3">How We Help You</h3>
              <ul class="list-unstyled">
                <li class="mb-3 d-flex align-items-start">
                  <i class="fa fa-check-circle text-primary me-3 mt-1"></i>
                  <div>
                    <strong>Personalized Assessment</strong>
                    <p class="text-muted mb-0 small">Complete questionnaires to understand your mental state</p>
                  </div>
                </li>
                <li class="mb-3 d-flex align-items-start">
                  <i class="fa fa-check-circle text-primary me-3 mt-1"></i>
                  <div>
                    <strong>Guided Activities</strong>
                    <p class="text-muted mb-0 small">Get customized tasks to boost mood and reduce stress</p>
                  </div>
                </li>
                <li class="mb-3 d-flex align-items-start">
                  <i class="fa fa-check-circle text-primary me-3 mt-1"></i>
                  <div>
                    <strong>Track Your Progress</strong>
                    <p class="text-muted mb-0 small">Monitor improvements in your mental well-being</p>
                  </div>
                </li>
                <li class="mb-3 d-flex align-items-start">
                  <i class="fa fa-check-circle text-primary me-3 mt-1"></i>
                  <div>
                    <strong>Professional Support</strong>
                    <p class="text-muted mb-0 small">Access resources and guidance when you need it</p>
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Right Side: Registration Form -->
          <div class="col-12 col-md-6 wow fadeInRight" data-wow-delay="0.4s">
            <div class="card border-0 shadow-lg rounded">
              <div class="card-body p-4 p-md-5">
                <h2 class="fw-bold mb-2 text-center">Create Your Account</h2>
                <p class="text-center text-muted mb-3">Join thousands on their path to better mental health</p>

                <!-- Alert Message (compact, above form) -->
                <transition name="slide-fade">
                  <div v-if="alert.show" :class="['alert', alert.type === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible', 'fade', 'show', 'py-2', 'mb-3']" role="alert">
                    <small>
                      <i :class="alert.type === 'success' ? 'fa fa-check-circle' : 'fa fa-exclamation-circle'" class="me-2"></i>
                      <strong>{{ alert.message }}</strong>
                    </small>
                    <button @click="closeAlert" type="button" class="btn-close btn-close-sm" aria-label="Close"></button>
                  </div>
                </transition>

                <form @submit.prevent="handleSubmit">

                  <!-- Username -->
                  <div class="mb-3">
                    <label for="username" class="form-label fw-bold">
                      <i class="fa fa-user text-primary me-2"></i>User Name
                    </label>
                    <input type="text" class="form-control form-control-lg" id="username" v-model="formData.username"
                      placeholder="Enter your user name" maxlength="50">
                  </div>

                  <!-- Email -->
                  <div class="mb-3">
                    <label for="email" class="form-label fw-bold">
                      <i class="fa fa-envelope text-primary me-2"></i>Email Address
                    </label>
                    <input type="text" class="form-control form-control-lg" id="email" v-model="formData.email"
                      placeholder="your.email@example.com" maxlength="100">
                    <small class="text-muted">We'll send your wellness reports here</small>
                  </div>

                  <!-- Age and Gender Row -->
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="age" class="form-label fw-bold">
                        <i class="fa fa-birthday-cake text-primary me-2"></i>Age
                      </label>
                      <input type="number" class="form-control form-control-lg" id="age" v-model="formData.age"
                        placeholder="25" min="18" max="100">
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="gender" class="form-label fw-bold">
                        <i class="fa fa-venus-mars text-primary me-2"></i>Gender
                      </label>
                      <select class="form-control form-control-lg" id="gender" v-model="formData.gender">
                        <option value="">Select</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                       
                      </select>
                    </div>
                  </div>

                  <!-- Password -->
                  <div class="mb-3">
                    <label for="password" class="form-label fw-bold">
                      <i class="fa fa-lock text-primary me-2"></i>Password
                    </label>
                    <input type="password" class="form-control form-control-lg" id="password"
                      v-model="formData.password" placeholder="Create a strong password (min 8 characters)" maxlength="100">
                  </div>

                  <!-- Confirm Password -->
                  <div class="mb-4">
                    <label for="confirmPassword" class="form-label fw-bold">
                      <i class="fa fa-lock text-primary me-2"></i>Confirm Password
                    </label>
                    <input type="password" class="form-control form-control-lg" id="confirmPassword"
                      v-model="formData.confirmPassword" placeholder="Re-enter your password" maxlength="100">
                  </div>

                  <!-- Privacy Notice -->
                  <div class="alert alert-info mb-4">
                    <small>
                      <i class="fa fa-shield-alt me-2"></i>
                      <strong>Your privacy matters.</strong> All your data is confidential and secure.
                    </small>
                  </div>

                  <!-- Submit Button -->
                  <button type="submit" class="btn btn-primary rounded-pill px-4 w-100 shadow-sm btn-lg">
                    <i class="fa fa-arrow-right me-2"></i>Start My Wellness Journey
                  </button>

                  <!-- Login Link -->
                  <p class="text-center mt-4 mb-0 text-muted">
                    Already have an account?
                    <router-link to="/login" class="text-primary fw-bold text-decoration-none">Login here</router-link>
                  </p>
                </form>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
/* Slide fade animation for alert */
.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Matching the AboutView image hover effect */
.image-wrapper img {
  width: 100%;
  height: auto;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-wrapper:hover img {
  transform: scale(1.05);
}

/* Form styling */
.form-control {
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.15);
}

.card {
  background: #ffffff;
}

/* Button hover effect */
.btn-primary {
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(13, 110, 253, 0.3);
}

/* Alert styling */
.alert-info {
  background-color: #e7f3ff;
  border: 1px solid #b3d9ff;
  border-radius: 8px;
}

/* Compact alert styling */
.alert {
  border-radius: 8px;
}

.alert-success {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}

.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}
</style>