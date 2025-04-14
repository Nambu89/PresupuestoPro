import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Loader2, Edit2 } from 'lucide-react';
import PDFChat from './PDFChat';

interface PDFViewerProps {
  projectId: number;
  projectName?: string; // Añadimos el nombre del proyecto como prop
  onClose: () => void;
  onRequestEdit?: (section?: string) => void; // Callback para editar el documento
}

const PDFViewer: React.FC<PDFViewerProps> = ({ 
  projectId, 
  projectName = 'Proyecto',
  onClose,
  onRequestEdit 
}) => {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Mapeo de secciones a elementos en el documento
  const sectionRefs = new Map<string, HTMLElement>();
  
  // Estado para mostrar u ocultar el botón de edición
  const [showEditButton, setShowEditButton] = useState(false);

  useEffect(() => {
    const fetchPDF = async () => {
      try {
        setLoading(true);
        
        // Obtener el PDF como blob
        const response = await axios.get(`/api/v1/projects/${projectId}/view-pdf`, {
          responseType: 'blob',
          headers: {
            'Accept': 'application/pdf'
          }
        });
        
        // Crear URL para el blob
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
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
  
  // Función para desplazarse a una sección específica
  const scrollToSection = (section: string) => {
    // Simplemente registrar la intención en la consola sin mostrar ninguna notificación al usuario
    console.log(`Referencia a la sección: ${section} - El usuario puede verla en el documento`);
    // No mostramos ninguna ventana emergente ni notificación para no interrumpir la experiencia
  };
  
  // Función para manejar solicitudes de edición sin diálogos de confirmación
  const handleEditRequest = (section?: string) => {
    // Simplemente llamar a la función de edición si está disponible
    if (onRequestEdit) {
      console.log(`Solicitando edición para: ${section || 'documento completo'}`);
      onRequestEdit(section);
    } else {
      // Registrar en consola pero no mostrar alerta al usuario
      console.error(`Función de edición no disponible para: ${section || 'documento completo'}`);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-6xl h-[90vh] flex flex-col relative">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold">Visualizando Presupuesto</h2>
          <button 
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>
        
        <div className="flex-grow overflow-hidden p-2 relative">
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
            <>
              <iframe 
                src={pdfUrl} 
                className="w-full h-full border-0"
                title="PDF Viewer"
              />
              
              {/* Botón de edición (opcional, si se muestra cuando el usuario lo solicita) */}
              {showEditButton && onRequestEdit && (
                <button
                  className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg"
                  onClick={() => handleEditRequest()}
                >
                  <Edit2 className="h-6 w-6 text-blue-600" />
                </button>
              )}
              
              {/* Integrar el componente de chat */}
              <PDFChat
                projectId={projectId}
                projectName={projectName || 'Proyecto'}
                onRequestEdit={handleEditRequest}
                onScrollToSection={scrollToSection}
              />
            </>
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