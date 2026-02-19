<script setup>
import { ref, onMounted, computed, watch, reactive } from 'vue';
import { useRouter } from 'vue-router';
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

// Handle preset task uncompleted
const handleTaskUncompleted = (task) => {
  activitiesCompleted.value--;
  totalPoints.value -= 50;
  
  const index = tasks.value.findIndex(t => t.id === task.id && !t.isCustom);
  if (index !== -1) {
    tasks.value[index].completed = false;
  }
  saveProgress();
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
      if (progress.tasks) {
        tasks.value = progress.tasks;
      }
      if (progress.userState) {
        userState.value = progress.userState;
      }
      if (progress.showTasks !== undefined) {
        showTasks.value = progress.showTasks;
      }
    } catch (e) {
      console.error('Error loading progress:', e);
    }
  }
};

// Check for assessment results - WITH EXACT SCORE RANGES
const checkForAssessment = () => {
  console.log('=== CHECKING FOR ASSESSMENT ===');
  
  const assessmentResult = localStorage.getItem('assessmentResult');
  console.log('Assessment result from localStorage:', assessmentResult);
  
  if (!assessmentResult) {
    console.log('No assessment result found');
    return false;
  }

  try {
    const result = JSON.parse(assessmentResult);
    console.log('Parsed result:', result);
    
    // Get last processed assessment for this user
    const lastProcessedKey = `lastProcessedAssessment_${userId.value}`;
    const lastProcessed = localStorage.getItem(lastProcessedKey);
    
    // If this is the same as last processed, skip
    if (assessmentResult === lastProcessed) {
      console.log('Assessment already processed, skipping');
      return false;
    }
    
    // Get the score from the result
    const score = result.score || 0;
    console.log('Score:', score);
    
    // Determine new state based on YOUR EXACT SCORE RANGES:
    // 0-4: Healthy
    // 5-9: Mild Anxiety
    // 10-14: Moderate Anxiety
    // 15-27: Severe Anxiety
    let newState = 'healthy';
    if (score >= 15) {
      newState = 'severe-anxiety';
    } else if (score >= 10 && score <= 14) {
      newState = 'moderate-anxiety';
    } else if (score >= 5 && score <= 9) {
      newState = 'mild-anxiety';
    } else {
      newState = 'healthy';
    }
    
    console.log('New state determined:', newState);
    console.log('Current state:', userState.value);
    
    // Update state
    userState.value = newState;
    showTasks.value = true;
    
    // Get tasks for new state
    const baseTasks = getTasksForState(newState);
    console.log('Base tasks for new state:', baseTasks.length);
    
    // Keep custom tasks, replace preset tasks
    const customTasksOnly = tasks.value.filter(t => t.isCustom);
    const newPresetTasks = baseTasks.map(task => ({
      ...task,
      completed: false,
      isCustom: false
    }));
    
    // Update tasks
    tasks.value = [...newPresetTasks, ...customTasksOnly];
    activitiesCompleted.value = 0;
    totalPoints.value = 0;
    
    // Mark as processed
    localStorage.setItem(lastProcessedKey, assessmentResult);
    
    // Update dbStats
    dbStats.value.assessments = (dbStats.value.assessments || 0) + 1;
    
    // Save progress
    saveProgress();
    
    console.log('=== ASSESSMENT PROCESSED SUCCESSFULLY ===');
    console.log('New state:', newState);
    console.log('Tasks updated:', tasks.value.length);
    
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

// Debug functions
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
  console.log('Force checking assessment...');
  const assessmentProcessed = checkForAssessment();
  
  if (assessmentProcessed) {
    console.log('Assessment processed successfully in force check');
  } else {
    console.log('No new assessment to process');
  }
};

// --- INITIALIZATION ---
onMounted(() => {
  console.log('=== DASHBOARD MOUNTED ===');
  
  AOS.init({ duration: 1000, once: true });
  
  // Get user info
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      const userData = JSON.parse(userStr);
      userName.value = userData.username || 'User';
      userId.value = userData.id || userData.userId || Date.now().toString();
      console.log('User ID:', userId.value);
    } catch (e) {
      console.error('Error parsing user data:', e);
    }
  }

  // If no user ID, create one
  if (!userId.value) {
    userId.value = 'guest_' + Date.now();
    console.log('Created guest user ID:', userId.value);
  }

  // Load saved progress
  loadUserProgress();
  
  // Check for new assessment
  const assessmentProcessed = checkForAssessment();
  console.log('Assessment processed on mount:', assessmentProcessed);
  
  // If still no tasks and no assessment, show welcome message
  if (!showTasks.value && !assessmentProcessed) {
    console.log('No assessment found, showing welcome screen');
  }

  // Expose for debugging
  window.forceTasks = forceShowTasks;
  window.resetUser = resetForNewUser;
  window.checkAssessment = forceCheckAssessment;
  window.debug = {
    userState,
    showTasks,
    tasks,
    userId
  };
});

watch(tasks, (newVal) => {
    localStorage.setItem('userTasks', JSON.stringify(newVal));
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
                    <div class="d-flex gap-2 mt-2">
                      <select class="form-select form-select-sm" 
                              v-model="newPriority">
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                      </select>
                      <button type="button" 
                              class="btn btn-sm btn-primary" 
                              @click="addCustomTask">
                        <i class="bi bi-check-lg"></i>
                      </button>
                      <button type="button" 
                              class="btn btn-sm btn-outline-secondary"
                              @click="showAddTask = false">
                        <i class="bi bi-x-lg"></i>
                      </button>
                    </div>
                  </div>

                  <!-- Custom Tasks List - FIXED CHECKBOX HANDLER -->
                  <div v-if="customTasks.length > 0" class="custom-tasks-list">
                    <div v-for="task in customTasks" 
                         :key="task.id"
                         class="d-flex align-items-start gap-2 p-2 border-bottom custom-task-item">
                      
                      <input class="form-check-input mt-1" 
                             type="checkbox" 
                             :checked="task.completed"
                             @change="task.completed ? handleCustomTaskUncompleted(task) : handleCustomTaskCompleted(task)"
                             style="cursor: pointer;">

                      <div class="flex-grow-1">
                        <div class="small fw-bold" 
                             :class="{ 'text-decoration-line-through text-muted': task.completed }">
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

                      <button class="btn btn-link text-danger p-0" 
                              style="font-size: 0.8rem;"
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

                <!-- Debug buttons (only in development) -->
                <div v-if="isDev" class="card border-0 shadow-sm p-3">
                  <h6 class="mb-3">Help Settings</h6>
                  <div class="d-flex gap-2">
                    <button @click="forceShowTasks" class="btn btn-sm btn-warning">
                      Show Tasks
                    </button>
                    <button @click="resetForNewUser" class="btn btn-sm btn-danger">
                      Reset all Tasks
                    </button>

                  </div>
                  <small class="text-muted mt-2">
                    Current State: {{ userState }} | Tasks: {{ tasks.length }} | Completed: {{ activitiesCompleted }}
                  </small>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column - Tasks with Quote -->
          <div class="col-lg-8" data-aos="fade-left">
            <div class="card border-0 shadow-sm tasks-card">
              <!-- Tasks Header -->
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

              <!-- Tasks Body -->
              <div class="card-body p-0 tasks-body">
                <div class="tasks-list">
                  <!-- Show message if no assessment taken -->
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
                    
                    <!-- Show current state for debugging -->
                    <div v-if="isDev" class="mt-3 text-muted small">
                      User State: {{ userState }} | Show Tasks: {{ showTasks }}
                    </div>
                  </div>

                  <!-- Show tasks if assessment taken -->
                  <template v-else>
                    <!-- Preset Tasks Component -->
                    <TasksDisplay 
                      :tasks="presetTasks"
                      :userState="userState"
                      @task-completed="handleTaskCompleted"
                      @task-uncompleted="handleTaskUncompleted"
                    />
                    
                    <!-- Quote Card -->
                    <div class="mt-4 px-3">
                      <hr class="my-3">
                      <div class="quote-card bg-primary text-white p-4 rounded-3 shadow-sm" data-aos="fade-up">
                        <div class="text-center">
                          <i class="bi bi-quote fs-1 opacity-50"></i>
                          <h5 class="fw-light fst-italic mb-3">"Happiness is not something ready made. It comes from your own actions."</h5>
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

.dashboard-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.sticky-sidebar {
  position: sticky;
  top: 1rem;
}

.custom-tasks-sidebar {
  background: white;
  border-radius: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.task-row:hover {
    background-color: #f8f9fa;
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

.tasks-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 500px;
}

.tasks-card .card-header {
  flex-shrink: 0;
}

.tasks-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.tasks-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

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
  background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%);
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