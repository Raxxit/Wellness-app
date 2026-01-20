<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import * as wowModule from "wowjs";
import "wowjs/css/libs/animate.css";

// --- STATE ---
const userName = ref('User');
const dbStats = ref({ assessments: 0 }); // From Database
const streak = ref(12); // Mock Streak

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
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
});

// --- ACTIONS ---
const addTask = () => {
    // 1. Debugging: Check if function runs
    console.log("Attempting to add task...");

    // 2. Validation: Ensure text exists and isn't just whitespace
    if (!newTaskInput.value || newTaskInput.value.trim() === '') {
        console.log("Input is empty, cancelling.");
        return;
    }

    // 3. Add to array
    tasks.value.unshift({
        id: Date.now(),
        title: newTaskInput.value.trim(), // Trim whitespace
        priority: newPriority.value,
        completed: false
    });

    console.log("Task added!");

    // 4. Clear input
    newTaskInput.value = '';
};

const removeTask = (id) => {
    tasks.value = tasks.value.filter(t => t.id !== id);
};

onMounted(async () => {
    const wowModule = await import("wowjs");
    const WOW = wowModule.default || wowModule;
    new WOW().init();
});
onMounted(async () => {
    // 1. Get User Name
    const userStr = localStorage.getItem('user');
    if (userStr) userName.value = JSON.parse(userStr).username || 'User';

    // 2. Load Tasks
    const savedTasks = localStorage.getItem('userTasks');
    if (savedTasks) tasks.value = JSON.parse(savedTasks);
    else tasks.value = [
        { id: 1, title: 'Drink Water', priority: 'high', completed: false },
        { id: 2, title: 'Read 10 pages', priority: 'low', completed: true },
    ];

    // 3. Fetch DB Stats
    const token = localStorage.getItem('token');
    if (token) {
        try {
            const res = await fetch('/api/dashboard-stats', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                dbStats.value.assessments = data.assessments_completed;
            }
        } catch (e) { console.error(e); }
    }
});

// Save to LocalStorage automatically
watch(tasks, (newVal) => {
    localStorage.setItem('userTasks', JSON.stringify(newVal));
}, { deep: true });
</script>

<template>
    <div class="dashboard-container d-flex flex-column">

        <header class="d-flex justify-content-between align-items-end px-4 py-4 bg-white border-bottom shadow-sm mb-3">
            <div>
                <h6 class="text-uppercase text-muted small fw-bold ls-1 mb-1">
                    Wellness Journey
                </h6>
                <h2 class="fw-bold text-dark mb-0">
                    Daily Overview
                </h2>
            </div>

            <div class="d-none d-sm-flex align-items-center bg-light rounded-pill px-3 py-2 border">
                <i class="bi bi-calendar3 text-primary me-2"></i>
                <span class="fw-semibold text-secondary small">{{ currentDate }}</span>
            </div>
        </header>
        <div class="container-fluid grow p-4 bg-light">
            <div class="row h-100 g-4">

                <div class="col-lg-4 d-flex flex-column gap-4 wow fadeInLeft">

                    <div class="row g-3">
                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Assessments</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-clipboard-data text-primary fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ dbStats.assessments }}</h2>
                                </div>
                            </div>
                        </div>

                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Day Streak</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-fire text-warning fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ streak }}</h2>
                                </div>
                            </div>
                        </div>

                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Activities</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-check-circle-fill text-success fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ activitiesCompleted }}</h2>
                                </div>
                            </div>
                        </div>

                        <div class="col-6">
                            <div class="card border-0 shadow-sm p-3 h-100">
                                <div class="text-muted small text-uppercase fw-bold mb-2">Total Points</div>
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-star-fill text-info fs-3 me-3"></i>
                                    <h2 class="fw-bold mb-0">{{ totalPoints }}</h2>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div
                        class="card border-0 shadow-sm bg-primary text-white p-4 grow d-flex justify-content-center align-items-center text-center">
                        <div>
                            <i class="bi bi-quote fs-1 opacity-50"></i>
                            <h4 class="fw-light fst-italic mb-3">"Happiness is not something ready made. It comes from
                                your own actions."</h4>
                            <div class="opacity-75">— Dalai Lama</div>
                        </div>
                    </div>
                </div>

                <div class="col-lg-8 wow fadeInRight">
                    <div class="card border-0 shadow-sm h-100 d-flex flex-column">

                        <div class="card-header bg-white border-bottom py-3 px-4">
                            <div class="d-flex justify-content-between align-items-center">
                                <h5 class="fw-bold mb-0">My Tasks & Goals</h5>
                                <span class="badge bg-light text-dark border">
                                    {{ tasks.length }} Pending
                                </span>
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
                                        <i class="bi bi-plus-lg"></i> Add
                                    </button>
                                </div>
                            </div>

                            <div class="grow overflow-auto p-3 custom-scrollbar">
                                <div v-if="tasks.length === 0"
                                    class="h-100 d-flex flex-column align-items-center justify-content-center text-muted opacity-50">
                                    <i class="bi bi-clipboard2-check fs-1 mb-2"></i>
                                    <p>No tasks yet. Start your day!</p>
                                </div>

                                <div v-else class="list-group list-group-flush">
                                    <div v-for="task in tasks" :key="task.id"
                                        class="list-group-item border-0 border-bottom py-3 d-flex align-items-center task-row">

                                        <input class="form-check-input fs-5 me-3 rounded-circle" type="checkbox"
                                            v-model="task.completed" style="cursor: pointer;">

                                        <div class="">
                                            <div class="fw-bold"
                                                :class="{ 'text-decoration-line-through text-muted': task.completed }">
                                                {{ task.title }}
                                            </div>
                                            <span class="badge rounded-pill" style="font-size: 0.65rem;" :class="{
                                                'bg-danger': task.priority === 'high',
                                                'bg-warning text-dark': task.priority === 'medium',
                                                'bg-secondary': task.priority === 'low'
                                            }">
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
    </div>
</template>

<style scoped>
/* Full Screen Layout */
.dashboard-container {
    height: 100vh;
    /* Fill full viewport height */
    overflow: hidden;
    /* Prevent global scrollbar */
    background-color: #f4f7f6;
}

/* Scrollbar for Task List only */
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

.avatar-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Hover effects */
.task-row:hover {
    background-color: #f8f9fa;
}

.task-row:hover .delete-btn {
    opacity: 1 !important;
}

/* Responsive: Allow scroll on mobile */
@media (max-width: 991px) {
    .dashboard-container {
        height: auto;
        overflow: auto;
    }
}

.ls-1 {
    letter-spacing: 1px;
}
</style>