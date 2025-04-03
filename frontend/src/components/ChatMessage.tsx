import React from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import ReactMarkdown from 'react-markdown';
import { FaUser, FaRobot } from 'react-icons/fa';
import clsx from 'clsx';

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div 
      className={clsx(
        'flex gap-3 p-4 rounded-lg max-w-[85%]',
        isUser ? 'ml-auto bg-blue-600 text-white' : 'mr-auto bg-gray-100 text-gray-800'
      )}
    >
      <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center">
        {isUser ? (
          <FaUser className="text-white" />
        ) : (
          <FaRobot className="text-blue-600" />
        )}
      </div>
      <div className="flex-1 overflow-hidden">
        <ReactMarkdown 
          className={clsx(
            'prose', 
            'max-w-none', 
            isUser ? 'prose-invert' : '',
            'prose-p:my-1 prose-headings:mb-2'
          )}
        >
          {message.content}
        </ReactMarkdown>
        <div className={clsx('text-xs mt-1', isUser ? 'text-blue-200' : 'text-gray-500')}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage; 