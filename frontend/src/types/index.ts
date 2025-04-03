// Tipos para o ChatMessage
export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

// Tipo para a resposta da API
export interface ApiResponse {
  answer: string;
}

// Tipo para o estado do chat
export interface ChatState {
  messages: ChatMessage[];
  loading: boolean;
  error: string | null;
}

// Tipo para o usuário atual/aluno
export interface User {
  id: number;
  name: string;
} 