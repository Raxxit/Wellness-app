<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import * as wowModule from "wowjs";
import "wowjs/css/libs/animate.css";

const router = useRouter();
const history = ref([]);
const loading = ref(true);
const userName = ref('User');

// --- Computed Properties ---
// Get the most recent submission (Index 0 because backend sorts by date desc)
const latestResult = computed(() => {
    return history.value.length > 0 ? history.value[0] : null;
});

// onMounted: Fetch Data
onMounted(async () => {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');

    // Set User Name from LocalStorage
    if (userStr) {
        try {
            const userObj = JSON.parse(userStr);
            userName.value = userObj.username || 'User';
        } catch (e) { }
    }

    if (!token) {
        router.push('/login');
        return;
    }

    try {
        const res = await fetch('/api/wellness-history', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            history.value = await res.json();
        } else {
            console.error("Failed to fetch history");
        }
    } catch (e) {
        console.error("Network error:", e);
    } finally {
        loading.value = false;
        // Initialize animations after data load
        setTimeout(() => { new wowModule.WOW().init(); }, 100);
    }
});
</script>

<template>
    <div class="report-page py-5">
        <div class="container">

            <div class="d-flex justify-content-between align-items-center mb-5 wow fadeIn">
                <div>
                    <h1 class="fw-bold">{{ userName }}'s Wellness Journey</h1>
                    <p class="text-muted mb-0">Your assessment history and progress.</p>
                </div>
                <button @click="router.push('/')" class="btn btn-outline-primary rounded-pill px-4">
                    New Check-in
                </button>
            </div>

            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status"></div>
            </div>

            <div v-else>
                <div v-if="latestResult"
                    class="card border-0 shadow-lg mb-5 bg-primary text-white rounded-4 overflow-hidden wow fadeInUp">
                    <div class="card-body p-5 text-center position-relative">
                        <div class="bg-circle-overlay"></div>

                        <div class="position-relative z-1">
                            <h6 class="text-uppercase opacity-75 mb-3 letter-spacing-2">Latest • {{ latestResult.date }}
                            </h6>
                            <div class="display-1 fw-bold mb-2">{{ latestResult.score }}</div>
                            <h2 class="fw-bold mb-3">{{ latestResult.diagnosis }}</h2>
                            <p class="opacity-75 mx-auto" style="max-width: 600px;">
                                This is your current wellness snapshot based on your latest answers.
                            </p>
                        </div>
                    </div>
                </div>

                <div v-else class="text-center py-5 text-muted wow fadeInUp">
                    <h4>No Assessments Yet</h4>
                    <p>Complete your first questionnaire to see your results here.</p>
                    <button @click="router.push('/')" class="btn btn-primary mt-3">Start Now</button>
                </div>

                <div v-if="history.length > 0" class="wow fadeInUp" data-wow-delay="0.2s">
                    <h4 class="fw-bold mb-4 ps-2 border-start border-4 border-primary">History Log</h4>

                    <div class="list-group shadow-sm rounded-4 overflow-hidden border-0">
                        <div v-for="(item, index) in history" :key="item.id"
                            class="list-group-item list-group-item-action p-4 d-flex align-items-center justify-content-between border-light">

                            <div class="d-flex align-items-center">
                                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center me-3 text-secondary fw-bold"
                                    style="width: 50px; height: 50px;">
                                    {{ history.length - index }}
                                </div>

                                <div>
                                    <h5 class="mb-1 fw-bold text-dark">{{ item.diagnosis }}</h5>
                                    <small class="text-muted">
                                        <i class="far fa-calendar-alt me-1"></i> {{ item.date }}
                                    </small>
                                </div>
                            </div>

                            <div class="text-end">
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

/* Gradient for the main result card */
.bg-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

/* Overlay effect */
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

/* List Item Styling */
.list-group-item {
    transition: background-color 0.2s, transform 0.2s;
    border-left: 0;
    border-right: 0;
}

.list-group-item:hover {
    background-color: #f8f9fa;
    transform: translateX(5px);
    z-index: 2;
}
</style>