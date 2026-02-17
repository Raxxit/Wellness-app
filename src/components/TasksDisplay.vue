<script setup>
import { computed, onMounted } from 'vue';

const props = defineProps({
  userState: {
    type: String,
    default: 'healthy' // healthy, mild-anxiety, severe-anxiety
  }
});

// Hardcoded tasks for each state
const tasksByState = {
  'healthy': [
    { id: 1, title: 'Morning meditation (10 mins)', priority: 'medium', completed: false },
    { id: 2, title: 'Drink 8 glasses of water', priority: 'high', completed: false },
    { id: 3, title: '15-minute walk outside', priority: 'medium', completed: false },
    { id: 4, title: 'Read a book (20 mins)', priority: 'low', completed: false },
    { id: 5, title: 'Practice gratitude journaling', priority: 'medium', completed: false },
    { id: 6, title: 'Connect with a friend', priority: 'low', completed: false }
  ],
  'mild-anxiety': [
    { id: 1, title: 'Deep breathing exercise (5 mins)', priority: 'high', completed: false },
    { id: 2, title: 'Progressive muscle relaxation', priority: 'high', completed: false },
    { id: 3, title: 'Limit caffeine intake', priority: 'medium', completed: false },
    { id: 4, title: 'Go for a 20-minute walk', priority: 'high', completed: false },
    { id: 5, title: 'Write down worries & challenge them', priority: 'medium', completed: false },
    { id: 6, title: 'Listen to calming music', priority: 'low', completed: false },
    { id: 7, title: 'Avoid news/social media for 2 hours', priority: 'medium', completed: false }
  ],
  'severe-anxiety': [
    { id: 1, title: '5-4-3-2-1 grounding exercise', priority: 'high', completed: false },
    { id: 2, title: 'Contact your therapist or helpline', priority: 'high', completed: false },
    { id: 3, title: 'Take prescribed medication (if any)', priority: 'high', completed: false },
    { id: 4, title: 'Guided meditation (10-15 mins)', priority: 'high', completed: false },
    { id: 5, title: 'Avoid triggers & stressful situations', priority: 'medium', completed: false },
    { id: 6, title: 'Gentle stretching or yoga', priority: 'medium', completed: false },
    { id: 7, title: 'Stay with a trusted person', priority: 'high', completed: false },
    { id: 8, title: 'Drink herbal tea & rest', priority: 'low', completed: false }
  ]
};

// Emit events
const emit = defineEmits(['task-completed', 'task-uncompleted', 'tasks-loaded']);

const tasks = computed(() => tasksByState[props.userState] || tasksByState.healthy);

const handleTaskToggle = (task) => {
  if (task.completed) {
    emit('task-completed', task);
  } else {
    emit('task-uncompleted', task);
  }
};

// Emit tasks when component is mounted or userState changes
onMounted(() => {
  emit('tasks-loaded', tasks.value);
});

// Helper to get state display name
const stateDisplayName = computed(() => {
  switch(props.userState) {
    case 'healthy': return 'Maintenance Plan';
    case 'mild-anxiety': return 'Mild Anxiety Recovery';
    case 'severe-anxiety': return 'Severe Anxiety Care';
    default: return 'Daily Tasks';
  }
});

// Helper for state-specific styling
const stateBadgeClass = computed(() => {
  switch(props.userState) {
    case 'healthy': return 'bg-success';
    case 'mild-anxiety': return 'bg-warning text-dark';
    case 'severe-anxiety': return 'bg-danger';
    default: return 'bg-primary';
  }
});
</script>

<template>
  <div class="tasks-display">
    <!-- State Header -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="fw-bold mb-0">Today's Recommended Tasks</h6>
      <span class="badge" :class="stateBadgeClass">
        {{ stateDisplayName }}
      </span>
    </div>

    <!-- Tasks List -->
    <div v-if="tasks.length === 0" 
         class="text-center text-muted py-4">
      <i class="bi bi-clipboard2-check fs-1 mb-2"></i>
      <p>No tasks available for your current state.</p>
    </div>

    <div v-else class="list-group list-group-flush">
      <div v-for="task in tasks" :key="task.id"
           class="list-group-item border-0 border-bottom py-3 d-flex align-items-center task-row">
        
        <input class="form-check-input fs-5 me-3 rounded-circle" 
               type="checkbox" 
               v-model="task.completed" 
               @change="handleTaskToggle(task)"
               style="cursor: pointer;">

        <div class="flex-grow-1">
          <div class="fw-bold" 
               :class="{ 'text-decoration-line-through text-muted': task.completed }">
            {{ task.title }}
          </div>
          <span class="badge rounded-pill" style="font-size: 0.65rem;" :class="{
            'bg-danger': task.priority === 'high',
            'bg-warning text-dark': task.priority === 'medium',
            'bg-secondary': task.priority === 'low'
          }">
            {{ task.priority.toUpperCase() }}
          </span>
        </div>
      </div>
    </div>

    <!-- Info Message -->
    <div class="alert alert-info bg-light border-0 mt-3 mb-0 small py-2">
      <i class="bi bi-info-circle me-2"></i>
      These tasks are personalized based on your assessment results.
    </div>
  </div>
</template>

<style scoped>
.task-row:hover {
  background-color: #f8f9fa;
}

.list-group-item {
  transition: background-color 0.2s ease;
  padding-left: 0;
  padding-right: 0;
}

.list-group-item:first-child {
  border-top: none !important;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>