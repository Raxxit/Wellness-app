<template>
  <div class="profile-page">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading your profile...</p>
    </div>

    <!-- Not Logged In State -->
    <div v-else-if="!isAuthenticated" class="not-logged-in">
      <div class="lock-icon">🔒</div>
      <h2>Authentication Required</h2>
      <p>You need to be logged in to view your profile.</p>
      <button @click="redirectToLogin" class="login-button">
        Go to Login
      </button>
    </div>

    <!-- Profile Content (only shown when logged in) -->
    <div v-else class="profile-container">
      <!-- Header -->
      <div class="profile-header wow fadeIn">
        <div class="header-content">
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <img 
                :src="profileImage" 
                alt="Profile Picture" 
                class="profile-avatar"
              />
              <input 
                type="file" 
                ref="fileInput" 
                @change="onImageChange" 
                accept="image/*"
                class="file-input"
                hidden
              />
              <button @click="triggerFileInput" class="change-photo-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                Change Photo
              </button>
            </div>
          </div>
          
          <div class="user-info">
            <h1>{{ fullName }}</h1>
            <p class="user-email">{{ user.email }}</p>
            <div class="user-meta">
              <span v-if="user.age" class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                {{ user.age }} years old
              </span>
              <span v-if="user.gender" class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                {{ user.gender === 1 ? 'Male' : user.gender === 2 ? 'Female' : 'Other' }}
              </span>
              <span class="meta-item">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="3" y1="9" x2="21" y2="9"></line>
                  <line x1="9" y1="21" x2="9" y2="9"></line>
                </svg>
                Member since {{ joinDate }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Edit Form -->
      <div class="profile-content wow fadeInUp">
        <div class="profile-card">
          <div class="card-header">
            <h2>Edit Profile</h2>
            <p>Update your personal information</p>
          </div>

          <!-- Success/Error Messages -->
          <div v-if="successMessage" class="alert alert-success">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            {{ successMessage }}
          </div>

          <div v-if="errorMessage" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            {{ errorMessage }}
          </div>

          <div v-if="imageError" class="alert alert-warning">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            {{ imageError }}
          </div>

          <form @submit.prevent="handleSubmit" class="profile-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="firstName">First Name</label>
                <input 
                  id="firstName" 
                  v-model="profile.firstName" 
                  type="text" 
                  placeholder="Enter first name"
                  required
                />
              </div>

              <div class="form-group">
                <label for="lastName">Last Name</label>
                <input 
                  id="lastName" 
                  v-model="profile.lastName" 
                  type="text" 
                  placeholder="Enter last name"
                  required
                />
              </div>

              <div class="form-group">
                <label for="email">Email Address</label>
                <input 
                  id="email" 
                  v-model="profile.email" 
                  type="email" 
                  placeholder="Enter email"
                  required
                  disabled
                />
                <small class="hint">Email cannot be changed</small>
              </div>

              <div class="form-group">
                <label for="phone">Phone Number</label>
                <input 
                  id="phone" 
                  v-model="profile.phone" 
                  type="tel" 
                  placeholder="Enter phone number"
                />
              </div>

              <div class="form-group">
                <label for="city">City</label>
                <input 
                  id="city" 
                  v-model="profile.city" 
                  type="text" 
                  placeholder="Enter your city"
                />
              </div>

              <div class="form-group full-width">
                <label for="bio">Bio</label>
                <textarea 
                  id="bio" 
                  v-model="profile.bio" 
                  placeholder="Tell us about yourself..."
                  rows="4"
                ></textarea>
              </div>
            </div>

            <div class="form-actions">
              <button 
                type="submit" 
                :disabled="isSaving" 
                class="save-btn"
                :class="{ 'loading': isSaving }"
              >
                <span v-if="isSaving" class="btn-loading">
                  <span class="spinner-small"></span>
                  Saving...
                </span>
                <span v-else>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                    <polyline points="17 21 17 13 7 13 7 21"></polyline>
                    <polyline points="7 3 7 8 15 8"></polyline>
                  </svg>
                  Save Changes
                </span>
              </button>

              <button 
                type="button" 
                @click="handleLogout" 
                class="logout-btn"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Logout
              </button>
            </div>
          </form>
        </div>

        <!-- Session Info Card -->
        <div class="session-card wow fadeInUp" data-wow-delay="0.2s">
          <div class="card-header">
            <h2>Session Information</h2>
          </div>
          <div class="session-info">
            <div class="info-item">
              <span class="info-label">Logged in as:</span>
              <span class="info-value">{{ user.username || user.email }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">User ID:</span>
              <span class="info-value">{{ user.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Session Started:</span>
              <span class="info-value">{{ sessionStartTime }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Status:</span>
              <span class="status-badge active">Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { WOW } from "wowjs";
import axios from "axios";
import "wowjs/css/libs/animate.css";

const router = useRouter();

const user = ref({
  id: null,
  username: "",
  email: "",
  age: null,
  gender: null
});

const isAuthenticated = ref(false);
const isLoading = ref(true);

const profile = ref({
  firstName: "",
  lastName: "",
  email: "",
  phone: "",
  city: "",
  bio: "",
});

const profileImage = ref("/profile-placeholder.webp");
const imageError = ref("");
const fileInput = ref(null);
const isSaving = ref(false);
const successMessage = ref("");
const errorMessage = ref("");
const sessionStartTime = ref("");
const fullName = computed(() => {
  return `${profile.value.firstName} ${profile.value.lastName}`.trim() || user.value.username;
});

const joinDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
});

onMounted(async () => {
  await checkAuth();
  new WOW({ mobile: false }).init();
});

const checkAuth = async () => {
  try {
    const token = localStorage.getItem('token');
    
    if (!token) {
      isAuthenticated.value = false;
      isLoading.value = false;
      return;
    }

    const response = await axios.get('http://127.0.0.1:5000/api/profile', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.data.success) {
      user.value = response.data.user;
      isAuthenticated.value = true;
      profile.value.email = user.value.email;
      
      sessionStartTime.value = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      });
    } else {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      isAuthenticated.value = false;
    }
  } catch (error) {
    console.error("Auth check failed:", error);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    isAuthenticated.value = false;
  } finally {
    isLoading.value = false;
  }
};

const redirectToLogin = () => {
  router.push('/login');
};

const onImageChange = (event) => {
  const file = event.target.files[0];
  imageError.value = "";

  if (!file) return;

  if (!file.type.startsWith("image/")) {
    imageError.value = "Please upload a valid image file.";
    return;
  }

  if (file.size > 2 * 1024 * 1024) {
    imageError.value = "Image must be under 2MB.";
    return;
  }

  profileImage.value = URL.createObjectURL(file);
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleSubmit = async () => {
  isSaving.value = true;
  successMessage.value = "";
  errorMessage.value = "";

  try {
    const token = localStorage.getItem('token');
    const data = new FormData();
    
    Object.entries(profile.value).forEach(([key, value]) => {
      data.append(key, value);
    });

    await axios.post(
      'http://127.0.0.1:5000/api/update-profile',
      data,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );

    successMessage.value = "Profile updated successfully.";
    
    setTimeout(() => {
      successMessage.value = "";
    }, 3000);
    
  } catch (error) {
    console.error(error);
    errorMessage.value = "Something went wrong while updating your profile.";
    
    if (error.response && error.response.status === 401) {
      errorMessage.value = "Session expired. Please login again.";
      setTimeout(() => {
        handleLogout();
      }, 2000);
    }
  } finally {
    isSaving.value = false;
  }
};

const handleLogout = async () => {
  try {
    const token = localStorage.getItem('token');
    
    if (token) {
      await axios.post('http://127.0.0.1:5000/api/logout', {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
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
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

/* Loading State */
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

/* Not Logged In State */
.not-logged-in {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 40px auto;
}

.not-logged-in .lock-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.not-logged-in h2 {
  color: #2d3748;
  margin-bottom: 10px;
}

.not-logged-in p {
  color: #718096;
  margin-bottom: 30px;
}

.login-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

/* Profile Container */
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
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
}

.change-photo-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  color: #667eea;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s;
}

.change-photo-btn:hover {
  background: #f8fafc;
  transform: translateY(-2px);
}

.user-info h1 {
  font-size: 32px;
  margin-bottom: 5px;
}

.user-email {
  opacity: 0.9;
  margin-bottom: 15px;
}

.user-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  opacity: 0.9;
}

/* Profile Content */
.profile-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.profile-card, .session-card {
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
}

.card-header p {
  color: #718096;
}

/* Alerts */
.alert {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
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

.alert-warning {
  background: #fffaf0;
  color: #c05621;
  border: 1px solid #feebc8;
}

/* Form */
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
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled {
  background: #f8fafc;
  cursor: not-allowed;
}

.hint {
  display: block;
  margin-top: 5px;
  color: #a0aec0;
  font-size: 12px;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.save-btn, .logout-btn {
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
}

.logout-btn:hover {
  background: #fed7d7;
}

/* Session Card */
.session-info {
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

/* Animations */
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
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
}
</style>