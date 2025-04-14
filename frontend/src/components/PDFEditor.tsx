// frontend/src/components/PDFEditor.tsx
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Loader2 } from 'lucide-react';

interface PDFEditorProps {
  projectId: number;
  section?: string;
  initialContent?: string;
  isOpen: boolean;
  onClose: () => void;
  onSave: (content: string) => Promise<void>;
}

const PDFEditor: React.FC<PDFEditorProps> = ({
  projectId,
  section,
  initialContent = "",
  isOpen,
  onClose,
  onSave
}) => {
  const [content, setContent] = useState(initialContent);
  const [isSaving, setIsSaving] = useState(false);
  
  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onSave(content);
      onClose();
    } catch (error) {
      console.error("Error al guardar:", error);
      alert("Error al guardar los cambios. Por favor, inténtalo de nuevo.");
    } finally {
      setIsSaving(false);
    }
  };
  
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[800px]">
        <DialogHeader>
          <DialogTitle>
            {section ? `Editar sección: ${section}` : "Editar documento"}
          </DialogTitle>
        </DialogHeader>
        
        <div className="my-4">
          <Textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="min-h-[400px] font-mono text-sm"
            placeholder="Escribe aquí el nuevo contenido..."
          />
        </div>
        
        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isSaving}>
            Cancelar
          </Button>
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Guardando...
              </>
            ) : (
              "Guardar cambios"
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default PDFEditor;