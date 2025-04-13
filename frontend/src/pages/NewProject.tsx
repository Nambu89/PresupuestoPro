import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/components/ui/use-toast";
import { ArrowLeft, Wand2 } from "lucide-react";
import axios from "axios";

const NewProject = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isGenerating, setIsGenerating] = useState(false);
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: "",
    client: "",
    projectType: "",
    description: "",
    features: "",
    deadline: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSelectChange = (name, value) => {
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  
  // Función para convertir el tipo de proyecto a un nombre legible
  const getProjectTypeName = (projectType: string): string => {
    const projectTypes = {
      "web": "Desarrollo Web",
      "mobile": "Aplicación Móvil",
      "ecommerce": "E-commerce",
      "dashboard": "Dashboard",
      "redesign": "Rediseño",
      "other": "Otro"
    };
    
    return projectTypes[projectType] || projectType;
  };

  const handleNext = () => {
    // Validación básica
    if (step === 1) {
      if (!formData.name || !formData.client || !formData.projectType) {
        toast({
          title: "Campos requeridos",
          description: "Por favor, completa todos los campos obligatorios.",
          variant: "destructive",
        });
        return;
      }
    }
    
    if (step === 2) {
      if (!formData.description || !formData.features) {
        toast({
          title: "Campos requeridos",
          description: "Por favor, completa todos los campos obligatorios.",
          variant: "destructive",
        });
        return;
      }
    }
    
    setStep(step + 1);
  };

  const handleBack = () => {
    setStep(step - 1);
  };

  const handleGenerateWithAI = async () => {
    setIsGenerating(true);
    
    try {
      // Preparar una descripción estructurada con todos los datos del formulario
      let structuredDescription = `Cliente: ${formData.client}\n`;
      structuredDescription += `Tipo de proyecto: ${getProjectTypeName(formData.projectType)}\n`;
      structuredDescription += `Descripción: ${formData.description}\n`;
      structuredDescription += `Funcionalidades: ${formData.features}\n`;
      
      if (formData.deadline) {
        structuredDescription += `Fecha límite: ${formData.deadline}\n`;
      }
      
      // Crear el objeto de proyecto para enviar al backend
      const projectData = {
        name: formData.name,
        description: structuredDescription,
        estimated_duration_weeks: parseInt(formData.deadline) || 8 // Valor por defecto si no hay plazo
      };
      
      console.log('Enviando datos del proyecto:', projectData);
      
      // Enviar los datos al backend
      const response = await axios.post('/api/v1/projects/', projectData);
      
      console.log('Respuesta del servidor:', response.data);
      
      toast({
        title: "¡Presupuesto generado!",
        description: "Se ha generado un presupuesto basado en tus requisitos.",
        variant: "default",
      });
      
      // Redirigir al dashboard después de un breve retraso
      setTimeout(() => {
        navigate("/dashboard");
      }, 1500);
    } catch (error) {
      console.error('Error al crear el proyecto:', error);
      
      toast({
        title: "Error",
        description: "No se pudo crear el proyecto. Por favor, inténtalo de nuevo.",
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => navigate("/dashboard")}
        >
          <ArrowLeft className="h-4 w-4 mr-2" /> Volver al dashboard
        </Button>

        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl font-bold mb-2">Nuevo Presupuesto</h1>
          <p className="text-gray-600 mb-8">
            Crea un nuevo presupuesto para tu proyecto utilizando nuestra IA
          </p>

          {/* Pasos */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div
                  className={`h-2 rounded-full ${
                    step >= 1 ? "bg-primary-blue" : "bg-gray-200"
                  }`}
                ></div>
              </div>
              <div className="mx-2">
                <div
                  className={`h-2 w-2 rounded-full ${
                    step >= 2 ? "bg-primary-blue" : "bg-gray-200"
                  }`}
                ></div>
              </div>
              <div className="flex-1">
                <div
                  className={`h-2 rounded-full ${
                    step >= 2 ? "bg-primary-blue" : "bg-gray-200"
                  }`}
                ></div>
              </div>
              <div className="mx-2">
                <div
                  className={`h-2 w-2 rounded-full ${
                    step >= 3 ? "bg-primary-blue" : "bg-gray-200"
                  }`}
                ></div>
              </div>
              <div className="flex-1">
                <div
                  className={`h-2 rounded-full ${
                    step >= 3 ? "bg-primary-blue" : "bg-gray-200"
                  }`}
                ></div>
              </div>
            </div>
            <div className="flex justify-between mt-2 text-sm text-gray-500">
              <span>Información básica</span>
              <span>Detalles del proyecto</span>
              <span>Revisión y generación</span>
            </div>
          </div>

          <Card>
            {step === 1 && (
              <>
                <CardHeader>
                  <CardTitle>Información básica</CardTitle>
                  <CardDescription>
                    Introduce la información básica del proyecto
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Nombre del proyecto *</Label>
                    <Input
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="Ej: Tienda Online para Moda Express"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="client">Cliente *</Label>
                    <Input
                      id="client"
                      name="client"
                      value={formData.client}
                      onChange={handleChange}
                      placeholder="Ej: Moda Express S.L."
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="projectType">Tipo de proyecto *</Label>
                    <Select
                      onValueChange={(value) =>
                        handleSelectChange("projectType", value)
                      }
                      value={formData.projectType}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Selecciona un tipo de proyecto" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="web">Desarrollo Web</SelectItem>
                        <SelectItem value="mobile">Aplicación Móvil</SelectItem>
                        <SelectItem value="ecommerce">E-commerce</SelectItem>
                        <SelectItem value="dashboard">Dashboard</SelectItem>
                        <SelectItem value="redesign">Rediseño</SelectItem>
                        <SelectItem value="other">Otro</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-end">
                  <Button onClick={handleNext}>Siguiente</Button>
                </CardFooter>
              </>
            )}

            {step === 2 && (
              <>
                <CardHeader>
                  <CardTitle>Detalles del proyecto</CardTitle>
                  <CardDescription>
                    Describe los detalles y requerimientos del proyecto
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="description">Descripción del proyecto *</Label>
                    <Textarea
                      id="description"
                      name="description"
                      value={formData.description}
                      onChange={handleChange}
                      placeholder="Describe brevemente el proyecto y sus objetivos"
                      rows={4}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="features">Funcionalidades principales *</Label>
                    <Textarea
                      id="features"
                      name="features"
                      value={formData.features}
                      onChange={handleChange}
                      placeholder="Lista las funcionalidades principales que debe tener el proyecto"
                      rows={4}
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="deadline">Fecha límite (opcional)</Label>
                      <Input
                        id="deadline"
                        name="deadline"
                        type="date"
                        value={formData.deadline}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button variant="outline" onClick={handleBack}>
                    Atrás
                  </Button>
                  <Button onClick={handleNext}>Siguiente</Button>
                </CardFooter>
              </>
            )}

            {step === 3 && (
              <>
                <CardHeader>
                  <CardTitle>Revisión y generación</CardTitle>
                  <CardDescription>
                    Revisa la información y genera tu presupuesto con IA
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="font-medium mb-2">Información básica</h3>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <p className="text-sm text-gray-500">Nombre del proyecto</p>
                          <p>{formData.name}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Cliente</p>
                          <p>{formData.client}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Tipo de proyecto</p>
                          <p>
                            {formData.projectType === "web"
                              ? "Desarrollo Web"
                              : formData.projectType === "mobile"
                              ? "Aplicación Móvil"
                              : formData.projectType === "ecommerce"
                              ? "E-commerce"
                              : formData.projectType === "dashboard"
                              ? "Dashboard"
                              : formData.projectType === "redesign"
                              ? "Rediseño"
                              : "Otro"}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="font-medium mb-2">Detalles del proyecto</h3>
                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-500">Descripción</p>
                          <p className="whitespace-pre-line">{formData.description}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Funcionalidades</p>
                          <p className="whitespace-pre-line">{formData.features}</p>
                        </div>
                        {formData.deadline && (
                          <div>
                            <p className="text-sm text-gray-500">Fecha límite</p>
                            <p>{formData.deadline}</p>
                          </div>
                        )}

                      </div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex flex-col sm:flex-row justify-between gap-4">
                  <Button variant="outline" onClick={handleBack} className="w-full sm:w-auto">
                    Atrás
                  </Button>
                  <Button
                    onClick={handleGenerateWithAI}
                    className="w-full sm:w-auto"
                    disabled={isGenerating}
                  >
                    {isGenerating ? (
                      <>Generando...</>
                    ) : (
                      <>
                        <Wand2 className="h-4 w-4 mr-2" /> Generar con IA
                      </>
                    )}
                  </Button>
                </CardFooter>
              </>
            )}
          </Card>
        </div>
      </div>
    </Layout>
  );
};

export default NewProject;
