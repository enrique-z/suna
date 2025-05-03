'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface UsageDisplayProps {
  className?: string;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
    cost: number | null;
  } | null;
}

export function UsageDisplay({ className, usage }: UsageDisplayProps) {
  if (!usage) return null;

  return (
    <div className={cn("flex items-center justify-between text-xs text-muted-foreground px-4 py-2", className)}>
      <div className="flex gap-4">
        <div>
          <span className="font-medium">Input:</span> {usage.prompt_tokens?.toLocaleString() || 0} tokens
        </div>
        <div>
          <span className="font-medium">Output:</span> {usage.completion_tokens?.toLocaleString() || 0} tokens
        </div>
        <div>
          <span className="font-medium">Total:</span> {usage.total_tokens?.toLocaleString() || 0} tokens
        </div>
        <div>
          <span className="font-medium">Cost:</span> ${usage.cost?.toFixed(6) || 0}
        </div>
      </div>
    </div>
  );
}