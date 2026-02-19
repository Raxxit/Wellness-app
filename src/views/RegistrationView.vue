<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import AOS from "aos";
import "aos/dist/aos.css";
import registrationBg from '@/assets/img/3.png';

const router = useRouter();

const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  gender: '',
});

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  gender: ''
});

const isLoading = ref(false);
const feedbackMessage = ref({ text: '', type: '' });

const isValidEmail = (email) => {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};

const validateField = (field) => {
  feedbackMessage.value = { text: '', type: '' };

  const val = formData[field];

  switch (field) {
    case 'username':
      errors.username = (!val || val.trim().length < 2)
        ? "Username must be at least 2 characters." : "";
      break;

    case 'email':
      errors.email = !isValidEmail(val)
        ? "Please enter a valid email address." : "";
      break;

    case 'age':
      const ageNum = parseInt(val);
      errors.age = (isNaN(ageNum) || ageNum < 13 || ageNum > 120)
        ? "Age must be between 13 and 120." : "";
      break;

    case 'gender':
      errors.gender = (!val) ? "Please select a gender." : "";
      break;

    case 'password':
      errors.password = (!val || val.length < 6)
        ? "Password must be at least 6 characters." : "";
      if (formData.confirmPassword) validateField('confirmPassword');
      break;

    case 'confirmPassword':
      errors.confirmPassword = (val !== formData.password)
        ? "Passwords do not match." : "";
      break;
  }
};

const handleSubmit = async () => {
  Object.keys(formData).forEach(key => validateField(key));

  const hasErrors = Object.values(errors).some(error => error !== "");
  if (hasErrors) {
    feedbackMessage.value = { text: "Please fix the errors mentioned.", type: 'error' };
    return;
  }

  // 3. Prepare Data
  isLoading.value = true;
  const cleanUsername = formData.username.trim();
  const cleanEmail = formData.email.trim().toLowerCase();

  const dataPayload = new FormData();
  dataPayload.append('username', cleanUsername);
  dataPayload.append('email', cleanEmail);
  dataPayload.append('password', formData.password);
  dataPayload.append('age', formData.age);
  dataPayload.append('gender', formData.gender);

  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      body: dataPayload
    });

    const data = await response.json();

    if (response.ok && data.success) {
      feedbackMessage.value = { text: "Registration successful! Redirecting...", type: 'success' };
      // Clear form
      Object.keys(formData).forEach(key => formData[key] = '');
      setTimeout(() => { router.push('/login'); }, 2000);
    } else {
      feedbackMessage.value = { text: data.message || "Registration failed.", type: 'error' };

      // If server returns specific field error (optional advanced step), map it here
      if (data.field === 'email') errors.email = data.message;
    }

  } catch (error) {
    console.error("Registration error:", error);
    feedbackMessage.value = { text: "Cannot connect to server.", type: 'error' };
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  AOS.init({ duration: 800, once: true });
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
          <div class="col-12 col-md-6 mb-4 mb-md-0" data-aos="fade-right">
            <div class="image-wrapper shadow rounded overflow-hidden">
              <img :src="registrationBg" alt="Mental wellness journey" class="img-fluid">
            </div>
          </div>

          <div class="col-12 col-md-6" data-aos="fade-left" data-aos-delay="300">
            <div class="card border-0 shadow-lg rounded">
              <div class="card-body p-4 p-md-5">
                <h2 class="fw-bold mb-2 text-center">Create Your Account</h2>

                <div v-if="feedbackMessage.text" class="alert mb-4"
                  :class="feedbackMessage.type === 'success' ? 'alert-success' : 'alert-danger'">
                  {{ feedbackMessage.text }}
                </div>

                <form @submit.prevent="handleSubmit" novalidate>
                  <div class="mb-3">
                    <label for="username" class="form-label fw-bold">User Name</label>
                    <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errors.username }"
                      id="username" v-model="formData.username" @blur="validateField('username')"
                      @input="errors.username = ''" placeholder="Enter your user name">
                    <div class="invalid-feedback">{{ errors.username }}</div>
                  </div>

                  <div class="mb-3">
                    <label for="email" class="form-label fw-bold">Email Address</label>
                    <input type="email" class="form-control form-control-lg" :class="{ 'is-invalid': errors.email }"
                      id="email" v-model="formData.email" @blur="validateField('email')" @input="errors.email = ''"
                      placeholder="your.email@example.com">
                    <div class="invalid-feedback">{{ errors.email }}</div>
                  </div>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="age" class="form-label fw-bold">Age</label>
                      <input type="number" class="form-control form-control-lg" :class="{ 'is-invalid': errors.age }"
                        id="age" v-model="formData.age" @blur="validateField('age')" @input="errors.age = ''"
                        placeholder="25">
                      <div class="invalid-feedback">{{ errors.age }}</div>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="gender" class="form-label fw-bold">Gender</label>
                      <select class="form-control form-control-lg" :class="{ 'is-invalid': errors.gender }" id="gender"
                        v-model="formData.gender" @blur="validateField('gender')" @change="validateField('gender')">
                        <option value="" disabled selected>Select</option>
                        <option value="1">Male</option>
                        <option value="2">Female</option>
                        <option value="3">Other</option>
                        <option value="0">Prefer not to say</option>
                      </select>
                      <div class="invalid-feedback">{{ errors.gender }}</div>
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="password" class="form-label fw-bold">Password</label>
                    <input type="password" class="form-control form-control-lg"
                      :class="{ 'is-invalid': errors.password }" id="password" v-model="formData.password"
                      @blur="validateField('password')" @input="errors.password = ''"
                      placeholder="Create a strong password">
                    <div class="invalid-feedback">{{ errors.password }}</div>
                  </div>

                  <div class="mb-4">
                    <label for="confirmPassword" class="form-label fw-bold">Confirm Password</label>
                    <input type="password" class="form-control form-control-lg"
                      :class="{ 'is-invalid': errors.confirmPassword }" id="confirmPassword"
                      v-model="formData.confirmPassword" @blur="validateField('confirmPassword')"
                      @input="errors.confirmPassword = ''" placeholder="Re-enter your password">
                    <div class="invalid-feedback">{{ errors.confirmPassword }}</div>
                  </div>

                  <button type="submit" class="btn btn-primary rounded-pill px-4 w-100 shadow-sm btn-lg"
                    :disabled="isLoading">
                    <span v-if="isLoading">
                      <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                      Registering...
                    </span>
                    <span v-else>Start My Wellness Journey</span>
                  </button>

                  <p class="text-center mt-4 mb-0 text-muted">
                    Register as an advisor?
                    <router-link to="/register-professional" class="text-primary fw-bold text-decoration-none">Register
                      Here</router-link>
                  </p>

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
.image-wrapper img {
  width: 100%;
  height: auto;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-wrapper:hover img {
  transform: scale(1.05);
}

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

.form-control.is-invalid,
.form-select.is-invalid {
  border-color: #dc3545;
  background-image: none;
}

.invalid-feedback {
  display: block;
  font-size: 0.875em;
  color: #dc3545;
  margin-top: 0.25rem;
}
</style>