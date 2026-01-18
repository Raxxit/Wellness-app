<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import * as wowModule from "wowjs";
import "wowjs/css/libs/animate.css";
import axios from 'axios';

const router = useRouter();

// Reactive state for selections
const selectedGoals = ref([]);
const selectedSleepQuality = ref(null);
const selectedStressLevel = ref(5);
const selectedHabits = ref([]);
const energyLevels = ref({
    morning: 'medium',
    afternoon: 'high',
    evening: 'low'
});

// NEW: Database questions
const dbQuestions = ref([]);
const dbAnswers = ref({});

// Alert state
const alert = ref({
  show: false,
  type: '',
  message: ''
});

// Show alert
const showAlert = (type, message) => {
  alert.value.show = true;
  alert.value.type = type;
  alert.value.message = message;

  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });

  setTimeout(() => {
    alert.value.show = false;
  }, 5000);
};

// Close alert
const closeAlert = () => {
  alert.value.show = false;
};

// Fetch questions from database
const fetchQuestions = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      showAlert('error', 'Please login to access the questionnaire');
      router.push('/login');
      return;
    }

    const response = await axios.get('http://127.0.0.1:5000/api/questionnaire/questions', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.data.success) {
      dbQuestions.value = response.data.questions;
      // Initialize answers object
      dbQuestions.value.forEach(q => {
        dbAnswers.value[q.question_id] = null;
      });
    }
  } catch (error) {
    console.error('Error fetching questions:', error);
    if (error.response && error.response.status === 401) {
      showAlert('error', 'Session expired. Please login again');
      router.push('/login');
    } else {
      showAlert('error', 'Failed to load questions. Please try again.');
    }
  }
};

// Select answer for database question
const selectAnswer = (questionId, optionId) => {
  dbAnswers.value[questionId] = optionId;
};

// Function to toggle goal selection
const toggleGoal = (goal) => {
    const index = selectedGoals.value.indexOf(goal);
    if (index === -1) {
        selectedGoals.value.push(goal);
    } else {
        selectedGoals.value.splice(index, 1);
    }
};

// Function to select sleep quality
const selectSleepQuality = (quality) => {
    selectedSleepQuality.value = quality;
};

// Function to toggle habit selection
const toggleHabit = (habit) => {
    const index = selectedHabits.value.indexOf(habit);
    if (index === -1) {
        selectedHabits.value.push(habit);
    } else {
        selectedHabits.value.splice(index, 1);
    }
};

// Function to select energy level
const selectEnergyLevel = (time, level) => {
    energyLevels.value[time] = level;
};

// Get energy level class based on value
const getEnergyClass = (level) => {
    switch (level) {
        case 'low': return 'bg-danger';
        case 'medium': return 'bg-warning';
        case 'high': return 'bg-success';
        default: return 'bg-secondary';
    }
};

// Get energy height based on value
const getEnergyHeight = (level) => {
    switch (level) {
        case 'low': return '30%';
        case 'medium': return '60%';
        case 'high': return '90%';
        default: return '50%';
    }
};

// Form submission handler
const submitQuestionnaire = async () => {
  try {
    // Validate that all DB questions are answered
    const unansweredQuestions = dbQuestions.value.filter(q => !dbAnswers.value[q.question_id]);
    if (unansweredQuestions.length > 0) {
      showAlert('error', 'Please answer all questions before submitting');
      return;
    }

    // Prepare answers array for backend
    const answers = Object.keys(dbAnswers.value).map(questionId => ({
      question_id: parseInt(questionId),
      option_id: dbAnswers.value[questionId]
    }));

    const token = localStorage.getItem('token');
    if (!token) {
      showAlert('error', 'Please login to submit the questionnaire');
      router.push('/login');
      return;
    }

    // Submit to backend
    const response = await axios.post(
      'http://127.0.0.1:5000/api/questionnaire/submit',
      { answers },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    if (response.data.success) {
      const result = response.data.result;
      showAlert('success', `Assessment complete! Your wellness level: ${result.result_level}/5`);
      
      // Optionally redirect to results page after 3 seconds
      setTimeout(() => {
        // You can create a results page later
        console.log('Result:', result);
      }, 3000);
    }

  } catch (error) {
    console.error('Submission error:', error);
    if (error.response && error.response.data && error.response.data.message) {
      showAlert('error', error.response.data.message);
    } else {
      showAlert('error', 'Failed to submit questionnaire. Please try again.');
    }
  }
};

onMounted(() => {
  const WOW = wowModule.WOW || wowModule.default.WOW;
  new WOW().init();
  
  // Fetch questions from database
  fetchQuestions();
});

</script>

<template>
    <div class="questionnaire-page">

        <!-- Header Section -->
        <header class="py-5 bg-gradient-primary border-bottom">
            <div class="container text-center">
                <h1 class="display-4 fw-bold text-white wow fadeInUp" data-wow-delay="0.1s">
                    Wellness Assessment
                </h1>
                <p class="lead text-light wow fadeInUp" data-wow-delay="0.2s">
                    Take 5 minutes to help us personalize your wellness journey
                </p>
                <div class="progress mt-4 wow fadeInUp" data-wow-delay="0.3s"
                    style="height: 8px; max-width: 300px; margin: 0 auto;">
                    <div class="progress-bar bg-white" style="width: 25%"></div>
                </div>
            </div>
        </header>

        <!-- Questionnaire Form -->
        <section class="py-5">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-12 col-lg-8">

                        <!-- Alert Message -->
                        <transition name="slide-fade">
                          <div v-if="alert.show" :class="['alert', alert.type === 'success' ? 'alert-success' : 'alert-danger', 'alert-dismissible', 'fade', 'show', 'mb-4']" role="alert">
                            <i :class="alert.type === 'success' ? 'fa fa-check-circle' : 'fa fa-exclamation-circle'" class="me-2"></i>
                            <strong>{{ alert.message }}</strong>
                            <button @click="closeAlert" type="button" class="btn-close" aria-label="Close"></button>
                          </div>
                        </transition>

                        <!-- DATABASE QUESTIONS (Mental Health Assessment) -->
                        <div v-for="(question, qIndex) in dbQuestions" :key="question.question_id" 
                             class="card shadow-sm border-0 mb-4 wow fadeInUp" :data-wow-delay="`${0.1 * (qIndex + 1)}s`">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    {{ qIndex + 1 }}. {{ question.question_text }}
                                </h4>
                                
                                <div class="d-grid gap-2">
                                    <button 
                                        v-for="option in question.options" 
                                        :key="option.option_id"
                                        type="button"
                                        class="btn btn-outline-primary text-start p-3"
                                        :class="{ 'active': dbAnswers[question.question_id] === option.option_id }"
                                        @click="selectAnswer(question.question_id, option.option_id)"
                                    >
                                        <i class="fa fa-circle me-2" :class="dbAnswers[question.question_id] === option.option_id ? 'fa-check-circle' : 'fa-circle-o'"></i>
                                        {{ option.option_text }}
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Question 1: Wellness Goals (KEEPING YOUR ORIGINAL UI) -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.1s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    {{ dbQuestions.length + 1 }}. What are your primary wellness goals?
                                </h4>
                                <p class="text-muted mb-4">Select all that apply</p>

                                <div class="row g-3">
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('stress') }"
                                            @click="toggleGoal('stress')">
                                            <div class="display-4 mb-2">🧘</div>
                                            <p class="mb-0 fw-medium">Stress Relief</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('sleep') }"
                                            @click="toggleGoal('sleep')">
                                            <div class="display-4 mb-2">😴</div>
                                            <p class="mb-0 fw-medium">Better Sleep</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('energy') }"
                                            @click="toggleGoal('energy')">
                                            <div class="display-4 mb-2">💪</div>
                                            <p class="mb-0 fw-medium">More Energy</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('mindfulness') }"
                                            @click="toggleGoal('mindfulness')">
                                            <div class="display-4 mb-2">🧠</div>
                                            <p class="mb-0 fw-medium">Mindfulness</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('mental') }"
                                            @click="toggleGoal('mental')">
                                            <div class="display-4 mb-2">❤️</div>
                                            <p class="mb-0 fw-medium">Mental Health</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('nutrition') }"
                                            @click="toggleGoal('nutrition')">
                                            <div class="display-4 mb-2">🥗</div>
                                            <p class="mb-0 fw-medium">Nutrition</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- ALL YOUR OTHER ORIGINAL QUESTIONS STAY THE SAME -->
                        <!-- Question 2: Sleep Quality -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.2s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    {{ dbQuestions.length + 2 }}. How would you rate your sleep quality?
                                </h4>

                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="sleep-option text-center" @click="selectSleepQuality('poor')">
                                        <div class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 'active': selectedSleepQuality === 'poor' }">
                                            <span class="display-4">😴</span>
                                        </div>
                                        <p class="small mb-0">Poor</p>
                                    </div>
                                    <div class="sleep-option text-center" @click="selectSleepQuality('fair')">
                                        <div class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 'active': selectedSleepQuality === 'fair' }">
                                            <span class="display-4">😐</span>
                                        </div>
                                        <p class="small mb-0">Fair</p>
                                    </div>
                                    <div class="sleep-option text-center" @click="selectSleepQuality('good')">
                                        <div class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 'active': selectedSleepQuality === 'good' }">
                                            <span class="display-4">😊</span>
                                        </div>
                                        <p class="small mb-0">Good</p>
                                    </div>
                                    <div class="sleep-option text-center" @click="selectSleepQuality('great')">
                                        <div class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 'active': selectedSleepQuality === 'great' }">
                                            <span class="display-4">😄</span>
                                        </div>
                                        <p class="small mb-0">Great</p>
                                    </div>
                                    <div class="sleep-option text-center" @click="selectSleepQuality('excellent')">
                                        <div class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 'active': selectedSleepQuality === 'excellent' }">
                                            <span class="display-4">🤩</span>
                                        </div>
                                        <p class="small mb-0">Excellent</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Question 3: Stress Level Slider -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.3s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-4">
                                    {{ dbQuestions.length + 3 }}. Current stress level
                                </h4>

                                <div class="stress-slider-container">
                                    <div class="d-flex justify-content-between mb-2">
                                        <span class="text-muted">Very Low</span>
                                        <span class="text-muted">Very High</span>
                                    </div>
                                    <input type="range" class="form-range" min="1" max="10" step="1"
                                        style="height: 12px; cursor: pointer;" v-model="selectedStressLevel">
                                    <div class="d-flex justify-content-between mt-1">
                                        <span class="badge bg-success">Calm</span>
                                        <span class="badge bg-warning">Moderate</span>
                                        <span class="badge bg-danger">Stressed</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Question 4: Daily Habits -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.4s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    {{ dbQuestions.length + 4 }}. Which wellness activities do you currently practice?
                                </h4>

                                <div class="row g-2">
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('meditation') }"
                                            @click="toggleHabit('meditation')">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="meditation"
                                                    :checked="selectedHabits.includes('meditation')"
                                                    @change="toggleHabit('meditation')">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="meditation">
                                                Meditation
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('exercise') }"
                                            @click="toggleHabit('exercise')">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="exercise"
                                                    :checked="selectedHabits.includes('exercise')"
                                                    @change="toggleHabit('exercise')">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="exercise">
                                                Exercise
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('journaling') }"
                                            @click="toggleHabit('journaling')">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="journaling"
                                                    :checked="selectedHabits.includes('journaling')"
                                                    @change="toggleHabit('journaling')">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="journaling">
                                                Journaling
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('yoga') }"
                                            @click="toggleHabit('yoga')">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="yoga"
                                                    :checked="selectedHabits.includes('yoga')"
                                                    @change="toggleHabit('yoga')">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="yoga">
                                                Yoga
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('walking') }"
                                            @click="toggleHabit('walking')">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="walking"
                                                    :checked="selectedHabits.includes('walking')"
                                                    @change="toggleHabit('walking')">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="walking">
                                                Walking
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('breathing') }"
                                            @click="toggleHabit('breathing')">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="breathing"
                                                    :checked="selectedHabits.includes('breathing')"
                                                    @change="toggleHabit('breathing')">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="breathing">
                                                Breathing
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Question 5: Energy Level -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.5s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-4">
                                    {{ dbQuestions.length + 5 }}. How's your energy throughout the day?
                                </h4>

                                <div class="energy-chart">
                                    <div class="row text-center">
                                        <div class="col">
                                            <p class="small text-muted mb-1">Morning</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div class="energy-fill rounded-top"
                                                    :class="getEnergyClass(energyLevels.morning)"
                                                    :style="{ height: getEnergyHeight(energyLevels.morning) }"></div>
                                            </div>
                                            <div class="btn-group btn-group-sm mt-2" role="group">
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.morning === 'low' }"
                                                    @click="selectEnergyLevel('morning', 'low')">Low</button>
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.morning === 'medium' }"
                                                    @click="selectEnergyLevel('morning', 'medium')">Med</button>
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.morning === 'high' }"
                                                    @click="selectEnergyLevel('morning', 'high')">High</button>
                                            </div>
                                        </div>
                                        <div class="col">
                                            <p class="small text-muted mb-1">Afternoon</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div class="energy-fill rounded-top"
                                                    :class="getEnergyClass(energyLevels.afternoon)"
                                                    :style="{ height: getEnergyHeight(energyLevels.afternoon) }"></div>
                                            </div>
                                            <div class="btn-group btn-group-sm mt-2" role="group">
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.afternoon === 'low' }"
                                                    @click="selectEnergyLevel('afternoon', 'low')">Low</button>
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.afternoon === 'medium' }"
                                                    @click="selectEnergyLevel('afternoon', 'medium')">Med</button>
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.afternoon === 'high' }"
                                                    @click="selectEnergyLevel('afternoon', 'high')">High</button>
                                            </div>
                                        </div>
                                        <div class="col">
                                            <p class="small text-muted mb-1">Evening</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div class="energy-fill rounded-top"
                                                    :class="getEnergyClass(energyLevels.evening)"
                                                    :style="{ height: getEnergyHeight(energyLevels.evening) }"></div>
                                            </div>
                                            <div class="btn-group btn-group-sm mt-2" role="group">
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.evening === 'low' }"
                                                    @click="selectEnergyLevel('evening', 'low')">Low</button>
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.evening === 'medium' }"
                                                    @click="selectEnergyLevel('evening', 'medium')">Med</button>
                                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 'active': energyLevels.evening === 'high' }"
                                                    @click="selectEnergyLevel('evening', 'high')">High</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Submit Section -->
                        <div class="text-center mt-5 wow fadeInUp" data-wow-delay="0.6s">
                            <button 
                                class="btn btn-primary btn-lg rounded-pill px-5 py-3 shadow-sm"
                                @click="submitQuestionnaire"
                            >
                                <i class="fa fa-check me-2"></i>
                                Get My Wellness Plan
                            </button>
                            <p class="text-muted mt-3 small">
                                Your responses help us create a personalized wellness journey
                            </p>
                        </div>

                    </div>
                    </div>
            </div>
        </section>
</div>
        </template>
<style scoped>
/* Slide fade animation */
.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Custom styles for the questionnaire page */
.bg-gradient-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.goal-card {
    transition: all 0.3s ease;
    cursor: pointer;
    border: 2px solid transparent;
}

.goal-card:hover {
    transform: translateY(-5px);
    border-color: #667eea;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.goal-card.active {
    border-color: #667eea;
    background-color: rgba(102, 126, 234, 0.1);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.15);
}

.emoji-wrapper {
    transition: all 0.3s ease;
    cursor: pointer;
    padding: 10px;
    border-radius: 50%;
    border: 3px solid transparent;
}

.emoji-wrapper:hover {
    transform: scale(1.1);
    border-color: #667eea;
    background-color: rgba(102, 126, 234, 0.1);
}

.emoji-wrapper.active {
    border-color: #667eea;
    background-color: rgba(102, 126, 234, 0.15);
    transform: scale(1.1);
}

.stress-slider-container {
    max-width: 600px;
    margin: 0 auto;
}

.form-range::-webkit-slider-thumb {
    background: #667eea;
    border: 3px solid white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.form-range::-moz-range-thumb {
    background: #667eea;
    border: 3px solid white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.habit-item {
    transition: all 0.2s ease;
    cursor: pointer;
}

.habit-item:hover {
    background-color: rgba(102, 126, 234, 0.05);
    border-color: #667eea;
}

.habit-item.active {
    background-color: rgba(102, 126, 234, 0.1);
    border-color: #667eea;
}

.energy-bar {
    background-color: #f8f9fa;
    border-radius: 4px;
    position: relative;
    overflow: hidden;
}

.energy-fill {
    position: absolute;
    bottom: 0;
    width: 100%;
    transition: all 0.3s ease;
}

.btn-group .btn.active {
    background-color: #667eea;
    border-color: #667eea;
    color: white;
}

/* Database questions styling */
.btn-outline-primary.active {
    background-color: #667eea;
    border-color: #667eea;
    color: white;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .sleep-option span {
        font-size: 2.5rem !important;
    }

    .btn-group .btn {
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
    }
}

@media (max-width: 576px) {
    .goal-card {
        padding: 1rem !important;
    }

    .energy-bar {
        width: 30px !important;
        height: 60px !important;
    }
}
</style>