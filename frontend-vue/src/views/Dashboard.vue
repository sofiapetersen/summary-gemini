<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <p>{{ welcomeMessage }}</p>

    <h2>Processar Arquivo com IA</h2>
    <input type="file" ref="fileInput" @change="handleFileUpload" accept=".txt,.pdf">
    <button @click="uploadAndSummarize" :disabled="!selectedFile || loading">
      {{ loading ? 'Processando...' : 'Upload e Resumir' }}
    </button>

    <p v-if="message">{{ message }}</p>
    <p v-if="downloadUrl"><a :href="downloadUrl" download="resumo_gerado.pdf">Baixar Resumo PDF</a></p>

    <button @click="logout">Sair</button>
  </div>
</template>

<script>
import axios from 'axios';

// URL base da API Flask
const API_URL = 'http://localhost:5000';

export default {
  name: 'UserDashboard',
  data() {
    return {
      welcomeMessage: 'Carregando...',
      selectedFile: null,
      loading: false,
      message: '',
      downloadUrl: null
    };
  },
  async created() {
     await this.fetchProtectedData(); // Chama a função ao criar o componente
  },
  methods: {
    async fetchProtectedData() {
        const token = localStorage.getItem('jwt_token');
        if (!token) {
            this.welcomeMessage = 'Você não está autenticado.';
            this.$router.push('/login');
            return;
        }

        try {
            const response = await axios.get(`${API_URL}/protected`, {
                headers: {
                    Authorization: `Bearer ${token}` // Inclui o token no cabeçalho
                }
            });
            this.welcomeMessage = response.data.message + ' \n Logado como: ' + response.data.logged_in_as;
        } catch (error) {
            console.error("Erro ao buscar dados protegidos:", error);
             this.handleAuthError(error);
        }
    },

    handleFileUpload(event) {
        // Limpa estado anterior ao selecionar novo arquivo
        this.selectedFile = null;
        this.message = '';
        this.downloadUrl = null;

        const files = event.target.files;
        if (files.length > 0) {
            const file = files[0];
            const allowedTypes = ['text/plain', 'application/pdf'];
            // Verifica o tipo MIME e a extensão do arquivo
            if (allowedTypes.includes(file.type) || /\.(txt|pdf)$/i.test(file.name)) {
                this.selectedFile = file;
                this.message = `Arquivo selecionado: ${file.name}`;
            } else {
                this.message = 'Por favor, selecione um arquivo .txt ou .pdf.';
                // Limpar o input do arquivo visualmente
                this.$refs.fileInput.value = '';
            }
        }
    },

    async uploadAndSummarize() {
        if (!this.selectedFile) {
            this.message = 'Por favor, selecione um arquivo primeiro.';
            return;
        }

        this.loading = true;
        this.message = 'Enviando arquivo e processando...';
        this.downloadUrl = null; // Reset download URL

        const token = localStorage.getItem('jwt_token');
        if (!token) {
            this.message = 'Você não está autenticado. Faça login novamente.';
             this.$router.push('/login');
             return;
        }

        const formData = new FormData();
        formData.append('file', this.selectedFile); 

        try {
            const response = await axios.post(`${API_URL}/upload-and-summarize`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', 
                    'Authorization': `Bearer ${token}`
                },
                responseType: 'blob' 
            });

            const blob = new Blob([response.data], { type: 'application/pdf' });
            this.downloadUrl = URL.createObjectURL(blob); 
            this.message = 'Resumo gerado! Clique no link para baixar.';

             this.$refs.fileInput.value = '';
             this.selectedFile = null;


        } catch (error) {
            console.error("Erro no upload/processamento:", error);
            this.selectedFile = null; 

            let errorMessage = 'Erro ao processar o arquivo.';
            if (error.response) {
                 if (error.response.status === 401) {
                     errorMessage = 'Sessão expirada ou inválida. Faça login novamente.';
                     this.handleAuthError(error); // Trata erro de autenticação
                     return; // Sai daqui após tratar 401
                 } else if (error.response.data && error.response.data.message) {
                       errorMessage = `Erro do servidor: ${error.response.status}`;
                 } else {
                    errorMessage = `Erro do servidor: ${error.response.status}`;
                 }
            } else if (error.request) {
                errorMessage = 'Erro de rede. Servidor inalcançável.';
            } else {
                errorMessage = 'Erro ao configurar a requisição.';
            }
             this.message = errorMessage;

        } finally {
            this.loading = false;
        }
    },

    handleAuthError(error) {
         if (error.response && error.response.status === 401) {
              localStorage.removeItem('jwt_token'); 
              this.$router.push('/login'); 
              this.message = 'Sessão expirada ou inválida. Faça login novamente.';
         } else {
             console.error("Erro não tratado na autenticação:", error);
         }
    },


    logout() {
        localStorage.removeItem('jwt_token');
        this.$router.push('/login'); 
    }
  },
  beforeUnmount() {
    if (this.downloadUrl) {
      URL.revokeObjectURL(this.downloadUrl);
    }
  }
}
</script>

<style scoped>
 .dashboard {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  h2 {
      margin-top: 30px;
      margin-bottom: 15px;
  }
  input[type="file"] {
      margin-bottom: 15px;
  }
  button {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 10px;
    margin-right: 10px;
  }
  button:hover:not(:disabled) {
    background-color: #0056b3;
  }
   button:disabled {
       background-color: #cccccc;
       cursor: not-allowed;
   }
  button:last-child { 
    background-color: #dc3545;
    margin-right: 0;
    margin-top: 20px;
  }
   button:last-child:hover:not(:disabled) {
       background-color: #c82333;
   }
   a {
       color: #007bff;
       text-decoration: none;
   }
   a:hover {
       text-decoration: underline;
   }
</style>