import api from './client';

export const testConnection = () => api.get('/test');