import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Loader2 } from 'lucide-react';

interface PDFViewerProps {
  projectId: number;
  onClose: () => void;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ projectId, onClose }) => {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPDF = async () => {
      try {
        setLoading(true);
        
        // Obtener el PDF como blob
        const response = await axios.get(`/api/v1/projects/${projectId}/view-pdf`, {
          responseType: 'blob',
        });
        
        // Crear URL para el blob
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
        
        // Limpiar URL cuando el componente se desmonte
        return () => {
          URL.revokeObjectURL(url);
        };
      } catch (err) {
        console.error('Error al cargar el PDF:', err);
        setError('No se pudo cargar el PDF. Por favor, inténtalo de nuevo más tarde.');
      } finally {
        setLoading(false);
      }
    };

    fetchPDF();
  }, [projectId]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-6xl h-[90vh] flex flex-col">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold">Visualizando Presupuesto</h2>
          <button 
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>
        
        <div className="flex-grow overflow-hidden p-2">
          {loading ? (
            <div className="h-full flex items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-primary-blue" />
              <span className="ml-2">Cargando PDF...</span>
            </div>
          ) : error ? (
            <div className="h-full flex items-center justify-center text-red-500">
              {error}
            </div>
          ) : pdfUrl ? (
            <iframe 
              src={pdfUrl} 
              className="w-full h-full border-0"
              title="PDF Viewer"
            />
          ) : (
            <div className="h-full flex items-center justify-center text-red-500">
              No se pudo cargar el PDF.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PDFViewer;
