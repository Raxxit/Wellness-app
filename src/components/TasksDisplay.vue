<script setup>
defineProps({
  tasks: {
    type: Array,
    required: true
  },
  userState: {
    type: String,
    default: 'healthy'
  }
});

const emit = defineEmits(['task-completed', 'task-uncompleted']);

const handleTaskToggle = (task) => {
  const updatedTask = { ...task, completed: !task.completed };
  if (updatedTask.completed) {
    emit('task-completed', updatedTask);
  } else {
    emit('task-uncompleted', updatedTask);
  }
};
</script>

<template>
  <div class="list-group list-group-flush">
    <div v-for="task in tasks" :key="task.id"
         class="list-group-item border-0 border-bottom py-3 d-flex align-items-center">
      
      <input class="form-check-input fs-5 me-3 rounded-circle" 
             type="checkbox" 
             :checked="task.completed"
             @change="handleTaskToggle(task)"
             style="cursor: pointer;">

      <div class="flex-grow-1">
        <div class="fw-bold" :class="{ 'text-decoration-line-through text-muted': task.completed }">
          {{ task.title }}
        </div>
        <span class="badge rounded-pill" :class="{
          'bg-danger': task.priority === 'high',
          'bg-warning text-dark': task.priority === 'medium',
          'bg-secondary': task.priority === 'low'
        }">
          {{ task.priority.toUpperCase() }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.list-group-item {
  transition: background-color 0.2s ease;
  padding-left: 0;
  padding-right: 0;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>