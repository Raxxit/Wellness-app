<script setup>
import { ref } from "vue"

const username = ref("")
const email = ref("")
const password = ref("")

function register() {
  if (!username.value || !email.value || !password.value) {
    alert("Please fill in all fields.")
    return
  }

  alert(`Registered successfully!
User: ${username.value}
Email: ${email.value}`)
}
</script>

<template>
  <div class="container">
    <h2>Create Account</h2>

    <form @submit.prevent="register">
      <input v-model="username" type="text" placeholder="Username" />
      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />

      <button type="submit">Register</button>
    </form>
  </div>
</template>

<style scoped>

:global(body) {
  margin: 0;
  padding: 0;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eef5f2; 
}

.container {
  width: 500px;
  padding: 3rem;
  background: linear-gradient(145deg, #ffffff, #f4f4f4);
  border-radius: 20px;
  box-shadow: 10px 10px 20px #d4d4d4,
              -10px -10px 20px #ffffff;
}


h2 {
  text-align: center;
  font-weight: 700;
  color: #42b883;
  font-size: 2rem;
  margin-bottom: 2rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

input {
  padding: 14px 16px;
  font-size: 1.1rem;
  border-radius: 10px;
  border: 1px solid #ececec;
  background: #fafafa;
  transition: 0.3s;
}

input:focus {
  background: white;
  border-color: #42b883;
  box-shadow: 0 0 8px rgba(66,184,131,.4);
}

button {
  padding: 14px;
  border-radius: 10px;
  border: none;
  color: white;
  background: #42b883;
  font-size: 1.2rem;
  transition: 0.3s;
  cursor: pointer;
}

button:hover {
  background: #2e7b62;
}

</style>
