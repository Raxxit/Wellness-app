<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import TasksDisplay from '@/components/TasksDisplay.vue'; // Adjust path as needed

// --- AOS Imports ---
import AOS from "aos";
import "aos/dist/aos.css";

// --- STATE ---
const userName = ref('User');
const dbStats = ref({ assessments: 0 });
const streak = ref(0);
const userState = ref('healthy'); // Default state

// To-Do List State (simplified - just for tracking)
const tasks = ref([]);
const activitiesCompleted = ref(0);
const totalPoints = ref(0);

// --- COMPUTED LOGIC ---
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

// --- TASK HANDLERS ---
const handleTaskCompleted = (task) => {
    activitiesCompleted.value++;
    totalPoints.value += 50;
    updateTasksList(task, true);
};

const handleTaskUncompleted = (task) => {
    activitiesCompleted.value--;
    totalPoints.value -= 50;
    updateTasksList(task, false);
};

const updateTasksList = (updatedTask, completed) => {
    const index = tasks.value.findIndex(t => t.id === updatedTask.id);
    if (index !== -1) {
        tasks.value[index].completed = completed;
    } else {
        // If task doesn't exist in our tracking array, add it
        tasks.value.push(updatedTask);
    }
    // Save progress
    localStorage.setItem('taskProgress', JSON.stringify({
        completedCount: activitiesCompleted.value,
        totalPoints: totalPoints.value,
        completedTaskIds: tasks.value.filter(t => t.completed).map(t => t.id)
    }));
};

// --- INITIALIZATION ---
onMounted(async () => {
    // 1. Initialize AOS
    AOS.init({
        duration: 1000,
        once: true
    });

    // 2. Get User Name
    const userStr = localStorage.getItem('user');
    if (userStr) userName.value = JSON.parse(userStr).username || 'User';

    // 3. Get User State from assessment results
    const assessmentResult = localStorage.getItem('assessmentResult');
    if (assessmentResult) {
        try {
            const result = JSON.parse(assessmentResult);
            // Map your assessment result to state
            if (result.severity === 'severe' || result.score > 15) {
                userState.value = 'severe-anxiety';
            } else if (result.severity === 'mild' || result.score > 8) {
                userState.value = 'mild-anxiety';
            } else {
                userState.value = 'healthy';
            }
        } catch (e) {
            console.error('Error parsing assessment result:', e);
        }
    }

    // 4. Load saved progress
    const savedProgress = localStorage.getItem('taskProgress');
    if (savedProgress) {
        try {
            const progress = JSON.parse(savedProgress);
            activitiesCompleted.value = progress.completedCount || 0;
            totalPoints.value = progress.totalPoints || 0;
        } catch (e) {
            console.error('Error loading progress:', e);
        }
    }

    // 5. Fetch DB Stats
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

// Watch for changes in user tasks (if we need to save them)
watch(tasks, (newVal) => {
    // Optional: Save full task states if needed
    // localStorage.setItem('userTasks', JSON.stringify(newVal));
}, { deep: true });
</script>

<template>
    <div class="dashboard-container d-flex flex-column">

        <header class="d-flex justify-content-between align-items-end px-4 py-4 bg-white border-bottom shadow-sm mb-3">
            <div>
                <h6 class="text-uppercase text-muted small fw-bold ls-1 mb-1">
                    Welcome back, {{ userName }}
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

                <!-- Left Column - Stats & Quote -->
                <div class="col-lg-4 d-flex flex-column gap-4" data-aos="fade-right">
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

                <!-- Right Column - Tasks (using new component) -->
                <div class="col-lg-8" data-aos="fade-left">
                    <div class="card border-0 shadow-sm h-100 d-flex flex-column">
                        <div class="card-header bg-white border-bottom py-3 px-4">
                            <div class="d-flex justify-content-between align-items-center">
                                <h5 class="fw-bold mb-0">My Tasks & Goals</h5>
                                <span class="badge bg-light text-dark border">
                                    {{ activitiesCompleted }} / {{ tasks.length }} Completed
                                </span>
                            </div>
                            <div class="progress mt-3" style="height: 6px;">
                                <div class="progress-bar bg-primary" :style="{ width: progressPercent + '%' }"></div>
                            </div>
                        </div>

                        <div class="card-body p-0 d-flex flex-column overflow-hidden">
                            <div class="grow overflow-auto p-3 custom-scrollbar">
                                <TasksDisplay 
                                    :userState="userState"
                                    @task-completed="handleTaskCompleted"
                                    @task-uncompleted="handleTaskUncompleted"
                                />
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<style scoped>
.dashboard-container {
    height: 100vh;
    overflow: hidden;
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