import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";
import Layout from "@/components/layout/Layout";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { AlertCircle, User, Mail, Lock, Bell, Globe, Palette } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import axios from "axios";

const Settings = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [activeTab, setActiveTab] = useState("profile");

  // Estados para los datos del perfil
  const [userData, setUserData] = useState({
    email: "",
    first_name: "",
    last_name: "",
  });

  // Estados para cambio de contraseña
  const [passwordData, setPasswordData] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });

  // Estados para configuración
  const [configData, setConfigData] = useState({
    notification_email: true,
    notification_sms: false,
    language: "es",
    theme: "light",
    currency: "EUR",
  });

  // Estado para errores
  const [errors, setErrors] = useState({
    profile: "",
    password: "",
    config: "",
  });

  // Cargar datos del usuario y configuración
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const loadUserData = async () => {
      try {
        setIsLoading(true);
        
        // Cargar datos del usuario
        const userResponse = await axios.get("/api/v1/auth/me");
        if (userResponse.data) {
          setUserData({
            email: userResponse.data.email || "",
            first_name: userResponse.data.first_name || "",
            last_name: userResponse.data.last_name || "",
          });
        }
        
        // Cargar configuración del usuario
        const configResponse = await axios.get("/api/v1/config/");
        if (configResponse.data) {
          setConfigData({
            notification_email: configResponse.data.notification_email,
            notification_sms: configResponse.data.notification_sms,
            language: configResponse.data.language,
            theme: configResponse.data.theme,
            currency: configResponse.data.currency,
          });
        }
      } catch (error) {
        console.error("Error al cargar datos:", error);
        toast({
          title: "Error",
          description: "No se pudieron cargar tus datos. Inténtalo de nuevo más tarde.",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    loadUserData();
  }, [navigate, toast]);

  // Manejar cambios en los campos de perfil
  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setUserData({
      ...userData,
      [name]: value,
    });
  };

  // Manejar cambios en los campos de contraseña
  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData({
      ...passwordData,
      [name]: value,
    });
  };

  // Manejar cambios en la configuración
  const handleConfigChange = (name, value) => {
    setConfigData({
      ...configData,
      [name]: value,
    });

    // Si se cambia el tema, aplicarlo inmediatamente
    if (name === "theme") {
      // Aplicar el tema directamente al elemento HTML
      const root = window.document.documentElement;
      root.classList.remove("light", "dark", "system");
      root.classList.add(value);
      localStorage.setItem("presupuestopro-ui-theme", value);
    }
  };

  // Guardar cambios del perfil
  const handleSaveProfile = async () => {
    try {
      setIsSaving(true);
      setErrors({ ...errors, profile: "" });

      const response = await axios.put("/api/v1/users/me", userData);
      
      toast({
        title: "Perfil actualizado",
        description: "Tus datos de perfil se han actualizado correctamente.",
      });
    } catch (error) {
      console.error("Error al actualizar perfil:", error);
      setErrors({
        ...errors,
        profile: "No se pudo actualizar el perfil. Verifica los datos e inténtalo de nuevo.",
      });
      toast({
        title: "Error",
        description: "No se pudo actualizar el perfil. Inténtalo de nuevo más tarde.",
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  // Cambiar contraseña
  const handleChangePassword = async () => {
    // Validar que las contraseñas coincidan
    if (passwordData.new_password !== passwordData.confirm_password) {
      setErrors({
        ...errors,
        password: "Las contraseñas nuevas no coinciden.",
      });
      return;
    }

    try {
      setIsSaving(true);
      setErrors({ ...errors, password: "" });

      console.log("Enviando solicitud de cambio de contraseña...");
      
      // Usar la URL correcta y asegurarse de que los datos se envían en el formato correcto
      const response = await axios.post("/api/v1/auth/change-password", {
        current_password: passwordData.current_password,
        new_password: passwordData.new_password,
      });

      console.log("Respuesta del servidor:", response.data);

      // Limpiar campos de contraseña
      setPasswordData({
        current_password: "",
        new_password: "",
        confirm_password: "",
      });

      toast({
        title: "Contraseña actualizada",
        description: "Tu contraseña se ha actualizado correctamente.",
      });
    } catch (error) {
      console.error("Error al cambiar contraseña:", error);
      
      // Mostrar mensaje de error más específico si es posible
      const errorMessage = error.response?.data?.detail || 
                          "No se pudo cambiar la contraseña. Verifica que la contraseña actual sea correcta.";
      
      setErrors({
        ...errors,
        password: errorMessage,
      });
      
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  // Guardar configuración
  const handleSaveConfig = async () => {
    try {
      setIsSaving(true);
      setErrors({ ...errors, config: "" });

      await axios.put("/api/v1/config/", configData);

      toast({
        title: "Configuración guardada",
        description: "Tu configuración se ha actualizado correctamente.",
      });
    } catch (error) {
      console.error("Error al guardar configuración:", error);
      setErrors({
        ...errors,
        config: "No se pudo guardar la configuración. Inténtalo de nuevo más tarde.",
      });
      toast({
        title: "Error",
        description: "No se pudo guardar la configuración. Inténtalo de nuevo más tarde.",
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Configuración de la cuenta</h1>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="mb-6">
            <TabsTrigger value="profile" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              Perfil
            </TabsTrigger>
            <TabsTrigger value="security" className="flex items-center gap-2">
              <Lock className="h-4 w-4" />
              Seguridad
            </TabsTrigger>
            <TabsTrigger value="preferences" className="flex items-center gap-2">
              <Palette className="h-4 w-4" />
              Preferencias
            </TabsTrigger>
          </TabsList>

          {/* Pestaña de Perfil */}
          <TabsContent value="profile">
            <Card>
              <CardHeader>
                <CardTitle>Información de perfil</CardTitle>
                <CardDescription>
                  Actualiza tu información personal y de contacto.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {errors.profile && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>{errors.profile}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <Label htmlFor="email">Correo electrónico</Label>
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-gray-500" />
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      placeholder="tu@email.com"
                      value={userData.email}
                      onChange={handleProfileChange}
                    />
                  </div>
                  <p className="text-sm text-gray-500">
                    Este correo se utilizará para iniciar sesión y enviar presupuestos a tus clientes.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="first_name">Nombre</Label>
                    <Input
                      id="first_name"
                      name="first_name"
                      placeholder="Tu nombre"
                      value={userData.first_name}
                      onChange={handleProfileChange}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="last_name">Apellidos</Label>
                    <Input
                      id="last_name"
                      name="last_name"
                      placeholder="Tus apellidos"
                      value={userData.last_name}
                      onChange={handleProfileChange}
                    />
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button onClick={handleSaveProfile} disabled={isLoading || isSaving}>
                  {isSaving ? "Guardando..." : "Guardar cambios"}
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>

          {/* Pestaña de Seguridad */}
          <TabsContent value="security">
            <Card>
              <CardHeader>
                <CardTitle>Cambiar contraseña</CardTitle>
                <CardDescription>
                  Actualiza tu contraseña para mantener tu cuenta segura.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {errors.password && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>{errors.password}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <Label htmlFor="current_password">Contraseña actual</Label>
                  <Input
                    id="current_password"
                    name="current_password"
                    type="password"
                    value={passwordData.current_password}
                    onChange={handlePasswordChange}
                  />
                </div>

                <Separator />

                <div className="space-y-2">
                  <Label htmlFor="new_password">Nueva contraseña</Label>
                  <Input
                    id="new_password"
                    name="new_password"
                    type="password"
                    value={passwordData.new_password}
                    onChange={handlePasswordChange}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirm_password">Confirmar nueva contraseña</Label>
                  <Input
                    id="confirm_password"
                    name="confirm_password"
                    type="password"
                    value={passwordData.confirm_password}
                    onChange={handlePasswordChange}
                  />
                </div>
              </CardContent>
              <CardFooter>
                <Button onClick={handleChangePassword} disabled={isLoading || isSaving}>
                  {isSaving ? "Actualizando..." : "Cambiar contraseña"}
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>

          {/* Pestaña de Preferencias */}
          <TabsContent value="preferences">
            <Card>
              <CardHeader>
                <CardTitle>Preferencias de usuario</CardTitle>
                <CardDescription>
                  Personaliza tu experiencia en PresupuestoPro.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {errors.config && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>{errors.config}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-4">
                  <h3 className="text-lg font-medium flex items-center gap-2">
                    <Bell className="h-4 w-4" />
                    Notificaciones
                  </h3>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="notification_email">Notificaciones por email</Label>
                      <p className="text-sm text-gray-500">
                        Recibe actualizaciones sobre tus presupuestos por correo electrónico.
                      </p>
                    </div>
                    <Switch
                      id="notification_email"
                      checked={configData.notification_email}
                      onCheckedChange={(checked) => handleConfigChange("notification_email", checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="notification_sms">Notificaciones por SMS</Label>
                      <p className="text-sm text-gray-500">
                        Recibe actualizaciones sobre tus presupuestos por SMS.
                      </p>
                    </div>
                    <Switch
                      id="notification_sms"
                      checked={configData.notification_sms}
                      onCheckedChange={(checked) => handleConfigChange("notification_sms", checked)}
                    />
                  </div>
                </div>

                <Separator />

                <div className="space-y-4">
                  <h3 className="text-lg font-medium flex items-center gap-2">
                    <Globe className="h-4 w-4" />
                    Localización
                  </h3>
                  <div className="space-y-2">
                    <Label htmlFor="language">Idioma</Label>
                    <Select
                      value={configData.language}
                      onValueChange={(value) => handleConfigChange("language", value)}
                    >
                      <SelectTrigger id="language">
                        <SelectValue placeholder="Selecciona un idioma" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="es">Español</SelectItem>
                        <SelectItem value="en">English</SelectItem>
                        <SelectItem value="fr">Français</SelectItem>
                        <SelectItem value="de">Deutsch</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="currency">Moneda</Label>
                    <Select
                      value={configData.currency}
                      onValueChange={(value) => handleConfigChange("currency", value)}
                    >
                      <SelectTrigger id="currency">
                        <SelectValue placeholder="Selecciona una moneda" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="EUR">Euro (€)</SelectItem>
                        <SelectItem value="USD">Dólar estadounidense ($)</SelectItem>
                        <SelectItem value="GBP">Libra esterlina (£)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <Separator />

                <div className="space-y-4">
                  <h3 className="text-lg font-medium flex items-center gap-2">
                    <Palette className="h-4 w-4" />
                    Apariencia
                  </h3>
                  <div className="space-y-2">
                    <Label htmlFor="theme">Tema</Label>
                    <Select
                      value={configData.theme}
                      onValueChange={(value) => handleConfigChange("theme", value)}
                    >
                      <SelectTrigger id="theme">
                        <SelectValue placeholder="Selecciona un tema" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="light">Claro</SelectItem>
                        <SelectItem value="dark">Oscuro</SelectItem>
                        <SelectItem value="system">Sistema</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button onClick={handleSaveConfig} disabled={isLoading || isSaving}>
                  {isSaving ? "Guardando..." : "Guardar preferencias"}
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </Layout>
  );
};

export default Settings;
