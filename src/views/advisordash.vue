<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
const router = useRouter();

const dashboardData = ref(null);
const isLoading = ref(true);
const error = ref(null);

const showModal = ref(false);
const selectedAppt = ref(null);
const modalLoading = ref(false);

const editForm = reactive({
    id: null,
    status: '',
    date: '',
    time: '',
    notes: ''
});

const minDate = computed(() => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
});

// --- Fetch Data ---
const fetchDashboard = async () => {
    try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/advisor/dashboard', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        dashboardData.value = res.data;
    } catch (e) {
        console.error(e);
        error.value = "Could not load dashboard data.";
    } finally {
        isLoading.value = false;
    }
};

// --- Modal Actions ---
const openDetails = (appt) => {
    selectedAppt.value = appt;
    editForm.id = appt.id;
    editForm.status = appt.status;
    editForm.date = appt.date;
    editForm.time = appt.time;
    editForm.notes = appt.notes;
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    selectedAppt.value = null;
};

const viewPatientHistory = (clientId) => {
    if (clientId) {
        router.push(`/advisor/patient/${clientId}`);
    }
};

// --- API Actions ---
const updateAppointment = async (action) => {
    modalLoading.value = true;
    const token = localStorage.getItem('token');

    let payload = {
        notes: editForm.notes,
        date: editForm.date,
        time: editForm.time
    };

    if (action === 'confirm') payload.status = 'Confirmed';
    else if (action === 'cancel') payload.status = 'Cancelled';
    else payload.status = editForm.status;

    try {
        await axios.post(`/api/advisor/appointment/${editForm.id}/update`, payload, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        await fetchDashboard();
        closeModal();
    } catch (e) {
        alert("Error updating appointment: " + e.message);
    } finally {
        modalLoading.value = false;
    }
};

onMounted(fetchDashboard);
</script>

<template>
    <div class="container-fluid py-4 bg-light min-vh-100">

        <div v-if="isLoading" class="d-flex flex-column align-items-center justify-content-center py-5"
            style="height: 60vh;">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;"></div>
            <p class="mt-3 text-muted fw-medium">Loading your practice dashboard...</p>
        </div>

        <div v-else-if="error" class="alert alert-danger shadow-sm mx-auto" style="max-width: 600px;">
            <i class="bi bi-exclamation-triangle-fill me-2"></i> {{ error }}
        </div>

        <div v-else class="container-xl">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h6 class="text-uppercase text-muted small fw-bold mb-1">Professional Portal</h6>
                    <h3 class="fw-bold text-dark mb-0">Advisor Dashboard</h3>
                </div>
                <button class="btn btn-primary shadow-sm px-4 rounded-pill">
                    <i class="bi bi-clock-history me-2"></i> Update Availability
                </button>
            </div>

            <div class="row g-4 mb-4">
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm h-100 text-center py-2 stat-card">
                        <div class="card-body">
                            <h6 class="text-muted text-uppercase small fw-bold ls-1">Total Clients</h6>
                            <h2 class="fw-bold mb-0 text-primary display-5">{{ dashboardData.stats.total_clients }}</h2>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card border-0 shadow-sm h-100 text-center py-2 stat-card">
                        <div class="card-body">
                            <h6 class="text-muted text-uppercase small fw-bold ls-1">Upcoming Sessions</h6>
                            <h2 class="fw-bold mb-0 text-success display-5">{{ dashboardData.stats.upcoming_sessions }}
                            </h2>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row g-4">
                <div class="col-lg-8">
                    <div class="card shadow-sm border-0 h-100 overflow-hidden">
                        <div
                            class="card-header bg-white py-3 px-4 d-flex justify-content-between align-items-center border-bottom">
                            <h5 class="fw-bold mb-0 text-dark">
                                <i class="bi bi-calendar-week me-2 text-primary"></i>Appointments
                            </h5>
                            <span class="badge bg-light text-dark border rounded-pill px-3">
                                {{ dashboardData.appointments.length }} Total
                            </span>
                        </div>

                        <div class="card-body p-0">
                            <div v-if="dashboardData.appointments.length === 0" class="text-center py-5 text-muted">
                                <div class="bg-light rounded-circle d-inline-flex p-4 mb-3">
                                    <i class="bi bi-calendar-check display-6 text-secondary opacity-50"></i>
                                </div>
                                <p class="fw-medium mb-0">No appointments scheduled.</p>
                                <small>Enjoy your free time!</small>
                            </div>

                            <div v-else class="list-group list-group-flush">
                                <div v-for="appt in dashboardData.appointments" :key="appt.id"
                                    class="list-group-item p-4 d-flex align-items-center hover-bg transition-all border-bottom-0 border-top">

                                    <div class="rounded-circle bg-primary-subtle d-flex align-items-center justify-content-center me-4 text-primary fw-bold shadow-sm"
                                        style="width: 50px; height: 50px; font-size: 1.25rem;">
                                        {{ appt.avatar }}
                                    </div>

                                    <div class="flex-grow-1">
                                        <div class="d-flex justify-content-between align-items-center mb-1">
                                            <h6 class="fw-bold mb-0 text-dark fs-5">{{ appt.client_name }}</h6>
                                            <span class="badge rounded-pill px-3 py-2" :class="{
                                                'bg-success-subtle text-success border border-success-subtle': appt.status === 'Confirmed',
                                                'bg-warning-subtle text-warning-emphasis border border-warning-subtle': appt.status === 'Pending',
                                                'bg-danger-subtle text-danger border border-danger-subtle': appt.status === 'Cancelled'
                                            }">
                                                <i class="bi me-1" :class="{
                                                    'bi-check-circle-fill': appt.status === 'Confirmed',
                                                    'bi-clock-fill': appt.status === 'Pending',
                                                    'bi-x-circle-fill': appt.status === 'Cancelled'
                                                }"></i>
                                                {{ appt.status }}
                                            </span>
                                        </div>
                                        <div class="text-muted small d-flex align-items-center">
                                            <span class="me-3"><i class="bi bi-calendar-event me-1"></i> {{ appt.date
                                                }}</span>
                                            <span><i class="bi bi-clock me-1"></i> {{ appt.time }}</span>
                                        </div>
                                    </div>

                                    <div class="d-flex flex-column gap-2 ms-4">
                                        <button @click="openDetails(appt)"
                                            class="btn btn-outline-secondary btn-sm px-3 rounded-pill"
                                            style="min-width: 100px;">
                                            Manage
                                        </button>
                                        <button @click="viewPatientHistory(appt.client_id)"
                                            class="btn btn-primary btn-sm px-3 rounded-pill border-0"
                                            style="min-width: 100px; background-color: #eef2ff; color: #4f46e5;">
                                            Reports
                                        </button>
                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-lg-4">
                    <div class="card shadow-sm border-0 bg-dark text-white mb-4 overflow-hidden position-relative">
                        <div class="position-absolute top-0 end-0 p-5 bg-white opacity-10 rounded-circle"
                            style="margin-top: -30px; margin-right: -30px;"></div>
                        <div class="card-body p-4 position-relative">
                            <h5 class="fw-bold mb-1">Welcome, {{ dashboardData.advisor_name }}</h5>
                            <p class="small opacity-75 mb-0">You are making a difference today.</p>
                        </div>
                    </div>

                    <div class="card shadow-sm border-0">
                        <div class="card-header bg-white py-3 border-bottom fw-bold">
                            Quick Actions
                        </div>
                        <div class="list-group list-group-flush">
                            <button
                                class="list-group-item list-group-item-action py-3 d-flex align-items-center text-muted">
                                <i class="bi bi-person-gear me-3 fs-5"></i> Edit Profile Bio
                            </button>
                            <button
                                class="list-group-item list-group-item-action py-3 d-flex align-items-center text-muted">
                                <i class="bi bi-gear me-3 fs-5"></i> Account Settings
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="showModal" class="modal-backdrop-custom d-flex align-items-center justify-content-center">
            <div class="card shadow-lg border-0 rounded-4 overflow-hidden modal-card">
                <div
                    class="card-header bg-white py-3 px-4 d-flex justify-content-between align-items-center border-bottom">
                    <h5 class="mb-0 fw-bold text-dark">Manage Appointment</h5>
                    <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                </div>
                <div class="card-body p-4">
                    <div class="d-flex align-items-center mb-4 p-3 bg-light rounded-3">
                        <div class="rounded-circle bg-white d-flex align-items-center justify-content-center me-3 text-dark fw-bold border shadow-sm"
                            style="width: 48px; height: 48px; font-size: 1.2rem;">
                            {{ selectedAppt.avatar }}
                        </div>
                        <div>
                            <h5 class="mb-0 fw-bold">{{ selectedAppt.client_name }}</h5>
                            <div class="text-muted small">
                                Status: <span class="fw-bold"
                                    :class="{ 'text-success': selectedAppt.status === 'Confirmed', 'text-warning': selectedAppt.status === 'Pending', 'text-danger': selectedAppt.status === 'Cancelled' }">{{
                                    selectedAppt.status }}</span>
                            </div>
                        </div>
                    </div>
                    <form @submit.prevent>
                        <div class="mb-4">
                            <label class="form-label fw-bold small text-uppercase text-secondary ls-1 mb-2">Reschedule
                                Session</label>
                            <div class="row g-2">
                                <div class="col-6">
                                    <input type="date" class="form-control" v-model="editForm.date" :min="minDate">
                                </div>
                                <div class="col-6">
                                    <input type="time" class="form-control" v-model="editForm.time">
                                </div>
                            </div>
                            <div class="form-text small text-muted mt-1"><i class="bi bi-info-circle me-1"></i>Changing
                                these updates the booking time.</div>
                        </div>
                        <div class="mb-4">
                            <label class="form-label fw-bold small text-uppercase text-secondary ls-1 mb-2">Private
                                Notes</label>
                            <textarea class="form-control bg-light border-0" rows="4" v-model="editForm.notes"
                                placeholder="Add clinical notes or session details here..."></textarea>
                        </div>
                        <div class="d-flex justify-content-between align-items-center pt-3 border-top mt-3">
                            <button @click="updateAppointment('cancel')" class="btn btn-outline-danger btn-sm px-3"
                                :disabled="modalLoading">
                                <i class="bi bi-x-lg me-1"></i> Cancel Appt
                            </button>
                            <div class="d-flex gap-2">
                                <button @click="updateAppointment('save')" class="btn btn-light border fw-medium"
                                    :disabled="modalLoading">Save Changes</button>
                                <button v-if="editForm.status === 'Pending'" @click="updateAppointment('confirm')"
                                    class="btn btn-success text-white px-4 fw-medium shadow-sm"
                                    :disabled="modalLoading">
                                    <i class="bi bi-check-lg me-1"></i> Confirm
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.ls-1 {
    letter-spacing: 0.5px;
}

.stat-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .08) !important;
}

.hover-bg {
    transition: background-color 0.2s;
}

.hover-bg:hover {
    background-color: #f8f9fa;
}

.modal-backdrop-custom {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1050;
    backdrop-filter: blur(4px);
    animation: fadeIn 0.2s ease-out;
}

.modal-card {
    width: 550px;
    max-width: 95%;
    animation: slideUp 0.3s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideUp {
    from {
        transform: translateY(20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.bg-success-subtle {
    background-color: #d1e7dd;
}

.bg-warning-subtle {
    background-color: #fff3cd;
}

.bg-danger-subtle {
    background-color: #f8d7da;
}
</style>