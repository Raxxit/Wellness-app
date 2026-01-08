<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { WOW } from 'wowjs';

// Reactive state for all questions
const selectedGoals = ref([]);
const selectedSleepQuality = ref(null);
const selectedStressLevel = ref(5);
const selectedHabits = ref([]);
const energyLevels = ref({
  morning: null,
  afternoon: null, 
  evening: null
});

// Yes/No questions state (Questions 1-5)
const yesNoAnswers = ref({
  hasChronicCondition: null,
  takesMedication: null,
  drinksAlcohol: null,
  smokes: null,
  exercisesRegularly: null
});

// Multiple choice questions state (Questions 6-10)
const multipleChoiceAnswers = ref({
  workSchedule: null,
  mealFrequency: null,
  waterIntake: null,
  screenTime: null,
  workLifeBalance: null
});

// Validation states
const validationErrors = ref({
  goals: '',
  sleepQuality: '',
  energyMorning: '',
  energyAfternoon: '',
  energyEvening: '',
  yesNoQuestions: '',
  multipleChoiceQuestions: ''
});

const hasSubmitted = ref(false);

// Yes/No functions
const selectYesNo = (question, value) => {
  yesNoAnswers.value[question] = value;
  validateYesNoQuestions();
};

// Multiple choice functions
const selectMultipleChoice = (question, value) => {
  multipleChoiceAnswers.value[question] = value;
  validateMultipleChoiceQuestions();
};

// Existing functions - EXACTLY THE SAME AS YOUR ORIGINAL
const toggleGoal = (goal) => {
  const index = selectedGoals.value.indexOf(goal);
  if (index === -1) {
    selectedGoals.value.push(goal);
  } else {
    selectedGoals.value.splice(index, 1);
  }
  validateGoals();
};

const selectSleepQuality = (quality) => {
  selectedSleepQuality.value = quality;
  validateSleepQuality();
};

const toggleHabit = (habit) => {
  const index = selectedHabits.value.indexOf(habit);
  if (index === -1) {
    selectedHabits.value.push(habit);
  } else {
    selectedHabits.value.splice(index, 1);
  }
  validateHabits();
};

const selectEnergyLevel = (time, level) => {
  energyLevels.value[time] = level;
  validateEnergyLevel(time);
};

const getEnergyClass = (level) => {
  switch(level) {
    case 'low': return 'bg-danger';
    case 'medium': return 'bg-warning';
    case 'high': return 'bg-success';
    default: return 'bg-secondary';
  }
};

const getEnergyHeight = (level) => {
  switch(level) {
    case 'low': return '30%';
    case 'medium': return '60%';
    case 'high': return '90%';
    default: return '0%';
  }
};

// Validation functions - EXACTLY THE SAME AS YOUR ORIGINAL
const validateGoals = () => {
  if (selectedGoals.value.length === 0) {
    validationErrors.value.goals = 'Please select at least one wellness goal';
    return false;
  }
  validationErrors.value.goals = '';
  return true;
};

const validateSleepQuality = () => {
  if (!selectedSleepQuality.value) {
    validationErrors.value.sleepQuality = 'Please rate your sleep quality';
    return false;
  }
  validationErrors.value.sleepQuality = '';
  return true;
};

const validateHabits = () => {
  validationErrors.value.habits = '';
  return true;
};

const validateEnergyLevel = (time) => {
  if (!energyLevels.value[time]) {
    validationErrors.value[`energy${time.charAt(0).toUpperCase() + time.slice(1)}`] = `Please select your ${time} energy level`;
    return false;
  }
  validationErrors.value[`energy${time.charAt(0).toUpperCase() + time.slice(1)}`] = '';
  return true;
};

const validateAllEnergyLevels = () => {
  const morningValid = validateEnergyLevel('morning');
  const afternoonValid = validateEnergyLevel('afternoon');
  const eveningValid = validateEnergyLevel('evening');
  return morningValid && afternoonValid && eveningValid;
};

// New validation for Yes/No questions
const validateYesNoQuestions = () => {
  const allAnswered = Object.values(yesNoAnswers.value).every(answer => answer !== null);
  if (!allAnswered) {
    validationErrors.value.yesNoQuestions = 'Please answer all Yes/No questions';
    return false;
  }
  validationErrors.value.yesNoQuestions = '';
  return true;
};

// New validation for Multiple Choice questions
const validateMultipleChoiceQuestions = () => {
  const allAnswered = Object.values(multipleChoiceAnswers.value).every(answer => answer !== null);
  if (!allAnswered) {
    validationErrors.value.multipleChoiceQuestions = 'Please answer all multiple choice questions';
    return false;
  }
  validationErrors.value.multipleChoiceQuestions = '';
  return true;
};

// Combined validation
const validateForm = () => {
  const yesNoValid = validateYesNoQuestions();
  const multiValid = validateMultipleChoiceQuestions();
  const goalsValid = validateGoals();
  const sleepValid = validateSleepQuality();
  const energyValid = validateAllEnergyLevels();
  
  return yesNoValid && multiValid && goalsValid && sleepValid && energyValid;
};

const isFormValid = computed(() => {
  return Object.values(yesNoAnswers.value).every(answer => answer !== null) &&
         Object.values(multipleChoiceAnswers.value).every(answer => answer !== null) &&
         selectedGoals.value.length > 0 &&
         selectedSleepQuality.value !== null &&
         energyLevels.value.morning !== null &&
         energyLevels.value.afternoon !== null &&
         energyLevels.value.evening !== null;
});

// Watch for changes to auto-validate
watch([selectedGoals, selectedSleepQuality, selectedHabits, energyLevels, yesNoAnswers, multipleChoiceAnswers], () => {
  if (hasSubmitted.value) {
    validateForm();
  }
}, { deep: true });

// Form submission handler - EXACTLY THE SAME AS YOUR ORIGINAL
const submitQuestionnaire = () => {
  hasSubmitted.value = true;
  
  if (!validateForm()) {
    // Scroll to first error
    setTimeout(() => {
      const firstError = document.querySelector('.has-error');
      if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
    return;
  }
  
  const data = {
    yesNoAnswers: yesNoAnswers.value,
    multipleChoiceAnswers: multipleChoiceAnswers.value,
    goals: selectedGoals.value,
    sleepQuality: selectedSleepQuality.value,
    stressLevel: selectedStressLevel.value,
    habits: selectedHabits.value,
    energyLevels: energyLevels.value
  };
  
  console.log('Submitting questionnaire:', data);
  
  // Show success message
  alert('✅ Wellness assessment submitted successfully! Your personalized plan is being created.');
  
  // Reset form (optional)
  // resetForm();
};

onMounted(() => {
  new WOW().init();
})
</script>

<template>
    <div class="questionnaire-page">

        <!-- Header Section - EXACTLY THE SAME AS YOUR ORIGINAL -->
        <header class="py-5 bg-gradient-primary border-bottom">
            <div class="container text-center">
                <h1 class="display-4 fw-bold text-white wow fadeInUp" data-wow-delay="0.1s">
                    Wellness Assessment
                </h1>
                <p class="lead text-light wow fadeInUp" data-wow-delay="0.2s">
                    Take 5 minutes to help us personalize your wellness journey
                </p>
                <div class="progress mt-4 wow fadeInUp" data-wow-delay="0.3s" style="height: 8px; max-width: 300px; margin: 0 auto;">
                    <div class="progress-bar bg-white" style="width: 25%"></div>
                </div>
            </div>
        </header>

        <!-- Questionnaire Form -->
        <section class="py-5">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-12 col-lg-8">
                        
                        <!-- SECTION 1: Yes/No Questions (1-5) -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.1s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    1. Health & Lifestyle Questions
                                    <span class="text-danger">*</span>
                                </h4>
                                <p class="text-muted mb-4">Please answer these quick yes/no questions</p>
                                
                                <!-- Question 1.1 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">Do you have any chronic health conditions? (e.g., diabetes, hypertension)</p>
                                    <div class="btn-group" role="group">
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.hasChronicCondition === true }"
                                            @click="selectYesNo('hasChronicCondition', true)"
                                        >
                                            Yes
                                        </button>
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.hasChronicCondition === false }"
                                            @click="selectYesNo('hasChronicCondition', false)"
                                        >
                                            No
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 1.2 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">Do you take any regular medication?</p>
                                    <div class="btn-group" role="group">
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.takesMedication === true }"
                                            @click="selectYesNo('takesMedication', true)"
                                        >
                                            Yes
                                        </button>
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.takesMedication === false }"
                                            @click="selectYesNo('takesMedication', false)"
                                        >
                                            No
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 1.3 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">Do you drink alcohol regularly? (more than 2 drinks per week)</p>
                                    <div class="btn-group" role="group">
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.drinksAlcohol === true }"
                                            @click="selectYesNo('drinksAlcohol', true)"
                                        >
                                            Yes
                                        </button>
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.drinksAlcohol === false }"
                                            @click="selectYesNo('drinksAlcohol', false)"
                                        >
                                            No
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 1.4 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">Do you smoke or use tobacco products?</p>
                                    <div class="btn-group" role="group">
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.smokes === true }"
                                            @click="selectYesNo('smokes', true)"
                                        >
                                            Yes
                                        </button>
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.smokes === false }"
                                            @click="selectYesNo('smokes', false)"
                                        >
                                            No
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 1.5 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">Do you exercise for at least 30 minutes, 3 times per week?</p>
                                    <div class="btn-group" role="group">
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.exercisesRegularly === true }"
                                            @click="selectYesNo('exercisesRegularly', true)"
                                        >
                                            Yes
                                        </button>
                                        <button 
                                            type="button" 
                                            class="btn btn-outline-primary"
                                            :class="{ 'active': yesNoAnswers.exercisesRegularly === false }"
                                            @click="selectYesNo('exercisesRegularly', false)"
                                        >
                                            No
                                        </button>
                                    </div>
                                </div>

                                <!-- Error message -->
                                <div v-if="hasSubmitted && validationErrors.yesNoQuestions" class="alert alert-danger mt-3">
                                    <i class="fas fa-exclamation-circle me-2"></i>
                                    {{ validationErrors.yesNoQuestions }}
                                </div>
                            </div>
                        </div>

                        <!-- SECTION 2: Multiple Choice Questions (6-10) -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.2s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    2. Daily Life & Habits
                                    <span class="text-danger">*</span>
                                </h4>
                                <p class="text-muted mb-4">Choose the option that best describes your situation</p>
                                
                                <!-- Question 2.1 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">What is your typical work schedule?</p>
                                    <div class="options-grid">
                                        <button 
                                            v-for="option in ['9-5 office job', 'Shift work', 'Remote/flexible', 'Unemployed/retired']"
                                            :key="option"
                                            class="option-btn"
                                            :class="{ 'active': multipleChoiceAnswers.workSchedule === option }"
                                            @click="selectMultipleChoice('workSchedule', option)"
                                        >
                                            {{ option }}
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 2.2 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">How many meals do you eat per day?</p>
                                    <div class="options-grid">
                                        <button 
                                            v-for="option in ['1-2 meals', '3 regular meals', '3 meals + snacks', 'Irregular schedule']"
                                            :key="option"
                                            class="option-btn"
                                            :class="{ 'active': multipleChoiceAnswers.mealFrequency === option }"
                                            @click="selectMultipleChoice('mealFrequency', option)"
                                        >
                                            {{ option }}
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 2.3 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">How much water do you drink daily?</p>
                                    <div class="options-grid">
                                        <button 
                                            v-for="option in ['Less than 4 glasses', '4-6 glasses', '7-8 glasses', 'More than 8 glasses']"
                                            :key="option"
                                            class="option-btn"
                                            :class="{ 'active': multipleChoiceAnswers.waterIntake === option }"
                                            @click="selectMultipleChoice('waterIntake', option)"
                                        >
                                            {{ option }}
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 2.4 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">Daily screen time (outside of work)?</p>
                                    <div class="options-grid">
                                        <button 
                                            v-for="option in ['Less than 1 hour', '1-3 hours', '3-5 hours', 'More than 5 hours']"
                                            :key="option"
                                            class="option-btn"
                                            :class="{ 'active': multipleChoiceAnswers.screenTime === option }"
                                            @click="selectMultipleChoice('screenTime', option)"
                                        >
                                            {{ option }}
                                        </button>
                                    </div>
                                </div>

                                <!-- Question 2.5 -->
                                <div class="question-item mb-3">
                                    <p class="fw-bold mb-2">How would you rate your work-life balance?</p>
                                    <div class="options-grid">
                                        <button 
                                            v-for="option in ['Poor', 'Fair', 'Good', 'Excellent']"
                                            :key="option"
                                            class="option-btn"
                                            :class="{ 'active': multipleChoiceAnswers.workLifeBalance === option }"
                                            @click="selectMultipleChoice('workLifeBalance', option)"
                                        >
                                            {{ option }}
                                        </button>
                                    </div>
                                </div>

                                <!-- Error message -->
                                <div v-if="hasSubmitted && validationErrors.multipleChoiceQuestions" class="alert alert-danger mt-3">
                                    <i class="fas fa-exclamation-circle me-2"></i>
                                    {{ validationErrors.multipleChoiceQuestions }}
                                </div>
                            </div>
                        </div>

                        <!-- SECTION 3: Original Questions (11-15) -->

                        <!-- Question 3: Wellness Goals - EXACTLY THE SAME AS YOUR ORIGINAL -->
                        <div 
                            class="card shadow-sm border-0 mb-4 wow fadeInUp" 
                            data-wow-delay="0.3s"
                            :class="{ 'has-error': validationErrors.goals }"
                        >
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    3. What are your primary wellness goals?
                                    <span class="text-danger">*</span>
                                </h4>
                                <p class="text-muted mb-4">Select all that apply</p>
                                
                                <div class="row g-3">
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('stress'), 'error-border': validationErrors.goals }"
                                            @click="toggleGoal('stress')"
                                        >
                                            <div class="display-4 mb-2">🧘</div>
                                            <p class="mb-0 fw-medium">Stress Relief</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('sleep'), 'error-border': validationErrors.goals }"
                                            @click="toggleGoal('sleep')"
                                        >
                                            <div class="display-4 mb-2">😴</div>
                                            <p class="mb-0 fw-medium">Better Sleep</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('energy'), 'error-border': validationErrors.goals }"
                                            @click="toggleGoal('energy')"
                                        >
                                            <div class="display-4 mb-2">💪</div>
                                            <p class="mb-0 fw-medium">More Energy</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('mindfulness'), 'error-border': validationErrors.goals }"
                                            @click="toggleGoal('mindfulness')"
                                        >
                                            <div class="display-4 mb-2">🧠</div>
                                            <p class="mb-0 fw-medium">Mindfulness</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('mental'), 'error-border': validationErrors.goals }"
                                            @click="toggleGoal('mental')"
                                        >
                                            <div class="display-4 mb-2">❤️</div>
                                            <p class="mb-0 fw-medium">Mental Health</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="goal-card text-center p-3 rounded border hover-effect"
                                            :class="{ 'active': selectedGoals.includes('nutrition'), 'error-border': validationErrors.goals }"
                                            @click="toggleGoal('nutrition')"
                                        >
                                            <div class="display-4 mb-2">🥗</div>
                                            <p class="mb-0 fw-medium">Nutrition</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Error message -->
                                <div v-if="validationErrors.goals" class="error-message mt-3">
                                    <i class="fas fa-exclamation-circle me-2 text-danger"></i>
                                    <span class="text-danger">{{ validationErrors.goals }}</span>
                                </div>
                                
                                <div v-if="selectedGoals.length > 0" class="selected-goals mt-3">
                                    <small class="text-success">
                                        <i class="fas fa-check-circle me-1"></i>
                                        Selected: {{ selectedGoals.length }} goal{{ selectedGoals.length !== 1 ? 's' : '' }}
                                    </small>
                                </div>
                            </div>
                        </div>

                        <!-- Question 4: Sleep Quality - EXACTLY THE SAME AS YOUR ORIGINAL -->
                        <div 
                            class="card shadow-sm border-0 mb-4 wow fadeInUp" 
                            data-wow-delay="0.4s"
                            :class="{ 'has-error': validationErrors.sleepQuality }"
                        >
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    4. How would you rate your sleep quality?
                                    <span class="text-danger">*</span>
                                </h4>
                                
                                <div class="d-flex justify-content-between align-items-center">
                                    <div 
                                        class="sleep-option text-center"
                                        @click="selectSleepQuality('poor')"
                                    >
                                        <div 
                                            class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 
                                                'active': selectedSleepQuality === 'poor',
                                                'error-border': validationErrors.sleepQuality 
                                            }"
                                        >
                                            <span class="display-4">😴</span>
                                        </div>
                                        <p class="small mb-0">Poor</p>
                                    </div>
                                    <div 
                                        class="sleep-option text-center"
                                        @click="selectSleepQuality('fair')"
                                    >
                                        <div 
                                            class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 
                                                'active': selectedSleepQuality === 'fair',
                                                'error-border': validationErrors.sleepQuality 
                                            }"
                                        >
                                            <span class="display-4">😐</span>
                                        </div>
                                        <p class="small mb-0">Fair</p>
                                    </div>
                                    <div 
                                        class="sleep-option text-center"
                                        @click="selectSleepQuality('good')"
                                    >
                                        <div 
                                            class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 
                                                'active': selectedSleepQuality === 'good',
                                                'error-border': validationErrors.sleepQuality 
                                            }"
                                        >
                                            <span class="display-4">😊</span>
                                        </div>
                                        <p class="small mb-0">Good</p>
                                    </div>
                                    <div 
                                        class="sleep-option text-center"
                                        @click="selectSleepQuality('great')"
                                    >
                                        <div 
                                            class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 
                                                'active': selectedSleepQuality === 'great',
                                                'error-border': validationErrors.sleepQuality 
                                            }"
                                        >
                                            <span class="display-4">😄</span>
                                        </div>
                                        <p class="small mb-0">Great</p>
                                    </div>
                                    <div 
                                        class="sleep-option text-center"
                                        @click="selectSleepQuality('excellent')"
                                    >
                                        <div 
                                            class="emoji-wrapper mb-2 mx-auto"
                                            :class="{ 
                                                'active': selectedSleepQuality === 'excellent',
                                                'error-border': validationErrors.sleepQuality 
                                            }"
                                        >
                                            <span class="display-4">🤩</span>
                                        </div>
                                        <p class="small mb-0">Excellent</p>
                                    </div>
                                </div>
                                
                                <!-- Error message -->
                                <div v-if="validationErrors.sleepQuality" class="error-message mt-3">
                                    <i class="fas fa-exclamation-circle me-2 text-danger"></i>
                                    <span class="text-danger">{{ validationErrors.sleepQuality }}</span>
                                </div>
                                
                                <div v-if="selectedSleepQuality" class="selected-sleep mt-3">
                                    <small class="text-success">
                                        <i class="fas fa-check-circle me-1"></i>
                                        Selected: {{ selectedSleepQuality.charAt(0).toUpperCase() + selectedSleepQuality.slice(1) }}
                                    </small>
                                </div>
                            </div>
                        </div>

                        <!-- Question 5: Stress Level Slider - EXACTLY THE SAME AS YOUR ORIGINAL -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.5s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-4">
                                    5. Current stress level
                                </h4>
                                
                                <div class="stress-slider-container">
                                    <div class="d-flex justify-content-between mb-2">
                                        <span class="text-muted">Very Low</span>
                                        <span class="text-muted">Very High</span>
                                    </div>
                                    <input 
                                        type="range" 
                                        class="form-range" 
                                        min="1" 
                                        max="10" 
                                        step="1" 
                                        style="height: 12px; cursor: pointer;"
                                        v-model="selectedStressLevel"
                                    >
                                    <div class="d-flex justify-content-between mt-1">
                                        <span class="badge bg-success">Calm</span>
                                        <span class="badge bg-warning">Moderate</span>
                                        <span class="badge bg-danger">Stressed</span>
                                    </div>
                                    <div class="text-center mt-3">
                                        <span class="badge bg-primary">
                                            Current Level: {{ selectedStressLevel }}/10
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Question 6: Daily Habits - EXACTLY THE SAME AS YOUR ORIGINAL -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.6s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    6. Which wellness activities do you currently practice?
                                </h4>
                                <p class="text-muted mb-3 small">(Optional)</p>
                                
                                <div class="row g-2">
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('meditation') }"
                                            @click="toggleHabit('meditation')"
                                        >
                                            <div class="form-check form-check-inline m-0">
                                                <input 
                                                    class="form-check-input" 
                                                    type="checkbox" 
                                                    id="meditation"
                                                    :checked="selectedHabits.includes('meditation')"
                                                    @change="toggleHabit('meditation')"
                                                >
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="meditation">
                                                Meditation
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('exercise') }"
                                            @click="toggleHabit('exercise')"
                                        >
                                            <div class="form-check form-check-inline m-0">
                                                <input 
                                                    class="form-check-input" 
                                                    type="checkbox" 
                                                    id="exercise"
                                                    :checked="selectedHabits.includes('exercise')"
                                                    @change="toggleHabit('exercise')"
                                                >
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="exercise">
                                                Exercise
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('journaling') }"
                                            @click="toggleHabit('journaling')"
                                        >
                                            <div class="form-check form-check-inline m-0">
                                                <input 
                                                    class="form-check-input" 
                                                    type="checkbox" 
                                                    id="journaling"
                                                    :checked="selectedHabits.includes('journaling')"
                                                    @change="toggleHabit('journaling')"
                                                >
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="journaling">
                                                Journaling
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('yoga') }"
                                            @click="toggleHabit('yoga')"
                                        >
                                            <div class="form-check form-check-inline m-0">
                                                <input 
                                                    class="form-check-input" 
                                                    type="checkbox" 
                                                    id="yoga"
                                                    :checked="selectedHabits.includes('yoga')"
                                                    @change="toggleHabit('yoga')"
                                                >
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="yoga">
                                                Yoga
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('walking') }"
                                            @click="toggleHabit('walking')"
                                        >
                                            <div class="form-check form-check-inline m-0">
                                                <input 
                                                    class="form-check-input" 
                                                    type="checkbox" 
                                                    id="walking"
                                                    :checked="selectedHabits.includes('walking')"
                                                    @change="toggleHabit('walking')"
                                                >
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="walking">
                                                Walking
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div 
                                            class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                            :class="{ 'active': selectedHabits.includes('breathing') }"
                                            @click="toggleHabit('breathing')"
                                        >
                                            <div class="form-check form-check-inline m-0">
                                                <input 
                                                    class="form-check-input" 
                                                    type="checkbox" 
                                                    id="breathing"
                                                    :checked="selectedHabits.includes('breathing')"
                                                    @change="toggleHabit('breathing')"
                                                >
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="breathing">
                                                Breathing
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                
                                <div v-if="selectedHabits.length > 0" class="selected-habits mt-3">
                                    <small class="text-success">
                                        <i class="fas fa-check-circle me-1"></i>
                                        Selected {{ selectedHabits.length }} habit{{ selectedHabits.length !== 1 ? 's' : '' }}
                                    </small>
                                </div>
                            </div>
                        </div>

                        <!-- Question 7: Energy Level - EXACTLY THE SAME AS YOUR ORIGINAL -->
                        <div 
                            class="card shadow-sm border-0 mb-4 wow fadeInUp" 
                            data-wow-delay="0.7s"
                            :class="{ 'has-error': validationErrors.energyMorning || validationErrors.energyAfternoon || validationErrors.energyEvening }"
                        >
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-4">
                                    7. How's your energy throughout the day?
                                    <span class="text-danger">*</span>
                                </h4>
                                
                                <div class="energy-chart">
                                    <div class="row text-center">
                                        <!-- Morning Energy -->
                                        <div class="col" :class="{ 'has-error': validationErrors.energyMorning }">
                                            <p class="small text-muted mb-1">Morning</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div 
                                                    class="energy-fill rounded-top"
                                                    :class="getEnergyClass(energyLevels.morning)"
                                                    :style="{ height: getEnergyHeight(energyLevels.morning) }"
                                                ></div>
                                            </div>
                                            <div class="btn-group btn-group-sm mt-2" role="group">
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.morning === 'low',
                                                        'error-border': validationErrors.energyMorning 
                                                    }"
                                                    @click="selectEnergyLevel('morning', 'low')"
                                                >Low</button>
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.morning === 'medium',
                                                        'error-border': validationErrors.energyMorning 
                                                    }"
                                                    @click="selectEnergyLevel('morning', 'medium')"
                                                >Med</button>
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.morning === 'high',
                                                        'error-border': validationErrors.energyMorning 
                                                    }"
                                                    @click="selectEnergyLevel('morning', 'high')"
                                                >High</button>
                                            </div>
                                            <div v-if="validationErrors.energyMorning" class="error-message mt-1">
                                                <small class="text-danger">{{ validationErrors.energyMorning }}</small>
                                            </div>
                                        </div>
                                        
                                        <!-- Afternoon Energy -->
                                        <div class="col" :class="{ 'has-error': validationErrors.energyAfternoon }">
                                            <p class="small text-muted mb-1">Afternoon</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div 
                                                    class="energy-fill rounded-top"
                                                    :class="getEnergyClass(energyLevels.afternoon)"
                                                    :style="{ height: getEnergyHeight(energyLevels.afternoon) }"
                                                ></div>
                                            </div>
                                            <div class="btn-group btn-group-sm mt-2" role="group">
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.afternoon === 'low',
                                                        'error-border': validationErrors.energyAfternoon 
                                                    }"
                                                    @click="selectEnergyLevel('afternoon', 'low')"
                                                >Low</button>
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.afternoon === 'medium',
                                                        'error-border': validationErrors.energyAfternoon 
                                                    }"
                                                    @click="selectEnergyLevel('afternoon', 'medium')"
                                                >Med</button>
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.afternoon === 'high',
                                                        'error-border': validationErrors.energyAfternoon 
                                                    }"
                                                    @click="selectEnergyLevel('afternoon', 'high')"
                                                >High</button>
                                            </div>
                                            <div v-if="validationErrors.energyAfternoon" class="error-message mt-1">
                                                <small class="text-danger">{{ validationErrors.energyAfternoon }}</small>
                                            </div>
                                        </div>
                                        
                                        <!-- Evening Energy -->
                                        <div class="col" :class="{ 'has-error': validationErrors.energyEvening }">
                                            <p class="small text-muted mb-1">Evening</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div 
                                                    class="energy-fill rounded-top"
                                                    :class="getEnergyClass(energyLevels.evening)"
                                                    :style="{ height: getEnergyHeight(energyLevels.evening) }"
                                                ></div>
                                            </div>
                                            <div class="btn-group btn-group-sm mt-2" role="group">
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.evening === 'low',
                                                        'error-border': validationErrors.energyEvening 
                                                    }"
                                                    @click="selectEnergyLevel('evening', 'low')"
                                                >Low</button>
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.evening === 'medium',
                                                        'error-border': validationErrors.energyEvening 
                                                    }"
                                                    @click="selectEnergyLevel('evening', 'medium')"
                                                >Med</button>
                                                <button 
                                                    type="button" 
                                                    class="btn btn-outline-secondary btn-sm"
                                                    :class="{ 
                                                        'active': energyLevels.evening === 'high',
                                                        'error-border': validationErrors.energyEvening 
                                                    }"
                                                    @click="selectEnergyLevel('evening', 'high')"
                                                >High</button>
                                            </div>
                                            <div v-if="validationErrors.energyEvening" class="error-message mt-1">
                                                <small class="text-danger">{{ validationErrors.energyEvening }}</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div v-if="energyLevels.morning && energyLevels.afternoon && energyLevels.evening" 
                                     class="selected-energy mt-3 text-center">
                                    <small class="text-success">
                                        <i class="fas fa-check-circle me-1"></i>
                                        All energy levels set
                                    </small>
                                </div>
                            </div>
                        </div>

                        <!-- Validation Summary - EXACTLY THE SAME AS YOUR ORIGINAL -->
                        <div v-if="hasSubmitted && !isFormValid" class="alert alert-danger wow fadeInUp" data-wow-delay="0.8s">
                            <h5 class="alert-heading">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                Please complete all required fields
                            </h5>
                            <ul class="mb-0 mt-2">
                                <li v-if="validationErrors.yesNoQuestions">{{ validationErrors.yesNoQuestions }}</li>
                                <li v-if="validationErrors.multipleChoiceQuestions">{{ validationErrors.multipleChoiceQuestions }}</li>
                                <li v-if="validationErrors.goals">{{ validationErrors.goals }}</li>
                                <li v-if="validationErrors.sleepQuality">{{ validationErrors.sleepQuality }}</li>
                                <li v-if="validationErrors.energyMorning">{{ validationErrors.energyMorning }}</li>
                                <li v-if="validationErrors.energyAfternoon">{{ validationErrors.energyAfternoon }}</li>
                                <li v-if="validationErrors.energyEvening">{{ validationErrors.energyEvening }}</li>
                            </ul>
                        </div>

                        <!-- Submit Section - EXACTLY THE SAME AS YOUR ORIGINAL -->
                        <div class="text-center mt-5 wow fadeInUp" data-wow-delay="0.9s">
                            <button 
                                class="btn btn-primary btn-lg rounded-pill px-5 py-3 shadow-sm"
                                :class="{ 'disabled': !isFormValid }"
                                :disabled="!isFormValid"
                                @click="submitQuestionnaire"
                            >
                                <i class="fas fa-heartbeat me-2"></i>
                                {{ isFormValid ? 'Get My Wellness Plan' : 'Complete all required fields' }}
                            </button>
                            <p class="text-muted mt-3 small">
                                <span class="text-danger">*</span> Required fields
                            </p>
                            
                            <div v-if="isFormValid" class="alert alert-success mt-3">
                                <i class="fas fa-check-circle me-2"></i>
                                All 15 questions answered! You can now submit your assessment.
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </section>

    </div>
</template>

<style scoped>
/* EXACTLY THE SAME AS YOUR ORIGINAL STYLES */

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

.goal-card.error-border {
    border-color: #dc3545 !important;
    animation: shake 0.5s ease;
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

.emoji-wrapper.error-border {
    border-color: #dc3545 !important;
    animation: pulse 1s infinite;
}

.stress-slider-container {
    max-width: 600px;
    margin: 0 auto;
}

.form-range::-webkit-slider-thumb {
    background: #667eea;
    border: 3px solid white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.form-range::-moz-range-thumb {
    background: #667eea;
    border: 3px solid white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
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

.btn-group .btn.error-border {
    border-color: #dc3545 !important;
    color: #dc3545;
}

.btn-group .btn.error-border.active {
    background-color: #dc3545;
    border-color: #dc3545;
    color: white;
}

.has-error {
    border-left: 4px solid #dc3545;
}

.error-message {
    animation: fadeIn 0.3s ease;
}

.selected-goals, .selected-sleep, .selected-habits, .selected-energy {
    animation: fadeIn 0.5s ease;
}

/* Disabled button styling */
.btn.disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Animations */
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); }
    50% { box-shadow: 0 0 0 5px rgba(220, 53, 69, 0); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
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

/* New styles for yes/no and multiple choice questions */
.question-item {
    padding: 1rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.question-item:last-child {
    border-bottom: none;
}

.btn-group .btn {
    flex: 1;
    border-color: #667eea;
    color: #667eea;
}

.btn-group .btn.active {
    background-color: #667eea;
    border-color: #667eea;
    color: white;
}

.options-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
}

.option-btn {
    padding: 0.75rem 0.5rem;
    border: 2px solid #e9ecef;
    border-radius: 6px;
    background: white;
    color: #495057;
    transition: all 0.2s ease;
    cursor: pointer;
    text-align: center;
    font-weight: 500;
    font-size: 0.9rem;
}

.option-btn:hover {
    border-color: #667eea;
    color: #667eea;
}

.option-btn.active {
    background-color: #667eea;
    border-color: #667eea;
    color: white;
    box-shadow: 0 2px 5px rgba(102, 126, 234, 0.2);
}

/* Responsive adjustments for new questions */
@media (max-width: 768px) {
    .options-grid {
        grid-template-columns: 1fr;
    }
    
    .btn-group .btn {
        padding: 0.5rem;
        font-size: 0.9rem;
    }
}
</style>