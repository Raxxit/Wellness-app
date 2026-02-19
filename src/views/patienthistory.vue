<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const isLoading = ref(true);
const patient = ref({});
const completionRate = ref(0);
const taskHistory = ref([]);

const fetchHistory = async () => {
    try {
        const token = localStorage.getItem('token');
        const userId = route.params.id;
        const res = await axios.get(`/api/advisor/patient/${userId}/history`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        patient.value = res.data.patient;
        completionRate.value = res.data.completionRate;
        taskHistory.value = res.data.history;
    } catch (e) {
        console.error("Failed to load history", e);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchHistory);
</script>

<template>
    <div class="patient-history container py-5">

        <button @click="router.back()" class="btn btn-outline-secondary mb-4">
            <i class="bi bi-arrow-left me-2"></i> Back to Dashboard
        </button>

        <div v-if="isLoading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status"></div>
        </div>

        <div v-else>
            <div class="text-center mb-5">
                <h2 class="fw-bold text-dark">Patient Overview</h2>
                <p class="text-muted">Reviewing records for <span class="fw-bold text-primary">{{ patient.name }}</span>
                </p>
            </div>

            <div class="summary-card shadow-sm p-4 mb-5 border-0">
                <div class="row align-items-center">
                    <div class="col-md-6 border-end">
                        <h5 class="fw-bold mb-3">Patient Details</h5>
                        <p class="mb-1"><strong class="text-muted">Name:</strong> {{ patient.name }}</p>
                        <p class="mb-1"><strong class="text-muted">Email:</strong> {{ patient.email }}</p>
                        <p class="mb-0"><strong class="text-muted">Client ID:</strong> #{{ patient.id }}</p>
                    </div>
                    <div class="col-md-6 ps-md-4 mt-3 mt-md-0">
                        <h5 class="fw-bold mb-3">Wellness Snapshot</h5>
                        <p class="mb-2">
                            <strong class="text-muted me-2">Current Status:</strong>
                            <span class="badge"
                                :class="patient.riskLevel === 'Needs Attention' ? 'bg-danger' : 'bg-success'">
                                {{ patient.riskLevel }}
                            </span>
                        </p>

                        <div class="mb-0">
                            <strong class="text-muted me-2">Task Adherence:</strong>
                            <div class="progress mt-2" style="height: 10px;">
                                <div class="progress-bar bg-primary" :style="{ width: completionRate + '%' }"></div>
                            </div>
                            <small class="text-muted">{{ completionRate }}% Completed</small>
                        </div>

                    </div>
                </div>
            </div>

            <div class="card shadow-sm border-0">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0 fw-bold">Recent Activity Log</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover mb-0 align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Date</th>
                                    <th>Assigned Task</th>
                                    <th>Status</th>
                                    <th>Mood Reported</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in taskHistory" :key="index">
                                    <td class="ps-4 text-muted">{{ item.date }}</td>
                                    <td class="fw-medium">{{ item.task }}</td>
                                    <td>
                                        <span class="badge rounded-pill"
                                            :class="item.status === 'Completed' ? 'bg-success-subtle text-success' :
                                                item.status === 'Missed' ? 'bg-danger-subtle text-danger' : 'bg-warning-subtle text-dark'">
                                            {{ item.status }}
                                        </span>
                                    </td>
                                    <td>
                                        <span v-if="item.mood !== '-'">{{ item.mood }}</span>
                                        <span v-else class="text-muted small">--</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.summary-card {
    background: #ffffff;
    border-left: 5px solid #0d6efd;
}

.bg-success-subtle {
    background-color: #d1e7dd;
}

.bg-danger-subtle {
    background-color: #f8d7da;
}

.bg-warning-subtle {
    background-color: #fff3cd;
}
</style>