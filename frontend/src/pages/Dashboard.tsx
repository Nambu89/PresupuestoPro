import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus, FileText, Download, Mail, MessageCircle, Search, Filter, ChevronDown, Trash2, AlertCircle } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import PDFViewer from "@/components/PDFViewer";
import Layout from "@/components/layout/Layout";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/components/ui/use-toast";
import axios from "axios";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

// Configurar axios para incluir el token en todas las solicitudes
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const Dashboard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [searchTerm, setSearchTerm] = useState("");
  const [filterStatus, setFilterStatus] = useState("Todos");
  const [chatOpen, setChatOpen] = useState(false);
  const [chatProjectId, setChatProjectId] = useState(null);
  const [chatQuery, setChatQuery] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [projects, setProjects] = useState([]);
  const [viewingPdfProject, setViewingPdfProject] = useState<number | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [projectToDelete, setProjectToDelete] = useState<number | null>(null);
  
  // Función para cargar los proyectos desde el backend
  const loadProjects = async () => {
    try {
      setIsLoading(true);
      console.log('Obteniendo proyectos del backend...');
      
      const token = localStorage.getItem('token');
      console.log('Token disponible:', !!token);
      
      const response = await axios.get('/api/v1/projects/');
      console.log('Respuesta del servidor:', response.data);
      
      if (response.data && Array.isArray(response.data)) {
        if (response.data.length === 0) {
          console.log('No se encontraron proyectos en el servidor');
          setProjects([]);
          return;
        }
        
        const formattedProjects = response.data.map(project => {
          console.log('Procesando proyecto:', project);
          return {
            id: project.id,
            name: project.name,
            client: project.description?.split('\n')[0] || 'Cliente',
            date: project.created_at ? new Date(project.created_at).toLocaleDateString() : 'Fecha desconocida',
            price: `${(project.estimated_cost || 0).toLocaleString()} €`,
            status: project.is_premium ? 'Completo' : 'Vista Previa',
            isPremium: project.is_premium || false,
            description: project.description || ''
          };
        });
        
        console.log('Proyectos formateados:', formattedProjects);
        setProjects(formattedProjects);
        
        toast({
          title: "Proyectos cargados",
          description: `Se han cargado ${formattedProjects.length} proyectos correctamente.`,
        });
      } else {
        console.error('Formato de respuesta inesperado:', response.data);
        toast({
          title: "Error de formato",
          description: "El formato de los datos recibidos no es válido.",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error('Error al cargar proyectos:', error);
      console.error('Detalles del error:', error.response?.data || error.message);
      
      toast({
        title: "Error",
        description: "No se pudieron cargar los proyectos. Inténtalo de nuevo más tarde.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  useEffect(() => {
    // Verificar si el usuario está autenticado
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    
    // Cargar los proyectos
    loadProjects();
  }, [navigate]);
  
  // Filtrar proyectos según búsqueda y filtro
  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         project.client.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === "Todos" || project.status === filterStatus;
    return matchesSearch && matchesFilter;
  });
  
  const handleCreateNewProject = () => {
    navigate("/new-project");
  };
  
  const handleUpgradeProject = (projectId) => {
    // Simular actualización a premium
    const updatedProjects = projects.map(project => {
      if (project.id === projectId) {
        return { ...project, isPremium: true, status: "Completo" };
      }
      return project;
    });
    
    setProjects(updatedProjects);
    
    toast({
      title: "¡Proyecto actualizado!",
      description: "Has desbloqueado todas las funcionalidades premium para este proyecto.",
      variant: "default",
    });
  };

  const handleViewComplete = async (projectId: number) => {
    try {
      // Mostrar el visor de PDF
      setViewingPdfProject(projectId);
      
      toast({
        title: "Visualizando Presupuesto",
        description: "Cargando el presupuesto...",
      });
    } catch (error) {
      console.error('Error al abrir el presupuesto:', error);
      toast({
        title: "Error",
        description: "No se pudo abrir el presupuesto. Inténtalo de nuevo más tarde.",
        variant: "destructive",
      });
    }
  };

  // Función para descargar PDF
  const handleDownloadPDF = async (projectId: number) => {
    try {
      setIsLoading(true);
      
      // Obtener el proyecto para usar su nombre en el archivo
      const projectResponse = await axios.get(`/api/v1/projects/${projectId}`);
      const projectName = projectResponse.data.name.replace(/ /g, '_');
      
      // Usar axios para obtener el PDF como blob
      const response = await axios.get(`/api/v1/projects/${projectId}/pdf`, {
        responseType: 'blob',
        headers: {
          'Accept': 'application/pdf'
        }
      });
      
      // Crear un objeto URL para el blob
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      
      // Crear un enlace temporal para descargar el PDF
      const link = document.createElement('a');
      link.href = url;
      link.download = `presupuesto_${projectName}.pdf`;
      document.body.appendChild(link);
      link.click();
      
      // Limpiar
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast({
        title: "PDF Descargado",
        description: "El presupuesto se ha descargado correctamente.",
      });
    } catch (error) {
      console.error('Error al descargar PDF:', error);
      toast({
        title: "Error",
        description: "No se pudo descargar el PDF. Inténtalo de nuevo más tarde.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Función para enviar por email
  const handleSendEmail = (projectId) => {
    setIsLoading(true);
    
    axios.post(`/api/v1/projects/${projectId}/email`)
      .then((response) => {
        setIsLoading(false);
        toast({
          title: "Email enviado",
          description: "El presupuesto se ha enviado correctamente por email.",
          variant: "default",
        });
      })
      .catch((error) => {
        console.error('Error al enviar el email:', error);
        setIsLoading(false);
        toast({
          title: "Error",
          description: "No se pudo enviar el email. Inténtalo de nuevo más tarde.",
          variant: "destructive",
        });
      });
  };

  // Función para abrir el chat
  const handleOpenChat = (projectId) => {
    setChatProjectId(projectId);
    setChatQuery("");
    setChatResponse("");
    setChatOpen(true);
  };

  // Función para enviar consulta al chat
  const handleSendChatQuery = () => {
    if (!chatQuery.trim()) return;

    setIsLoading(true);
    axios.post(`/api/v1/projects/${chatProjectId}/chat`, { query: chatQuery })
      .then((response) => {
        setChatResponse(response.data.response);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Error en la consulta al chat:', error);
        setIsLoading(false);
        toast({
          title: "Error",
          description: "No se pudo procesar tu consulta. Inténtalo de nuevo más tarde.",
          variant: "destructive",
        });
      });
  };

  // Función para mostrar el diálogo de confirmación de eliminación
  const handleShowDeleteConfirmation = (projectId: number) => {
    setProjectToDelete(projectId);
    setDeleteDialogOpen(true);
  };

  // Función para eliminar un proyecto
  const handleDeleteProject = async () => {
    if (!projectToDelete) return;
    
    try {
      setIsLoading(true);
      
      // Llamar al endpoint de eliminación
      await axios.delete(`/api/v1/projects/${projectToDelete}`);
      
      // Actualizar la lista de proyectos eliminando el proyecto borrado
      setProjects(projects.filter(project => project.id !== projectToDelete));
      
      // Cerrar el diálogo de confirmación
      setDeleteDialogOpen(false);
      setProjectToDelete(null);
      
      toast({
        title: "Proyecto eliminado",
        description: "El presupuesto se ha eliminado correctamente.",
      });
    } catch (error) {
      console.error('Error al eliminar el proyecto:', error);
      toast({
        title: "Error",
        description: "No se pudo eliminar el presupuesto. Inténtalo de nuevo más tarde.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout hideFooter={true}>
      {viewingPdfProject !== null && (
        <PDFViewer 
          projectId={viewingPdfProject} 
          onClose={() => setViewingPdfProject(null)} 
        />
      )}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold">Panel de Control</h1>
            <p className="text-gray-600">Gestiona tus presupuestos de proyectos</p>
          </div>
          <Button className="flex items-center gap-2" onClick={handleCreateNewProject}>
            <Plus className="h-4 w-4" />
            Nuevo Presupuesto
          </Button>
        </div>
        
        {/* Filtros y búsqueda */}
        <div className="mb-6 flex flex-col md:flex-row gap-4">
          <div className="relative flex-grow">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input 
              className="pl-10" 
              placeholder="Buscar por nombre o cliente..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="flex items-center gap-2">
                <Filter className="h-4 w-4" />
                {filterStatus}
                <ChevronDown className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setFilterStatus("Todos")}>Todos</DropdownMenuItem>
              <DropdownMenuItem onClick={() => setFilterStatus("Completo")}>Completo</DropdownMenuItem>
              <DropdownMenuItem onClick={() => setFilterStatus("Vista Previa")}>Vista Previa</DropdownMenuItem>
              <DropdownMenuItem onClick={() => setFilterStatus("Borrador")}>Borrador</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>

        <h2 className="text-xl font-semibold mb-4">Presupuestos {filterStatus !== "Todos" ? filterStatus + "s" : ""}</h2>
        
        {filteredProjects.length === 0 ? (
          <div className="bg-gray-50 rounded-lg p-8 text-center">
            <p className="text-gray-500 mb-4">No se encontraron presupuestos que coincidan con tu búsqueda.</p>
            <Button variant="outline" onClick={() => {setSearchTerm(""); setFilterStatus("Todos");}}>
              Limpiar filtros
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {filteredProjects.map((project) => (
            <Card key={project.id} className="overflow-hidden hover:shadow-md transition-shadow duration-200">
              <CardHeader className="pb-3">
                <CardTitle className="flex justify-between items-start">
                  <span>{project.name}</span>
                  <div className="flex items-center gap-2">
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-6 w-6 text-gray-500 hover:text-red-500"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleShowDeleteConfirmation(project.id);
                      }}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                    <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                      project.isPremium 
                        ? "bg-green-100 text-green-800" 
                        : project.status === "Vista Previa" 
                          ? "bg-blue-100 text-blue-800"
                          : "bg-yellow-100 text-yellow-800"
                    }`}>
                      {project.status}
                    </div>
                  </div>
                </CardTitle>
                <CardDescription>
                  <div className="flex flex-col">
                    <span className="text-sm">{project.client}</span>
                    <span className="text-xs text-gray-500">{project.date}</span>
                  </div>
                </CardDescription>
              </CardHeader>
              <CardContent className="pb-3">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm text-gray-500">Precio estimado</p>
                    <p className="text-2xl font-bold">{project.price}</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="flex flex-col items-stretch gap-3">
                {!project.isPremium ? (
                  <Button 
                    className="w-full" 
                    onClick={() => handleUpgradeProject(project.id)}
                  >
                    Desbloquear completo
                  </Button>
                ) : (
                  <>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1"
                        onClick={() => handleDownloadPDF(project.id)}
                        disabled={isLoading}
                      >
                        <Download className="h-4 w-4 mr-1" /> PDF
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1"
                        onClick={() => handleSendEmail(project.id)}
                        disabled={isLoading}
                      >
                        <Mail className="h-4 w-4 mr-1" /> Email
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1"
                        onClick={() => handleOpenChat(project.id)}
                        disabled={isLoading}
                      >
                        <MessageCircle className="h-4 w-4 mr-1" /> Chat
                      </Button>
                    </div>
                    <Button 
                      variant="default" 
                      size="sm"
                      onClick={() => handleViewComplete(project.id)}
                      disabled={isLoading}
                    >
                      <FileText className="h-4 w-4 mr-1" /> Ver completo
                    </Button>
                  </>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
        )}
      </main>

      {/* Diálogo de Chat con IA */}
      <Dialog open={chatOpen} onOpenChange={setChatOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Consulta sobre tu presupuesto</DialogTitle>
            <DialogDescription>
              Haz cualquier pregunta sobre costes, plazos, tecnologías u otros aspectos de tu presupuesto.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 my-4">
            {chatResponse && (
              <div className="bg-gray-100 p-4 rounded-lg">
                <p className="whitespace-pre-line">{chatResponse}</p>
              </div>
            )}
            
            <div className="flex gap-2">
              <Input
                placeholder="Escribe tu consulta..."
                value={chatQuery}
                onChange={(e) => setChatQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendChatQuery()}
              />
              <Button onClick={handleSendChatQuery} disabled={isLoading || !chatQuery.trim()}>
                Enviar
              </Button>
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setChatOpen(false)}>
              Cerrar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Diálogo de confirmación para eliminar proyecto */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-red-600">
              <AlertCircle className="h-5 w-5" />
              Confirmar eliminación
            </DialogTitle>
            <DialogDescription>
              ¿Estás seguro de que deseas eliminar este presupuesto? Esta acción no se puede deshacer.
            </DialogDescription>
          </DialogHeader>
          
          <DialogFooter className="mt-4">
            <Button
              variant="outline"
              onClick={() => {
                setDeleteDialogOpen(false);
                setProjectToDelete(null);
              }}
            >
              Cancelar
            </Button>
            <Button
              variant="destructive"
              onClick={handleDeleteProject}
              disabled={isLoading}
            >
              {isLoading ? "Eliminando..." : "Eliminar"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Layout>
  );
};

export default Dashboard;