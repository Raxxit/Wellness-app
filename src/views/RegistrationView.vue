<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import AOS from "aos";
import "aos/dist/aos.css";
import registrationBg from '@/assets/img/3.png';

const router = useRouter();

// --- STATE ---
const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  gender: '',
});

const isLoading = ref(false);
const feedbackMessage = ref({ text: '', type: '' }); // type: 'success' | 'error'

// --- ACTIONS ---
const handleSubmit = async () => {
  feedbackMessage.value = { text: '', type: '' };

  // 1. Basic Validation
  if (formData.password !== formData.confirmPassword) {
    feedbackMessage.value = { text: "Passwords do not match.", type: 'error' };
    return;
  }
  if (formData.password.length < 6) {
    feedbackMessage.value = { text: "Password must be at least 6 characters.", type: 'error' };
    return;
  }

  isLoading.value = true;

  // 2. Prepare Payload (Match Backend Expectations)
  const payload = {
    username: formData.username,
    email: formData.email,
    password: formData.password,
    age: parseInt(formData.age),
    gender: parseInt(formData.gender)
  };

  try {
    // 3. API Call
    const response = await fetch('http://127.0.0.1:5000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok && data.success) {
      feedbackMessage.value = { text: "Registration successful! Redirecting...", type: 'success' };
      // Clear form
      Object.keys(formData).forEach(key => formData[key] = '');

      // Redirect to login after 2 seconds
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } else {
      feedbackMessage.value = { text: data.message || "Registration failed.", type: 'error' };
    }

  } catch (error) {
    console.error("Registration error:", error);
    feedbackMessage.value = { text: "Cannot connect to server. Is Flask running?", type: 'error' };
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  AOS.init({
    duration: 800,
    once: true
  });
});
</script>

<template>
  <div class="registration-page">

    <header class="py-5 bg-light border-bottom">
      <div class="container text-center">
        <h1 class="display-4 fw-bold text-primary" data-aos="fade-up">Begin Your Wellness Journey</h1>
        <p class="lead text-secondary" data-aos="fade-up" data-aos-delay="100">
          Take the first step towards better mental health and emotional well-being.
        </p>
      </div>
    </header>

    <section class="py-5">
      <div class="container">
        <div class="row align-items-center">

          <div class="col-12 col-md-6 mb-4 mb-md-0" data-aos="fade-right" data-aos-delay="200">
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

          <div class="col-12 col-md-6" data-aos="fade-left" data-aos-delay="300">
            <div class="card border-0 shadow-lg rounded">
              <div class="card-body p-4 p-md-5">
                <h2 class="fw-bold mb-2 text-center">Create Your Account</h2>
                <p class="text-center text-muted mb-4">Join thousands on their path to better mental health</p>

                <div v-if="feedbackMessage.text" class="alert mb-4"
                  :class="feedbackMessage.type === 'success' ? 'alert-success' : 'alert-danger'">
                  {{ feedbackMessage.text }}
                </div>

                <form @submit.prevent="handleSubmit">

                  <div class="mb-3">
                    <label for="username" class="form-label fw-bold">
                      <i class="fa fa-user text-primary me-2"></i>User Name
                    </label>
                    <input type="text" class="form-control form-control-lg" id="username" v-model="formData.username"
                      placeholder="Enter your user name" required>
                  </div>

                  <div class="mb-3">
                    <label for="email" class="form-label fw-bold">
                      <i class="fa fa-envelope text-primary me-2"></i>Email Address
                    </label>
                    <input type="email" class="form-control form-control-lg" id="email" v-model="formData.email"
                      placeholder="your.email@example.com" required>
                    <small class="text-muted">We'll send your wellness reports here</small>
                  </div>

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
                        <option value="1">Male</option>
                        <option value="2">Female</option>
                        <option value="3">Other</option>
                        <option value="0">Prefer not to say</option>
                      </select>
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="password" class="form-label fw-bold">
                      <i class="fa fa-lock text-primary me-2"></i>Password
                    </label>
                    <input type="password" class="form-control form-control-lg" id="password"
                      v-model="formData.password" placeholder="Create a strong password" required>
                  </div>

                  <div class="mb-4">
                    <label for="confirmPassword" class="form-label fw-bold">
                      <i class="fa fa-lock text-primary me-2"></i>Confirm Password
                    </label>
                    <input type="password" class="form-control form-control-lg" id="confirmPassword"
                      v-model="formData.confirmPassword" placeholder="Re-enter your password" required>
                  </div>

                  <div class="alert alert-info mb-4">
                    <small>
                      <i class="fa fa-shield-alt me-2"></i>
                      <strong>Your privacy matters.</strong> All your data is confidential and secure.
                    </small>
                  </div>

                  <button type="submit" class="btn btn-primary rounded-pill px-4 w-100 shadow-sm btn-lg"
                    :disabled="isLoading">
                    <span v-if="isLoading">
                      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Registering...
                    </span>
                    <span v-else>
                      <i class="fa fa-arrow-right me-2"></i>Start My Wellness Journey
                    </span>
                  </button>

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
.form-control,
.form-select {
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
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

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(13, 110, 253, 0.3);
}

.btn-primary:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

/* Alert styling */
.alert-info {
  background-color: #e7f3ff;
  border: 1px solid #b3d9ff;
  border-radius: 8px;
}
</style>