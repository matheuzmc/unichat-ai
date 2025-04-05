import React from 'react';
import { FaRobot } from 'react-icons/fa';
import { cn } from '@/lib/utils';
import { Skeleton } from '@/components/ui/skeleton';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-3 p-4 rounded-lg mr-auto bg-secondary text-secondary-foreground max-w-[85%]">
      <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-primary/10">
        <FaRobot className="text-primary" size={14} />
      </div>
      <div className="flex items-center">
        <div className="flex space-x-2">
          <div className="typing-dot w-2 h-2 rounded-full bg-secondary-foreground/70" 
               style={{ animationDelay: '0ms' }} />
          <div className="typing-dot w-2 h-2 rounded-full bg-secondary-foreground/70" 
               style={{ animationDelay: '300ms' }} />
          <div className="typing-dot w-2 h-2 rounded-full bg-secondary-foreground/70" 
               style={{ animationDelay: '600ms' }} />
        </div>
      </div>
    </div>
  );
};

// Versão alternativa com Skeleton do shadcn/ui
export const SkeletonMessage: React.FC = () => {
  return (
    <div className="flex gap-3 p-4 rounded-lg mr-auto bg-secondary text-secondary-foreground max-w-[85%]">
      <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-primary/10">
        <FaRobot className="text-primary" size={14} />
      </div>
      <div className="flex-1">
        <div className="space-y-2">
          <Skeleton className="h-4 w-[250px]" />
          <Skeleton className="h-4 w-[200px]" />
          <Skeleton className="h-4 w-[150px]" />
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator; 