<template>
  <div class="dashboard">
    <h1 class="title">Admin Dashboard</h1>
    
    <div class="cards-container">
      <div class="card" @click="page = 'resources'">
        <div class="icon">📚</div>
        <h2>Resources</h2>
        <p>Manage your resources</p>
        <button class="card-btn">Go to Resources →</button>
      </div>

      <div class="card" @click="page = 'questions'">
        <div class="icon">❓</div>
        <h2>Questions</h2>
        <p>Manage your questions</p>
        <button class="card-btn">Go to Questions →</button>
      </div>

      <div class="card" @click="page = 'more'">
        <div class="icon">➕</div>
        <h2>More</h2>
        <p>Additional features</p>
        <button class="card-btn">Go to More →</button>
      </div>
    </div>

    <!-- Pages with your components -->
    <div v-if="page === 'resources'" class="page">
      <button class="back-btn" @click="page = null">← Back to Dashboard</button>
      <ManageResources />
    </div>

    <div v-if="page === 'questions'" class="page">
      <button class="back-btn" @click="page = null">← Back to Dashboard</button>
      <AdminQuestionManager />
    </div>

    <div v-if="page === 'more'" class="page">
      <button class="back-btn" @click="page = null">← Back to Dashboard</button>
      <h2>More Page</h2>
      <p>Coming soon...</p>
    </div>
  </div>
</template>

<script>
import ManageResources from './ManageResources.vue'
import AdminQuestionManager from './AdminQuestionManager.vue'

export default {
  components: {
    ManageResources,  // This should match the import name
    AdminQuestionManager
  },
  data() {
    return {
      page: null
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.title {
  text-align: center;
  color: white;
  font-size: 2.5rem;
  margin-bottom: 50px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.cards-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.card {
  background: white;
  border-radius: 20px;
  padding: 40px 30px;
  width: 300px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.card h2 {
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.card p {
  color: #666;
  margin-bottom: 25px;
}

.card-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 50px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.card-btn:hover {
  transform: scale(1.05);
}

.page {
  background: white;
  border-radius: 20px;
  padding: 40px;
  margin-top: 40px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.back-btn {
  background: #f0f0f0;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  cursor: pointer;
  font-size: 1rem;
}

.back-btn:hover {
  background: #e0e0e0;
}
</style>