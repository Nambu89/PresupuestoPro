// frontend/src/pages/ViewProject.tsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import PDFViewer from '../components/PDFViewer';
import { Button } from '../components/ui/button';
import { Spinner } from '../components/ui/spinner';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '../components/ui/dialog';
import { Textarea } from '../components/ui/textarea';
import { toast } from '../hooks/use-toast'; // Asegúrate de que esta importación sea correcta según tu estructura

const ViewProject = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [pdfUrl, setPdfUrl] = useState('');
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingSection, setEditingSection] = useState<string | undefined>(undefined);
  const [editContent, setEditContent] = useState('');
  const [regeneratingPdf, setRegeneratingPdf] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProject = async () => {
      try {
        const response = await fetch(`/api/projects/${id}`);
        
        if (!response.ok) {
          throw new Error('Error al cargar el proyecto');
        }
        
        const data = await response.json();
        setProject(data);
        
        // Cargar el PDF
        await loadPdf();
      } catch (error) {
        console.error('Error:', error);
        toast({
          title: "Error",
          description: "No se pudo cargar el proyecto",
          variant: "destructive"
        });
        navigate('/dashboard');
      } finally {
        setLoading(false);
      }
    };
    
    fetchProject();
    
    // Limpiar URL del PDF al desmontar
    return () => {
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }
    };
  }, [id, navigate]);

  const loadPdf = async () => {
    try {
      const pdfResponse = await fetch(`/api/projects/${id}/pdf`, {
        headers: {
          'Accept': 'application/pdf',
        },
      });
      
      if (!pdfResponse.ok) {
        throw new Error('Error al cargar el PDF');
      }
      
      // Crear URL para el PDF
      const pdfBlob = await pdfResponse.blob();
      const url = URL.createObjectURL(pdfBlob);
      setPdfUrl(url);
    } catch (error) {
      console.error('Error al cargar PDF:', error);
      toast({
        title: "Error",
        description: "No se pudo cargar el PDF del proyecto",
        variant: "destructive"
      });
    }
  };

  const handleEditRequest = (section?: string) => {
    setEditingSection(section);
    
    // Simulamos el contenido actual basado en la sección
    let initialContent = "";
    
    if (section === "1. OBJETO") {
      initialContent = `Cliente: ${project.name} tiene la necesidad de este proyecto para mejorar sus procesos de negocio.`;
    } else if (section === "2. DESCRIPCIÓN DEL PROYECTO") {
      initialContent = `Se desarrollará un proyecto de desarrollo web con las siguientes características...`;
    } else if (section === "2.1 FUNCIONALIDADES PRINCIPALES") {
      initialContent = `El proyecto incluirá las siguientes funcionalidades principales:
- Funcionalidad 1
- Funcionalidad 2
- Funcionalidad 3`;
    } else if (section === "3. PLANIFICACIÓN") {
      initialContent = `El proyecto se finalizará en ${project.estimated_duration_weeks} semanas. Una vez aprobada la oferta se dará fecha de entrega en el entorno de desarrollo.`;
    } else if (section === "4. COSTE") {
      initialContent = `El coste total de este evolutivo es de ${project.estimated_cost} euros, de los cuales el 50% se facturarán con la firma del contrato y el 50% restante después de finalizado el soporte post arranque de 5 días.`;
    }
    
    setEditContent(initialContent);
    setEditDialogOpen(true);
  };

  const handleSaveEdit = async () => {
    setRegeneratingPdf(true);
    
    try {
      // Aquí llamaríamos a la API para actualizar el contenido
      const response = await fetch(`/api/projects/${id}/update-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          section: editingSection,
          content: editContent
        }),
      });
      
      if (!response.ok) {
        throw new Error('Error al actualizar contenido');
      }
      
      // Recargar el PDF
      await loadPdf();
      
      // Cerrar el diálogo
      setEditDialogOpen(false);
      
      toast({
        title: "¡Éxito!",
        description: "El documento ha sido actualizado correctamente",
        variant: "default"
      });
    } catch (error) {
      console.error('Error al actualizar el contenido:', error);
      toast({
        title: "Error",
        description: "No se pudo actualizar el contenido del documento",
        variant: "destructive"
      });
    } finally {
      setRegeneratingPdf(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center min-h-screen">
          <Spinner className="h-8 w-8" />
          <span className="ml-2">Cargando proyecto...</span>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto py-8">
        <div className="mb-6 flex justify-between items-center">
          <h1 className="text-2xl font-bold">
            {project?.name || 'Proyecto'}
          </h1>
          
          <Button onClick={() => navigate('/dashboard')} variant="outline">
            Volver al Dashboard
          </Button>
        </div>
        
        {pdfUrl ? (
          <PDFViewer 
            projectId={parseInt(id || '0')} 
            projectName={project?.name || 'Proyecto'} 
            onClose={() => {}} // No necesitamos cerrar ya que está integrado en la página
            onRequestEdit={handleEditRequest}
          />
        ) : (
          <div className="text-center p-8 border rounded-md shadow-sm">
            No se pudo cargar el PDF del proyecto
          </div>
        )}
      </div>
      
      {/* Diálogo de edición */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent className="sm:max-w-[800px]">
          <DialogHeader>
            <DialogTitle>
              {editingSection ? `Editar sección: ${editingSection}` : "Editar documento"}
            </DialogTitle>
          </DialogHeader>
          
          <div className="my-4">
            <Textarea
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              className="min-h-[400px] font-mono text-sm"
              placeholder="Escribe aquí el nuevo contenido..."
            />
          </div>
          
          <DialogFooter>
            <Button 
              variant="outline" 
              onClick={() => setEditDialogOpen(false)} 
              disabled={regeneratingPdf}
            >
              Cancelar
            </Button>
            <Button 
              onClick={handleSaveEdit} 
              disabled={regeneratingPdf}
            >
              {regeneratingPdf ? (
                <>
                  <Spinner className="mr-2 h-4 w-4" />
                  Guardando...
                </>
              ) : (
                "Guardar cambios"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Layout>
  );
};

export default ViewProject;