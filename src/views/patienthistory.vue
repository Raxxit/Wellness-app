<script setup>
import { computed, onMounted } from "vue";
import { WOW } from "wowjs";

const patient = {
  name: "Emily Carter",
  id: "MW-1024",
  riskLevel: "Needs Attention",
};

const taskHistory = [
  {
    date: "2026-02-01",
    task: "10-min Meditation",
    status: "Completed",
    mood: "Calm",
  },
  {
    date: "2026-02-02",
    task: "Gratitude Journal",
    status: "Missed",
    mood: "Anxious",
  },
  {
    date: "2026-02-03",
    task: "Breathing Exercise",
    status: "Completed",
    mood: "Stable",
  },
  {
    date: "2026-02-04",
    task: "Evening Reflection",
    status: "Missed",
    mood: "Low",
  },
];

const completionRate = computed(() => {
  const completed = taskHistory.filter((t) => t.status === "Completed").length;
  return Math.round((completed / taskHistory.length) * 100);
});

onMounted(() => {
  new WOW().init();
});
</script>

<template>
  <div class="patient-history container py-5">
    <!-- Header -->
    <div class="text-center mb-5 wow fadeInDown">
      <h2 class="fw-bold text-primary">Professional Patient Overview</h2>
      <p class="text-muted">Review task adherence and emotional condition.</p>
    </div>

    <!-- Patient Summary Card -->
    <div class="summary-card shadow-sm p-4 mb-5 wow fadeInUp">
      <div class="row">
        <div class="col-md-6">
          <p><strong>Name:</strong> {{ patient.name }}</p>
          <p><strong>Client ID:</strong> {{ patient.id }}</p>
        </div>
        <div class="col-md-6">
          <p>
            <strong>Status:</strong>
            <span
              class="badge bg-danger"
              v-if="patient.riskLevel === 'Needs Attention'"
            >
              {{ patient.riskLevel }}
            </span>
            <span class="badge bg-success" v-else> Stable </span>
          </p>
          <p><strong>Task Completion:</strong> {{ completionRate }}%</p>
        </div>
      </div>
    </div>

    <!-- Task History Table -->
    <div class="card shadow-sm wow fadeInUp">
      <div class="card-body">
        <h5 class="mb-3 text-secondary">Task History</h5>

        <div class="table-responsive">
          <table class="table table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th>Date</th>
                <th>Assigned Task</th>
                <th>Status</th>
                <th>Mood</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in taskHistory" :key="item.date">
                <td>{{ item.date }}</td>
                <td>{{ item.task }}</td>
                <td>
                  <span
                    class="badge"
                    :class="
                      item.status === 'Completed'
                        ? 'bg-success'
                        : 'bg-warning text-dark'
                    "
                  >
                    {{ item.status }}
                  </span>
                </td>
                <td>{{ item.mood }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.summary-card {
  background: #f4f7fb;
  border-radius: 15px;
}

.badge {
  font-size: 0.85rem;
  padding: 6px 10px;
}
</style>
