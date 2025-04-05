import React, { useState, FormEvent } from 'react';
import { FaPaperPlane } from 'react-icons/fa';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled = false }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  return (
    <form 
      onSubmit={handleSubmit} 
      className="flex items-center gap-2 p-4 border-t border-border bg-card/80"
    >
      <Input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Digite sua pergunta..."
        disabled={disabled}
        className="bg-background/60 focus-visible:ring-primary"
      />
      <Button
        type="submit"
        disabled={!message.trim() || disabled}
        size="icon"
        variant="default"
        className="rounded-full"
      >
        <FaPaperPlane className="h-4 w-4" />
      </Button>
    </form>
  );
};

export default ChatInput; 