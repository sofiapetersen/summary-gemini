<template>
  <v-container class="d-flex align-center justify-center fill-height" fluid>
    <v-card class="pa-8 register-card" width="100%" max-width="440" elevation="16">
      <div class="graphic-decoration">
        <svg viewBox="0 0 100 100" class="blob">
          <path fill="currentColor" d="M30,-36.4C38.6,-27.5,45.2,-17.3,47.5,-5.8C49.8,5.7,47.9,18.4,39.3,27.9C30.7,37.4,15.4,43.7,0.7,43.1C-14.1,42.4,-28.1,34.8,-37.3,23.8C-46.5,12.9,-50.9,-1.4,-47.2,-14.1C-43.5,-26.8,-31.7,-38,-20.4,-45.9C-9.1,-53.8,1.7,-58.5,12.3,-56.1C23,-53.8,33.5,-44.5,30,-36.4Z"/>
        </svg>
      </div>
      <div class="d-flex justify-end mb-2">
        <v-btn icon variant="text" @click="toggleTheme" class="theme-toggle-btn">
          <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waxing-crescent' }}</v-icon>
        </v-btn>
      </div>

      <v-card-title class="text-h4 text-center mb-6 font-weight-bold text-primary">
        Cadastre-se
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="register" class="form-content">
          <v-text-field
            v-model="username"
            label="Nome de Usuário"
            prepend-inner-icon="mdi-account-plus-outline"
            variant="outlined"
            color="primary"
            density="comfortable"
            :rules="[rules.required, rules.minUsernameLength]"
            autocomplete="username"
            rounded="lg"
            :bg-color="isDark ? 'field-bg' : '#f8f9fa'"
            class="mb-4"
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
            :rules="[rules.required, rules.minLength(8)]"
            autocomplete="new-password"
            rounded="lg"
            :bg-color="isDark ? 'field-bg' : '#f8f9fa'"
            class="mb-4"
          ></v-text-field>

          <v-alert
            v-if="message"
            :type="messageType"
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
          >
            Cadastrar
          </v-btn>

          <v-divider class="my-6"></v-divider>

          <div class="text-center text-body-2">
            Já tem uma conta?
            <router-link 
              to="/login" 
              class="text-primary text-decoration-none font-weight-bold"
            >
              Faça login
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
const messageType = ref('error')
const showPassword = ref(false)
const loading = ref(false)
const router = useRouter()

const rules = {
  required: value => !!value || 'Campo obrigatório',
  minLength: length => value => (value || '').length >= length || `Mínimo ${length} caracteres`,
  minUsernameLength: value => (value || '').length >= 3 || 'Nome de usuário muito curto'
}

const register = async () => {
  message.value = ''
  loading.value = true
  try {
    const API_URL = import.meta.env.VITE_API_URL
    const response = await axios.post(`${API_URL}/register`, {
      username: username.value,
      password: password.value
    })
    
    message.value = response.data.message || 'Cadastro realizado com sucesso!'
    messageType.value = 'success'
    
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (error) {
    message.value = error.response?.data?.message || 'Erro ao realizar cadastro. Tente novamente.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-card {
  position: relative;
  overflow: hidden;
  border-radius: 24px !important;
  transition: transform 0.3s ease;
}

.register-card:hover {
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
  .register-card {
    margin: 16px;
    border-radius: 16px !important;
  }
  
  .graphic-decoration {
    display: none;
  }
}
</style>