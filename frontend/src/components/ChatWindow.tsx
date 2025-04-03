import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { ChatMessage as ChatMessageType } from '../types';
import { chatService } from '../services/api';

// Usuário fictício para o MVP
const MOCK_USER = {
  id: 1,
  name: 'Aluno Teste'
};

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessageType[]>([
    {
      id: uuidv4(),
      content: `Olá, ${MOCK_USER.name}! Sou o UniChat, seu assistente acadêmico. Como posso ajudar você hoje?`,
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Efeito para rolar para o final quando novas mensagens são adicionadas
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    // Adiciona a mensagem do usuário
    const userMessage: ChatMessageType = {
      id: uuidv4(),
      content,
      role: 'user',
      timestamp: new Date(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    
    try {
      // Envia a pergunta para o LLM
      const response = await chatService.sendQuestion(content, MOCK_USER.id);
      
      // Adiciona a resposta do assistente
      const assistantMessage: ChatMessageType = {
        id: uuidv4(),
        content: response.answer,
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
      
      // Salva a mensagem no histórico de chat (não bloqueante)
      chatService.saveChatMessage(MOCK_USER.id, content, response.answer)
        .catch(err => console.error('Erro ao salvar histórico:', err));
        
    } catch (error) {
      console.error('Erro ao processar mensagem:', error);
      
      // Mensagem de erro amigável
      const errorMessage: ChatMessageType = {
        id: uuidv4(),
        content: 'Desculpe, tive um problema ao processar sua pergunta. Poderia tentar novamente?',
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 rounded-lg shadow-md overflow-hidden">
      <div className="bg-blue-600 text-white p-4">
        <h1 className="text-xl font-bold">UniChat</h1>
        <p className="text-sm opacity-80">Seu assistente acadêmico inteligente</p>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <ChatInput onSendMessage={handleSendMessage} disabled={loading} />
    </div>
  );
};

export default ChatWindow; 