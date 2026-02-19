<script setup>
import { ref, onMounted, computed, watch, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import TasksDisplay from '@/components/TasksDisplay.vue';
// --- AOS Imports ---
import AOS from "aos";
import "aos/dist/aos.css";
// --- Axios for API ---
import axios from 'axios';

// --- STATE ---
const router = useRouter();
const route = useRoute();
const userName = ref('User');
const userId = ref(null);
const dbStats = ref({ assessments: 0 });
const streak = ref(0);
const userState = ref('healthy');
const showTasks = ref(false);

// Appointment State
const appointments = ref([]);
const advisors = ref([]);

// Modal Controls
const showBookingModal = ref(false);
const showDetailsModal = ref(false);
const selectedAppt = ref(null);

const bookingLoading = ref(false);
const bookingMessage = ref(null);

const newAppointment = reactive({
  advisor_id: '',
  date: '',
  time: '',
  notes: ''
});

// To-Do List State (now with completion tracking)
const tasks = ref([]);
const activitiesCompleted = ref(0);
const totalPoints = ref(0);

// New Task Input State
const newTaskInput = ref('');
const newPriority = ref('medium');
const showAddTask = ref(false);

// --- TASKS DEFINITION - WITH 4 LEVELS ---
const getTasksForState = (state) => {
  const tasksByState = {
    'healthy': [
      { id: 1, title: 'Morning meditation (10 mins)', priority: 'medium' },
      { id: 2, title: 'Drink 8 glasses of water', priority: 'high' },
      { id: 3, title: '15-minute walk outside', priority: 'medium' },
      { id: 4, title: 'Read a book (20 mins)', priority: 'low' },
      { id: 5, title: 'Practice gratitude journaling', priority: 'medium' },
      { id: 6, title: 'Connect with a friend', priority: 'low' }
    ],
    'mild-anxiety': [
      { id: 1, title: 'Deep breathing exercise (5 mins)', priority: 'high' },
      { id: 2, title: 'Progressive muscle relaxation', priority: 'high' },
      { id: 3, title: 'Limit caffeine intake', priority: 'medium' },
      { id: 4, title: 'Go for a 20-minute walk', priority: 'high' },
      { id: 5, title: 'Write down worries & challenge them', priority: 'medium' },
      { id: 6, title: 'Listen to calming music', priority: 'low' },
      { id: 7, title: 'Avoid news/social media for 2 hours', priority: 'medium' }
    ],
    'moderate-anxiety': [
      { id: 1, title: 'Guided meditation (15 mins)', priority: 'high' },
      { id: 2, title: 'Breathing exercises (10 mins)', priority: 'high' },
      { id: 3, title: 'Call a friend or family member', priority: 'high' },
      { id: 4, title: 'Write in journal', priority: 'medium' },
      { id: 5, title: 'Avoid caffeine and sugar', priority: 'medium' },
      { id: 6, title: 'Take a warm bath or shower', priority: 'medium' },
      { id: 7, title: 'Listen to calming music', priority: 'low' },
      { id: 8, title: 'Gentle stretching (10 mins)', priority: 'medium' }
    ],
    'severe-anxiety': [
      { id: 1, title: '5-4-3-2-1 grounding exercise', priority: 'high' },
      { id: 2, title: 'Contact your therapist or helpline', priority: 'high' },
      { id: 3, title: 'Take prescribed medication (if any)', priority: 'high' },
      { id: 4, title: 'Guided meditation (10-15 mins)', priority: 'high' },
      { id: 5, title: 'Avoid triggers & stressful situations', priority: 'medium' },
      { id: 6, title: 'Gentle stretching or yoga', priority: 'medium' },
      { id: 7, title: 'Stay with a trusted person', priority: 'high' },
      { id: 8, title: 'Drink herbal tea & rest', priority: 'low' }
    ]
  };
  return tasksByState[state] || tasksByState.healthy;
};

// --- COMPUTED LOGIC ---
const progressPercent = computed(() => {
  if (tasks.value.length === 0) return 0;
  return Math.round((activitiesCompleted.value / tasks.value.length) * 100);
});

const currentDate = new Date().toLocaleDateString('en-US', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
});

const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

// Get preset tasks with saved completion status
const presetTasks = computed(() => {
  if (!showTasks.value) return [];
  const baseTasks = getTasksForState(userState.value);
  return baseTasks.map(baseTask => {
    const savedTask = tasks.value.find(t => t.id === baseTask.id && !t.isCustom);
    return {
      ...baseTask,
      completed: savedTask ? savedTask.completed : false,
      isCustom: false
    };
  });
});

// Get custom tasks only
const customTasks = computed(() => {
  return tasks.value.filter(t => t.isCustom);
});

// --- TASK HANDLERS ---
const handleTaskCompleted = (task) => {
  activitiesCompleted.value++;
  totalPoints.value += 50;
  const index = tasks.value.findIndex(t => t.id === task.id && !t.isCustom);
  if (index !== -1) {
    tasks.value[index].completed = true;
  } else {
    tasks.value.push({ ...task, completed: true, isCustom: false });
  }
  saveProgress();
};

const handleTaskUncompleted = (task) => {
  activitiesCompleted.value--;
  totalPoints.value -= 50;
  const index = tasks.value.findIndex(t => t.id === task.id && !t.isCustom);
  if (index !== -1) {
    tasks.value[index].completed = false;
  }
  saveProgress();
};

const handleCustomTaskCompleted = (task) => {
  if (!task.completed) {
    activitiesCompleted.value++;
    totalPoints.value += 50;
    task.completed = true;
  }
  saveProgress();
};

const handleCustomTaskUncompleted = (task) => {
  if (task.completed) {
    activitiesCompleted.value--;
    totalPoints.value -= 50;
    task.completed = false;
  }
  saveProgress();
};

const addCustomTask = () => {
  if (!newTaskInput.value || newTaskInput.value.trim() === '') return;
  const newTask = {
    id: Date.now(),
    title: newTaskInput.value.trim(),
    priority: newPriority.value,
    completed: false,
    isCustom: true
  };
  tasks.value.push(newTask);
  newTaskInput.value = '';
  showAddTask.value = false;
  saveProgress();
};

const removeCustomTask = (taskId) => {
  const taskToRemove = tasks.value.find(t => t.id === taskId);
  if (taskToRemove && taskToRemove.isCustom) {
    if (taskToRemove.completed) {
      activitiesCompleted.value--;
      totalPoints.value -= 50;
    }
    tasks.value = tasks.value.filter(t => t.id !== taskId);
    saveProgress();
  }
};

// Save all progress with user-specific key
const saveProgress = () => {
  if (!userId.value) return;
  const userTaskKey = `taskProgress_${userId.value}`;
  localStorage.setItem(userTaskKey, JSON.stringify({
    completedCount: activitiesCompleted.value,
    totalPoints: totalPoints.value,
    tasks: tasks.value,
    userState: userState.value,
    showTasks: showTasks.value,
    dbStats: dbStats.value,
    lastUpdated: new Date().toISOString()
  }));
};

// Load user-specific progress
const loadUserProgress = () => {
  if (!userId.value) return;
  const userTaskKey = `taskProgress_${userId.value}`;
  const savedProgress = localStorage.getItem(userTaskKey);
  if (savedProgress) {
    try {
      const progress = JSON.parse(savedProgress);
      activitiesCompleted.value = progress.completedCount || 0;
      totalPoints.value = progress.totalPoints || 0;
      if (progress.tasks) tasks.value = progress.tasks;
      if (progress.userState) userState.value = progress.userState;
      if (progress.showTasks !== undefined) showTasks.value = progress.showTasks;
      if (progress.dbStats) dbStats.value = progress.dbStats;
    } catch (e) {
      console.error('Error loading progress:', e);
    }
  }
};

// Check for assessment results
const checkForAssessment = () => {
  const assessmentResult = localStorage.getItem('assessmentResult');
  if (!assessmentResult) return false;
  try {
    const result = JSON.parse(assessmentResult);
    const lastProcessedKey = `lastProcessedAssessment_${userId.value}`;
    const lastProcessed = localStorage.getItem(lastProcessedKey);
    if (assessmentResult === lastProcessed) return false;

    const score = result.score || 0;
    let newState = 'healthy';
    if (score >= 15) newState = 'severe-anxiety';
    else if (score >= 10) newState = 'moderate-anxiety';
    else if (score >= 5) newState = 'mild-anxiety';

    userState.value = newState;
    showTasks.value = true;

    const baseTasks = getTasksForState(newState);
    const customTasksOnly = tasks.value.filter(t => t.isCustom);
    const newPresetTasks = baseTasks.map(task => ({
      ...task,
      completed: false,
      isCustom: false
    }));
    tasks.value = [...newPresetTasks, ...customTasksOnly];
    activitiesCompleted.value = 0;
    totalPoints.value = 0;

    localStorage.setItem(lastProcessedKey, assessmentResult);
    dbStats.value.assessments = (dbStats.value.assessments || 0) + 1;
    saveProgress();
    return true;
  } catch (e) {
    console.error('Error parsing assessment result:', e);
    return false;
  }
};

// Navigate to assessment
const goToAssessment = () => {
  router.push('/dynamicques');
};

// Debug functions (kept for console use, no UI)
const forceShowTasks = () => {
  showTasks.value = true;
  if (tasks.value.length === 0) {
    const baseTasks = getTasksForState(userState.value);
    tasks.value = baseTasks.map(task => ({
      ...task,
      completed: false,
      isCustom: false
    }));
  }
  saveProgress();
};

const resetForNewUser = () => {
  showTasks.value = false;
  tasks.value = [];
  activitiesCompleted.value = 0;
  totalPoints.value = 0;
  userState.value = 'healthy';
  saveProgress();
};

const forceCheckAssessment = () => {
  checkForAssessment();
};

// --- APPOINTMENT ACTIONS ---
const fetchAppointments = async () => {
  try {
    const res = await axios.get('/api/appointments/my-appointments');
    appointments.value = res.data;
  } catch (e) {
    console.error("Error fetching appointments", e);
  }
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

const closeDetailsModal = () => {
  showDetailsModal.value = false;
  selectedAppt.value = null;
};

const submitBooking = async () => {
  bookingLoading.value = true;
  bookingMessage.value = null;
  try {
    const res = await axios.post('/api/appointments/book', newAppointment);
    if (res.data.success) {
      bookingMessage.value = { type: 'success', text: 'Request Sent!' };
      fetchAppointments();
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

  // Get user info
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      const userData = JSON.parse(userStr);
      userName.value = userData.username || 'User';
      userId.value = userData.id || userData.userId || Date.now().toString();
    } catch (e) {
      console.error('Error parsing user data:', e);
    }
  }
  if (!userId.value) {
    userId.value = 'guest_' + Date.now();
  }

  // Load saved progress (tasks, state, etc.)
  loadUserProgress();

  // Check for new assessment
  checkForAssessment();

  // Set up axios auth and fetch appointments
  const token = localStorage.getItem('token');
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    try {
      const res = await axios.get('/api/dashboard-stats');
      dbStats.value.assessments = res.data.assessments_completed;
    } catch (e) { console.error(e); }
    fetchAppointments();
  }

  // Expose debug helpers to console (optional)
  window.forceTasks = forceShowTasks;
  window.resetUser = resetForNewUser;
  window.checkAssessment = forceCheckAssessment;
  window.debug = { userState, showTasks, tasks, userId };
});

// Watch for route changes (when returning from assessment)
watch(() => route.path, (newPath) => {
  if (newPath === '/dashboard') {
    setTimeout(() => checkForAssessment(), 100);
    setTimeout(() => checkForAssessment(), 500);
  }
});

// Watch for query params (when returning with ?assessment=completed)
watch(() => route.query, (newQuery) => {
  if (newQuery.assessment === 'completed') {
    setTimeout(() => forceCheckAssessment(), 100);
    setTimeout(() => forceCheckAssessment(), 500);
    setTimeout(() => {
      router.replace({ path: route.path, query: {} });
    }, 1000);
  }
});

// Storage event for multi‑tab support
window.addEventListener('storage', (e) => {
  if (e.key === 'assessmentResult') forceCheckAssessment();
});

// Watch for changes and save
watch([tasks, activitiesCompleted, totalPoints, userState, showTasks, dbStats], () => {
  saveProgress();
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

        <!-- Left Column: Stats, Appointments, Custom Tasks -->
        <div class="col-lg-5 d-flex flex-column gap-4" data-aos="fade-right">
          <!-- Stats Cards -->
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
                <div class="text-muted small text-uppercase fw-bold mb-2">Streak</div>
                <div class="d-flex align-items-center">
                  <i class="bi bi-fire text-warning fs-3 me-3"></i>
                  <h2 class="fw-bold mb-0">{{ streak }}</h2>
                </div>
              </div>
            </div>
          </div>

          <!-- Professional Support Card -->
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
              <h5 class="fw-bold mb-0 text-primary"><i class="bi bi-heart-pulse me-2"></i>Professional Support</h5>
              <button @click="openBookingModal" class="btn btn-sm btn-primary rounded-pill px-3">
                <i class="bi bi-plus-lg me-1"></i> Book
              </button>
            </div>
            <div class="card-body p-0">
              <div v-if="appointments.length === 0" class="text-center py-5 text-muted">
                <i class="bi bi-calendar-x fs-1 mb-2 opacity-50"></i>
                <p class="small mb-0">No upcoming sessions.</p>
              </div>
              <div v-else class="list-group list-group-flush">
                <div v-for="appt in appointments" :key="appt.id" class="list-group-item p-3 border-0 border-bottom">
                  <div class="d-flex justify-content-between align-items-start">
                    <div>
                      <span class="fw-bold text-dark d-block">{{ appt.advisor_name }}</span>
                      <div class="small text-muted mt-1">
                        <i class="bi bi-clock me-1"></i> {{ appt.date }} @ {{ appt.time }}
                      </div>
                    </div>
                    <div class="text-end">
                      <span class="badge rounded-pill d-block mb-2" :class="{
                        'bg-warning text-dark': appt.status === 'Pending',
                        'bg-success': appt.status === 'Confirmed',
                        'bg-danger': appt.status === 'Cancelled'
                      }">{{ appt.status }}</span>
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

          <!-- Custom Tasks Card (only if assessment taken) -->
          <div v-if="showTasks" class="card border-0 shadow-sm p-4 custom-tasks-sidebar">
            <h5 class="fw-bold mb-3">
              <i class="bi bi-pencil-square me-2"></i>
              My Custom Tasks
            </h5>
            <!-- Add Custom Task Button -->
            <button v-if="!showAddTask" class="btn btn-outline-primary w-100 mb-3 py-2" @click="showAddTask = true">
              <i class="bi bi-plus-circle me-2"></i>
              Add New Task
            </button>
            <!-- Add Task Form -->
            <div v-else class="add-task-form mb-3">
              <div class="input-group input-group-sm">
                <input type="text" class="form-control" placeholder="Enter task..." v-model="newTaskInput"
                  @keyup.enter="addCustomTask" autofocus>
              </div>
              <div class="d-flex gap-2 mt-2">
                <select class="form-select form-select-sm" v-model="newPriority">
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
                <button type="button" class="btn btn-sm btn-primary" @click="addCustomTask">
                  <i class="bi bi-check-lg"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="showAddTask = false">
                  <i class="bi bi-x-lg"></i>
                </button>
              </div>
            </div>
            <!-- Custom Tasks List -->
            <div v-if="customTasks.length > 0" class="custom-tasks-list">
              <div v-for="task in customTasks" :key="task.id"
                class="d-flex align-items-start gap-2 p-2 border-bottom custom-task-item">
                <input class="form-check-input mt-1" type="checkbox" :checked="task.completed"
                  @change="task.completed ? handleCustomTaskUncompleted(task) : handleCustomTaskCompleted(task)"
                  style="cursor: pointer;">
                <div class="flex-grow-1">
                  <div class="small fw-bold" :class="{ 'text-decoration-line-through text-muted': task.completed }">
                    {{ task.title }}
                  </div>
                  <div class="d-flex gap-1 mt-1">
                    <span class="badge rounded-pill" style="font-size: 0.6rem;" :class="{
                      'bg-danger': task.priority === 'high',
                      'bg-warning text-dark': task.priority === 'medium',
                      'bg-secondary': task.priority === 'low'
                    }">
                      {{ task.priority }}
                    </span>
                  </div>
                </div>
                <button class="btn btn-link text-danger p-0" style="font-size: 0.8rem;"
                  @click="removeCustomTask(task.id)">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            <!-- Empty State -->
            <div v-else class="text-center text-muted py-4">
              <i class="bi bi-clipboard2-plus fs-1 mb-2"></i>
              <p class="small mb-0">No custom tasks yet</p>
              <p class="small">Click "Add New Task" to create one</p>
            </div>
          </div>
        </div>

        <!-- Right Column: Recommended Tasks -->
        <div class="col-lg-7" data-aos="fade-left">
          <div class="card border-0 shadow-sm h-100 d-flex flex-column">
            <div class="card-header bg-white border-bottom py-3 px-4">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0">Today's Recommended Tasks</h5>
                <span v-if="showTasks" class="badge bg-light text-dark border">
                  {{ activitiesCompleted }} / {{ tasks.length }} Completed
                </span>
              </div>
              <div v-if="showTasks" class="progress mt-3" style="height: 6px;">
                <div class="progress-bar bg-primary" :style="{ width: progressPercent + '%' }"></div>
              </div>
            </div>

            <div class="card-body p-0 d-flex flex-column flex-grow-1">
              <div class="flex-grow-1 overflow-auto p-3 custom-scrollbar" style="max-height: 500px;">
                <!-- Welcome message if no assessment taken -->
                <div v-if="!showTasks" class="text-center py-5">
                  <div class="mb-4">
                    <i class="bi bi-clipboard2-heart fs-1 text-primary opacity-50"></i>
                  </div>
                  <h4 class="fw-bold mb-3">Welcome to Your Dashboard!</h4>
                  <p class="text-muted mb-4">
                    To get personalized task recommendations, please complete your first assessment.
                  </p>
                  <button @click="goToAssessment" class="btn btn-primary btn-lg px-5 py-3">
                    <i class="bi bi-pencil-square me-2"></i>
                    Take Assessment
                  </button>
                </div>

                <!-- Tasks after assessment -->
                <template v-else>
                  <TasksDisplay :tasks="presetTasks" :userState="userState" @task-completed="handleTaskCompleted"
                    @task-uncompleted="handleTaskUncompleted" />
                  <!-- Quote Card -->
                  <div class="mt-4 px-3">
                    <hr class="my-3">
                    <div class="quote-card bg-primary text-white p-4 rounded-3 shadow-sm" data-aos="fade-up">
                      <div class="text-center">
                        <i class="bi bi-quote fs-1 opacity-50"></i>
                        <h5 class="fw-light fst-italic mb-3">"Happiness is not something ready made. It comes from your
                          own actions."</h5>
                        <div class="opacity-75 small">— Dalai Lama</div>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="showBookingModal" class="modal-backdrop-custom d-flex align-items-center justify-content-center"
      @click.self="showBookingModal = false">
      <div class="card shadow-lg border-0" style="width: 500px; max-width: 95%;">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Book a Session</h5>
          <button type="button" class="btn-close btn-close-white" @click="showBookingModal = false"></button>
        </div>
        <div class="card-body p-4">
          <div v-if="bookingMessage" :class="`alert alert-${bookingMessage.type === 'error' ? 'danger' : 'success'}`">
            {{ bookingMessage.text }}
          </div>
          <form @submit.prevent="submitBooking">
            <div class="mb-3">
              <label class="form-label fw-bold small text-muted">Select Advisor</label>
              <select v-model="newAppointment.advisor_id" class="form-select" required>
                <option value="" disabled>Choose a professional...</option>
                <option v-for="adv in advisors" :key="adv.id" :value="adv.id">{{ adv.name }}</option>
              </select>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label fw-bold small text-muted">Date</label>
                <input type="date" v-model="newAppointment.date" class="form-control" :min="minDate" required>
              </div>
              <div class="col-6">
                <label class="form-label fw-bold small text-muted">Time</label>
                <input type="time" v-model="newAppointment.time" class="form-control" required>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold small text-muted">Notes</label>
              <textarea v-model="newAppointment.notes" class="form-control" rows="2"
                placeholder="What's on your mind?"></textarea>
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="bookingLoading">
              {{ bookingLoading ? 'Booking...' : 'Confirm Request' }}
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="modal-backdrop-custom d-flex align-items-center justify-content-center"
      @click.self="closeDetailsModal">
      <div class="card shadow-lg border-0" style="width: 450px; max-width: 95%;">
        <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
          <h5 class="mb-0 fw-bold text-dark">Session Details</h5>
          <button type="button" class="btn-close" @click="closeDetailsModal"></button>
        </div>
        <div class="card-body p-4" v-if="selectedAppt">
          <div class="text-center mb-4">
            <div class="small text-uppercase text-muted fw-bold mb-1">Status</div>
            <span class="badge fs-6 px-3" :class="{
              'bg-warning text-dark': selectedAppt.status === 'Pending',
              'bg-success': selectedAppt.status === 'Confirmed',
              'bg-danger': selectedAppt.status === 'Cancelled'
            }">{{ selectedAppt.status }}</span>
          </div>

          <div class="mb-3">
            <label class="small text-uppercase text-muted fw-bold d-block">Advisor</label>
            <div class="fs-5 fw-bold text-primary">{{ selectedAppt.advisor_name }}</div>
          </div>

          <div class="row mb-3 bg-light rounded p-3 mx-0">
            <div class="col-6 border-end">
              <label class="small text-uppercase text-muted fw-bold d-block">Date</label>
              <div class="fw-semibold">{{ selectedAppt.date }}</div>
            </div>
            <div class="col-6 ps-3">
              <label class="small text-uppercase text-muted fw-bold d-block">Time</label>
              <div class="fw-semibold">{{ selectedAppt.time }}</div>
            </div>
          </div>

          <div class="mb-4">
            <label class="small text-uppercase text-muted fw-bold d-block">Session Notes</label>
            <div class="p-2 border-start border-4 border-primary mt-2 italic text-secondary"
              style="min-height: 60px; background: #fcfcfc;">
              "{{ selectedAppt.notes || "No notes provided for this session." }}"
            </div>
          </div>

          <button class="btn btn-outline-secondary w-100" @click="closeDetailsModal">Close Details</button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.dashboard-container {
  height: 100vh;
  background-color: #f4f7f6;
}

.modal-backdrop-custom {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.transition-all {
  transition: all 0.4s ease;
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

.ls-1 {
  letter-spacing: 1px;
}

/* Custom tasks sidebar styles */
.custom-tasks-sidebar {
  background: white;
  border-radius: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.custom-tasks-sidebar::-webkit-scrollbar {
  width: 4px;
}

.custom-tasks-sidebar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.custom-tasks-sidebar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

.custom-tasks-sidebar::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.custom-task-item {
  transition: background-color 0.2s ease;
}

.custom-task-item:hover {
  background-color: #f8f9fa;
}

.add-task-form {
  animation: slideDown 0.3s ease;
}

.quote-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  transition: transform 0.3s ease;
  position: relative;
  overflow: hidden;
}

.quote-card:hover {
  transform: translateY(-2px);
}

.quote-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
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
</style>