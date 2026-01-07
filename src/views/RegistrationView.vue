<script setup>
import { ref, onMounted } from 'vue';
import { WOW } from 'wowjs';

import registrationBg from '@/assets/img/3.jpg';

const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  gender: '',
});

const handleSubmit = async () => {
  const data = new FormData();
  data.append('username', formData.value.username);
  data.append('email', formData.value.email);
  data.append('age', formData.value.age);
  data.append('gender', formData.value.gender);
  data.append('password', formData.value.password);

  try {
    // 2. Send as Form Data
    // Axios automatically sets header to 'multipart/form-data' or 'application/x-www-form-urlencoded'
    const response = await axios.post('http://127.0.0.1:5000/api/register', data);

    if (response.status === 200) {
      alert('Registration successful!');
    }
  } catch (error) {
    console.error(error);
    alert('Registration failed');
  }
};

onMounted(() => {
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
                <p class="text-center text-muted mb-4">Join thousands on their path to better mental health</p>

                <form @submit.prevent="handleSubmit">

                  <!-- Full Name -->
                  <div class="mb-3">
                    <label for="username" class="form-label fw-bold">
                      <i class="fa fa-user text-primary me-2"></i>User Name
                    </label>
                    <input type="text" class="form-control form-control-lg" id="username" v-model="formData.username"
                      placeholder="Enter your user name" required>
                  </div>

                  <!-- Email -->
                  <div class="mb-3">
                    <label for="email" class="form-label fw-bold">
                      <i class="fa fa-envelope text-primary me-2"></i>Email Address
                    </label>
                    <input type="email" class="form-control form-control-lg" id="email" v-model="formData.email"
                      placeholder="your.email@example.com" required>
                    <small class="text-muted">We'll send your wellness reports here</small>
                  </div>

                  <!-- Age and Gender Row -->
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="age" class="form-label fw-bold">
                        <i class="fa fa-birthday-cake text-primary me-2"></i>Age
                      </label>
                      <input type="number" class="form-control form-control-lg" id="age" v-model="formData.age"
                        placeholder="25" min="13" max="120" required>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="gender" class="form-label fw-bold">
                        <i class="fa fa-venus-mars text-primary me-2"></i>Gender
                      </label>
                      <select class="form-control form-control-lg" id="gender" v-model="formData.gender" required>
                        <option value="">Select</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                        <option value="prefer-not-to-say">Prefer not to say</option>
                      </select>
                    </div>
                  </div>

                  <!-- Password -->
                  <div class="mb-3">
                    <label for="password" class="form-label fw-bold">
                      <i class="fa fa-lock text-primary me-2"></i>Password
                    </label>
                    <input type="password" class="form-control form-control-lg" id="password"
                      v-model="formData.password" placeholder="Create a strong password" required>
                  </div>

                  <!-- Confirm Password -->
                  <div class="mb-4">
                    <label for="confirmPassword" class="form-label fw-bold">
                      <i class="fa fa-lock text-primary me-2"></i>Confirm Password
                    </label>
                    <input type="password" class="form-control form-control-lg" id="confirmPassword"
                      v-model="formData.confirmPassword" placeholder="Re-enter your password" required>
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
                    <router-link to="/" class="text-primary fw-bold text-decoration-none">Login here</router-link>
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
</style>