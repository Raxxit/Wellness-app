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
  related_docs: null,
  bio: ''
});

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  gender: '',
  related_docs: '',
  bio: ''
});

const isLoading = ref(false);
const feedbackMessage = ref({ text: '', type: '' });
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const fileName = ref('');

const isValidEmail = (email) => {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    formData.related_docs = file;
    fileName.value = file.name;
    validateField('related_docs');
  }
};

const validateField = (field) => {
  feedbackMessage.value = { text: '', type: '' };

  if (field === 'related_docs') {
    const file = formData.related_docs;
    if (!file) {
      errors.related_docs = "Please upload your license or certification document.";
      return;
    }
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
      errors.related_docs = "Invalid file type. Only PDF, JPG, PNG allowed.";
    } else if (file.size > 5 * 1024 * 1024) {
      errors.related_docs = "File size must be less than 5MB.";
    } else {
      errors.related_docs = "";
    }
    return;
  }

  const val = formData[field];
  switch (field) {
    case 'username':
      errors.username = (!val || val.trim().length < 2) ? "Username must be at least 2 characters." : "";
      break;
    case 'email':
      errors.email = !isValidEmail(val) ? "Please enter a valid email address." : "";
      break;
    case 'age':
      const ageNum = parseInt(val);
      errors.age = (isNaN(ageNum) || ageNum < 13 || ageNum > 120) ? "Age must be between 13 and 120." : "";
      break;
    case 'gender':
      errors.gender = (!val) ? "Please select your gender." : "";
      break;
    case 'password':
      errors.password = (!val || val.length < 6) ? "Password must be at least 6 characters." : "";
      if (formData.confirmPassword) validateField('confirmPassword');
      break;
    case 'confirmPassword':
      errors.confirmPassword = (val !== formData.password) ? "Passwords do not match." : "";
      break;
    case 'bio':
      errors.bio = (!val || val.trim().length < 10) ? "Professional bio required (min 10 chars)." : "";
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

  isLoading.value = true;

  const cleanUsername = formData.username.trim();
  const cleanEmail = formData.email.trim().toLowerCase();

  const dataPayload = new FormData();
  dataPayload.append('username', cleanUsername);
  dataPayload.append('email', cleanEmail);
  dataPayload.append('password', formData.password);
  dataPayload.append('age', formData.age);
  dataPayload.append('gender', formData.gender);
  dataPayload.append('bio', formData.bio.trim());

  if (formData.related_docs) {
    dataPayload.append('related_docs', formData.related_docs);
  }

  try {
    const response = await fetch('/api/register-professional', {
      method: 'POST',
      body: dataPayload
    });

    const data = await response.json();

    if (response.ok && data.success) {
      feedbackMessage.value = {
        text: "Registration successful! Your account is pending admin verification.",
        type: 'success'
      };

      Object.keys(formData).forEach(key => {
        if (key !== 'related_docs') formData[key] = '';
      });
      fileName.value = '';

      setTimeout(() => { router.push('/login'); }, 3000);
    } else {
      feedbackMessage.value = { text: data.message || "Registration failed.", type: 'error' };
      if (data.field === 'email') errors.email = data.message;
    }
  } catch (error) {
    console.error("Professional Registration error:", error);
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
  <div class="professional-registration-page">
    <header class="py-5 bg-light border-bottom">
      <div class="container text-center">

        <p class="lead text-secondary" data-aos="fade-up" data-aos-delay="100">
          Expand your practice and help more people on their wellness journey
        </p>
      </div>
    </header>

    <section class="py-5">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-12 col-lg-10" data-aos="fade-up">
            <div class="card border-0 shadow-lg rounded">
              <div class="card-body p-4 p-md-5">
                <div class="text-center mb-4">
                  <div class="professional-icon mb-3">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none"
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                      class="text-primary">
                      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                    </svg>
                  </div>
                  <h2 class="fw-bold mb-2">Professional Registration</h2>
                  <p class="text-muted">Doctors, Psychologists & Therapists</p>
                </div>

                <div v-if="feedbackMessage.text" class="alert mb-4"
                  :class="feedbackMessage.type === 'success' ? 'alert-success' : 'alert-danger'">
                  {{ feedbackMessage.text }}
                </div>

                <form @submit.prevent="handleSubmit" novalidate>
                  <h5 class="fw-bold mb-3 text-primary border-bottom pb-2">Personal Information</h5>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="username" class="form-label fw-bold">Full Name <span
                          class="text-danger">*</span></label>
                      <input type="text" class="form-control form-control-lg" :class="{ 'is-invalid': errors.username }"
                        id="username" v-model="formData.username" @blur="validateField('username')"
                        @input="errors.username = ''" placeholder="Dr. Jane Smith">
                      <div class="invalid-feedback">{{ errors.username }}</div>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="email" class="form-label fw-bold">Email Address <span
                          class="text-danger">*</span></label>
                      <input type="email" class="form-control form-control-lg" :class="{ 'is-invalid': errors.email }"
                        id="email" v-model="formData.email" @blur="validateField('email')" @input="errors.email = ''"
                        placeholder="professional@clinic.com">
                      <div class="invalid-feedback">{{ errors.email }}</div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-md-4 mb-3">
                      <label for="age" class="form-label fw-bold">Age <span class="text-danger">*</span></label>
                      <input type="number" class="form-control form-control-lg" :class="{ 'is-invalid': errors.age }"
                        id="age" v-model="formData.age" @blur="validateField('age')" @input="errors.age = ''"
                        placeholder="35">
                      <div class="invalid-feedback">{{ errors.age }}</div>
                    </div>

                    <div class="col-md-4 mb-3">
                      <label for="gender" class="form-label fw-bold">Gender <span class="text-danger">*</span></label>
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

                  <h5 class="fw-bold mb-3 text-primary border-bottom pb-2 mt-4">Professional Credentials</h5>

                  <div class="mb-3">
                    <label for="related_docs" class="form-label fw-bold">Upload License/Certification <span
                        class="text-danger">*</span></label>
                    <input type="file" class="form-control form-control-lg"
                      :class="{ 'is-invalid': errors.related_docs }" id="related_docs" @change="handleFileChange"
                      accept=".pdf,.jpg,.jpeg,.png">
                    <div v-if="fileName" class="mt-2 text-success">
                      <small>✓ {{ fileName }}</small>
                    </div>
                    <div class="invalid-feedback">{{ errors.related_docs }}</div>
                    <div class="form-text">Accepted formats: PDF, JPG, PNG. Max size: 5MB.</div>
                  </div>

                  <div class="mb-3">
                    <label for="bio" class="form-label fw-bold">Professional Bio <span
                        class="text-danger">*</span></label>
                    <textarea class="form-control form-control-lg" rows="5" :class="{ 'is-invalid': errors.bio }"
                      id="bio" v-model="formData.bio" @blur="validateField('bio')" @input="errors.bio = ''"
                      placeholder="Tell us about your experience, clinic name, specialization, and approach to therapy..."></textarea>
                    <div class="invalid-feedback">{{ errors.bio }}</div>
                    <div class="form-text">Include years of experience, clinic name, and specialization.</div>
                  </div>

                  <h5 class="fw-bold mb-3 text-primary border-bottom pb-2 mt-4">Account Security</h5>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="password" class="form-label fw-bold">Password <span
                          class="text-danger">*</span></label>
                      <div class="input-group">
                        <input :type="showPassword ? 'text' : 'password'" class="form-control form-control-lg"
                          :class="{ 'is-invalid': errors.password }" id="password" v-model="formData.password"
                          @blur="validateField('password')" @input="errors.password = ''"
                          placeholder="Create a strong password">
                        <button class="btn btn-outline-secondary" type="button" @click="showPassword = !showPassword">
                          <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                            fill="none" stroke="currentColor" stroke-width="2">
                            <path
                              d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24">
                            </path>
                            <line x1="1" y1="1" x2="23" y2="23"></line>
                          </svg>
                        </button>
                        <div class="invalid-feedback">{{ errors.password }}</div>
                      </div>
                    </div>

                    <div class="col-md-6 mb-3">
                      <label for="confirmPassword" class="form-label fw-bold">Confirm Password <span
                          class="text-danger">*</span></label>
                      <div class="input-group">
                        <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control form-control-lg"
                          :class="{ 'is-invalid': errors.confirmPassword }" id="confirmPassword"
                          v-model="formData.confirmPassword" @blur="validateField('confirmPassword')"
                          @input="errors.confirmPassword = ''" placeholder="Re-enter your password">
                        <button class="btn btn-outline-secondary" type="button"
                          @click="showConfirmPassword = !showConfirmPassword">
                          <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                            fill="none" stroke="currentColor" stroke-width="2">
                            <path
                              d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24">
                            </path>
                            <line x1="1" y1="1" x2="23" y2="23"></line>
                          </svg>
                        </button>
                        <div class="invalid-feedback">{{ errors.confirmPassword }}</div>
                      </div>
                    </div>
                  </div>

                  <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-primary rounded-pill px-4 shadow-sm btn-lg"
                      :disabled="isLoading">
                      <span v-if="isLoading">
                        <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                        Registering...
                      </span>
                      <span v-else>Submit Professional Application</span>
                    </button>
                  </div>


                  <p class="text-center mt-4 mb-0 text-muted">
                    Already have an account?
                    <router-link to="/login" class="text-primary fw-bold text-decoration-none">Login here</router-link>
                  </p>
                  <p class="text-center mt-2 text-muted">
                    Looking for a regular account?
                    <router-link to="/register" class="text-primary fw-bold text-decoration-none">Register as a
                      patient</router-link>
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
.professional-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4);
  }

  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 20px rgba(102, 126, 234, 0);
  }
}

.form-control,
.form-select {
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.15);
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

.form-text {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.input-group .btn-outline-secondary {
  border-left: none;
}

h5.border-bottom {
  border-color: #e0e0e0 !important;
}

input[type="file"]::file-selector-button {
  border: 2px solid #667eea;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  background-color: #f8fafc;
  color: #667eea;
  font-weight: 600;
  transition: all 0.2s;
}

input[type="file"]::file-selector-button:hover {
  background-color: #667eea;
  color: white;
}

@media (max-width: 768px) {
  .card-body {
    padding: 1.5rem !important;
  }
}
</style>