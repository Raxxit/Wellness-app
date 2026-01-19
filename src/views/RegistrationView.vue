<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const loading = ref(false);
const errorMessage = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  age: '',
  gender: '',
});

const handleRegister = async () => {
  errorMessage.value = '';

  if (form.password !== form.confirmPassword) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  if (form.password.length < 6) {
    errorMessage.value = "Password must be at least 6 characters.";
    return;
  }

  loading.value = true;

  try {
    const data = new FormData();

    data.append('username', form.username);

    data.append('email', form.email);
    data.append('password', form.password);
    data.append('age', form.age);
    data.append('gender', form.gender);

    const response = await axios.post('/api/register', data);


    if (response.status === 200) {
      alert('Registration successful! Please login.');
      router.push('/login');
    }
  } catch (error) {
    console.error(error);


    if (error.response) {
      if (error.response.status === 409) {
        errorMessage.value = 'This email is already registered.';
      }
      else if (error.response.status === 400) {
        errorMessage.value = 'Please fill in all required fields.';
      }
      else if (error.response.data && error.response.data.message) {
        errorMessage.value = error.response.data.message;
      }
      else {
        errorMessage.value = 'Registration failed. Please try again.';
      }
    } else {
      errorMessage.value = 'Network error. Please check your connection.';
    }
  } finally {
    loading.value = false;
  }
};

</script>

<template>
  <div class="register-wrapper">
    <div class="register-card">

      <div class="register-illustration">
        <div class="wellness-icon">
          <div class="leaf">🍃</div>
          <div class="heart">❤️</div>
          <div class="sun">☀️</div>
        </div>
        <h1>Join the Journey</h1>
        <p class="wellness-quote">"The first step towards getting somewhere is to decide you're not going to stay where
          you are."</p>
      </div>

      <div class="register-form-section">
        <div class="form-header">
          <h2>Create Account</h2>
          <p class="form-subtitle">Start your personalized wellness plan</p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">

          <div class="input-group">
            <div class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <input type="text" v-model="form.username" placeholder="" required :disabled="loading" class="form-input" />
            <label>Username</label>
          </div>

          <div class="input-group">
            <div class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </div>
            <input type="email" v-model="form.email" placeholder="" required :disabled="loading" class="form-input" />
            <label>Email Address</label>
          </div>

          <div class="row-group">
            <div class="input-group half-width">
              <div class="input-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
              </div>
              <input type="number" v-model="form.age" placeholder="" required min="13" max="120" :disabled="loading"
                class="form-input" />
              <label>Age</label>
            </div>

            <div class="input-group half-width">
              <div class="input-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 2 15 2 22 2 22 9"></polygon>
                </svg>
              </div>
              <select v-model="form.gender" required :disabled="loading" class="form-input select-input">
                <option value="1">Male</option>
                <option value="2">Female</option>
                <option value="3">Other</option>
              </select>
              <label class="select-label">Gender</label>
            </div>
          </div>

          <div class="input-group">
            <div class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <input :type="showPassword ? 'text' : 'password'" v-model="form.password" placeholder="" required
              :disabled="loading" class="form-input" />
            <label>Password</label>
            <button type="button" @click="showPassword = !showPassword" class="password-toggle">
              <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path
                  d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24">
                </path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
              </svg>
            </button>
          </div>

          <div class="input-group">
            <div class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path
                  d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4">
                </path>
              </svg>
            </div>
            <input :type="showConfirmPassword ? 'text' : 'password'" v-model="form.confirmPassword" placeholder=""
              required :disabled="loading" class="form-input" />
            <label>Confirm Password</label>
            <button type="button" @click="showConfirmPassword = !showConfirmPassword" class="password-toggle">
              <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path
                  d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24">
                </path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
              </svg>
            </button>
          </div>

          <button type="submit" :disabled="loading" class="submit-button" :class="{ loading: loading }">
            <span v-if="!loading">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <line x1="20" y1="8" x2="20" y2="14"></line>
                <line x1="23" y1="11" x2="17" y2="11"></line>
              </svg>
              Create Account
            </span>
            <span v-else class="loading-text">
              <div class="spinner"></div>
              Creating Account...
            </span>
          </button>

          <div class="divider">
            <span>already have an account?</span>
          </div>

          <p class="login-link">
            <router-link to="/login" class="login-text">Sign in here</router-link>
          </p>
        </form>

        <div v-if="errorMessage" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
.register-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.register-card {
  display: flex;
  max-width: 900px;
  width: 100%;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

/* Left Illustration Side */
.register-illustration {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
}

/* Animations */
.wellness-icon {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 30px;
}

.leaf,
.heart,
.sun {
  position: absolute;
  font-size: 40px;
  animation: float 3s ease-in-out infinite;
}

.leaf {
  top: 0;
  left: 0;
  animation-delay: 0s;
}

.heart {
  top: 20px;
  right: 10px;
  animation-delay: 0.5s;
}

.sun {
  bottom: 10px;
  left: 40px;
  animation-delay: 1s;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10px);
  }
}

.register-illustration h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 15px;
}

.wellness-quote {
  font-size: 16px;
  opacity: 0.9;
  font-style: italic;
  max-width: 300px;
  line-height: 1.6;
}

/* Right Form Side */
.register-form-section {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
}

.form-header {
  margin-bottom: 30px;
  text-align: center;
}

.form-header h2 {
  font-size: 28px;
  color: #2d3748;
  font-weight: 700;
}

.form-subtitle {
  color: #718096;
  font-size: 15px;
}

/* Form Inputs */
.input-group {
  position: relative;
  margin-bottom: 20px;
}

/* Row group for Age/Gender side-by-side */
.row-group {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.row-group .input-group {
  margin-bottom: 0;
  flex: 1;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
  pointer-events: none;
}

.form-input {
  width: 100%;
  padding: 16px 16px 16px 50px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s;
  background: #f8fafc;
}

/* Special styling for Select dropdown */
.select-input {
  appearance: none;
  cursor: pointer;
  height: 58px;
  /* Match text input height */
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Label Logic */
.input-group label {
  position: absolute;
  left: 50px;
  top: 18px;
  color: #a0aec0;
  font-size: 14px;
  transition: all 0.3s;
  pointer-events: none;
}

.form-input:focus+label,
.form-input:not(:placeholder-shown)+label,
.select-input+label {
  /* Always float label for Select */
  top: -8px;
  left: 16px;
  font-size: 12px;
  background: white;
  padding: 0 8px;
  color: #667eea;
}

.password-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
}

.password-toggle:hover {
  color: #667eea;
}

/* Submit Button */
.submit-button {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Loading Spinner */
.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Footer Links */
.divider {
  display: flex;
  align-items: center;
  margin: 25px 0 15px;
  color: #a0aec0;
  font-size: 13px;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: #e2e8f0;
}

.divider span {
  padding: 0 15px;
}

.login-link {
  text-align: center;
  color: #718096;
  font-size: 14px;
  margin-bottom: 0;
}

.login-text {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-text:hover {
  text-decoration: underline;
}

/* Error Message */
.error-message {
  margin-top: 20px;
  padding: 12px;
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 12px;
  color: #c53030;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .register-card {
    flex-direction: column;
    max-width: 450px;
  }

  .register-illustration {
    padding: 30px;
  }

  .register-form-section {
    padding: 30px;
  }

  .row-group {
    flex-direction: column;
    gap: 0;
  }

  .row-group .input-group {
    margin-bottom: 20px;
  }
}
</style>