<script setup>
import { ref, onMounted, computed } from 'vue'
import { WOW } from 'wowjs'

// Define question types
const QUESTION_TYPES = [
  { id: 'yes_no', name: 'Yes/No Question' },
  { id: 'multiple_choice', name: 'Multiple Choice' },
  { id: 'multiple_select', name: 'Multiple Selection (Checkboxes)' },
  { id: 'emoji_rating', name: 'Emoji Rating' },
  { id: 'slider', name: 'Slider/Range' },
  { id: 'energy_levels', name: 'Energy Levels (Morning/Afternoon/Evening)' }
]

// Sample data structure for existing questions
const existingQuestions = ref([
  {
    id: 1,
    section: 'Health & Lifestyle',
    title: 'Do you have any chronic health conditions? (e.g., diabetes, hypertension)',
    type: 'yes_no',
    required: true,
    order: 1,
    options: []
  },
  {
    id: 2,
    section: 'Health & Lifestyle',
    title: 'Do you take any regular medication?',
    type: 'yes_no',
    required: true,
    order: 2,
    options: []
  },
  {
    id: 3,
    section: 'Daily Life & Habits',
    title: 'What is your typical work schedule?',
    type: 'multiple_choice',
    required: true,
    order: 3,
    options: ['9-5 office job', 'Shift work', 'Remote/flexible', 'Unemployed/retired']
  },
  {
    id: 4,
    section: 'Daily Life & Habits',
    title: 'How much water do you drink daily?',
    type: 'multiple_choice',
    required: true,
    order: 4,
    options: ['Less than 4 glasses', '4-6 glasses', '7-8 glasses', 'More than 8 glasses']
  },
  {
    id: 5,
    section: 'Wellness Goals',
    title: 'What are your primary wellness goals?',
    type: 'multiple_select',
    required: true,
    order: 5,
    options: ['Stress Relief', 'Better Sleep', 'More Energy', 'Mindfulness', 'Mental Health', 'Nutrition']
  },
  {
    id: 6,
    section: 'Sleep Quality',
    title: 'How would you rate your sleep quality?',
    type: 'emoji_rating',
    required: true,
    order: 6,
    options: ['Poor', 'Fair', 'Good', 'Great', 'Excellent']
  },
  {
    id: 7,
    section: 'Stress Level',
    title: 'Current stress level',
    type: 'slider',
    required: false,
    order: 7,
    options: ['1', '10', '5'] // min, max, default
  },
  {
    id: 8,
    section: 'Daily Habits',
    title: 'Which wellness activities do you currently practice?',
    type: 'multiple_select',
    required: false,
    order: 8,
    options: ['Meditation', 'Exercise', 'Journaling', 'Yoga', 'Walking', 'Breathing']
  },
  {
    id: 9,
    section: 'Energy Levels',
    title: 'How\'s your energy throughout the day?',
    type: 'energy_levels',
    required: true,
    order: 9,
    options: ['Morning', 'Afternoon', 'Evening']
  }
])

// New question form
const newQuestion = ref({
  section: '',
  title: '',
  type: 'multiple_choice',
  required: true,
  options: [''],
  order: 0
})

// Edit mode
const editingQuestion = ref(null)
const showNewQuestionForm = ref(false)
const showDeleteModal = ref(false)
const questionToDelete = ref(null)

// Sections management
const sections = ref(['Health & Lifestyle', 'Daily Life & Habits', 'Wellness Goals', 'Sleep Quality', 'Stress Level', 'Daily Habits', 'Energy Levels'])
const newSection = ref('')

// Filter and sort
const searchQuery = ref('')
const selectedSection = ref('')

// Filtered questions
const filteredQuestions = computed(() => {
  let filtered = [...existingQuestions.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(q => 
      q.title.toLowerCase().includes(query) || 
      q.section.toLowerCase().includes(query)
    )
  }
  
  if (selectedSection.value) {
    filtered = filtered.filter(q => q.section === selectedSection.value)
  }
  
  return filtered.sort((a, b) => a.order - b.order)
})

// Add new option field for multiple choice/multiple select questions
const addOption = () => {
  newQuestion.value.options.push('')
}

// Remove option field
const removeOption = (index) => {
  if (newQuestion.value.options.length > 1) {
    newQuestion.value.options.splice(index, 1)
  }
}

// Reset new question form
const resetNewQuestionForm = () => {
  newQuestion.value = {
    section: '',
    title: '',
    type: 'multiple_choice',
    required: true,
    options: [''],
    order: existingQuestions.value.length + 1
  }
  showNewQuestionForm.value = true
  editingQuestion.value = null
}

// Start editing a question
const startEditQuestion = (question) => {
  editingQuestion.value = question
  newQuestion.value = {
    section: question.section,
    title: question.title,
    type: question.type,
    required: question.required,
    options: [...question.options],
    order: question.order
  }
  showNewQuestionForm.value = true
}

// Add new question
const addQuestion = () => {
  if (!newQuestion.value.title.trim() || !newQuestion.value.section.trim()) {
    alert('Please fill in all required fields')
    return
  }
  
  const question = {
    id: existingQuestions.value.length > 0 ? Math.max(...existingQuestions.value.map(q => q.id)) + 1 : 1,
    ...newQuestion.value,
    options: [...newQuestion.value.options.filter(opt => opt.trim() !== '')]
  }
  
  existingQuestions.value.push(question)
  resetNewQuestionForm()
  showNewQuestionForm.value = false
  
  alert('Question added successfully!')
}

// Update existing question
const updateQuestion = () => {
  if (!newQuestion.value.title.trim() || !newQuestion.value.section.trim()) {
    alert('Please fill in all required fields')
    return
  }
  
  const index = existingQuestions.value.findIndex(q => q.id === editingQuestion.value.id)
  if (index !== -1) {
    existingQuestions.value[index] = {
      ...existingQuestions.value[index],
      ...newQuestion.value,
      options: [...newQuestion.value.options.filter(opt => opt.trim() !== '')]
    }
  }
  
  resetNewQuestionForm()
  showNewQuestionForm.value = false
  editingQuestion.value = null
  
  alert('Question updated successfully!')
}

// Delete question
const confirmDelete = (question) => {
  questionToDelete.value = question
  showDeleteModal.value = true
}

const deleteQuestion = () => {
  if (questionToDelete.value) {
    const index = existingQuestions.value.findIndex(q => q.id === questionToDelete.value.id)
    if (index !== -1) {
      existingQuestions.value.splice(index, 1)
      // Reorder remaining questions
      existingQuestions.value.forEach((q, idx) => {
        q.order = idx + 1
      })
    }
  }
  showDeleteModal.value = false
  questionToDelete.value = null
  alert('Question deleted successfully!')
}

// Move question up/down
const moveQuestion = (question, direction) => {
  const currentIndex = existingQuestions.value.findIndex(q => q.id === question.id)
  const newIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1
  
  if (newIndex >= 0 && newIndex < existingQuestions.value.length) {
    // Swap orders
    const tempOrder = existingQuestions.value[currentIndex].order
    existingQuestions.value[currentIndex].order = existingQuestions.value[newIndex].order
    existingQuestions.value[newIndex].order = tempOrder
    
    // Swap array positions
    [existingQuestions.value[currentIndex], existingQuestions.value[newIndex]] = 
    [existingQuestions.value[newIndex], existingQuestions.value[currentIndex]]
  }
}

// Add new section
const addSection = () => {
  if (newSection.value.trim() && !sections.value.includes(newSection.value.trim())) {
    sections.value.push(newSection.value.trim())
    newSection.value = ''
    alert('New section added!')
  }
}

// Remove section (if no questions are using it)
const removeSection = (section) => {
  const questionsInSection = existingQuestions.value.filter(q => q.section === section)
  if (questionsInSection.length > 0) {
    alert(`Cannot delete section "${section}" because it has ${questionsInSection.length} question(s). Move or delete those questions first.`)
    return
  }
  
  sections.value = sections.value.filter(s => s !== section)
  alert('Section removed!')
}

// Export questions as JSON
const exportQuestions = () => {
  const dataStr = JSON.stringify(existingQuestions.value, null, 2)
  const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
  
  const exportFileDefaultName = 'wellness-questions.json'
  
  const linkElement = document.createElement('a')
  linkElement.setAttribute('href', dataUri)
  linkElement.setAttribute('download', exportFileDefaultName)
  linkElement.click()
  
  alert('Questions exported successfully!')
}

// Import questions from JSON
const importQuestions = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const importedQuestions = JSON.parse(e.target.result)
      // Validate imported data
      if (Array.isArray(importedQuestions)) {
        existingQuestions.value = importedQuestions
        alert('Questions imported successfully!')
      } else {
        alert('Invalid file format. Please upload a valid JSON file.')
      }
    } catch (error) {
      alert('Error parsing JSON file. Please check the file format.')
    }
  }
  reader.readAsText(file)
}

// Preview questions
const previewQuestions = () => {
  // Save current questions to localStorage for preview
  localStorage.setItem('wellnessQuestionsPreview', JSON.stringify(existingQuestions.value))
  window.open('/preview', '_blank') // You would need to create a preview page
}

// Helper function to safely get array element with default value
const getOptionValue = (options, index, defaultValue = '') => {
  return options && options.length > index ? options[index] : defaultValue
}

onMounted(() => {
  new WOW().init()
})
</script>

<template>
  <div class="admin-page">
    <!-- Header -->
    <header class="py-4 bg-gradient-primary border-bottom">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="display-5 fw-bold text-white">Questionnaire Admin Panel</h1>
            <p class="lead text-light mb-0">Manage your wellness assessment questions</p>
          </div>
          <div class="col-md-6 text-end">
            <div class="btn-group">
              <button class="btn btn-light me-2" @click="previewQuestions">
                <i class="fas fa-eye me-2"></i>Preview
              </button>
              <button class="btn btn-light me-2" @click="exportQuestions">
                <i class="fas fa-download me-2"></i>Export
              </button>
              <label class="btn btn-light">
                <i class="fas fa-upload me-2"></i>Import
                <input type="file" accept=".json" @change="importQuestions" class="d-none">
              </label>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="container-fluid py-4">
      <div class="row">
        <!-- Left Sidebar: Sections & Stats -->
        <div class="col-lg-3 mb-4">
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Statistics</h5>
            </div>
            <div class="card-body">
              <div class="row text-center">
                <div class="col-6 mb-3">
                  <div class="display-6 fw-bold text-primary">{{ existingQuestions.length }}</div>
                  <small class="text-muted">Total Questions</small>
                </div>
                <div class="col-6 mb-3">
                  <div class="display-6 fw-bold text-success">{{ sections.length }}</div>
                  <small class="text-muted">Sections</small>
                </div>
                <div class="col-6">
                  <div class="display-6 fw-bold text-warning">
                    {{ existingQuestions.filter(q => q.required).length }}
                  </div>
                  <small class="text-muted">Required</small>
                </div>
                <div class="col-6">
                  <div class="display-6 fw-bold text-info">
                    {{ existingQuestions.filter(q => !q.required).length }}
                  </div>
                  <small class="text-muted">Optional</small>
                </div>
              </div>
            </div>
          </div>

          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="fas fa-folder me-2"></i>Sections</h5>
              <button class="btn btn-sm btn-light" @click="resetNewQuestionForm">
                <i class="fas fa-plus"></i>
              </button>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="input-group">
                  <input 
                    type="text" 
                    v-model="newSection" 
                    class="form-control" 
                    placeholder="New section name"
                    @keyup.enter="addSection"
                  >
                  <button class="btn btn-primary" @click="addSection">
                    <i class="fas fa-plus"></i>
                  </button>
                </div>
              </div>
              
              <div class="list-group">
                <div 
                  v-for="section in sections" 
                  :key="section"
                  class="list-group-item d-flex justify-content-between align-items-center"
                >
                  <span>{{ section }}</span>
                  <button 
                    class="btn btn-sm btn-outline-danger"
                    @click="removeSection(section)"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content: Questions List & Form -->
        <div class="col-lg-9">
          <!-- Search and Filter -->
          <div class="card shadow-sm mb-4">
            <div class="card-body">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <div class="input-group">
                    <span class="input-group-text"><i class="fas fa-search"></i></span>
                    <input 
                      type="text" 
                      v-model="searchQuery" 
                      class="form-control" 
                      placeholder="Search questions..."
                    >
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <select v-model="selectedSection" class="form-select">
                    <option value="">All Sections</option>
                    <option v-for="section in sections" :key="section" :value="section">
                      {{ section }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="d-flex justify-content-between">
                <span class="text-muted">
                  Showing {{ filteredQuestions.length }} of {{ existingQuestions.length }} questions
                </span>
                <button class="btn btn-primary" @click="resetNewQuestionForm">
                  <i class="fas fa-plus me-2"></i>Add New Question
                </button>
              </div>
            </div>
          </div>

          <!-- New/Edit Question Form -->
          <div v-if="showNewQuestionForm" class="card shadow-sm mb-4 wow fadeInUp">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">
                <i class="fas fa-question-circle me-2"></i>
                {{ editingQuestion ? 'Edit Question' : 'Add New Question' }}
              </h5>
              <button class="btn btn-sm btn-light" @click="showNewQuestionForm = false">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="card-body">
              <form @submit.prevent="editingQuestion ? updateQuestion() : addQuestion()">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label class="form-label">Section *</label>
                    <select v-model="newQuestion.section" class="form-select" required>
                      <option value="">Select a section</option>
                      <option v-for="section in sections" :key="section" :value="section">
                        {{ section }}
                      </option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label">Question Type *</label>
                    <select v-model="newQuestion.type" class="form-select" required>
                      <option v-for="type in QUESTION_TYPES" :key="type.id" :value="type.id">
                        {{ type.name }}
                      </option>
                    </select>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Question Text *</label>
                  <textarea 
                    v-model="newQuestion.title" 
                    class="form-control" 
                    rows="3" 
                    placeholder="Enter your question..."
                    required
                  ></textarea>
                </div>

                <!-- Options for multiple choice/select questions -->
                <div v-if="['multiple_choice', 'multiple_select'].includes(newQuestion.type)" class="mb-3">
                  <label class="form-label">Options *</label>
                  <div v-for="(option, index) in newQuestion.options" :key="index" class="input-group mb-2">
                    <input 
                      type="text" 
                      v-model="newQuestion.options[index]" 
                      class="form-control" 
                      :placeholder="`Option ${index + 1}`"
                      required
                    >
                    <button 
                      v-if="newQuestion.options.length > 1"
                      class="btn btn-outline-danger" 
                      type="button"
                      @click="removeOption(index)"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                  <button class="btn btn-outline-primary btn-sm" type="button" @click="addOption">
                    <i class="fas fa-plus me-1"></i>Add Option
                  </button>
                </div>

                <!-- Options for emoji rating -->
                <div v-if="newQuestion.type === 'emoji_rating'" class="mb-3">
                  <label class="form-label">Rating Labels</label>
                  <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    Emoji rating questions use predefined labels: Poor, Fair, Good, Great, Excellent
                  </div>
                </div>

                <!-- Options for slider -->
                <div v-if="newQuestion.type === 'slider'" class="mb-3">
                  <div class="row">
                    <div class="col-md-4">
                      <label class="form-label">Minimum Value</label>
                      <input 
                        type="number" 
                        :value="getOptionValue(newQuestion.options, 0, '1')"
                        @input="newQuestion.options[0] = $event.target.value || '1'"
                        class="form-control" 
                        min="0"
                        max="100"
                      >
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Maximum Value</label>
                      <input 
                        type="number" 
                        :value="getOptionValue(newQuestion.options, 1, '10')"
                        @input="newQuestion.options[1] = $event.target.value || '10'"
                        class="form-control" 
                        min="1"
                        max="100"
                      >
                    </div>
                    <div class="col-md-4">
                      <label class="form-label">Default Value</label>
                      <input 
                        type="number" 
                        :value="getOptionValue(newQuestion.options, 2, '5')"
                        @input="newQuestion.options[2] = $event.target.value || '5'"
                        class="form-control"
                        :min="getOptionValue(newQuestion.options, 0, 1)"
                        :max="getOptionValue(newQuestion.options, 1, 10)"
                      >
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="form-check mb-3">
                      <input 
                        type="checkbox" 
                        v-model="newQuestion.required" 
                        class="form-check-input" 
                        id="requiredCheck"
                      >
                      <label class="form-check-label" for="requiredCheck">
                        Required Question
                      </label>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Display Order</label>
                      <input 
                        type="number" 
                        v-model="newQuestion.order" 
                        class="form-control" 
                        min="1"
                        :max="existingQuestions.length + 1"
                      >
                    </div>
                  </div>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="button" class="btn btn-outline-secondary me-2" @click="showNewQuestionForm = false">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save me-2"></i>
                    {{ editingQuestion ? 'Update Question' : 'Save Question' }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Questions List -->
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0"><i class="fas fa-list me-2"></i>Questions List</h5>
            </div>
            <div class="card-body">
              <div v-if="filteredQuestions.length === 0" class="text-center py-5">
                <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                <h5>No questions found</h5>
                <p class="text-muted">Try adjusting your search or add a new question</p>
              </div>

              <div v-else class="list-group">
                <div 
                  v-for="question in filteredQuestions" 
                  :key="question.id"
                  class="list-group-item list-group-item-action"
                >
                  <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                      <div class="d-flex align-items-center mb-1">
                        <span class="badge bg-primary me-2">#{{ question.order }}</span>
                        <span class="badge" :class="{
                          'bg-success': question.required,
                          'bg-secondary': !question.required
                        }">
                          {{ question.required ? 'Required' : 'Optional' }}
                        </span>
                        <span class="badge bg-info ms-2">{{ question.type }}</span>
                        <small class="text-muted ms-2">{{ question.section }}</small>
                      </div>
                      <h6 class="mb-1">{{ question.title }}</h6>
                      <div v-if="question.options && question.options.length > 0" class="mt-2">
                        <small class="text-muted">Options:</small>
                        <div class="d-flex flex-wrap gap-1 mt-1">
                          <span 
                            v-for="(option, idx) in question.options" 
                            :key="idx"
                            class="badge bg-light text-dark border"
                          >
                            {{ option }}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div class="btn-group btn-group-sm">
                      <button 
                        class="btn btn-outline-primary"
                        @click="moveQuestion(question, 'up')"
                        :disabled="question.order === 1"
                      >
                        <i class="fas fa-arrow-up"></i>
                      </button>
                      <button 
                        class="btn btn-outline-primary"
                        @click="moveQuestion(question, 'down')"
                        :disabled="question.order === existingQuestions.length"
                      >
                        <i class="fas fa-arrow-down"></i>
                      </button>
                      <button 
                        class="btn btn-outline-warning"
                        @click="startEditQuestion(question)"
                      >
                        <i class="fas fa-edit"></i>
                      </button>
                      <button 
                        class="btn btn-outline-danger"
                        @click="confirmDelete(question)"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="fas fa-exclamation-triangle me-2"></i>
              Confirm Deletion
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this question?</p>
            <div class="alert alert-warning">
              <strong>"{{ questionToDelete?.title }}"</strong>
              <br>
              <small>Section: {{ questionToDelete?.section }} | Type: {{ questionToDelete?.type }}</small>
            </div>
            <p class="text-danger">
              <i class="fas fa-exclamation-circle me-1"></i>
              This action cannot be undone.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
              Cancel
            </button>
            <button type="button" class="btn btn-danger" @click="deleteQuestion">
              <i class="fas fa-trash me-2"></i>Delete Question
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
.admin-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card {
  border: none;
  border-radius: 10px;
  margin-bottom: 20px;
}

.card-header {
  border-radius: 10px 10px 0 0 !important;
  padding: 1rem 1.5rem;
}

.list-group-item {
  border: 1px solid rgba(0,0,0,.125);
  margin-bottom: 8px;
  border-radius: 8px !important;
  transition: all 0.2s ease;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
}

/* Question type badges */
.bg-info {
  background-color: #17a2b8 !important;
}

/* Custom scrollbar */
.card-body {
  max-height: 500px;
  overflow-y: auto;
}

.card-body::-webkit-scrollbar {
  width: 6px;
}

.card-body::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.card-body::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

.card-body::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Input group styling */
.input-group-text {
  background-color: #f8f9fa;
  border-right: none;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Modal styling */
.modal-content {
  border: none;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .btn-group {
    flex-wrap: wrap;
    margin-top: 10px;
  }
  
  .btn-group .btn {
    margin-bottom: 5px;
  }
  
  .list-group-item {
    padding: 0.75rem;
  }
  
  .btn-group-sm .btn {
    padding: 0.2rem 0.4rem;
    font-size: 0.8rem;
  }
}
</style>