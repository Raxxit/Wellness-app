<script setup>
import { ref, onMounted } from "vue";
import { WOW } from "wowjs";
import axios from "axios";

// Profile data
const profile = ref({
  firstName: "",
  lastName: "",
  email: "",
  phone: "",
  city: "",
  bio: "",
});

// Profile picture and errors
const profileImage = ref("/profile-placeholder.webp");
const imageError = ref("");

// Loading & feedback states
const isSaving = ref(false);
const successMessage = ref("");
const errorMessage = ref("");

// Handle profile image change
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

// Form submission
const handleSubmit = async () => {
  isSaving.value = true;
  successMessage.value = "";
  errorMessage.value = "";

  try {
    const data = new FormData();
    Object.entries(profile.value).forEach(([key, value]) => {
      data.append(key, value);
    });

    await axios.post(
      import.meta.env.VITE_API_BASE_URL + "/api/update-profile",
      data
    );

    successMessage.value = "Profile updated successfully.";
  } catch (error) {
    console.error(error);
    errorMessage.value = "Something went wrong while updating your profile.";
  } finally {
    isSaving.value = false;
  }
};

// Initialize WOW.js
onMounted(() => {
  new WOW({ mobile: false }).init();
});
</script>

<template>
  <div class="edit-profile-page">
    <!-- Header -->
    <header class="page-header">
      <div class="container text-center">
        <h1 class="wow fadeInUp">Edit Profile</h1>
        <p class="wow fadeInUp" data-wow-delay="0.1s">
          Keep your information accurate and up to date
        </p>
      </div>
    </header>

    <!-- Profile Section -->
    <section class="py-5">
      <div class="container">
        <div class="row g-4 align-items-start">
          <!-- Profile Picture -->
          <div
            class="col-12 col-md-4 wow fadeInLeft d-flex justify-content-center"
          >
            <div class="card profile-card text-center p-4">
              <img
                :src="profileImage"
                alt="User profile picture"
                class="avatar"
              />

              <label class="btn btn-outline-primary mt-3">
                <i class="fa fa-camera me-2"></i>Change Photo
                <input
                  type="file"
                  hidden
                  accept="image/*"
                  @change="onImageChange"
                />
              </label>

              <small v-if="imageError" class="text-danger d-block mt-2">
                {{ imageError }}
              </small>
              <small v-else class="text-muted d-block mt-2">
                JPG / PNG / WEBP · Max 2MB
              </small>
            </div>
          </div>

          <!-- Profile Form -->
          <div
            class="col-12 col-md-8 wow fadeInRight d-flex justify-content-center"
          >
            <div class="card profile-form-card w-100">
              <div class="card-body p-4 p-md-5">
                <h2>Personal Information</h2>
                <p class="text-muted mb-4">
                  This information will be visible on your profile
                </p>

                <form @submit.prevent="handleSubmit">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">First Name</label>
                      <input
                        class="form-control"
                        v-model="profile.firstName"
                        required
                      />
                    </div>

                    <div class="col-md-6 mb-3">
                      <label class="form-label">Last Name</label>
                      <input
                        class="form-control"
                        v-model="profile.lastName"
                        required
                      />
                    </div>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input
                      type="email"
                      class="form-control"
                      v-model="profile.email"
                      required
                    />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input class="form-control" v-model="profile.phone" />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">City</label>
                    <input class="form-control" v-model="profile.city" />
                  </div>

                  <div class="mb-4">
                    <label class="form-label">About You</label>
                    <textarea
                      class="form-control"
                      rows="4"
                      v-model="profile.bio"
                    ></textarea>
                  </div>

                  <!-- Feedback -->
                  <p v-if="successMessage" class="text-success">
                    {{ successMessage }}
                  </p>
                  <p v-if="errorMessage" class="text-danger">
                    {{ errorMessage }}
                  </p>

                  <button
                    type="submit"
                    class="btn btn-primary w-100"
                    :disabled="isSaving"
                  >
                    <span v-if="isSaving">Saving...</span>
                    <span v-else>Save Changes</span>
                  </button>
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
.edit-profile-page {
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  background: white;
  border-bottom: 1px solid #e5e5e5;
  padding: 4rem 0;
  text-align: center;
}

.page-header h1 {
  font-weight: 700;
  font-size: 2.5rem;
  color: #0d6efd;
}

.page-header p {
  color: #6c757d;
  font-size: 1.1rem;
  margin-top: 0.5rem;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #dee2e6;
}

.profile-card,
.profile-form-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.profile-form-card {
  max-width: 100%;
}

.form-control {
  border-radius: 8px;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.15);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-primary {
  border-radius: 50px;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(13, 110, 253, 0.3);
}
</style>
