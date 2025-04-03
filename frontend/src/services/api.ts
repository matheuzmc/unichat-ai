import axios from 'axios';
import { ApiResponse } from '../types';

// Definir baseURL do axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Serviço para o LLM
const llmApi = axios.create({
  baseURL: import.meta.env.VITE_LLM_URL || 'http://localhost:8080/api',
  timeout: 30000, // Timeout maior para requisições de LLM
  headers: {
    'Content-Type': 'application/json',
  }
});

// Funções de API
export const chatService = {
  // Função para enviar perguntas ao LLM
  sendQuestion: async (question: string, studentId: number): Promise<ApiResponse> => {
    try {
      const response = await llmApi.post('/query', {
        question,
        student_id: studentId
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao enviar pergunta para o LLM:', error);
      throw error;
    }
  },

  // Função para buscar dados do aluno
  getStudentDetails: async (studentId: number) => {
    try {
      const response = await api.get(`/alunos/${studentId}/detalhes/`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar detalhes do aluno:', error);
      throw error;
    }
  },

  // Função para buscar histórico de chat
  getChatHistory: async (studentId: number) => {
    try {
      const response = await api.get(`/chat-historico/por_aluno/?aluno_id=${studentId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar histórico de chat:', error);
      throw error;
    }
  },

  // Função para salvar uma mensagem no histórico
  saveChatMessage: async (studentId: number, question: string, answer: string) => {
    try {
      const response = await api.post('/chat-historico/', {
        aluno: studentId,
        pergunta: question,
        resposta: answer
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao salvar mensagem de chat:', error);
      // Ignorar erro para não interromper o fluxo do usuário
      return null;
    }
  }
};

export default api; 