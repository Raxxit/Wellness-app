<script setup>
import { ref } from 'vue';

const questionText = ref('');
const selectedType = ref('0'); // Default to Type 0
const options = ref([{ text: '', weight: 0 }]);

// The 7 Types mapped to 0-6
const questionTypes = [
    { val: '0', label: 'Type 0: Goals Grid (Emoji Cards)' },
    { val: '1', label: 'Type 1: Sleep Row (Emoji Scale)' },
    { val: '2', label: 'Type 2: Slider (Min/Max Labels)' },
    { val: '3', label: 'Type 3: Habits List (Checkboxes)' },
    { val: '4', label: 'Type 4: Energy (3-Part Day)' },
    { val: '5', label: 'Type 5: Simple Radio List' },
    { val: '6', label: 'Type 6: Open Text Box' }
];

const addOptionRow = () => options.value.push({ text: '', weight: 0 });
const removeOptionRow = (index) => options.value.splice(index, 1);

const submitQuestion = async () => {
    // Basic validation
    if (!questionText.value) return alert("Enter a question text");

    const payload = {
        text: questionText.value,
        type: selectedType.value, // Sends "0", "1", etc.
        options: options.value
    };

    const res = await fetch('/api/add-question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert('Question Saved!');
        questionText.value = '';
        options.value = [{ text: '', weight: 0 }];
    }
};
</script>

<template>
    <div class="container py-5">
        <div class="card shadow p-4">
            <h2 class="mb-4">Add Question</h2>

            <div class="mb-3">
                <label class="form-label">Question</label>
                <input v-model="questionText" type="text" class="form-control" placeholder="e.g. What are your goals?">
            </div>

            <div class="mb-3">
                <label class="form-label">Display Style</label>
                <select v-model="selectedType" class="form-select">
                    <option v-for="t in questionTypes" :key="t.val" :value="t.val">
                        {{ t.label }}
                    </option>
                </select>
                <div class="form-text text-primary" v-if="['0', '1'].includes(selectedType)">
                    💡 Tip: For this style, add an emoji at the start of your answer text! <br>
                    (e.g. "🧘 Stress Relief" or "😴 Poor")
                </div>
            </div>

            <h5 class="mt-4">Answers</h5>
            <div v-for="(opt, index) in options" :key="index" class="row g-2 mb-2">
                <div class="col-8">
                    <input v-model="opt.text" type="text" class="form-control"
                        placeholder="Answer (e.g. 🧘 Stress Relief)">
                </div>
                <div class="col-2">
                    <input v-model="opt.weight" type="number" class="form-control" placeholder="Pts">
                </div>
                <div class="col-2">
                    <button @click="removeOptionRow(index)" class="btn btn-danger btn-sm">X</button>
                </div>
            </div>
            <button @click="addOptionRow" class="btn btn-secondary btn-sm mt-2">+ Add Option</button>

            <hr>
            <button @click="submitQuestion" class="btn btn-success w-100">Save to Database</button>
        </div>
    </div>
</template>