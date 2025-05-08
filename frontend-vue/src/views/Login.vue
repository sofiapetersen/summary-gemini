<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="username">Nome de Usuário:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">Senha:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="message">{{ message }}</p>
     <p><router-link to="/register">Não tem uma conta? Crie uma</router-link></p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async login() {
       this.message = ''; 
       try {
        const API_URL = process.env.VUE_APP_API_URL;
        const response = await axios.post(`${API_URL}/login`, { // URL base da API Flask
          username: this.username,
          password: this.password
        });
        // Sucesso no login
        const token = response.data.access_token;
        localStorage.setItem('jwt_token', token);
        this.$router.push('/dashboard'); 
       } catch (error) {
          console.error("Erro no login:", error);
           if (error.response && error.response.data && error.response.data.message) {
              this.message = 'Erro: ' + error.response.data.message;
           } else {
              this.message = 'Erro ao conectar com o servidor ou erro desconhecido.';
           }
       }
    }
  }
}
</script>

<style scoped>
 .login {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
div {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input[type="text"], input[type="password"] {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>