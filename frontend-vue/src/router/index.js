import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/UserRegister.vue'
import Login from '../views/UserLogin.vue'
import Dashboard from '../views/UserDashboard.vue' // Crie este arquivo depois

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true } // Adiciona meta field para rotas protegidas
  },
  {
    path: '/',
    redirect: '/login' // Redireciona a raiz para o login
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation Guard para rotas protegidas
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = localStorage.getItem('jwt_token'); // Verifica se o token existe

  if (requiresAuth && !isAuthenticated) {
    // Se a rota requer autenticação e o usuário NÃO está autenticado
    next('/login'); // Redireciona para login
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
    // Se o usuário TÁ autenticado e tenta ir para Login/Register
     next('/dashboard'); // Redireciona para dashboard
  }
  else {
    next(); // Permite acesso
  }
});


export default router