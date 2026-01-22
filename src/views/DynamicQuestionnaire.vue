<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AOS from "aos";
import "aos/dist/aos.css";

const router = useRouter();
const questions = ref([]);
const answers = ref({});
const errors = ref({}); // Store error messages per question
const isLoading = ref(false);

const splitEmoji = (str) => {
    if (!str) return { icon: null, text: '' };
    const emojiRegex = /(\p{Emoji_Presentation}|\p{Extended_Pictographic})/u;
    const match = str.match(emojiRegex);
    if (match && str.indexOf(match[0]) === 0) {
        return { icon: match[0], text: str.replace(match[0], '').trim() };
    }
    return { icon: null, text: str };
};

const toggle = (qId, optId, isMulti) => {
    // Clear error when user interacts
    if (errors.value[qId]) delete errors.value[qId];

    if (!answers.value[qId]) answers.value[qId] = isMulti ? [] : null;

    if (isMulti) {
        const arr = answers.value[qId];
        const idx = arr.indexOf(optId);
        if (idx === -1) arr.push(optId);
        else arr.splice(idx, 1);
    } else {
        answers.value[qId] = optId;
    }
};

const isSelected = (qId, optId) => {
    const val = answers.value[qId];
    return Array.isArray(val) ? val.includes(optId) : val === optId;
};

// --- VALIDATION LOGIC ---
const validateForm = () => {
    errors.value = {}; // Reset errors
    let isValid = true;

    questions.value.forEach(q => {
        const ans = answers.value[q.id];
        const type = String(q.type);

        // Type 0 & 3: Multi-select (Must pick at least one)
        if (['0', '3'].includes(type)) {
            if (!ans || !Array.isArray(ans) || ans.length === 0) {
                errors.value[q.id] = "Please select at least one option.";
                isValid = false;
            }
        }
        // Type 1 & 5: Single Select / Radio (Must pick one)
        else if (['1', '5'].includes(type)) {
            if (ans === null || ans === undefined) {
                errors.value[q.id] = "Please select an option.";
                isValid = false;
            }
        }
        // Type 4: Complex Matrix (Must answer all sub-questions)
        else if (type === '4') {
            // Check if ans is an object and has keys for all options
            if (!ans || Object.keys(ans).length < q.options.length) {
                errors.value[q.id] = "Please rate all items.";
                isValid = false;
            }
        }
        // Type 6: Textarea (Must not be empty)
        else if (type === '6') {
            if (!ans || typeof ans !== 'string' || ans.trim() === '') {
                errors.value[q.id] = "Please write a short answer.";
                isValid = false;
            }
        }
        // Type 2: Slider (Always has a default value, so usually valid)
    });

    return isValid;
};

onMounted(async () => {
    AOS.init({ duration: 800, once: true });

    try {
        const res = await fetch('/api/questionnaire');
        questions.value = await res.json();

        // Initialize answers structure correctly
        questions.value.forEach(q => {
            const type = String(q.type);
            if (['0', '3'].includes(type)) {
                answers.value[q.id] = [];
            } else if (type === '2') {
                answers.value[q.id] = 5;
            } else if (type === '4') {
                answers.value[q.id] = {}; // Initialize object for matrix
            } else {
                answers.value[q.id] = null;
            }
        });

    } catch (e) {
        console.error("Error loading questions", e);
    }
});

const submit = async () => {
    // 1. Run Validation
    if (!validateForm()) {
        // Optional: Scroll to top or first error
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
    }

    isLoading.value = true;
    try {
        const token = localStorage.getItem('token');
        if (!token) return alert("You must be logged in to submit.");

        // Flatten answers for simple ID storage if needed by backend
        let selectedOptionIds = [];
        for (const [qId, ans] of Object.entries(answers.value)) {
            if (Array.isArray(ans)) {
                selectedOptionIds.push(...ans);
            } else if (typeof ans === 'number' && ans > 10) {
                // Assuming IDs > 10 logic from your snippet
                selectedOptionIds.push(ans);
            }
        }

        const response = await fetch('/api/submit-wellness', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                selected_options: selectedOptionIds, // Legacy support
                raw_answers: answers.value // Full data
            })
        });

        const result = await response.json();

        if (response.ok) {
            router.push('/report');
        } else {
            alert('Error: ' + result.message);
        }

    } catch (error) {
        console.error("Submission failed:", error);
        alert("An error occurred while submitting.");
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="container py-5">
        <h1 class="text-center mb-5" data-aos="fade-up">Wellness Assessment</h1>

        <div v-for="(q, i) in questions" :key="q.id" class="mb-4" data-aos="fade-up" :data-aos-delay="i * 100">

            <div class="card shadow-sm" :class="{ 'border-danger': errors[q.id], 'border-0': !errors[q.id] }">

                <div class="card-body p-4">
                    <h4 class="fw-bold mb-3" :class="errors[q.id] ? 'text-danger' : 'text-primary'">
                        {{ i + 1 }}. {{ q.text }}
                    </h4>

                    <div v-if="q.type == 0" class="row g-3">
                        <div v-for="opt in q.options" :key="opt.id" class="col-6 col-md-4">
                            <div class="goal-card text-center p-3 rounded border hover-effect"
                                :class="{ 'active': isSelected(q.id, opt.id) }" @click="toggle(q.id, opt.id, true)">
                                <div class="display-4 mb-2" v-if="splitEmoji(opt.text).icon">
                                    {{ splitEmoji(opt.text).icon }}
                                </div>
                                <p class="mb-0 fw-medium">{{ splitEmoji(opt.text).text }}</p>
                            </div>
                        </div>
                    </div>

                    <div v-if="q.type == 1" class="d-flex justify-content-between align-items-center mt-3">
                        <div v-for="opt in q.options" :key="opt.id" class="sleep-option text-center"
                            @click="toggle(q.id, opt.id, false)">
                            <div class="emoji-wrapper mb-2 mx-auto" :class="{ 'active': isSelected(q.id, opt.id) }">
                                <span class="display-4">{{ splitEmoji(opt.text).icon || '❓' }}</span>
                            </div>
                            <p class="small mb-0">{{ splitEmoji(opt.text).text }}</p>
                        </div>
                    </div>

                    <div v-if="q.type == 2" class="mt-4">
                        <div class="d-flex justify-content-between text-muted mb-2">
                            <span>{{ q.options[0]?.text || 'Low' }}</span>
                            <span>{{ q.options[1]?.text || 'High' }}</span>
                        </div>
                        <input type="range" class="form-range" min="1" max="10" v-model="answers[q.id]">
                        <div class="text-center fw-bold text-primary">{{ answers[q.id] }}</div>
                    </div>

                    <div v-if="q.type == 3" class="row g-2">
                        <div v-for="opt in q.options" :key="opt.id" class="col-6 col-md-4">
                            <div class="habit-item p-3 border rounded d-flex align-items-center mb-2"
                                :class="{ 'active': isSelected(q.id, opt.id) }" @click="toggle(q.id, opt.id, true)">
                                <input class="form-check-input me-2" type="checkbox"
                                    :checked="isSelected(q.id, opt.id)">
                                <label class="mb-0">{{ opt.text }}</label>
                            </div>
                        </div>
                    </div>

                    <div v-if="q.type == 4" class="row text-center mt-3">
                        <div v-for="opt in q.options" :key="opt.id" class="col">
                            <p class="small text-muted mb-1">{{ opt.text }}</p>
                            <div class="energy-bar mx-auto mb-2 bg-light rounded" style="height: 60px; width: 30px;">
                            </div>
                            <select class="form-select form-select-sm" @change="(e) => {
                                if (errors[q.id]) delete errors[q.id];
                                if (!answers[q.id]) answers[q.id] = {};
                                answers[q.id][opt.text] = e.target.value;
                            }">
                                <option value="" disabled selected>-</option>
                                <option value="low">Low</option>
                                <option value="medium">Med</option>
                                <option value="high">High</option>
                            </select>
                        </div>
                    </div>

                    <div v-if="q.type == 5" class="d-flex flex-column gap-2">
                        <div v-for="opt in q.options" :key="opt.id" class="form-check">
                            <input class="form-check-input" type="radio" :name="'q' + q.id" :value="opt.id"
                                v-model="answers[q.id]" @change="delete errors[q.id]">
                            <label class="form-check-label">{{ opt.text }}</label>
                        </div>
                    </div>

                    <div v-if="q.type == 6">
                        <textarea class="form-control" rows="3" v-model="answers[q.id]"
                            @input="delete errors[q.id]"></textarea>
                    </div>

                    <div v-if="errors[q.id]" class="mt-3 text-danger fw-bold small animate__animated animate__shakeX">
                        <i class="fa fa-exclamation-circle me-1"></i> {{ errors[q.id] }}
                    </div>

                </div>
            </div>
        </div>
        <div class="text-center mt-5">
            <button @click="submit" :disabled="isLoading" class="btn btn-primary btn-lg rounded-pill px-5">
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                {{ isLoading ? 'Processing...' : 'Submit Assessment' }}
            </button>
            <p v-if="Object.keys(errors).length > 0" class="text-danger mt-3">
                Please answer all questions marked in red above.
            </p>
        </div>
    </div>
</template>

<style scoped>
.goal-card {
    cursor: pointer;
    transition: all 0.3s;
    border: 2px solid transparent;
}

.goal-card.active {
    border-color: #667eea;
    background: #f0f4ff;
}

.sleep-option {
    cursor: pointer;
    opacity: 0.6;
    transition: 0.2s;
}

.sleep-option:hover,
.sleep-option .emoji-wrapper.active {
    opacity: 1;
    transform: scale(1.1);
}

.habit-item {
    cursor: pointer;
    transition: 0.2s;
}

.habit-item.active {
    background: #f0f4ff;
    border-color: #667eea !important;
}

.bg-gradient-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.goal-card {
    transition: all 0.3s ease;
    cursor: pointer;
    border: 2px solid transparent;
}

.goal-card:hover {
    transform: translateY(-5px);
    border-color: #667eea;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.goal-card.active {
    border-color: #667eea;
    background-color: rgba(102, 126, 234, 0.1);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.15);
}

.emoji-wrapper {
    transition: all 0.3s ease;
    cursor: pointer;
    padding: 10px;
    border-radius: 50%;
    border: 3px solid transparent;
}

.emoji-wrapper:hover {
    transform: scale(1.1);
    border-color: #667eea;
    background-color: rgba(102, 126, 234, 0.1);
}

.emoji-wrapper.active {
    border-color: #667eea;
    background-color: rgba(102, 126, 234, 0.15);
    transform: scale(1.1);
}

.stress-slider-container {
    max-width: 600px;
    margin: 0 auto;
}

.form-range::-webkit-slider-thumb {
    background: #667eea;
    border: 3px solid white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.form-range::-moz-range-thumb {
    background: #667eea;
    border: 3px solid white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.habit-item {
    transition: all 0.2s ease;
    cursor: pointer;
}

.habit-item:hover {
    background-color: rgba(102, 126, 234, 0.05);
    border-color: #667eea;
}

.habit-item.active {
    background-color: rgba(102, 126, 234, 0.1);
    border-color: #667eea;
}

.energy-bar {
    background-color: #f8f9fa;
    border-radius: 4px;
    position: relative;
    overflow: hidden;
}

.energy-fill {
    position: absolute;
    bottom: 0;
    width: 100%;
    transition: all 0.3s ease;
}

.btn-group .btn.active {
    background-color: #667eea;
    border-color: #667eea;
    color: white;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .sleep-option span {
        font-size: 2.5rem !important;
    }

    .btn-group .btn {
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
    }
}

@media (max-width: 576px) {
    .goal-card {
        padding: 1rem !important;
    }

    .energy-bar {
        width: 30px !important;
        height: 60px !important;
    }
}

.goal-card {
    cursor: pointer;
    transition: all 0.3s;
    border: 2px solid transparent;
}

.goal-card:hover {
    transform: translateY(-5px);
    border-color: #667eea;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.goal-card.active {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.1);
}

.sleep-option {
    cursor: pointer;
    opacity: 0.6;
    transition: 0.2s;
}

.sleep-option:hover,
.sleep-option .emoji-wrapper.active {
    opacity: 1;
    transform: scale(1.1);
}

.emoji-wrapper {
    transition: all 0.3s ease;
    padding: 10px;
    border-radius: 50%;
    border: 3px solid transparent;
}

.emoji-wrapper.active {
    border-color: #667eea;
    background-color: rgba(102, 126, 234, 0.15);
}

.habit-item {
    cursor: pointer;
    transition: 0.2s;
}

.habit-item:hover {
    background-color: rgba(102, 126, 234, 0.05);
    border-color: #667eea;
}

.habit-item.active {
    background: rgba(102, 126, 234, 0.1);
    border-color: #667eea !important;
}

.form-range::-webkit-slider-thumb {
    background: #667eea;
}

.energy-bar {
    background-color: #f8f9fa;
    border-radius: 4px;
}

@media (max-width: 576px) {
    .goal-card {
        padding: 1rem !important;
    }
}

.border-danger {
    border: 2px solid #dc3545 !important;
}
</style>