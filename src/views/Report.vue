<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import AOS from "aos";
import "aos/dist/aos.css";

const router = useRouter();
const history = ref([]);
const loading = ref(true);
const userName = ref('User');

// --- Computed Properties ---
const latestResult = computed(() => {
    return history.value.length > 0 ? history.value[0] : null;
});

// --- Helper Functions ---
const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// --- Lifecycle & Data Fetching ---
onMounted(async () => {
    // 1. Init Animation
    AOS.init({
        duration: 800,
        once: true,
    });

    // 2. Set User Name
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            const userObj = JSON.parse(userStr);
            userName.value = userObj.username || 'User';
        } catch (e) {
            console.error("Error parsing user data", e);
        }
    }

    // 3. Check Token
    const token = localStorage.getItem('token');
    if (!token) {
        router.push('/login');
        return;
    }

    // 4. Fetch History
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
        } else {
            if (res.status === 401) {
                // Token expired
                localStorage.removeItem('token');
                router.push('/login');
            }
            console.error("Failed to fetch history");
        }
    } catch (e) {
        console.error("Network error:", e);
    } finally {
        loading.value = false;
        // Refresh animations after data loads (ensures new DOM elements animate)
        setTimeout(() => { AOS.refresh(); }, 100);
    }
});
</script>


<template>
    <div class="report-page py-5">
        <div class="container">

            <div class="d-flex justify-content-between align-items-center mb-5" data-aos="fade-in">
                <div>
                    <h1 class="fw-bold">{{ userName }}'s Wellness Journey</h1>
                    <p class="text-muted mb-0">Your assessment history and progress.</p>
                </div>
                <button @click="router.push('/dynamicques')" class="btn btn-outline-primary rounded-pill px-4">
                    New Check-in
                </button>
            </div>

            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

            <div v-else>

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
                    <button @click="router.push('/questionnaire')" class="btn btn-primary mt-3">Start Now</button>
                </div>

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

/* Glassmorphism effect for advice box */
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