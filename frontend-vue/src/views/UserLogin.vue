<template>
  <v-container class="d-flex align-center justify-center fill-height" fluid>

    <v-card class="pa-8 login-card" width="100%" max-width="440" elevation="16">
      <div class="graphic-decoration">
        <svg viewBox="0 0 100 100" class="blob">
          <path fill="currentColor" d="M25.6,-25.1C33.4,-17.5,40,-5.8,39.3,6.8C38.6,19.4,30.5,33,18.8,40.3C7.1,47.7,-8.3,48.9,-21.1,43.4C-33.9,37.9,-44.1,25.8,-47.2,11.5C-50.3,-2.8,-46.3,-19.2,-37.1,-28.3C-27.9,-37.4,-13.9,-39.2,-0.7,-38.6C12.5,-38.1,25,-35.2,25.6,-25.1Z"/>
        </svg>
      </div>
      <div class="d-flex justify-end mb-2">
        <v-btn icon variant="text" @click="toggleTheme" class="theme-toggle-btn">
          <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waxing-crescent' }}</v-icon>
        </v-btn>
      </div>

      <v-card-title class="text-h4 text-center mb-6 font-weight-bold text-primary">
        Bem-vindo
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="login" class="form-content">
          <v-text-field
            v-model="username"
            label="Nome de Usuário"
            prepend-inner-icon="mdi-account-outline"
            variant="outlined"
            color="primary"
            density="comfortable"
            :rules="[rules.required]"
            autocomplete="username"
            rounded="lg"
            :bg-color="isDark ? 'field-bg' : '#f8f9fa'"
          ></v-text-field>

          <v-text-field
            v-model="password"
            label="Senha"
            prepend-inner-icon="mdi-lock-outline"
            :type="showPassword ? 'text' : 'password'"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            variant="outlined"
            color="primary"
            density="comfortable"
            autocomplete="current-password"
            rounded="lg"
            :bg-color="isDark ? 'field-bg' : '#f8f9fa'"
            class="mt-2"
          ></v-text-field>


          <v-alert
            v-if="message"
            type="error"
            density="compact"
            variant="tonal"
            class="mb-4 animate__animated animate__headShake"
          >
            {{ message }}
          </v-alert>

          <v-btn
            type="submit"
            color="primary"
            :loading="loading"
            block
            size="x-large"
            rounded="lg"
            class="text-button font-weight-bold"
            @mouseover="hover = true"
            @mouseleave="hover = false"
          >
            Entrar
          </v-btn>

          <v-divider class="my-6"></v-divider>

          <div class="text-center text-body-2">
            Não tem uma conta? 
            <router-link 
              to="/register" 
              class="text-primary text-decoration-none font-weight-bold"
            >
              Criar conta
            </router-link>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useTheme } from 'vuetify'

const theme = useTheme()
const isDark = computed(() => theme.global.name.value === 'dark')
const toggleTheme = () => {
  theme.global.name.value = isDark.value ? 'light' : 'dark'
}

const username = ref('')
const password = ref('')
const message = ref('')
const showPassword = ref(false)
const loading = ref(false)
const hover = ref(false)
const router = useRouter()

const rules = {
  required: value => !!value || 'Campo obrigatório',
}

const login = async () => {
  message.value = ''
  loading.value = true
  try {
    const API_URL = import.meta.env.VITE_API_URL
    const response = await axios.post(`${API_URL}/login`, {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('jwt_token', response.data.access_token)
    router.push('/dashboard')
  } catch (error) {
    message.value = error.response?.data?.message || 'Credenciais inválidas. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background-color: var(--v-theme-background);
  transition: background-color 0.3s ease;
}

.login-card {
  position: relative;
  overflow: hidden;
  border-radius: 24px !important;
  transition: transform 0.3s ease;
}

.login-card:hover {
  transform: translateY(-4px);
}

.graphic-decoration {
  position: absolute;
  top: -50px;
  right: -50px;
  opacity: 0.1;
  color: var(--v-primary);
}

.blob {
  width: 200px;
  height: 200px;
  animation: blobFloat 20s ease-in-out infinite;
}

@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(10px, 10px) rotate(5deg); }
  50% { transform: translate(-10px, 15px) rotate(-5deg); }
  75% { transform: translate(15px, -10px) rotate(3deg); }
}

.form-content {
  position: relative;
  z-index: 2;
}

.v-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 0.5px;
}

.v-btn:hover {
  letter-spacing: 1px;
}

@media (max-width: 600px) {
  .login-card {
    margin: 16px;
    border-radius: 16px !important;
  }
  
  .graphic-decoration {
    display: none;
  }
}
</style>
