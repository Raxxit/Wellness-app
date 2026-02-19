<script setup>
import { ref, onMounted } from 'vue';

const pendingUsers = ref([]);
const selectedUser = ref(null);
const isLoading = ref(false);
const message = ref(null);

const fetchPending = async () => {
    try {
        const token = localStorage.getItem('token');
        const res = await fetch('/api/admin/pending-advisors', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            pendingUsers.value = await res.json();
            if (pendingUsers.value.length > 0) selectedUser.value = pendingUsers.value[0];
            else selectedUser.value = null;
        }
    } catch (e) {
        console.error("Failed to load users", e);
    }
};

const processVerification = async (userId, action) => {
    if (!confirm(`Are you sure you want to ${action} this user?`)) return;

    isLoading.value = true;
    try {
        const token = localStorage.getItem('token');
        const res = await fetch(`/api/admin/verify-user/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ action })
        });

        const data = await res.json();

        if (res.ok) {
            message.value = { type: 'success', text: data.message };
            pendingUsers.value = pendingUsers.value.filter(u => u.user_id !== userId);
            selectedUser.value = pendingUsers.value[0] || null;
        } else {
            message.value = { type: 'error', text: data.message };
        }
    } catch (e) {
        message.value = { type: 'error', text: "Server error occurred." };
    } finally {
        isLoading.value = false;
        setTimeout(() => message.value = null, 3000);
    }
};

const getDocUrl = (filename) => {
    // Uses the secure route we created
    return `/api/admin/document/${filename}`;
};

onMounted(fetchPending);
</script>

<template>
    <div class="container-fluid py-4">
        <h2 class="mb-4 fw-bold text-primary"><i class="fa fa-shield-alt me-2"></i>Professional Verification</h2>

        <div v-if="message" :class="`alert alert-${message.type === 'error' ? 'danger' : 'success'}`">
            {{ message.text }}
        </div>

        <div v-if="pendingUsers.length === 0" class="text-center py-5 text-muted">
            <i class="fa fa-check-circle fa-3x mb-3"></i>
            <h4>All Caught Up!</h4>
            <p>No pending professional applications.</p>
        </div>

        <div v-else class="row g-4">
            <div class="col-md-4">
                <div class="list-group shadow-sm">
                    <button v-for="user in pendingUsers" :key="user.user_id"
                        class="list-group-item list-group-item-action d-flex justify-content-between align-items-center p-3"
                        :class="{ 'active': selectedUser?.user_id === user.user_id }" @click="selectedUser = user">
                        <div>
                            <div class="fw-bold">{{ user.user_name }}</div>
                            <small :class="selectedUser?.user_id === user.user_id ? 'text-light' : 'text-muted'">
                                {{ user.email }}
                            </small>
                        </div>
                        <span class="badge bg-warning text-dark">Pending</span>
                    </button>
                </div>
            </div>

            <div class="col-md-8">
                <div v-if="selectedUser" class="card shadow border-0">
                    <div class="card-header bg-white p-4 border-bottom">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h3 class="fw-bold mb-1">{{ selectedUser.user_name }}</h3>
                                <p class="text-muted mb-0">Registered: {{ selectedUser.created_at }}</p>
                            </div>
                            <div class="text-end">
                                <span class="badge bg-info me-2">{{ selectedUser.gender }}</span>
                                <span class="badge bg-secondary">Age: {{ selectedUser.age }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-body p-4">
                        <h5 class="fw-bold text-primary mb-3">Professional Bio</h5>
                        <div class="p-3 bg-light rounded mb-4 border">
                            {{ selectedUser.bio || 'No bio provided.' }}
                        </div>

                        <h5 class="fw-bold text-primary mb-3">Credentials</h5>
                        <div class="mb-4">
                            <div v-if="selectedUser.related_docs">
                                <a :href="getDocUrl(selectedUser.related_docs)" target="_blank"
                                    class="btn btn-outline-dark w-100 py-3 dashed-border">
                                    <i class="fa fa-file-pdf me-2 text-danger"></i>
                                    View Submitted Document ({{ selectedUser.related_docs }})
                                </a>
                            </div>
                            <div v-else class="text-danger">
                                <i class="fa fa-exclamation-triangle"></i> No documents uploaded.
                            </div>
                        </div>

                        <hr class="my-4">

                        <div class="d-flex gap-3 justify-content-end">
                            <button @click="processVerification(selectedUser.user_id, 'reject')" :disabled="isLoading"
                                class="btn btn-outline-danger px-4">
                                <i class="fa fa-times me-2"></i> Reject & Downgrade
                            </button>
                            <button @click="processVerification(selectedUser.user_id, 'approve')" :disabled="isLoading"
                                class="btn btn-success px-5">
                                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                                <i v-else class="fa fa-check me-2"></i> Approve Advisor Status
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dashed-border {
    border-style: dashed;
    border-width: 2px;
    transition: all 0.2s;
}

.dashed-border:hover {
    background-color: #f8f9fa;
    border-color: #0d6efd;
    color: #0d6efd;
}

.list-group-item.active {
    background-color: #0d6efd;
    border-color: #0d6efd;
}
</style>