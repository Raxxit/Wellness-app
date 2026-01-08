<template>
  <div id="app" :class="{'dark-mode': darkMode}">
    <div class="app-container">
      <!-- Header -->
      <header class="header">
        <div class="header-content">
          <h1 class="app-title">
            <i class="fas fa-check-circle"></i>
            Vue Habit Tracker
          </h1>
          <div class="header-actions">
            <button 
              class="theme-toggle" 
              @click="toggleTheme"
              :title="darkMode ? 'Switch to light mode' : 'Switch to dark mode'"
            >
              <i :class="darkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
            </button>
            <button class="btn-add" @click="showAddModal = true">
              <i class="fas fa-plus"></i> Add New
            </button>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="main-content">
        <!-- Stats Overview -->
        <div class="stats-container">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #4CAF50;">
              <i class="fas fa-tasks"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-value">{{ totalTasks }}</h3>
              <p class="stat-label">Total Tasks</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #2196F3;">
              <i class="fas fa-calendar-check"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-value">{{ completedToday }}</h3>
              <p class="stat-label">Completed Today</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #FF9800;">
              <i class="fas fa-fire"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-value">{{ currentStreak }}</h3>
              <p class="stat-label">Current Streak</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #9C27B0;">
              <i class="fas fa-chart-line"></i>
            </div>
            <div class="stat-info">
              <h3 class="stat-value">{{ completionRate }}%</h3>
              <p class="stat-label">Completion Rate</p>
            </div>
          </div>
        </div>

        <!-- Filter Tabs -->
        <div class="filter-tabs">
          <button 
            class="filter-tab" 
            :class="{ active: filter === 'all' }"
            @click="filter = 'all'"
          >
            All Tasks
          </button>
          <button 
            class="filter-tab" 
            :class="{ active: filter === 'active' }"
            @click="filter = 'active'"
          >
            Active
          </button>
          <button 
            class="filter-tab" 
            :class="{ active: filter === 'completed' }"
            @click="filter = 'completed'"
          >
            Completed
          </button>
          <button 
            class="filter-tab" 
            :class="{ active: filter === 'habits' }"
            @click="filter = 'habits'"
          >
            Habits
          </button>
          <button 
            class="filter-tab" 
            :class="{ active: filter === 'daily' }"
            @click="filter = 'daily'"
          >
            Daily
          </button>
        </div>

        <!-- Tasks/Habits List -->
        <div class="tasks-container">
          <div v-if="filteredTasks.length === 0" class="empty-state">
            <i class="fas fa-clipboard-list"></i>
            <h3>No tasks found</h3>
            <p>Add a new task or habit to get started!</p>
            <button class="btn-primary" @click="showAddModal = true">
              <i class="fas fa-plus"></i> Create Your First Task
            </button>
          </div>
          
          <div v-else class="tasks-list">
            <div 
              v-for="task in filteredTasks" 
              :key="task.id"
              class="task-card"
              :class="{
                'completed': task.completed,
                'habit': task.type === 'habit',
                'priority-high': task.priority === 'high',
                'priority-medium': task.priority === 'medium'
              }"
            >
              <div class="task-main">
                <div class="task-checkbox" @click="toggleTaskCompletion(task.id)">
                  <div class="checkbox" :class="{ checked: task.completed }">
                    <i v-if="task.completed" class="fas fa-check"></i>
                  </div>
                </div>
                
                <div class="task-info">
                  <h4 class="task-title" :class="{ completed: task.completed }">
                    {{ task.title }}
                  </h4>
                  <p class="task-description" v-if="task.description">
                    {{ task.description }}
                  </p>
                  
                  <div class="task-meta">
                    <span class="task-category" :style="{ backgroundColor: categoryColors[task.category] }">
                      {{ task.category }}
                    </span>
                    <span class="task-type">
                      <i v-if="task.type === 'habit'" class="fas fa-redo"></i>
                      <i v-else class="fas fa-calendar-day"></i>
                      {{ task.type === 'habit' ? 'Habit' : 'Daily Task' }}
                    </span>
                    <span v-if="task.priority" class="task-priority">
                      <i class="fas fa-flag"></i>
                      {{ task.priority }}
                    </span>
                    <span v-if="task.streak" class="task-streak">
                      <i class="fas fa-fire"></i>
                      {{ task.streak }} days
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="task-actions">
                <button 
                  class="task-action-btn" 
                  @click="toggleTaskCompletion(task.id)"
                  :title="task.completed ? 'Mark as incomplete' : 'Mark as complete'"
                >
                  <i :class="task.completed ? 'fas fa-undo' : 'fas fa-check'"></i>
                </button>
                <button 
                  class="task-action-btn" 
                  @click="editTask(task)"
                  title="Edit task"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  class="task-action-btn delete" 
                  @click="deleteTask(task.id)"
                  title="Delete task"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Progress Visualization -->
        <div class="progress-section">
          <h2 class="section-title">Weekly Progress</h2>
          <div class="progress-chart">
            <div 
              v-for="day in weekProgress" 
              :key="day.day"
              class="progress-day"
            >
              <div class="progress-bar-container">
                <div 
                  class="progress-bar" 
                  :style="{ height: day.percentage + '%' }"
                  :class="{ 'today': day.isToday }"
                ></div>
              </div>
              <span class="progress-day-label">{{ day.day }}</span>
              <span class="progress-day-value">{{ day.completed }}/{{ day.total }}</span>
            </div>
          </div>
        </div>
      </main>

      <!-- Add/Edit Task Modal -->
      <div v-if="showAddModal || showEditModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ showEditModal ? 'Edit Task' : 'Add New Task/Habit' }}</h2>
            <button class="modal-close" @click="closeModal">
              <i class="fas fa-times"></i>
            </button>
          </div>
          
          <div class="modal-body">
            <div class="form-group">
              <label for="taskTitle">Title *</label>
              <input 
                type="text" 
                id="taskTitle" 
                v-model="currentTask.title"
                placeholder="Enter task title"
              >
            </div>
            
            <div class="form-group">
              <label for="taskDescription">Description</label>
              <textarea 
                id="taskDescription" 
                v-model="currentTask.description"
                placeholder="Enter task description"
                rows="3"
              ></textarea>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>Type</label>
                <div class="type-selector">
                  <button 
                    class="type-option" 
                    :class="{ active: currentTask.type === 'task' }"
                    @click="currentTask.type = 'task'"
                  >
                    <i class="fas fa-calendar-day"></i>
                    Daily Task
                  </button>
                  <button 
                    class="type-option" 
                    :class="{ active: currentTask.type === 'habit' }"
                    @click="currentTask.type = 'habit'"
                  >
                    <i class="fas fa-redo"></i>
                    Habit
                  </button>
                </div>
              </div>
              
              <div class="form-group">
                <label for="taskCategory">Category</label>
                <select id="taskCategory" v-model="currentTask.category">
                  <option value="Health">Health</option>
                  <option value="Work">Work</option>
                  <option value="Personal">Personal</option>
                  <option value="Fitness">Fitness</option>
                  <option value="Learning">Learning</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="taskPriority">Priority</label>
                <select id="taskPriority" v-model="currentTask.priority">
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              
              <div class="form-group">
                <label>Color</label>
                <div class="color-selector">
                  <div 
                    v-for="color in availableColors" 
                    :key="color"
                    class="color-option" 
                    :style="{ backgroundColor: color }"
                    :class="{ selected: currentTask.color === color }"
                    @click="currentTask.color = color"
                  ></div>
                </div>
              </div>
            </div>
            
            <div v-if="currentTask.type === 'habit'" class="form-group">
              <label>Frequency</label>
              <div class="frequency-selector">
                <button 
                  class="frequency-option" 
                  :class="{ active: currentTask.frequency === 'daily' }"
                  @click="currentTask.frequency = 'daily'"
                >
                  Daily
                </button>
                <button 
                  class="frequency-option" 
                  :class="{ active: currentTask.frequency === 'weekly' }"
                  @click="currentTask.frequency = 'weekly'"
                >
                  Weekly
                </button>
                <button 
                  class="frequency-option" 
                  :class="{ active: currentTask.frequency === 'custom' }"
                  @click="currentTask.frequency = 'custom'"
                >
                  Custom
                </button>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button class="btn-secondary" @click="closeModal">
              Cancel
            </button>
            <button 
              class="btn-primary" 
              @click="showEditModal ? updateTask() : addTask()"
              :disabled="!currentTask.title"
            >
              {{ showEditModal ? 'Update Task' : 'Add Task' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      darkMode: false,
      filter: 'all',
      showAddModal: false,
      showEditModal: false,
      currentTask: {
        id: null,
        title: '',
        description: '',
        type: 'task',
        category: 'Personal',
        priority: 'medium',
        color: '#4CAF50',
        completed: false,
        createdAt: null,
        completedAt: null,
        streak: 0,
        frequency: 'daily'
      },
      tasks: [
        {
          id: 1,
          title: 'Morning Meditation',
          description: '10 minutes of mindfulness meditation',
          type: 'habit',
          category: 'Health',
          priority: 'high',
          color: '#4CAF50',
          completed: true,
          createdAt: '2023-05-01',
          completedAt: '2023-05-15',
          streak: 5,
          frequency: 'daily'
        },
        {
          id: 2,
          title: 'Workout at Gym',
          description: 'Strength training session',
          type: 'habit',
          category: 'Fitness',
          priority: 'high',
          color: '#FF9800',
          completed: true,
          createdAt: '2023-05-10',
          completedAt: '2023-05-15',
          streak: 3,
          frequency: 'daily'
        },
        {
          id: 3,
          title: 'Complete Project Report',
          description: 'Finish quarterly report for stakeholders',
          type: 'task',
          category: 'Work',
          priority: 'high',
          color: '#2196F3',
          completed: false,
          createdAt: '2023-05-14',
          completedAt: null,
          streak: 0,
          frequency: 'daily'
        },
        {
          id: 4,
          title: 'Read 30 pages',
          description: 'Current book: Atomic Habits',
          type: 'habit',
          category: 'Learning',
          priority: 'medium',
          color: '#9C27B0',
          completed: false,
          createdAt: '2023-05-01',
          completedAt: null,
          streak: 0,
          frequency: 'daily'
        },
        {
          id: 5,
          title: 'Weekly Planning',
          description: 'Plan tasks for the upcoming week',
          type: 'task',
          category: 'Personal',
          priority: 'medium',
          color: '#3F51B5',
          completed: false,
          createdAt: '2023-05-15',
          completedAt: null,
          streak: 0,
          frequency: 'daily'
        }
      ],
      availableColors: ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#3F51B5', '#F44336', '#00BCD4', '#8BC34A'],
      categoryColors: {
        'Health': '#4CAF50',
        'Work': '#2196F3',
        'Personal': '#FF9800',
        'Fitness': '#9C27B0',
        'Learning': '#3F51B5',
        'Other': '#607D8B'
      }
    }
  },
  computed: {
    totalTasks() {
      return this.tasks.length;
    },
    completedToday() {
      const today = new Date().toISOString().split('T')[0];
      return this.tasks.filter(task => 
        task.completed && task.completedAt && task.completedAt.startsWith(today)
      ).length;
    },
    currentStreak() {
      let maxStreak = 0;
      this.tasks.forEach(task => {
        if (task.streak > maxStreak) maxStreak = task.streak;
      });
      return maxStreak;
    },
    completionRate() {
      const completed = this.tasks.filter(task => task.completed).length;
      return this.tasks.length > 0 ? Math.round((completed / this.tasks.length) * 100) : 0;
    },
    filteredTasks() {
      if (this.filter === 'all') return this.tasks;
      if (this.filter === 'active') return this.tasks.filter(task => !task.completed);
      if (this.filter === 'completed') return this.tasks.filter(task => task.completed);
      if (this.filter === 'habits') return this.tasks.filter(task => task.type === 'habit');
      if (this.filter === 'daily') return this.tasks.filter(task => task.type === 'task');
      return this.tasks;
    },
    weekProgress() {
      const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
      const today = new Date().getDay();
      // Adjust to make Monday the first day (0 index)
      const adjustedToday = today === 0 ? 6 : today - 1;
      
      return days.map((day, index) => {
        // Mock data for demonstration
        const completed = Math.floor(Math.random() * 5);
        const total = 5;
        const percentage = (completed / total) * 100;
        
        return {
          day,
          completed,
          total,
          percentage,
          isToday: index === adjustedToday
        };
      });
    }
  },
  mounted() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('habitTrackerDarkMode');
    if (savedTheme !== null) {
      this.darkMode = savedTheme === 'true';
    }
    
    // Load tasks from localStorage if available
    const savedTasks = localStorage.getItem('habitTrackerTasks');
    if (savedTasks) {
      this.tasks = JSON.parse(savedTasks);
    }
  },
  methods: {
    toggleTheme() {
      this.darkMode = !this.darkMode;
      localStorage.setItem('habitTrackerDarkMode', this.darkMode);
    },
    toggleTaskCompletion(id) {
      const taskIndex = this.tasks.findIndex(task => task.id === id);
      if (taskIndex !== -1) {
        const task = this.tasks[taskIndex];
        task.completed = !task.completed;
        
        if (task.completed) {
          task.completedAt = new Date().toISOString().split('T')[0];
          task.streak++;
        } else {
          task.completedAt = null;
          if (task.streak > 0) task.streak--;
        }
        
        this.saveTasks();
      }
    },
    addTask() {
      const newTask = {
        ...this.currentTask,
        id: Date.now(),
        createdAt: new Date().toISOString().split('T')[0],
        completed: false,
        completedAt: null,
        streak: 0
      };
      
      this.tasks.unshift(newTask);
      this.saveTasks();
      this.closeModal();
      this.resetCurrentTask();
    },
    editTask(task) {
      this.currentTask = { ...task };
      this.showEditModal = true;
    },
    updateTask() {
      const taskIndex = this.tasks.findIndex(task => task.id === this.currentTask.id);
      if (taskIndex !== -1) {
        this.tasks[taskIndex] = { ...this.currentTask };
        this.saveTasks();
        this.closeModal();
        this.resetCurrentTask();
      }
    },
    deleteTask(id) {
      if (confirm('Are you sure you want to delete this task?')) {
        this.tasks = this.tasks.filter(task => task.id !== id);
        this.saveTasks();
      }
    },
    closeModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.resetCurrentTask();
    },
    resetCurrentTask() {
      this.currentTask = {
        id: null,
        title: '',
        description: '',
        type: 'task',
        category: 'Personal',
        priority: 'medium',
        color: '#4CAF50',
        completed: false,
        createdAt: null,
        completedAt: null,
        streak: 0,
        frequency: 'daily'
      };
    },
    saveTasks() {
      localStorage.setItem('habitTrackerTasks', JSON.stringify(this.tasks));
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

#app {
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #333;
  transition: background-color 0.3s, color 0.3s;
}

#app.dark-mode {
  background-color: #121212;
  color: #f5f5f5;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header Styles */
.header {
  padding: 24px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

#app.dark-mode .header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  font-size: 28px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #4CAF50;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.theme-toggle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-color: #e8f5e9;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4CAF50;
  font-size: 18px;
  transition: all 0.3s;
}

#app.dark-mode .theme-toggle {
  background-color: #333;
  color: #FFC107;
}

.theme-toggle:hover {
  transform: scale(1.05);
}

.btn-add {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-add:hover {
  background-color: #3d8b40;
  transform: translateY(-2px);
}

/* Stats Container */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}

#app.dark-mode .stat-card {
  background-color: #1e1e1e;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

#app.dark-mode .stat-label {
  color: #aaa;
}

/* Filter Tabs */
.filter-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filter-tab {
  padding: 10px 20px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

#app.dark-mode .filter-tab {
  background-color: #1e1e1e;
  border-color: #444;
  color: #f5f5f5;
}

.filter-tab.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.filter-tab:hover:not(.active) {
  background-color: #f5f5f5;
}

#app.dark-mode .filter-tab:hover:not(.active) {
  background-color: #333;
}

/* Tasks Container */
.tasks-container {
  margin-bottom: 40px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

#app.dark-mode .empty-state {
  color: #aaa;
}

.empty-state i {
  font-size: 64px;
  margin-bottom: 20px;
  color: #ddd;
}

.empty-state h3 {
  font-size: 24px;
  margin-bottom: 10px;
}

.empty-state p {
  margin-bottom: 20px;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-primary:hover {
  background-color: #3d8b40;
  transform: translateY(-2px);
}

/* Task Cards */
.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  border-left: 4px solid #4CAF50;
}

#app.dark-mode .task-card {
  background-color: #1e1e1e;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.task-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.task-card.completed {
  opacity: 0.8;
  border-left-color: #9e9e9e;
}

.task-card.habit {
  border-left-color: #FF9800;
}

.task-card.priority-high {
  border-left-color: #F44336;
}

.task-card.priority-medium {
  border-left-color: #FF9800;
}

.task-main {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  flex: 1;
}

.task-checkbox {
  margin-top: 4px;
}

.checkbox {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 2px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.checkbox.checked {
  background-color: #4CAF50;
  border-color: #4CAF50;
  color: white;
}

.task-info {
  flex: 1;
}

.task-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.task-title.completed {
  text-decoration: line-through;
  color: #9e9e9e;
}

.task-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.5;
}

#app.dark-mode .task-description {
  color: #aaa;
}

.task-meta {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.task-category, .task-type, .task-priority, .task-streak {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  background-color: #f5f5f5;
  color: #333;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

#app.dark-mode .task-category,
#app.dark-mode .task-type,
#app.dark-mode .task-priority,
#app.dark-mode .task-streak {
  background-color: #333;
  color: #f5f5f5;
}

.task-actions {
  display: flex;
  gap: 10px;
}

.task-action-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background-color: #f5f5f5;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

#app.dark-mode .task-action-btn {
  background-color: #333;
  color: #aaa;
}

.task-action-btn:hover {
  background-color: #e0e0e0;
  color: #333;
}

#app.dark-mode .task-action-btn:hover {
  background-color: #444;
  color: #f5f5f5;
}

.task-action-btn.delete:hover {
  background-color: #ffebee;
  color: #F44336;
}

/* Progress Section */
.progress-section {
  background-color: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

#app.dark-mode .progress-section {
  background-color: #1e1e1e;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.section-title {
  font-size: 20px;
  margin-bottom: 20px;
}

.progress-chart {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  height: 200px;
  padding-top: 20px;
}

.progress-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 80px;
}

.progress-bar-container {
  width: 30px;
  height: 120px;
  background-color: #f5f5f5;
  border-radius: 6px;
  margin-bottom: 10px;
  position: relative;
  overflow: hidden;
}

#app.dark-mode .progress-bar-container {
  background-color: #333;
}

.progress-bar {
  position: absolute;
  bottom: 0;
  width: 100%;
  background-color: #4CAF50;
  border-radius: 6px;
  transition: height 1s ease;
}

.progress-bar.today {
  background-color: #FF9800;
}

.progress-day-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

#app.dark-mode .progress-day-label {
  color: #aaa;
}

.progress-day-value {
  font-size: 11px;
  color: #999;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background-color: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

#app.dark-mode .modal-content {
  background-color: #1e1e1e;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #eee;
}

#app.dark-mode .modal-header {
  border-bottom: 1px solid #333;
}

.modal-header h2 {
  font-size: 22px;
  font-weight: 600;
}

.modal-close {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background-color: #f5f5f5;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

#app.dark-mode .modal-close {
  background-color: #333;
  color: #aaa;
}

.modal-close:hover {
  background-color: #e0e0e0;
  color: #333;
}

#app.dark-mode .modal-close:hover {
  background-color: #444;
  color: #f5f5f5;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 16px;
  transition: all 0.3s;
  background-color: white;
}

#app.dark-mode .form-group input,
#app.dark-mode .form-group textarea,
#app.dark-mode .form-group select {
  background-color: #333;
  border-color: #555;
  color: #f5f5f5;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-row .form-group {
  flex: 1;
}

.type-selector,
.frequency-selector {
  display: flex;
  gap: 10px;
}

.type-option,
.frequency-option {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

#app.dark-mode .type-option,
#app.dark-mode .frequency-option {
  background-color: #333;
  border-color: #555;
  color: #f5f5f5;
}

.type-option.active,
.frequency-option.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.color-selector {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.color-option {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
  border: 2px solid transparent;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.selected {
  border-color: #333;
  transform: scale(1.1);
}

#app.dark-mode .color-option.selected {
  border-color: #f5f5f5;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

#app.dark-mode .modal-footer {
  border-top: 1px solid #333;
}

.btn-secondary {
  padding: 12px 24px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background-color: white;
  color: #333;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

#app.dark-mode .btn-secondary {
  background-color: #333;
  border-color: #555;
  color: #f5f5f5;
}

.btn-secondary:hover {
  background-color: #f5f5f5;
}

#app.dark-mode .btn-secondary:hover {
  background-color: #444;
}

/* Responsive Design */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .progress-chart {
    height: 160px;
  }
  
  .progress-day {
    max-width: 40px;
  }
  
  .progress-bar-container {
    width: 20px;
  }
}

@media (max-width: 480px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .filter-tabs {
    justify-content: center;
  }
  
  .task-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .task-actions {
    align-self: flex-end;
  }
}
</style>