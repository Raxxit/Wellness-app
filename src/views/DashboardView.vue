<script setup>
import { ref, onMounted } from 'vue';
import { WOW } from 'wowjs';

// Mock statistics
const stats = ref({
  questionnairesCompleted: 12,
  activitiesCompleted: 45,
  currentStreak: 7,
  totalPoints: 350
});

// Mock recent activities
const recentActivities = ref([
  { id: 1, title: 'Morning Meditation', date: '2024-01-20', status: 'completed' },
  { id: 2, title: 'Stress Assessment', date: '2024-01-19', status: 'completed' },
  { id: 3, title: 'Gratitude Journal', date: '2024-01-18', status: 'completed' },
  { id: 4, title: 'Breathing Exercise', date: '2024-01-17', status: 'completed' }
]);

// Mock upcoming tasks
const upcomingTasks = ref([
  { id: 1, title: 'Daily Check-in', time: 'Today, 3:00 PM', priority: 'high' },
  { id: 2, title: 'Weekly Mood Assessment', time: 'Tomorrow, 9:00 AM', priority: 'medium' },
  { id: 3, title: 'Mindfulness Exercise', time: 'Jan 22, 2:00 PM', priority: 'low' }
]);

// Collapsible states
const activitiesOpen = ref(false);
const tasksOpen = ref(false);

onMounted(() => {
  new WOW().init();
});
</script>

<template>
  <div class="dashboard-page">

    <!-- Motivational Quote Section -->
    <section class="quote-section py-4">
      <div class="container">
        <div class="quote-card wow fadeIn" data-wow-delay="0.1s">
          <div class="quote-icon-wrapper">
            <i class="bi bi-heart-pulse-fill quote-icon"></i>
          </div>
          <h3 class="quote-text mb-2">
            "Your mental health is a priority. Your happiness is essential."
          </h3>
          <p class="quote-subtitle">
            <i class="bi bi-stars me-2"></i>
            Take one step at a time on your wellness journey
          </p>
        </div>
      </div>
    </section>

    <!-- Statistics Cards -->
    <section class="py-5">
      <div class="container">
        <div class="row g-4">
          
          <!-- ASSESSMENTS -->
          <div class="col-6 col-md-3 wow fadeInUp" data-wow-delay="0.1s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-primary bg-opacity-10 text-primary mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-clipboard-check" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0"/>
                    <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
                    <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
                  </svg>
                </div>
                <h2 class="fw-bold mb-1 display-6">{{ stats.questionnairesCompleted }}</h2>
                <p class="text-muted mb-0 small">Assessments</p>
              </div>
            </div>
          </div>

          <!-- ACTIVITIES -->
          <div class="col-6 col-md-3 wow fadeInUp" data-wow-delay="0.2s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-success bg-opacity-10 text-success mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-list-check" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M5 11.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5M3.854 2.146a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 1 1 .708-.708L2 3.293l1.146-1.147a.5.5 0 0 1 .708 0m0 4a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 1 1 .708-.708L2 7.293l1.146-1.147a.5.5 0 0 1 .708 0m0 4a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 0 1 .708-.708l.146.147 1.146-1.147a.5.5 0 0 1 .708 0"/>
                  </svg>
                </div>
                <h2 class="fw-bold mb-1 display-6">{{ stats.activitiesCompleted }}</h2>
                <p class="text-muted mb-0 small">Activities</p>
              </div>
            </div>
          </div>

          <!-- STREAK -->
          <div class="col-6 col-md-3 wow fadeInUp" data-wow-delay="0.3s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-warning bg-opacity-10 text-warning mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-fire" viewBox="0 0 16 16">
                    <path d="M8 16c3.314 0 6-2 6-5.5 0-1.5-.5-4-2.5-6 .25 1.5-1.25 2-1.25 2C11 4 9 .5 6 0c.357 2 .5 4-2 6-1.25 1-2 2.729-2 4.5C2 14 4.686 16 8 16m0-1c-1.657 0-3-1-3-2.75 0-.75.25-2 1.25-3C6.125 10 7 10.5 7 10.5c-.375-1.25.5-3.25 2-3.5-.179 1-.25 2 1 3 .625.5 1 1.364 1 2.25C11 14 9.657 15 8 15"/>
                  </svg>
                </div>
                <h2 class="fw-bold mb-1 display-6">{{ stats.currentStreak }}</h2>
                <p class="text-muted mb-0 small">Day Streak</p>
              </div>
            </div>
          </div>

          <!-- POINTS -->
          <div class="col-6 col-md-3 wow fadeInUp" data-wow-delay="0.4s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-info bg-opacity-10 text-info mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                  </svg>
                </div>
                <h2 class="fw-bold mb-1 display-6">{{ stats.totalPoints }}</h2>
                <p class="text-muted mb-0 small">Points</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Collapsible Sections -->
    <section class="py-4 mb-5">
      <div class="container">
        <div class="row g-4">

          <!-- Recent Activities - Collapsible -->
          <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.2s">
            <div class="card border-0 shadow-sm collapsible-card">
              <div 
                class="card-header collapsible-header py-3"
                @click="activitiesOpen = !activitiesOpen"
              >
                <div class="d-flex justify-content-between align-items-center">
                  <div class="header-content">
                    <i class="bi bi-clock-history text-primary me-2 fs-5"></i>
                    <h5 class="fw-bold mb-0 d-inline">Recent Activities</h5>
                  </div>
                  <div class="arrow-button">
                    <i 
                      :class="['bi', activitiesOpen ? 'bi-chevron-up' : 'bi-chevron-down']"
                    ></i>
                  </div>
                </div>
              </div>
              <div class="collapse-content" :class="{ 'show': activitiesOpen }">
                <div class="card-body p-0">
                  <div class="list-group list-group-flush">
                    <div 
                      v-for="activity in recentActivities" 
                      :key="activity.id"
                      class="list-group-item d-flex justify-content-between align-items-center py-3"
                    >
                      <div>
                        <h6 class="mb-1 fw-bold">{{ activity.title }}</h6>
                        <small class="text-muted">
                          <i class="bi bi-calendar me-1"></i>{{ activity.date }}
                        </small>
                      </div>
                      <span class="badge bg-success rounded-pill">
                        <i class="bi bi-check-lg me-1"></i>{{ activity.status }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Upcoming Tasks - Collapsible -->
          <div class="col-lg-6 wow fadeInUp" data-wow-delay="0.3s">
            <div class="card border-0 shadow-sm collapsible-card">
              <div 
                class="card-header collapsible-header py-3"
                @click="tasksOpen = !tasksOpen"
              >
                <div class="d-flex justify-content-between align-items-center">
                  <div class="header-content">
                    <i class="bi bi-calendar-check text-primary me-2 fs-5"></i>
                    <h5 class="fw-bold mb-0 d-inline">Upcoming Tasks</h5>
                  </div>
                  <div class="arrow-button">
                    <i 
                      :class="['bi', tasksOpen ? 'bi-chevron-up' : 'bi-chevron-down']"
                    ></i>
                  </div>
                </div>
              </div>
              <div class="collapse-content" :class="{ 'show': tasksOpen }">
                <div class="card-body p-0">
                  <div class="list-group list-group-flush">
                    <div 
                      v-for="task in upcomingTasks" 
                      :key="task.id"
                      class="list-group-item py-3"
                    >
                      <div class="d-flex align-items-start">
                        <span 
                          :class="[
                            'badge me-2 mt-1',
                            task.priority === 'high' ? 'bg-danger' : 
                            task.priority === 'medium' ? 'bg-warning text-dark' : 'bg-secondary'
                          ]"
                        >
                          {{ task.priority }}
                        </span>
                        <div class="flex-grow-1">
                          <h6 class="mb-1 fw-bold">{{ task.title }}</h6>
                          <small class="text-muted">
                            <i class="bi bi-clock me-1"></i>{{ task.time }}
                          </small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.dashboard-page {
  background: #f8f9fa;
  min-height: 100vh;
}

/* Quote Section - Simplified & Compact */
.quote-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.quote-card {
  max-width: 700px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.quote-icon-wrapper {
  margin-bottom: 1rem;
}

.quote-icon {
  font-size: 2.5rem;
  color: #667eea;
  display: inline-block;
}

.quote-text {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2d3748;
  line-height: 1.5;
  font-style: italic;
  margin-bottom: 0.5rem;
}

.quote-subtitle {
  font-size: 0.95rem;
  color: #667eea;
  font-weight: 500;
  margin-bottom: 0;
}

/* Stat Card Styling */
.stat-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-left: 4px solid transparent;
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15) !important;
}

.stat-card:nth-child(1) { border-left-color: #0d6efd; }
.stat-card:nth-child(2) { border-left-color: #198754; }
.stat-card:nth-child(3) { border-left-color: #ffc107; }
.stat-card:nth-child(4) { border-left-color: #0dcaf0; }

/* Stat Icon */
.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  transition: transform 0.3s ease;
}

.stat-card:hover .stat-icon {
  transform: scale(1.15) rotate(5deg);
}

/* Collapsible Cards */
.collapsible-card {
  overflow: hidden;
  transition: all 0.3s ease;
  border-radius: 15px;
}

.collapsible-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
  border: none;
  border-bottom: 2px solid #dee2e6;
}

.collapsible-header:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.header-content {
  display: flex;
  align-items: center;
}

/* Arrow Button */
.arrow-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.collapsible-header:hover .arrow-button {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
}

.arrow-button i {
  font-size: 1.2rem;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.collapse-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s ease;
}

.collapse-content.show {
  max-height: 1000px;
}

/* List items hover */
.list-group-item {
  transition: all 0.2s ease;
  border-color: #e9ecef !important;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .quote-card {
    padding: 1.5rem 1.25rem;
  }
  
  .quote-text {
    font-size: 1.1rem;
  }
  
  .quote-icon {
    font-size: 2rem;
  }
  
  .stat-card h2 {
    font-size: 1.75rem;
  }
  
  .stat-icon {
    width: 60px;
    height: 60px;
  }
  
  .stat-icon svg {
    width: 35px;
    height: 35px;
  }
}
</style>