<script setup>
import { ref, onMounted, reactive } from "vue";
import { useRouter } from "vue-router";
import AOS from "aos";
import "aos/dist/aos.css";

const router = useRouter();

// --- STATE ---
const user = ref({
  username: '',
  email: '',
  age: null,
  gender: null
});

const formData = reactive({
  username: '',
  age: '',
  gender: '',
  password: '',
  confirmPassword: ''
});

const isSaving = ref(false);
const isLoading = ref(true); // Starts true, needs fetchUserProfile to turn false
const successMessage = ref("");
const errorMessage = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const validationErrors = reactive({
  username: '',
  age: '',
  gender: '',
  password: '',
  confirmPassword: ''
});

// --- HELPERS ---
const getGenderText = (genderCode) => {
  const genderMap = {
    1: 'Male',
    2: 'Female',
    3: 'Other',
    0: 'Prefer not to say'
  };
  return genderMap[genderCode] || 'Not specified';
};

// --- API ACTIONS ---
const fetchUserProfile = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Fixed: Added full URL http://127.0.0.1:5000 to ensure it hits Flask
    const response = await fetch('http://127.0.0.1:5000/api/profile', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      if (data.success) {
        user.value = data.user;
        // Pre-fill form
        formData.username = data.user.username || '';
        formData.age = data.user.age || '';
        formData.gender = data.user.gender || '';
      } else {
        errorMessage.value = data.message || "Failed to load profile.";
        // If session invalid, redirect
        if (response.status === 401) setTimeout(() => router.push('/login'), 2000);
      }
    } else {
      errorMessage.value = "Failed to load profile. Please login again.";
      if (response.status === 401) setTimeout(() => router.push('/login'), 2000);
    }
  } catch (error) {
    console.error("Profile fetch error:", error);
    errorMessage.value = "Cannot connect to server. Is Flask running?";
  } finally {
    // CRITICAL: This turns off the spinner
    isLoading.value = false;
  }
};

const handleSubmit = async () => {
  successMessage.value = "";
  errorMessage.value = "";

  if (!validateForm()) {
    errorMessage.value = "Please fix the validation errors before submitting.";
    return;
  }

  isSaving.value = true;

  try {
    const token = localStorage.getItem('token');
    if (!token) {
      errorMessage.value = "You need to be logged in to update profile.";
      isSaving.value = false;
      return;
    }

    const updateData = {
      username: formData.username.trim(),
      age: formData.age ? parseInt(formData.age) : null,
      gender: formData.gender ? parseInt(formData.gender) : null
    };

    if (formData.password.trim()) {
      updateData.password = formData.password;
    }

    const response = await fetch('/api/profile/update', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updateData)
    });

    const data = await response.json();

    if (data.success) {
      successMessage.value = "Profile updated successfully!";
      user.value = data.user;
      localStorage.setItem('user', JSON.stringify(data.user));

      formData.password = '';
      formData.confirmPassword = '';

      // Clear errors
      Object.keys(validationErrors).forEach(key => validationErrors[key] = '');

      setTimeout(() => { successMessage.value = ""; }, 3000);
    } else {
      errorMessage.value = data.message || "Failed to update profile.";
    }
  } catch (error) {
    console.error("Update error:", error);
    errorMessage.value = "An unexpected error occurred. Please try again.";
  } finally {
    isSaving.value = false;
  }
};

const handleLogout = async () => {
  try {
    const token = localStorage.getItem('token');
    if (token) {
      await fetch('http://127.0.0.1:5000/api/logout', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
    }
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
  }
};

// --- VALIDATION LOGIC ---
const validateUsername = () => {
  validationErrors.username = '';
  if (!formData.username.trim()) {
    validationErrors.username = 'Username is required';
    return false;
  }
  if (formData.username.length < 3) {
    validationErrors.username = 'Username must be at least 3 characters';
    return false;
  }
  if (formData.username.length > 50) {
    validationErrors.username = 'Username cannot exceed 50 characters';
    return false;
  }
  const usernameRegex = /^[a-zA-Z0-9_]+$/;
  if (!usernameRegex.test(formData.username)) {
    validationErrors.username = 'Username can only contain letters, numbers, and underscores';
    return false;
  }
  return true;
};

const validateAge = () => {
  validationErrors.age = '';
  if (formData.age === '') return true;
  const ageNum = parseInt(formData.age);
  if (isNaN(ageNum)) {
    validationErrors.age = 'Age must be a number';
    return false;
  }
  if (ageNum < 1 || ageNum > 120) {
    validationErrors.age = 'Age must be between 1 and 120';
    return false;
  }
  return true;
};

const validateGender = () => {
  validationErrors.gender = '';
  return true;
};

const validatePassword = () => {
  validationErrors.password = '';
  if (!formData.password) return true;
  if (formData.password.length < 6) {
    validationErrors.password = 'Password must be at least 6 characters';
    return false;
  }
  if (formData.password.length > 100) {
    validationErrors.password = 'Password cannot exceed 100 characters';
    return false;
  }
  const hasLetter = /[a-zA-Z]/.test(formData.password);
  const hasNumber = /\d/.test(formData.password);
  if (!hasLetter || !hasNumber) {
    validationErrors.password = 'Password should contain both letters and numbers';
    return false;
  }
  return true;
};

const validateConfirmPassword = () => {
  validationErrors.confirmPassword = '';
  if (!formData.password && formData.confirmPassword) {
    validationErrors.confirmPassword = 'Please enter password first';
    return false;
  }
  if (formData.password && formData.confirmPassword !== formData.password) {
    validationErrors.confirmPassword = 'Passwords do not match';
    return false;
  }
  return true;
};

const validateForm = () => {
  let isValid = true;
  Object.keys(validationErrors).forEach(key => validationErrors[key] = '');
  if (!validateUsername()) isValid = false;
  if (!validateAge()) isValid = false;
  if (!validateGender()) isValid = false;
  if (!validatePassword()) isValid = false;
  if (!validateConfirmPassword()) isValid = false;
  return isValid;
};

// Input Handlers
const onUsernameInput = () => validateUsername();
const onAgeInput = () => validateAge();
const onGenderChange = () => validateGender();
const onPasswordInput = () => {
  validatePassword();
  if (formData.confirmPassword) validateConfirmPassword();
};
const onConfirmPasswordInput = () => validateConfirmPassword();
const hasValidationErrors = () => Object.values(validationErrors).some(error => error !== '');

// --- INITIALIZATION ---
onMounted(() => {
  // 1. Init Animations
  AOS.init({
    duration: 800,
    once: true,
  });

  // 2. Load Data (THIS WAS MISSING)
  fetchUserProfile();
});
</script>

<template>
  <div class="profile-page">
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading profile...</p>
    </div>

    <div v-else class="profile-container">
      <div class="profile-header" data-aos="fade-in">
        <div class="header-content">
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <img
                :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(user.username || 'User')}&background=667eea&color=fff`"
                :alt="user.username || 'User'" class="profile-avatar" />
            </div>
          </div>

          <div class="user-info">
            <h1>{{ user.username || 'User' }}</h1>
            <p class="user-email">{{ user.email || 'No email' }}</p>
            <div class="user-meta">
              <span v-if="user.age" class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                {{ user.age }} years old
              </span>
              <span v-if="user.gender" class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                {{ getGenderText(user.gender) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="profile-content" data-aos="fade-up">
        <div class="profile-card">
          <div class="card-header">
            <h2>Edit Profile</h2>
            <p>Update your personal information</p>
          </div>

          <div v-if="successMessage" class="alert alert-success">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            {{ successMessage }}
          </div>

          <div v-if="errorMessage" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            {{ errorMessage }}
          </div>

          <form @submit.prevent="handleSubmit" class="profile-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="username">Username <span class="required">*</span></label>
                <input id="username" v-model="formData.username" @input="onUsernameInput" @blur="validateUsername"
                  type="text" placeholder="Enter username" :class="{ 'error': validationErrors.username }" />
                <div v-if="validationErrors.username" class="validation-error">
                  {{ validationErrors.username }}
                </div>
                <small class="hint">3-50 characters, letters, numbers, and underscores only</small>
              </div>

              <div class="form-group">
                <label for="email">Email Address</label>
                <input id="email" :value="user.email" type="email" placeholder="Email" disabled />
                <small class="hint">Email cannot be changed</small>
              </div>

              <div class="form-group">
                <label for="age">Age</label>
                <input id="age" v-model="formData.age" @input="onAgeInput" @blur="validateAge" type="number" min="1"
                  max="120" placeholder="Enter age" :class="{ 'error': validationErrors.age }" />
                <div v-if="validationErrors.age" class="validation-error">
                  {{ validationErrors.age }}
                </div>
                <small class="hint">Optional, between 1-120</small>
              </div>

              <div class="form-group">
                <label for="gender">Gender</label>
                <select id="gender" v-model="formData.gender" @change="onGenderChange" class="form-select"
                  :class="{ 'error': validationErrors.gender }">
                  <option value="">Select Gender</option>
                  <option value="1">Male</option>
                  <option value="2">Female</option>
                  <option value="3">Other</option>
                  <option value="0">Prefer not to say</option>
                </select>
                <div v-if="validationErrors.gender" class="validation-error">
                  {{ validationErrors.gender }}
                </div>
              </div>

              <div class="form-group full-width">
                <label for="password">Change Password</label>
                <div class="password-input-wrapper">
                  <input id="password" v-model="formData.password" @input="onPasswordInput" @blur="validatePassword"
                    :type="showPassword ? 'text' : 'password'" placeholder="Enter new password"
                    :class="{ 'error': validationErrors.password }" />
                  <button type="button" @click="showPassword = !showPassword" class="password-toggle"
                    :class="{ 'active': showPassword }">
                    {{ showPassword ? 'Hide' : 'Show' }}
                  </button>
                </div>
                <div v-if="validationErrors.password" class="validation-error">
                  {{ validationErrors.password }}
                </div>
                <small class="hint">Optional, at least 6 characters with letters and numbers</small>
              </div>

              <div class="form-group full-width" v-if="formData.password">
                <label for="confirmPassword">Confirm Password</label>
                <div class="password-input-wrapper">
                  <input id="confirmPassword" v-model="formData.confirmPassword" @input="onConfirmPasswordInput"
                    @blur="validateConfirmPassword" :type="showConfirmPassword ? 'text' : 'password'"
                    placeholder="Confirm new password" :class="{ 'error': validationErrors.confirmPassword }" />
                  <button type="button" @click="showConfirmPassword = !showConfirmPassword" class="password-toggle"
                    :class="{ 'active': showConfirmPassword }">
                    {{ showConfirmPassword ? 'Hide' : 'Show' }}
                  </button>
                </div>
                <div v-if="validationErrors.confirmPassword" class="validation-error">
                  {{ validationErrors.confirmPassword }}
                </div>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" :disabled="isSaving || hasValidationErrors()" class="save-btn" :class="{
                'loading': isSaving,
                'disabled': hasValidationErrors()
              }">
                <span v-if="isSaving" class="btn-loading">
                  <span class="spinner-small"></span>
                  Saving...
                </span>
                <span v-else>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                    <polyline points="17 21 17 13 7 13 7 21"></polyline>
                    <polyline points="7 3 7 8 15 8"></polyline>
                  </svg>
                  Save Changes
                </span>
              </button>

              <button type="button" @click="handleLogout" class="logout-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Logout
              </button>
            </div>
          </form>
        </div>

        <div class="info-card" data-aos="fade-up" data-aos-delay="200">
          <div class="card-header">
            <h2>Account Information</h2>
          </div>
          <div class="account-info">
            <div class="info-item">
              <span class="info-label">Email:</span>
              <span class="info-value">{{ user.email || 'No email' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Account Status:</span>
              <span class="status-badge active">Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  gap: 20px;
}

.loading-overlay .spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-radius: 50%;
  border-top-color: #667eea;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 40px;
  margin-bottom: 30px;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 40px;
}

.avatar-wrapper {
  position: relative;
}

.profile-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
  background: white;
}

.user-info h1 {
  font-size: 32px;
  margin-bottom: 5px;
}

.user-email {
  opacity: 0.9;
  margin-bottom: 15px;
  font-size: 18px;
}

.user-meta {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  opacity: 0.9;
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 12px;
  border-radius: 20px;
}

.profile-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.profile-card,
.info-card {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.card-header {
  margin-bottom: 30px;
}

.card-header h2 {
  color: #2d3748;
  margin-bottom: 5px;
  font-size: 24px;
}

.card-header p {
  color: #718096;
  font-size: 14px;
}

.alert {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.alert-success {
  background: #f0fff4;
  color: #276749;
  border: 1px solid #c6f6d5;
}

.alert-error {
  background: #fff5f5;
  color: #c53030;
  border: 1px solid #fed7d7;
}

.profile-form {
  margin-top: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #4a5568;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled {
  background: #f8fafc;
  cursor: not-allowed;
}

.password-input-wrapper {
  position: relative;
}

.password-input-wrapper input {
  padding-right: 70px;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%234a5568' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
  padding-right: 40px;
}

.hint {
  display: block;
  margin-top: 5px;
  color: #a0aec0;
  font-size: 12px;
}

.form-actions {
  display: flex;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.save-btn,
.logout-btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.save-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  flex: 2;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.save-btn.loading {
  opacity: 0.7;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

.logout-btn {
  background: #fff5f5;
  color: #c53030;
  border: 2px solid #fed7d7;
  flex: 1;
}

.logout-btn:hover {
  background: #fed7d7;
}

.account-info {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e2e8f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #718096;
  font-size: 14px;
}

.info-value {
  color: #2d3748;
  font-weight: 500;
  font-size: 14px;
  text-align: right;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: #c6f6d5;
  color: #276749;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }

  .profile-content {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .profile-avatar {
    width: 120px;
    height: 120px;
  }

  .required {
    color: #c53030;
  }

  .validation-error {
    color: #c53030;
    font-size: 12px;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .validation-error::before {
    content: "⚠ ";
  }

  input.error,
  select.error,
  textarea.error {
    border-color: #c53030 !important;
    background-color: #fff5f5;
  }

  input.error:focus,
  select.error:focus,
  textarea.error:focus {
    box-shadow: 0 0 0 3px rgba(197, 48, 48, 0.1) !important;
  }

  .save-btn.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .save-btn.disabled:hover {
    transform: none !important;
    box-shadow: none !important;
  }
}
</style>