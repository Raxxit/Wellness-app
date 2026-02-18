<script setup>
import { ref, onMounted, computed, watch, reactive } from 'vue';
import { useRouter } from 'vue-router';
// --- AOS Imports ---
import AOS from "aos";
import "aos/dist/aos.css";
// --- Axios for API ---
import axios from 'axios';

// --- STATE ---
const userName = ref('User');
const dbStats = ref({ assessments: 0 });
const streak = ref(0);

// Appointment State
const appointments = ref([]);
const advisors = ref([]);

// Booking Modal State
const showBookingModal = ref(false);
const bookingLoading = ref(false);
const bookingMessage = ref(null);

// Details Modal State
const showDetailsModal = ref(false);
const selectedAppt = ref(null);

const newAppointment = reactive({
    advisor_id: '',
    date: '',
    time: '',
    notes: ''
});

// To-Do List State
const tasks = ref([]);
const newTaskInput = ref('');
const newPriority = ref('medium');

// --- COMPUTED LOGIC ---
const activitiesCompleted = computed(() => tasks.value.filter(t => t.completed).length);
const totalPoints = computed(() => activitiesCompleted.value * 50);
const progressPercent = computed(() => {
    if (tasks.value.length === 0) return 0;
    return Math.round((activitiesCompleted.value / tasks.value.length) * 100);
});
const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
});

// Calculate Today's Date in YYYY-MM-DD format for the Date Picker "min" attribute
const minDate = computed(() => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
});

// --- ACTIONS ---
const addTask = () => {
    if (!newTaskInput.value || newTaskInput.value.trim() === '') return;
    tasks.value.unshift({
        id: Date.now(),
        title: newTaskInput.value.trim(),
        priority: newPriority.value,
        completed: false
    });
    newTaskInput.value = '';
};

const removeTask = (id) => {
    tasks.value = tasks.value.filter(t => t.id !== id);
};

// --- APPOINTMENT ACTIONS ---
const fetchAppointments = async () => {
    try {
        const res = await axios.get('/api/appointments/my-appointments');
        appointments.value = res.data;
    } catch (e) { console.error("Error fetching appointments", e); }
};

const openBookingModal = async () => {
    showBookingModal.value = true;
    try {
        const res = await axios.get('/api/appointments/advisors');
        advisors.value = res.data;
    } catch (e) { console.error("Error fetching advisors", e); }
};

const openDetailsModal = (appt) => {
    selectedAppt.value = appt;
    showDetailsModal.value = true;
};

const submitBooking = async () => {
    bookingLoading.value = true;
    bookingMessage.value = null;
    try {
        const res = await axios.post('/api/appointments/book', newAppointment);
        if (res.data.success) {
            bookingMessage.value = { type: 'success', text: 'Request Sent!' };
            fetchAppointments(); // Refresh list

            // Reset Form
            newAppointment.advisor_id = '';
            newAppointment.date = '';
            newAppointment.time = '';
            newAppointment.notes = '';

            setTimeout(() => { showBookingModal.value = false; bookingMessage.value = null; }, 1500);
        }
    } catch (e) {
        bookingMessage.value = { type: 'error', text: 'Failed to book. Try again.' };
    } finally {
        bookingLoading.value = false;
    }
};

// --- INITIALIZATION ---
onMounted(async () => {
    AOS.init({ duration: 1000, once: true });

    const userStr = localStorage.getItem('user');
    if (userStr) userName.value = JSON.parse(userStr).username || 'User';

    const savedTasks = localStorage.getItem('userTasks');
    if (savedTasks) tasks.value = JSON.parse(savedTasks);
    else tasks.value = [
        { id: 1, title: 'Drink Water', priority: 'high', completed: false },
    ];

    const token = localStorage.getItem('token');
    if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        try {
            const res = await fetch('/api/dashboard-stats', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                dbStats.value.assessments = data.assessments_completed;
            }
        } catch (e) { console.error(e); }

        fetchAppointments();
    }
});

watch(tasks, (newVal) => {
    localStorage.setItem('userTasks', JSON.stringify(newVal));
}, { deep: true });
</script>

<template>
    <div class="dashboard-container d-flex flex-column">

        <header class="d-flex justify-content-between align-items-center px-4 py-3 bg-white border-bottom shadow-sm">
            <div>
                <h6 class="text-uppercase text-muted small fw-bold ls-1 mb-1">Wellness Journey</h6>
                <h2 class="fw-bold text-dark mb-0">Daily Overview</h2>
            </div>
            <div class="d-none d-sm-flex align-items-center bg-light rounded-pill px-3 py-2 border">
                <i class="bi bi-calendar3 text-primary me-2"></i>
                <span class="fw-semibold text-secondary small">{{ currentDate }}</span>
            </div>
        </header>

        <div class="container-fluid flex-grow-1 p-4 bg-light overflow-auto">
            <div class="row g-4">

                <div class="col-lg-5 d-flex flex-column gap-4" data-aos="fade-right">

                    <div class="row g-3">
                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100 stat-card">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Assessments</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-clipboard-data text-primary fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ dbStats.assessments }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100 stat-card">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Day Streak</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-fire text-warning fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ streak }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100 stat-card">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Activities</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-check-circle-fill text-success fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ activitiesCompleted }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100 stat-card">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Total Points</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-star-fill text-info fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ totalPoints }}</h2>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card border-0 shadow-sm h-100">
                        <div
                            class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
                            <h5 class="fw-bold mb-0 text-primary"><i class="bi bi-heart-pulse me-2"></i>Professional
                                Support</h5>
                            <button @click="openBookingModal" class="btn btn-sm btn-primary rounded-pill px-3">
                                <i class="bi bi-plus-lg me-1"></i> Book
                            </button>
                        </div>
                        <div class="card-body p-0">
                            <div v-if="appointments.length === 0" class="text-center py-4 text-muted">
                                <i class="bi bi-calendar-x fs-1 mb-2 opacity-50"></i>
                                <p class="small mb-0">No upcoming sessions.</p>
                            </div>
                            <div v-else class="list-group list-group-flush">
                                <div v-for="appt in appointments" :key="appt.id"
                                    class="list-group-item p-3 border-0 border-bottom">
                                    <div class="d-flex justify-content-between align-items-start">
                                        <div>
                                            <span class="fw-bold text-dark d-block">{{ appt.advisor_name }}</span>
                                            <div class="small text-muted mt-1">
                                                <i class="bi bi-clock me-1"></i> {{ appt.date }} @ {{ appt.time }}
                                            </div>
                                        </div>
                                        <div class="text-end">
                                            <span class="badge rounded-pill d-block mb-1" :class="{
                                                'bg-warning text-dark': appt.status === 'Pending',
                                                'bg-success': appt.status === 'Confirmed',
                                                'bg-danger': appt.status === 'Cancelled'
                                            }">
                                                {{ appt.status }}
                                            </span>
                                            <button class="btn btn-link btn-sm p-0 text-decoration-none small"
                                                @click="openDetailsModal(appt)">
                                                View Details
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

                <div class="col-lg-7" data-aos="fade-left">
                    <div class="card border-0 shadow-sm h-100 d-flex flex-column">
                        <div class="card-header bg-white border-bottom py-3 px-4">
                            <div class="d-flex justify-content-between align-items-center">
                                <h5 class="fw-bold mb-0">My Tasks & Goals</h5>
                                <span class="badge bg-light text-dark border">{{ tasks.length }} Pending</span>
                            </div>
                            <div class="progress mt-3" style="height: 6px;">
                                <div class="progress-bar bg-primary" :style="{ width: progressPercent + '%' }"></div>
                            </div>
                        </div>

                        <div class="card-body p-0 d-flex flex-column overflow-hidden">
                            <div class="p-4 bg-light border-bottom">
                                <div class="input-group">
                                    <input type="text" class="form-control border-0 shadow-none"
                                        placeholder="Add a new task..." v-model="newTaskInput" @keyup.enter="addTask">
                                    <select class="form-select border-0 shadow-none" style="max-width: 100px;"
                                        v-model="newPriority">
                                        <option value="high">High</option>
                                        <option value="medium">Med</option>
                                        <option value="low">Low</option>
                                    </select>
                                    <button type="button" class="btn btn-primary px-4" @click="addTask">
                                        <i class="bi bi-plus-lg"></i>
                                    </button>
                                </div>
                            </div>

                            <div class="flex-grow-1 overflow-auto p-3 custom-scrollbar" style="max-height: 400px;">
                                <div v-if="tasks.length === 0" class="text-center py-5 text-muted opacity-50">
                                    <i class="bi bi-clipboard2-check fs-1 mb-2"></i>
                                    <p>No tasks yet. Start your day!</p>
                                </div>
                                <div v-else class="list-group list-group-flush">
                                    <div v-for="task in tasks" :key="task.id"
                                        class="list-group-item border-0 border-bottom py-3 d-flex align-items-center task-row">
                                        <input class="form-check-input fs-5 me-3 rounded-circle" type="checkbox"
                                            v-model="task.completed" style="cursor: pointer;">
                                        <div class="flex-grow-1">
                                            <div class="fw-bold"
                                                :class="{ 'text-decoration-line-through text-muted': task.completed }">
                                                {{ task.title }}
                                            </div>
                                            <span class="badge rounded-pill" style="font-size: 0.65rem;"
                                                :class="{ 'bg-danger': task.priority === 'high', 'bg-warning text-dark': task.priority === 'medium', 'bg-secondary': task.priority === 'low' }">
                                                {{ task.priority.toUpperCase() }}
                                            </span>
                                        </div>
                                        <button class="btn btn-link text-danger p-2 opacity-0 delete-btn"
                                            @click="removeTask(task.id)">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div v-if="showBookingModal" class="modal-backdrop-custom d-flex align-items-center justify-content-center">
            <div class="card shadow-lg border-0" style="width: 500px; max-width: 90%;">
                <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Book a Session</h5>
                    <button type="button" class="btn-close btn-close-white" @click="showBookingModal = false"></button>
                </div>
                <div class="card-body p-4">
                    <div v-if="bookingMessage"
                        :class="`alert alert-${bookingMessage.type === 'error' ? 'danger' : 'success'}`">
                        {{ bookingMessage.text }}
                    </div>

                    <form @submit.prevent="submitBooking">
                        <div class="mb-3">
                            <label class="form-label fw-bold small text-muted">Select Advisor</label>
                            <select v-model="newAppointment.advisor_id" class="form-select" required>
                                <option value="" disabled>Choose a professional...</option>
                                <option v-for="adv in advisors" :key="adv.id" :value="adv.id">
                                    {{ adv.name }} ({{ adv.bio ? adv.bio.substring(0, 30) + '...' : 'Specialist' }})
                                </option>
                            </select>
                        </div>
                        <div class="row g-2 mb-3">
                            <div class="col-6">
                                <label class="form-label fw-bold small text-muted">Date</label>
                                <input type="date" v-model="newAppointment.date" class="form-control" :min="minDate"
                                    required>
                            </div>
                            <div class="col-6">
                                <label class="form-label fw-bold small text-muted">Time</label>
                                <input type="time" v-model="newAppointment.time" class="form-control" required>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small text-muted">Notes</label>
                            <textarea v-model="newAppointment.notes" class="form-control" rows="2"
                                placeholder="Describe what you want to discuss..."></textarea>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary" :disabled="bookingLoading">
                                {{ bookingLoading ? 'Booking...' : 'Confirm Request' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div v-if="showDetailsModal" class="modal-backdrop-custom d-flex align-items-center justify-content-center">
            <div class="card shadow-lg border-0" style="width: 450px; max-width: 90%;">
                <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
                    <h5 class="mb-0 fw-bold">Session Details</h5>
                    <button type="button" class="btn-close" @click="showDetailsModal = false"></button>
                </div>
                <div class="card-body p-4" v-if="selectedAppt">
                    <div class="mb-3">
                        <div class="small text-uppercase text-muted fw-bold">Status</div>
                        <span class="badge mt-1" :class="{
                            'bg-warning text-dark': selectedAppt.status === 'Pending',
                            'bg-success': selectedAppt.status === 'Confirmed',
                            'bg-danger': selectedAppt.status === 'Cancelled'
                        }">
                            {{ selectedAppt.status }}
                        </span>
                    </div>

                    <div class="mb-3">
                        <div class="small text-uppercase text-muted fw-bold">Advisor</div>
                        <div class="fs-5">{{ selectedAppt.advisor_name }}</div>
                    </div>

                    <div class="row mb-3">
                        <div class="col-6">
                            <div class="small text-uppercase text-muted fw-bold">Date</div>
                            <div>{{ selectedAppt.date }}</div>
                        </div>
                        <div class="col-6">
                            <div class="small text-uppercase text-muted fw-bold">Time</div>
                            <div>{{ selectedAppt.time }}</div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <div class="small text-uppercase text-muted fw-bold">My Notes</div>
                        <div class="p-2 bg-light rounded mt-1 small" style="min-height: 50px;">
                            {{ selectedAppt.notes || "No notes provided." }}
                        </div>
                    </div>

                    <div class="d-grid mt-4">
                        <button class="btn btn-outline-secondary" @click="showDetailsModal = false">Close</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
.dashboard-container {
    height: 100vh;
    background-color: #f4f7f6;
    display: flex;
    flex-direction: column;
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
}

/* Enhancements */
.stat-card {
    transition: transform 0.2s;
}

.stat-card:hover {
    transform: translateY(-5px);
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #bbb;
}

.task-row:hover {
    background-color: #f8f9fa;
}

.task-row:hover .delete-btn {
    opacity: 1 !important;
}
</style>