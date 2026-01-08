<script setup>
import { ref, onMounted } from 'vue';
import { WOW } from 'wowjs';


const user = ref({
  username: 'Dummy Dum',
  email: 'dummy.dum@example.com',
  age: 28,
  gender: 'Male',
  role: 'user',
  date_registered: '2024-01-15'
});


const stats = ref({
  questionnairesCompleted: 12,
  activitiesCompleted: 45,
  currentStreak: 7,
  totalPoints: 350
});


const recentActivities = ref([
  { id: 1, title: 'Morning Meditation', date: '2024-01-20', status: 'completed' },
  { id: 2, title: 'Stress Assessment', date: '2024-01-19', status: 'completed' },
  { id: 3, title: 'Gratitude Journal', date: '2024-01-18', status: 'completed' },
  { id: 4, title: 'Breathing Exercise', date: '2024-01-17', status: 'completed' }
]);


const upcomingTasks = ref([
  { id: 1, title: 'Daily Check-in', time: 'Today, 3:00 PM', priority: 'high' },
  { id: 2, title: 'Weekly Mood Assessment', time: 'Tomorrow, 9:00 AM', priority: 'medium' },
  { id: 3, title: 'Mindfulness Exercise', time: 'Jan 22, 2:00 PM', priority: 'low' }
]);

onMounted(() => {
  new WOW().init();
});


const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
};
</script>

<template>
  <div class="dashboard-page">

   
    <header class="py-4 bg-light border-bottom">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h1 class="display-5 fw-bold text-primary mb-2 wow fadeInUp" data-wow-delay="0.1s">
              Welcome back, {{ user.username }}! 👋
            </h1>
            <p class="text-muted mb-0 wow fadeInUp" data-wow-delay="0.2s">
              Here's your wellness journey overview
            </p>
          </div>
          <div class="col-md-4 text-md-end mt-3 mt-md-0">
            <button class="btn btn-primary rounded-pill px-4">
              <i class="bi bi-plus-lg me-2"></i>New Assessment
            </button>
          </div>
        </div>
      </div>
    </header>

   
    <section class="py-4 bg-white">
      <div class="container">
        <div class="card border-0 shadow-sm wow fadeInUp" data-wow-delay="0.2s">
          <div class="card-body p-4">
            <div class="row align-items-center">
              <div class="col-auto">
                <div class="avatar-circle bg-primary text-white">
                  <span class="display-6">{{ user.username.charAt(0) }}</span>
                </div>
              </div>
              <div class="col">
                <h4 class="fw-bold mb-1">{{ user.username }}</h4>
                <p class="text-muted mb-0">
                  <i class="bi bi-envelope me-2"></i>{{ user.email }}
                </p>
              </div>
              <div class="col-auto d-none d-md-block">
                <span class="badge bg-success px-3 py-2">{{ user.role }}</span>
              </div>
            </div>
            <hr class="my-3">
            <div class="row text-center text-md-start">
              <div class="col-6 col-md-3 mb-3 mb-md-0">
                <small class="text-muted d-block">Age</small>
                <strong>{{ user.age }} years</strong>
              </div>
              <div class="col-6 col-md-3 mb-3 mb-md-0">
                <small class="text-muted d-block">Gender</small>
                <strong>{{ user.gender }}</strong>
              </div>
              <div class="col-12 col-md-6">
                <small class="text-muted d-block">Member Since</small>
                <strong>{{ formatDate(user.date_registered) }}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    
    <section class="py-4">
      <div class="container">
        <div class="row g-4">
          
         
          <div class="col-6 col-md-3 wow fadeInLeft" data-wow-delay="0.3s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-primary bg-opacity-10 text-primary mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-clipboard-check" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0"/>
                    <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1z"/>
                    <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0z"/>
                  </svg>
                </div>
                <h3 class="fw-bold mb-1">{{ stats.questionnairesCompleted }}</h3>
                <small class="text-muted">Assessments</small>
              </div>
            </div>
          </div>

          
          <div class="col-6 col-md-3 wow fadeInLeft" data-wow-delay="0.4s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-success bg-opacity-10 text-success mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-list-check" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M5 11.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5M3.854 2.146a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 1 1 .708-.708L2 3.293l1.146-1.147a.5.5 0 0 1 .708 0m0 4a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 1 1 .708-.708L2 7.293l1.146-1.147a.5.5 0 0 1 .708 0m0 4a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0l-.5-.5a.5.5 0 0 1 .708-.708l.146.147 1.146-1.147a.5.5 0 0 1 .708 0"/>
                  </svg>
                </div>
                <h3 class="fw-bold mb-1">{{ stats.activitiesCompleted }}</h3>
                <small class="text-muted">Activities Done</small>
              </div>
            </div>
          </div>

         
          <div class="col-6 col-md-3 wow fadeInLeft" data-wow-delay="0.5s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-warning bg-opacity-10 text-warning mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-fire" viewBox="0 0 16 16">
                    <path d="M8 16c3.314 0 6-2 6-5.5 0-1.5-.5-4-2.5-6 .25 1.5-1.25 2-1.25 2C11 4 9 .5 6 0c.357 2 .5 4-2 6-1.25 1-2 2.729-2 4.5C2 14 4.686 16 8 16m0-1c-1.657 0-3-1-3-2.75 0-.75.25-2 1.25-3C6.125 10 7 10.5 7 10.5c-.375-1.25.5-3.25 2-3.5-.179 1-.25 2 1 3 .625.5 1 1.364 1 2.25C11 14 9.657 15 8 15"/>
                  </svg>
                </div>
                <h3 class="fw-bold mb-1">{{ stats.currentStreak }}</h3>
                <small class="text-muted">Day Streak</small>
              </div>
            </div>
          </div>

          
          <div class="col-6 col-md-3 wow fadeInLeft" data-wow-delay="0.6s">
            <div class="card border-0 shadow-sm h-100 text-center stat-card">
              <div class="card-body p-4">
                <div class="stat-icon bg-info bg-opacity-10 text-info mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                  </svg>
                </div>
                <h3 class="fw-bold mb-1">{{ stats.totalPoints }}</h3>
                <small class="text-muted">Total Points</small>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    
    <section class="py-4">
      <div class="container">
        <div class="row g-4">

          
          <div class="col-lg-8 wow fadeInUp" data-wow-delay="0.3s">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="fw-bold mb-0">
                  <i class="bi bi-clock-history text-primary me-2"></i>Recent Activities
                </h5>
              </div>
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

          
          <div class="col-lg-4 wow fadeInUp" data-wow-delay="0.4s">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-white border-bottom py-3">
                <h5 class="fw-bold mb-0">
                  <i class="bi bi-clock text-primary me-2"></i>Upcoming Tasks
                </h5>
              </div>
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
                          task.priority === 'medium' ? 'bg-warning' : 'bg-secondary'
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
              <div class="card-footer bg-white text-center py-3">
                <a href="#" class="text-primary fw-bold text-decoration-none">
                  View All Tasks <i class="bi bi-arrow-right ms-1"></i>
                </a>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    
    <section class="py-4 mb-5">
      <div class="container">
        <div class="card border-0 shadow-sm bg-primary bg-gradient text-white wow fadeInUp" data-wow-delay="0.5s">
          <div class="card-body p-4 text-center">
            <h4 class="fw-bold mb-3">Ready to improve your wellness?</h4>
            <p class="mb-4">Start a new assessment or continue your journey</p>
            <div class="d-flex flex-wrap justify-content-center gap-3">
              <button class="btn btn-light rounded-pill px-4">
                <i class="bi bi-clipboard-check me-2"></i>Take Assessment
              </button>
              <button class="btn btn-outline-light rounded-pill px-4">
                <i class="bi bi-book me-2"></i>View Resources
              </button>
              <button class="btn btn-outline-light rounded-pill px-4">
                <i class="bi bi-graph-up me-2"></i>View Progress
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>

.avatar-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}


.stat-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}


.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}


.list-group-item {
  transition: background-color 0.2s ease;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}
</style>