import React from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import ReactMarkdown from 'react-markdown';
import { FaUser, FaRobot } from 'react-icons/fa';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div 
      className={cn(
        'flex gap-3 p-4 rounded-lg max-w-[85%]',
        isUser 
          ? 'ml-auto bg-primary/90 text-primary-foreground' 
          : 'mr-auto bg-secondary text-secondary-foreground'
      )}
    >
      <div className={cn(
        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
        isUser 
          ? 'bg-primary-foreground/20' 
          : 'bg-primary/10'
      )}>
        {isUser ? (
          <FaUser className="text-primary-foreground" size={14} />
        ) : (
          <FaRobot className="text-primary" size={14} />
        )}
      </div>
      <div className="flex-1 overflow-hidden">
        <ReactMarkdown 
          className={cn(
            'prose', 
            'max-w-none', 
            isUser ? 'prose-invert' : '',
            'prose-p:my-1 prose-headings:mb-2'
          )}
        >
          {message.content}
        </ReactMarkdown>
        <div className={cn(
          'text-xs mt-1', 
          isUser ? 'text-primary-foreground/70' : 'text-secondary-foreground/70'
        )}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage; 