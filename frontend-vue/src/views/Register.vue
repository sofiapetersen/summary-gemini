<template>
  <div class="register">
    <h1>Cadastro de Usuário</h1>
    <form @submit.prevent="register">
      <div>
        <label for="username">Nome de Usuário:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">Senha:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Cadastrar</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <p><router-link to="/login">Já tem uma conta? Faça login</router-link></p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async register() {
      this.message = ''; // Limpa mensagens anteriores
      try {
        const response = await axios.post('http://localhost:5000/register', { // URL base da API Flask
          username: this.username,
          password: this.password
        });
        this.message = response.data.message;
        this.username = '';
        this.password = '';
        this.$router.push('/login');
      } catch (error) {
        console.error("Erro no cadastro:", error);
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
.register {
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