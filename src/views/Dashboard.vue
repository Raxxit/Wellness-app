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

// To-Do List State
const tasks = ref([]);
const activitiesCompleted = ref(0);
const totalPoints = ref(0);

// New Task Input State
const newTaskInput = ref('');
const newPriority = ref('medium');
const showAddTask = ref(false);

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

// Combine preset and custom tasks for display
const allTasks = computed(() => {
    return tasks.value;
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
    saveProgress();
};

// Add custom task
const addCustomTask = () => {
    if (!newTaskInput.value || newTaskInput.value.trim() === '') return;

    const newTask = {
        id: Date.now(), // Use timestamp as unique ID
        title: newTaskInput.value.trim(),
        priority: newPriority.value,
        completed: false,
        isCustom: true // Mark as custom task
    };

    tasks.value.push(newTask);
    newTaskInput.value = '';
    showAddTask.value = false;
    saveProgress();
};

// Remove custom task
const removeCustomTask = (taskId) => {
    const taskToRemove = tasks.value.find(t => t.id === taskId);
    if (taskToRemove && taskToRemove.isCustom) {
        // If it was completed, adjust counts
        if (taskToRemove.completed) {
            activitiesCompleted.value--;
            totalPoints.value -= 50;
        }
        tasks.value = tasks.value.filter(t => t.id !== taskId);
        saveProgress();
    }
};

// Save all progress
const saveProgress = () => {
    localStorage.setItem('taskProgress', JSON.stringify({
        completedCount: activitiesCompleted.value,
        totalPoints: totalPoints.value,
        tasks: tasks.value, // Save all tasks (preset + custom)
        completedTaskIds: tasks.value.filter(t => t.completed).map(t => t.id)
    }));
};

// Load saved tasks from TasksDisplay component
const handleTasksLoaded = (loadedTasks) => {
    // Only add tasks that aren't already in our list
    loadedTasks.forEach(loadedTask => {
        const exists = tasks.value.some(t => 
            t.id === loadedTask.id && !t.isCustom
        );
        if (!exists) {
            tasks.value.push(loadedTask);
        }
    });
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
            if (progress.tasks) {
                tasks.value = progress.tasks;
            }
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

// Watch for changes and save
watch(tasks, () => {
    saveProgress();
}, { deep: true });
</script>

<template>
    <div class="dashboard-container">
        <!-- Fixed Header -->
        <header class="dashboard-header d-flex justify-content-between align-items-center px-4 py-3 bg-white border-bottom shadow-sm">
            <div>
                <h6 class="text-uppercase text-muted small fw-bold ls-1 mb-0">
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

        <!-- Scrollable Content Area -->
        <div class="dashboard-content">
            <div class="container-fluid py-4 px-4">
                <div class="row g-4">

                    <!-- Left Column - Stats & Quote (Sticky on desktop) -->
                    <div class="col-lg-4" data-aos="fade-right">
                        <div class="sticky-sidebar">
                            <div class="d-flex flex-column gap-4">
                                <!-- Stats Cards -->
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

                                <!-- Quote Card -->
                                <div class="card border-0 shadow-sm bg-primary text-white p-4 d-flex justify-content-center align-items-center text-center">
                                    <div>
                                        <i class="bi bi-quote fs-1 opacity-50"></i>
                                        <h4 class="fw-light fst-italic mb-3">"Happiness is not something ready made. It comes from your own actions."</h4>
                                        <div class="opacity-75">— Dalai Lama</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right Column - Tasks (Scrollable) -->
                    <div class="col-lg-8" data-aos="fade-left">
                        <div class="card border-0 shadow-sm tasks-card">
                            <!-- Tasks Header (Fixed) -->
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

                            <!-- Tasks Body (Scrollable) -->
                            <div class="card-body p-0 tasks-body">
                                <!-- Add Task Section -->
                                <div class="p-3 bg-light border-bottom">
                                    <button v-if="!showAddTask" 
                                            class="btn btn-outline-primary w-100 py-2"
                                            @click="showAddTask = true">
                                        <i class="bi bi-plus-circle me-2"></i>
                                        Add Custom Task
                                    </button>
                                    
                                    <div v-else class="add-task-form">
                                        <div class="input-group">
                                            <input type="text" 
                                                   class="form-control border-0 shadow-none"
                                                   placeholder="Enter your task..."
                                                   v-model="newTaskInput" 
                                                   @keyup.enter="addCustomTask"
                                                   autofocus>
                                            
                                            <select class="form-select border-0 shadow-none" 
                                                    style="max-width: 100px;"
                                                    v-model="newPriority">
                                                <option value="high">High</option>
                                                <option value="medium">Med</option>
                                                <option value="low">Low</option>
                                            </select>
                                            
                                            <button type="button" 
                                                    class="btn btn-primary" 
                                                    @click="addCustomTask">
                                                <i class="bi bi-check-lg"></i>
                                            </button>
                                            
                                            <button type="button" 
                                                    class="btn btn-outline-secondary"
                                                    @click="showAddTask = false">
                                                <i class="bi bi-x-lg"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Tasks List (Scrollable) -->
                                <div class="tasks-list">
                                    <!-- Preset Tasks Component -->
                                    <TasksDisplay 
                                        :userState="userState"
                                        @task-completed="handleTaskCompleted"
                                        @task-uncompleted="handleTaskUncompleted"
                                        @tasks-loaded="handleTasksLoaded"
                                    />
                                    
                                    <!-- Custom Tasks Section (if any) -->
                                    <div v-if="tasks.filter(t => t.isCustom).length > 0" class="mt-4 px-3">
                                        <hr class="my-3">
                                        <h6 class="text-muted mb-3">
                                            <i class="bi bi-pencil-square me-2"></i>
                                            My Custom Tasks
                                        </h6>
                                        
                                        <div v-for="task in tasks.filter(t => t.isCustom)" 
                                             :key="task.id"
                                             class="list-group-item border-0 border-bottom py-3 d-flex align-items-center task-row px-0">
                                            
                                            <input class="form-check-input fs-5 me-3 rounded-circle" 
                                                   type="checkbox" 
                                                   v-model="task.completed" 
                                                   @change="task.completed ? handleTaskCompleted(task) : handleTaskUncompleted(task)"
                                                   style="cursor: pointer;">

                                            <div class="flex-grow-1">
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
                                                <span class="badge bg-light text-dark ms-2" style="font-size: 0.65rem;">
                                                    Custom
                                                </span>
                                            </div>

                                            <button class="btn btn-link text-danger p-2 opacity-0 delete-btn"
                                                    @click="removeCustomTask(task.id)">
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
    </div>
</template>

<style scoped>
.dashboard-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background-color: #f4f7f6;
}

.dashboard-header {
    flex-shrink: 0; /* Prevent header from shrinking */
    z-index: 10;
}

.dashboard-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
}

/* Sticky sidebar for desktop */
.sticky-sidebar {
    position: sticky;
    top: 1rem;
}

/* Tasks Card */
.tasks-card {
    height: 100%;
    display: flex;
    flex-direction: column;
    min-height: 500px; /* Minimum height */
}

.tasks-card .card-header {
    flex-shrink: 0;
}

.tasks-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-height: 0; /* Important for flex child scrolling */
}

.tasks-list {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}

/* Custom Scrollbar */
.tasks-list::-webkit-scrollbar,
.dashboard-content::-webkit-scrollbar {
    width: 8px;
}

.tasks-list::-webkit-scrollbar-track,
.dashboard-content::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.tasks-list::-webkit-scrollbar-thumb,
.dashboard-content::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 10px;
}

.tasks-list::-webkit-scrollbar-thumb:hover,
.dashboard-content::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}

/* Task row hover effect */
.task-row:hover {
    background-color: #f8f9fa;
}

.task-row:hover .delete-btn {
    opacity: 1 !important;
}

.delete-btn {
    transition: opacity 0.2s ease;
}

/* Add task form animation */
.add-task-form {
    animation: slideDown 0.3s ease;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Responsive adjustments */
@media (max-width: 991px) {
    .dashboard-container {
        height: auto;
        min-height: 100vh;
    }
    
    .dashboard-content {
        overflow-y: visible;
    }
    
    .sticky-sidebar {
        position: static;
    }
    
    .tasks-card {
        min-height: 400px;
    }
}

.ls-1 {
    letter-spacing: 1px;
}
</style>