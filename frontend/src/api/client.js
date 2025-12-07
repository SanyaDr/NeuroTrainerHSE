// src/api/client.js
import axios from 'axios';

const api = axios.create({
  // Замени на адрес твоего бэкенда
  baseURL: 'http://localhost:8000/api',  // ← если бэк на Node.js/Express
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Автоматически добавляет токен к каждому запросу (если есть)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;