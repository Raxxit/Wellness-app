<script setup>
import { onMounted } from 'vue';
import { WOW } from 'wowjs';

onMounted(() => {
    new WOW().init();
})
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
                        
                        <!-- Question 1: Wellness Goals -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.1s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    1. What are your primary wellness goals?
                                </h4>
                                <p class="text-muted mb-4">Select all that apply</p>
                                
                                <div class="row g-3">
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect">
                                            <div class="display-4 mb-2">🧘</div>
                                            <p class="mb-0 fw-medium">Stress Relief</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect">
                                            <div class="display-4 mb-2">😴</div>
                                            <p class="mb-0 fw-medium">Better Sleep</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect">
                                            <div class="display-4 mb-2">💪</div>
                                            <p class="mb-0 fw-medium">More Energy</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect">
                                            <div class="display-4 mb-2">🧠</div>
                                            <p class="mb-0 fw-medium">Mindfulness</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect">
                                            <div class="display-4 mb-2">❤️</div>
                                            <p class="mb-0 fw-medium">Mental Health</p>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="goal-card text-center p-3 rounded border hover-effect">
                                            <div class="display-4 mb-2">🥗</div>
                                            <p class="mb-0 fw-medium">Nutrition</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Question 2: Sleep Quality (UPDATED - removed circle background) -->
                        <div class="card shadow-sm border-0 mb-4 wow fadeInUp" data-wow-delay="0.2s">
                            <div class="card-body p-4">
                                <h4 class="fw-bold text-primary mb-3">
                                    2. How would you rate your sleep quality?
                                </h4>
                                
                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="sleep-option text-center">
                                        <div class="emoji-wrapper mb-2 mx-auto">
                                            <span class="display-4">😴</span>
                                        </div>
                                        <p class="small mb-0">Poor</p>
                                    </div>
                                    <div class="sleep-option text-center">
                                        <div class="emoji-wrapper mb-2 mx-auto">
                                            <span class="display-4">😐</span>
                                        </div>
                                        <p class="small mb-0">Fair</p>
                                    </div>
                                    <div class="sleep-option text-center">
                                        <div class="emoji-wrapper mb-2 mx-auto">
                                            <span class="display-4">😊</span>
                                        </div>
                                        <p class="small mb-0">Good</p>
                                    </div>
                                    <div class="sleep-option text-center">
                                        <div class="emoji-wrapper mb-2 mx-auto">
                                            <span class="display-4">😄</span>
                                        </div>
                                        <p class="small mb-0">Great</p>
                                    </div>
                                    <div class="sleep-option text-center">
                                        <div class="emoji-wrapper mb-2 mx-auto">
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
                                    3. Current stress level
                                </h4>
                                
                                <div class="stress-slider-container">
                                    <div class="d-flex justify-content-between mb-2">
                                        <span class="text-muted">Very Low</span>
                                        <span class="text-muted">Very High</span>
                                    </div>
                                    <input type="range" class="form-range" min="1" max="10" step="1" 
                                           style="height: 12px; cursor: pointer;">
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
                                    4. Which wellness activities do you currently practice?
                                </h4>
                                
                                <div class="row g-2">
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="meditation">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="meditation">
                                                Meditation
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="exercise">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="exercise">
                                                Exercise
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="journaling">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="journaling">
                                                Journaling
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="yoga">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="yoga">
                                                Yoga
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="walking">
                                            </div>
                                            <label class="form-check-label ms-2 mb-0" for="walking">
                                                Walking
                                            </label>
                                        </div>
                                    </div>
                                    <div class="col-6 col-md-4">
                                        <div class="habit-item p-3 border rounded d-flex align-items-center mb-2">
                                            <div class="form-check form-check-inline m-0">
                                                <input class="form-check-input" type="checkbox" id="breathing">
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
                                    5. How's your energy throughout the day?
                                </h4>
                                
                                <div class="energy-chart">
                                    <div class="row text-center">
                                        <div class="col">
                                            <p class="small text-muted mb-1">Morning</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div class="energy-fill bg-warning rounded-top" style="height: 60%;"></div>
                                            </div>
                                            <span class="badge bg-warning mt-2">Medium</span>
                                        </div>
                                        <div class="col">
                                            <p class="small text-muted mb-1">Afternoon</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div class="energy-fill bg-success rounded-top" style="height: 90%;"></div>
                                            </div>
                                            <span class="badge bg-success mt-2">High</span>
                                        </div>
                                        <div class="col">
                                            <p class="small text-muted mb-1">Evening</p>
                                            <div class="energy-bar mx-auto" style="height: 80px; width: 40px;">
                                                <div class="energy-fill bg-danger rounded-top" style="height: 30%;"></div>
                                            </div>
                                            <span class="badge bg-danger mt-2">Low</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Submit Section -->
                        <div class="text-center mt-5 wow fadeInUp" data-wow-delay="0.6s">
                            <button class="btn btn-primary btn-lg rounded-pill px-5 py-3 shadow-sm">
                                <i class="fas fa-heartbeat me-2"></i>
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
    background-color: rgba(102, 126, 234, 0.05);
}

/* Updated emoji styles - no circle background */
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
    background-color: rgba(102, 126, 234, 0.1);
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
    transition: height 0.5s ease;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .sleep-option span {
        font-size: 2.5rem !important;
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