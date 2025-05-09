<template>
  <v-container class="dashboard-container">
    <v-card class="pa-6 dashboard-card" elevation="12">
      <div class="graphic-decoration">
        <svg viewBox="0 0 100 100" class="blob">
          <path fill="currentColor" d="M31.8,-35.9C40.5,-27.7,46.7,-16.5,49.8,-3.8C52.9,8.9,52.9,23.1,45.1,34.4C37.3,45.7,21.7,54.1,5.3,52.5C-11.1,50.9,-28.4,39.3,-39.4,25.1C-50.5,10.9,-55.3,-5.9,-50.4,-19.8C-45.5,-33.7,-30.9,-44.7,-15.9,-50.1C-0.9,-55.6,14.5,-55.5,31.8,-35.9Z"/>
        </svg>
      </div>

      <div class="d-flex justify-end mb-2">
        <v-btn icon variant="text" @click="toggleTheme" class="theme-toggle-btn">
          <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waxing-crescent' }}</v-icon>
        </v-btn>
      </div>

      <v-card-title class="text-h3 text-center mb-4 font-weight-bold text-primary">
        ResumosIA
      </v-card-title>

      <v-card-text>
        <div class="text-h6 text-center mb-8">
          {{ welcomeMessage }}
        </div>

        <v-divider class="my-6"></v-divider>

        <v-card class="pa-4 mb-8" variant="outlined">
          <v-card-title class="text-h5 mb-4">
            <v-icon left>mdi-file-upload</v-icon>
            Resumir Arquivo com IA
          </v-card-title>

          <v-file-input
            v-model="selectedFile"
            accept=".txt,.pdf"
            label="Selecione um arquivo"
            prepend-icon="mdi-file-document"
            variant="outlined"
            color="primary"
            :rules="[rules.fileRequired, rules.fileType]"
            :loading="loading"
            @change="handleFileUpload"
            class="mb-4"
          ></v-file-input>

          <v-btn
            color="primary"
            size="large"
            block
            rounded="lg"
            :loading="loading"
            :disabled="!selectedFile || loading"
            @click="uploadAndSummarize"
          >
            <v-icon left>mdi-robot</v-icon>
            {{ loading ? 'Processando...' : 'Upload e Resumir' }}
          </v-btn>

          <v-alert
            v-if="message"
            :type="messageType"
            density="compact"
            variant="tonal"
            class="mt-4"
          >
            {{ message }}
          </v-alert>

          <v-btn
            v-if="downloadUrl"
            color="success"
            variant="outlined"
            block
            size="large"
            rounded="lg"
            class="mt-4"
            :href="downloadUrl"
            download="resumo_gerado.pdf"
          >
            <v-icon left>mdi-download</v-icon>
            Baixar Resumo PDF
          </v-btn>
        </v-card>

        <div class="text-center mt-8">
          <v-btn
            color="error"
            size="large"
            rounded="lg"
            @click="logout"
          >
            <v-icon left>mdi-logout</v-icon>
            Sair
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from 'vuetify'
import axios from 'axios'

const theme = useTheme()
const isDark = computed(() => theme.global.name.value === 'dark')
const toggleTheme = () => {
  theme.global.name.value = isDark.value ? 'light' : 'dark'
}

const API_URL = 'https://summary-gemini-ulr3.onrender.com';
const router = useRouter()

// Dados reativos
const welcomeMessage = ref('Carregando...')
const selectedFile = ref(null)
const loading = ref(false)
const message = ref('')
const messageType = ref('info')
const downloadUrl = ref(null)

// Regras de validação
const rules = {
  fileRequired: value => !!value || 'Arquivo obrigatório',
  fileType: value => !value || 
    ['text/plain', 'application/pdf'].includes(value.type) || 
    /\.(txt|pdf)$/i.test(value.name) || 
    'Apenas arquivos .txt ou .pdf'
}

// Funções
const fetchProtectedData = async () => {
  const token = localStorage.getItem('jwt_token')
  if (!token) {
    welcomeMessage.value = 'Você não está autenticado.'
    router.push('/login')
    return
  }

  try {
    const response = await axios.get(`${API_URL}/protected`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    welcomeMessage.value = `Carregue seu arquivo, ${response.data.logged_in_as}`
  } catch (error) {
    console.error("Erro ao buscar dados protegidos:", error)
    handleAuthError(error)
  }
}

const handleFileUpload = () => {
  message.value = ''
  messageType.value = 'info'
  downloadUrl.value = null
}

const uploadAndSummarize = async () => {
  if (!selectedFile.value) {
    message.value = 'Por favor, selecione um arquivo primeiro.'
    messageType.value = 'error'
    return
  }

  loading.value = true
  message.value = 'Enviando arquivo e processando...'
  messageType.value = 'info'
  downloadUrl.value = null

  const token = localStorage.getItem('jwt_token')
  if (!token) {
    message.value = 'Você não está autenticado. Faça login novamente.'
    messageType.value = 'error'
    router.push('/login')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const response = await axios.post(`${API_URL}/upload-and-summarize`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
      },
      responseType: 'blob'
    })

    const blob = new Blob([response.data], { type: 'application/pdf' })
    downloadUrl.value = URL.createObjectURL(blob)
    message.value = 'Resumo gerado com sucesso!'
    messageType.value = 'success'
    selectedFile.value = null
  } catch (error) {
    console.error("Erro no upload/processamento:", error)
    selectedFile.value = null
    
    if (error.response?.status === 401) {
      handleAuthError(error)
      return
    }

    message.value = error.response?.data?.message || 
      'Erro ao processar o arquivo. Tente novamente.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const handleAuthError = (error) => {
  if (error.response?.status === 401) {
    localStorage.removeItem('jwt_token')
    router.push('/login')
    message.value = 'Sessão expirada ou inválida. Faça login novamente.'
    messageType.value = 'error'
  }
}

const logout = () => {
  localStorage.removeItem('jwt_token')
  router.push('/login')
}

fetchProtectedData()

onBeforeUnmount(() => {
  if (downloadUrl.value) {
    URL.revokeObjectURL(downloadUrl.value)
  }
})
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
}

.dashboard-card {
  position: relative;
  overflow: hidden;
  border-radius: 24px !important;
  transition: transform 0.3s ease;
}

.dashboard-card:hover {
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

@media (max-width: 600px) {
  .dashboard-card {
    margin: 16px;
    border-radius: 16px !important;
  }
  
  .graphic-decoration {
    display: none;
  }
}
</style>