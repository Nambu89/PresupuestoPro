// components/ui/spinner.tsx
import { Loader2 } from 'lucide-react';
import React from 'react';

interface SpinnerProps {
  className?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({ className = "h-6 w-6" }) => {
  return <Loader2 className={`animate-spin ${className}`} />;
};

export default Spinner;