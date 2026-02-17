<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import AOS from "aos";
import "aos/dist/aos.css";

const router = useRouter();
const route = useRoute();
const history = ref([]);
const loading = ref(true);
const userName = ref('User');

// Computed Properties
const latestResult = computed(() => {
    return history.value.length > 0 ? history.value[0] : null;
});

// Helper Functions
const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// Determine severity based on score
const determineSeverity = (score) => {
    if (score > 15) return 'severe';
    if (score > 8) return 'mild';
    return 'healthy';
};

// Lifecycle & Data Fetching
onMounted(async () => {
    AOS.init({
        duration: 800,
        once: true,
    });

    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            const userObj = JSON.parse(userStr);
            userName.value = userObj.username || 'User';
        } catch (e) {
            console.error("Error parsing user data", e);
        }
    }

    const token = localStorage.getItem('token');
    if (!token) {
        router.push('/login');
        return;
    }

    try {
        const res = await fetch('/api/wellness-history', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (res.ok) {
            history.value = await res.json();
            
            // Store the latest result in localStorage for dashboard
            if (history.value.length > 0) {
                const latest = history.value[0];
                
                // Get user ID
                let userId = 'guest';
                if (userStr) {
                    const userData = JSON.parse(userStr);
                    userId = userData.id || userData.userId || Date.now().toString();
                }
                
                const assessmentResult = {
                    score: latest.score || 0,
                    severity: determineSeverity(latest.score || 0),
                    date: latest.date || new Date().toISOString(),
                    diagnosis: latest.diagnosis || 'Assessment Complete',
                    advice: latest.advice || 'Keep up the good work!',
                    userId: userId
                };
                
                // Store in localStorage for dashboard to detect
                localStorage.setItem('assessmentResult', JSON.stringify(assessmentResult));
                
                // Also store in user's assessment history if not already there
                const historyKey = `assessmentHistory_${userId}`;
                const localHistory = JSON.parse(localStorage.getItem(historyKey) || '[]');
                
                // Check if this assessment is already in local history
                const exists = localHistory.some(item => 
                    item.date === assessmentResult.date && item.score === assessmentResult.score
                );
                
                if (!exists) {
                    localHistory.unshift(assessmentResult);
                    localStorage.setItem(historyKey, JSON.stringify(localHistory));
                }
                
                // Clear processed flag to ensure dashboard picks it up
                const lastProcessedKey = `lastProcessedAssessment_${userId}`;
                localStorage.removeItem(lastProcessedKey);
                
                console.log('Assessment result stored in localStorage:', assessmentResult);
            }
        } else {
            if (res.status === 401) {
                localStorage.removeItem('token');
                router.push('/login');
            }
            console.error("Failed to fetch history");
        }
    } catch (e) {
        console.error("Network error:", e);
    } finally {
        loading.value = false;
        setTimeout(() => { AOS.refresh(); }, 100);
    }
});

// Navigate to new assessment
const goToNewAssessment = () => {
    router.push('/dynamicques');
};
</script>

<template>
    <div class="report-page py-5">
        <div class="container">

            <div class="d-flex justify-content-between align-items-center mb-5" data-aos="fade-in">
                <div>
                    <h1 class="fw-bold">{{ userName }}'s Wellness Journey</h1>
                    <p class="text-muted mb-0">Your assessment history and progress.</p>
                </div>
                <button @click="goToNewAssessment" class="btn btn-outline-primary rounded-pill px-4">
                    New Check-in
                </button>
            </div>

            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

            <div v-else>
                <!-- Latest Result Card -->
                <div v-if="latestResult"
                    class="card border-0 shadow-lg mb-5 bg-primary text-white rounded-4 overflow-hidden"
                    data-aos="fade-up">
                    <div class="card-body p-5 text-center position-relative">
                        <div class="bg-circle-overlay"></div>

                        <div class="position-relative z-1">
                            <h6 class="text-uppercase opacity-75 mb-3 letter-spacing-2">
                                Latest • {{ formatDate(latestResult.date) }}
                            </h6>
                            <div class="display-1 fw-bold mb-2">{{ latestResult.score }}</div>
                            <h2 class="fw-bold mb-3">{{ latestResult.diagnosis || 'Assessment Complete' }}</h2>

                            <div class="mx-auto p-3 rounded bg-white bg-opacity-10 backdrop-blur"
                                style="max-width: 700px;">
                                <i class="fa fa-quote-left opacity-50 mb-2 fs-5"></i>
                                <p class="lead mb-0 fst-italic">
                                    {{ latestResult.advice }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else class="text-center py-5 text-muted" data-aos="fade-up">
                    <h4>No Assessments Yet</h4>
                    <p>Complete your first questionnaire to see your results here.</p>
                    <button @click="goToNewAssessment" class="btn btn-primary mt-3">Start Now</button>
                </div>

                <!-- History Log -->
                <div v-if="history.length > 0" data-aos="fade-up" data-aos-delay="200">
                    <h4 class="fw-bold mb-4 ps-2 border-start border-4 border-primary">History Log</h4>

                    <div class="list-group shadow-sm rounded-4 overflow-hidden border-0">
                        <div v-for="(item, index) in history" :key="item.id || index"
                            class="list-group-item list-group-item-action p-4 d-flex align-items-center justify-content-between border-light">

                            <div class="d-flex align-items-center flex-grow-1">
                                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center me-3 text-secondary fw-bold flex-shrink-0"
                                    style="width: 50px; height: 50px;">
                                    {{ history.length - index }}
                                </div>

                                <div class="pe-3">
                                    <h5 class="mb-1 fw-bold text-dark">{{ item.diagnosis || 'Check-in' }}</h5>

                                    <div class="mb-1 text-muted small">
                                        <i class="fa fa-calendar-alt me-1"></i> {{ formatDate(item.date) }}
                                    </div>
                                    <p class="mb-0 text-secondary small text-truncate" style="max-width: 500px;">
                                        💡 {{ item.advice }}
                                    </p>
                                </div>
                            </div>

                            <div class="text-end ps-3">
                                <span class="d-block h3 fw-bold mb-0 text-primary">{{ item.score }}</span>
                                <span class="small text-muted text-uppercase" style="font-size: 0.7rem;">Total
                                    Score</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<style scoped>
.rounded-4 {
    border-radius: 1.5rem !important;
}

.bg-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.bg-circle-overlay {
    position: absolute;
    top: -50%;
    left: -20%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 70%);
    pointer-events: none;
}

.letter-spacing-2 {
    letter-spacing: 2px;
}

.backdrop-blur {
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}

.list-group-item {
    transition: background-color 0.2s, transform 0.2s;
    border-left: 0;
    border-right: 0;
}

.list-group-item:hover {
    background-color: #f8f9fa;
    transform: translateX(5px);
    z-index: 2;
    cursor: default;
}
</style>