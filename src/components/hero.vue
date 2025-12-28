<script setup>
defineProps({
    title: String,
    subtitle: String,
    buttonText: String
})
</script>

<template>
    <header class="bg-primary text-white text-center py-5">
        <div class="container">
            <h1>{{ title }}</h1>
            <p class="lead">{{ subtitle }}</p>
            <button class="btn btn-light btn-lg">{{ buttonText }}</button>
        </div>
    </header>
</template>

<style scoped>
header {
    border-bottom: 5px solid #004085;
}
</style>