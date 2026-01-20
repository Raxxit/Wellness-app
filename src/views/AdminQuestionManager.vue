<script setup>
import { ref, onMounted } from 'vue';

// --- STATE ---
const questionText = ref('');
const selectedType = ref('0');
const options = ref([{ text: '', weight: 0 }]);
const questionsList = ref([]); // Store loaded questions here

const questionTypes = [
    { val: '0', label: 'Type 0: Goals Grid (Emoji Cards)' },
    { val: '1', label: 'Type 1: Sleep Row (Emoji Scale)' },
    { val: '2', label: 'Type 2: Slider (Min/Max Labels)' },
    { val: '3', label: 'Type 3: Habits List (Checkboxes)' },
    { val: '4', label: 'Type 4: Energy (3-Part Day)' },
    { val: '5', label: 'Type 5: Simple Radio List' },
    { val: '6', label: 'Type 6: Open Text Box' }
];

// --- ACTIONS ---
const addOptionRow = () => options.value.push({ text: '', weight: 0 });
const removeOptionRow = (index) => options.value.splice(index, 1);

// 1. Fetch questions from server
const loadQuestions = async () => {
    try {
        const res = await fetch('/api/questionnaire');
        if (res.ok) {
            questionsList.value = await res.json();
        }
    } catch (err) {
        console.error("Failed to load questions", err);
    }
};

// 2. Submit new question
const submitQuestion = async () => {
    if (!questionText.value) return alert("Enter a question text");

    const payload = {
        text: questionText.value,
        type: selectedType.value,
        options: options.value
    };

    const res = await fetch('/api/add-question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert('Question Saved!');
        // Reset Form
        questionText.value = '';
        options.value = [{ text: '', weight: 0 }];
        // Refresh List
        await loadQuestions();
    }
};

// 3. Delete question
const deleteQuestion = async (id) => {
    if (!confirm("Are you sure you want to delete this question?")) return;

    const res = await fetch(`/api/delete-question/${id}`, {
        method: 'DELETE'
    });

    if (res.ok) {
        // Remove from local list immediately
        questionsList.value = questionsList.value.filter(q => q.id !== id);
    } else {
        alert("Failed to delete");
    }
};

// Load on startup
onMounted(() => {
    loadQuestions();
});
</script>

<template>
    <div class="container py-5">
        <div class="row">
            <div class="col-md-5">
                <div class="card shadow p-4 mb-4 sticky-top" style="top: 20px; z-index: 1;">
                    <h3 class="mb-3 text-primary">Add New Question</h3>

                    <div class="mb-3">
                        <label class="form-label fw-bold">Question Text</label>
                        <input v-model="questionText" type="text" class="form-control"
                            placeholder="e.g. How did you sleep?">
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-bold">Display Style</label>
                        <select v-model="selectedType" class="form-select">
                            <option v-for="t in questionTypes" :key="t.val" :value="t.val">
                                {{ t.label }}
                            </option>
                        </select>
                        <div class="form-text text-primary small" v-if="['0', '1'].includes(selectedType)">
                            💡 Tip: Add emojis for this style! (e.g. "😴 Poor")
                        </div>
                    </div>

                    <label class="form-label fw-bold mt-2">Answers & Weights</label>
                    <div v-for="(opt, index) in options" :key="index" class="row g-1 mb-2">
                        <div class="col-7">
                            <input v-model="opt.text" type="text" class="form-control form-control-sm"
                                placeholder="Answer text">
                        </div>
                        <div class="col-3">
                            <input v-model="opt.weight" type="number" class="form-control form-control-sm"
                                placeholder="Pts">
                        </div>
                        <div class="col-2">
                            <button @click="removeOptionRow(index)"
                                class="btn btn-outline-danger btn-sm w-100">×</button>
                        </div>
                    </div>
                    <button @click="addOptionRow" class="btn btn-light btn-sm border mt-1 w-100">+ Add Option</button>

                    <hr>
                    <button @click="submitQuestion" class="btn btn-primary w-100 fw-bold">Save Question</button>
                </div>
            </div>

            <div class="col-md-7">
                <h3 class="mb-3 text-secondary">Existing Questions ({{ questionsList.length }})</h3>

                <div v-if="questionsList.length === 0" class="alert alert-info">
                    No questions found in the database.
                </div>

                <div v-for="q in questionsList" :key="q.id" class="card mb-3 shadow-sm border-0">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <span class="badge bg-secondary mb-2">Type {{ q.type }}</span>
                                <h5 class="card-title mb-1">{{ q.text }}</h5>
                            </div>
                            <button @click="deleteQuestion(q.id)" class="btn btn-danger btn-sm">
                                <i class="fa fa-trash"></i> Delete
                            </button>
                        </div>

                        <div class="mt-3 bg-light p-2 rounded">
                            <small class="text-muted fw-bold text-uppercase">Options:</small>
                            <ul class="list-unstyled mb-0 mt-1">
                                <li v-for="opt in q.options" :key="opt.id"
                                    class="small d-flex justify-content-between border-bottom py-1">
                                    <span>{{ opt.text }}</span>
                                    <span class="badge bg-light text-dark border">{{ opt.weight }} pts</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>