import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";

interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
  general?: string;
}

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    
    // Limpiar errores al cambiar el valor
    if (errors[name as keyof FormErrors]) {
      setErrors({
        ...errors,
        [name]: undefined
      });
    }
  };

  const validateForm = () => {
    const newErrors: FormErrors = {};
    let isValid = true;

    if (!formData.email) {
      newErrors.email = 'El correo electrónico es obligatorio';
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'El correo electrónico no es válido';
      isValid = false;
    }

    if (!formData.password) {
      newErrors.password = 'La contraseña es obligatoria';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    setErrors({ ...errors, general: "" });
    
    try {
      console.log('Intentando iniciar sesión con:', {
        email: formData.email,
        password: formData.password.substring(0, 3) + '***'
      });
      
      // Usar el proxy configurado en Vite
      const API_VERSION = '/api/v1';
      
      // Crear objeto con formato para OAuth2
      const formBody = new URLSearchParams();
      formBody.append('username', formData.email);
      formBody.append('password', formData.password);
      
      console.log('Parámetros enviados:', formBody.toString());
      
      // Enviar solicitud de inicio de sesión usando fetch con el proxy
      const response = await fetch(`${API_VERSION}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formBody
      });
      
      console.log('Respuesta completa:', response);
      console.log('Status:', response.status);
      console.log('Status Text:', response.statusText);
      
      if (!response.ok) {
        let errorMessage = 'Error al iniciar sesión';
        try {
          const errorData = await response.json();
          console.log('Error en la respuesta:', errorData);
          errorMessage = errorData.detail || errorMessage;
        } catch (jsonError) {
          console.log('Error al parsear la respuesta de error:', jsonError);
        }
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      console.log('Respuesta del servidor:', data);
      
      // Guardar el token en localStorage
      localStorage.setItem('token', data.access_token);
      
      // Mostrar mensaje de éxito
      toast({
        title: "Inicio de sesión exitoso",
        description: "Has iniciado sesión correctamente.",
        variant: "default",
      });
      
      // Redirigir al dashboard
      navigate("/dashboard");
    } catch (error: any) {
      console.error("Error al iniciar sesión:", error);
      
      // Obtener mensaje de error más específico si está disponible
      let errorMessage = "Credenciales incorrectas. Por favor, verifica tu email y contraseña.";
      
      if (error.message) {
        errorMessage = error.message;
      }
      
      // Mostrar mensaje de error
      setErrors({
        ...errors,
        general: errorMessage
      });
      
      toast({
        title: "Error al iniciar sesión",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <Link to="/" className="mx-auto mb-4 flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-blue to-primary-dark rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">PI</span>
            </div>
            <span className="text-xl font-bold">
              Presupuesto<span className="text-primary-blue">Pro</span>
            </span>
          </Link>
          <CardTitle className="text-2xl font-bold">Iniciar sesión</CardTitle>
          <CardDescription>
            Accede a tu cuenta para gestionar tus presupuestos
          </CardDescription>
        </CardHeader>
        <CardContent>
          {errors.general && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {errors.general}
            </div>
          )}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input 
                id="email" 
                name="email"
                type="email" 
                placeholder="tu@email.com" 
                value={formData.email}
                onChange={handleChange}
                required 
              />
              {errors.email && <p className="text-sm text-red-500">{errors.email}</p>}
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Contraseña</Label>
                <Link to="/forgot-password" className="text-sm text-primary-blue hover:underline">
                  ¿Olvidaste tu contraseña?
                </Link>
              </div>
              <Input 
                id="password" 
                name="password"
                type="password" 
                value={formData.password}
                onChange={handleChange}
                required 
              />
              {errors.password && <p className="text-sm text-red-500">{errors.password}</p>}
            </div>
            <Button className="w-full mt-6" type="submit" disabled={isLoading}>
              {isLoading ? "Iniciando sesión..." : "Iniciar sesión"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <div className="text-center text-sm">
            ¿No tienes cuenta?{" "}
            <Link to="/register" className="text-primary-blue hover:underline font-medium">
              Regístrate
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
};

export default Login;
