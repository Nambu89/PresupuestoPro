import axios from 'axios';

// Configuración base de axios
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

// Crear instancia de axios con configuración base
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir el token de autenticación a las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Endpoints de autenticación
export const authApi = {
  login: (credentials) => {
    // Para FastAPI OAuth2, debemos usar directamente la URL completa
    // y no usar la configuración base de axios para evitar problemas
    return axios({
      method: 'post',
      url: `${API_URL}${API_VERSION}/auth/login`,
      data: credentials,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },
  register: (userData) => api.post(`${API_VERSION}/auth/register`, userData),
  refreshToken: () => api.post(`${API_VERSION}/auth/refresh-token`),
  forgotPassword: (email) => api.post(`${API_VERSION}/auth/forgot-password`, { email }),
  resetPassword: (data) => api.post(`${API_VERSION}/auth/reset-password`, data),
  me: () => api.get(`${API_VERSION}/auth/me`),
};

// Endpoints de usuarios
export const usersApi = {
  getAll: (params) => api.get(`${API_VERSION}/users`, { params }),
  getById: (id) => api.get(`${API_VERSION}/users/${id}`),
  create: (userData) => api.post(`${API_VERSION}/users`, userData),
  update: (id, userData) => api.put(`${API_VERSION}/users/${id}`, userData),
  delete: (id) => api.delete(`${API_VERSION}/users/${id}`),
  updateProfile: (userData) => api.put(`${API_VERSION}/users/me`, userData),
};

// Endpoints de proyectos
export const projectsApi = {
  getAll: (params) => api.get(`${API_VERSION}/projects`, { params }),
  getById: (id) => api.get(`${API_VERSION}/projects/${id}`),
  create: (projectData) => api.post(`${API_VERSION}/projects`, projectData),
  update: (id, projectData) => api.put(`${API_VERSION}/projects/${id}`, projectData),
  delete: (id) => api.delete(`${API_VERSION}/projects/${id}`),
};

// Endpoints de pagos
export const paymentsApi = {
  getAll: (params) => api.get(`${API_VERSION}/payments`, { params }),
  getById: (id) => api.get(`${API_VERSION}/payments/${id}`),
  create: (paymentData) => api.post(`${API_VERSION}/payments`, paymentData),
  update: (id, paymentData) => api.put(`${API_VERSION}/payments/${id}`, paymentData),
  delete: (id) => api.delete(`${API_VERSION}/payments/${id}`),
  processPayment: (paymentData) => api.post(`${API_VERSION}/payments/process`, paymentData),
};

// Interceptor para manejar errores de respuesta
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Manejar errores específicos (401, 403, etc.)
    if (error.response) {
      // Si el token expiró (401), intentar refrescar el token
      if (error.response.status === 401) {
        // Implementar lógica para refrescar token si es necesario
      }
      
      // Mostrar mensaje de error al usuario
      console.error('API Error:', error.response.data);
    }
    return Promise.reject(error);
  }
);

export default api;