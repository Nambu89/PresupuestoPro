import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { 
  Menu, 
  X, 
  ChevronDown,
  LayoutDashboard,
  Settings,
  LogOut
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/components/ui/use-toast";

interface NavbarProps {
  isAuthenticated?: boolean;
}

const Navbar: React.FC<NavbarProps> = ({ isAuthenticated = false }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { toast } = useToast();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    // Eliminar el token de autenticación y cualquier otro dato de sesión
    localStorage.removeItem("token");
    sessionStorage.clear(); // Limpiar cualquier dato en sessionStorage
    
    // Forzar la actualización del estado de autenticación
    setIsMenuOpen(false);
    
    toast({
      title: "Sesión cerrada",
      description: "Has cerrado sesión correctamente",
      variant: "default",
    });
    
    // Redirigir al inicio con un pequeño retraso para asegurar que se limpie todo
    setTimeout(() => {
      navigate("/", { replace: true });
      // Forzar recarga de la página para asegurar que se reinicie todo el estado
      window.location.reload();
    }, 100);
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-background shadow-sm border-b border-border sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-blue to-primary-dark rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">PI</span>
            </div>
            <span className="text-lg font-bold">
              Presupuesto<span className="text-primary-blue">Pro</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {isAuthenticated ? (
              <>
                <Link 
                  to="/features" 
                  className={`text-sm font-medium ${isActive("/features") ? "text-primary-blue" : "text-gray-600 hover:text-gray-900"}`}
                  state={{ authenticated: true }}
                >
                  Características
                </Link>
                <Link 
                  to="/pricing" 
                  className={`text-sm font-medium ${isActive("/pricing") ? "text-primary-blue" : "text-gray-600 hover:text-gray-900"}`}
                  state={{ authenticated: true }}
                >
                  Precios
                </Link>
              </>
            ) : (
              <>
                <Link 
                  to="/features" 
                  className={`text-sm font-medium ${isActive("/features") ? "text-primary-blue" : "text-gray-600 hover:text-gray-900"}`}
                >
                  Características
                </Link>
                <Link 
                  to="/pricing" 
                  className={`text-sm font-medium ${isActive("/pricing") ? "text-primary-blue" : "text-gray-600 hover:text-gray-900"}`}
                >
                  Precios
                </Link>
              </>
            )}
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <Link to="/dashboard">
                  <Button variant="ghost" size="sm">
                    Dashboard
                  </Button>
                </Link>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm" className="flex items-center gap-1">
                      Mi cuenta <ChevronDown className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Mi cuenta</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={() => navigate("/dashboard")}>
                      <LayoutDashboard className="mr-2 h-4 w-4" />
                      <span>Dashboard</span>
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => navigate("/settings")}>
                      <Settings className="mr-2 h-4 w-4" />
                      <span>Configuración</span>
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={handleLogout}>
                      <LogOut className="mr-2 h-4 w-4" />
                      <span>Cerrar sesión</span>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login">
                  <Button variant="ghost" size="sm">
                    Iniciar sesión
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">Registrarse</Button>
                </Link>
              </div>
            )}
          </nav>

          {/* Mobile menu button */}
          <button
            className="md:hidden text-gray-600 hover:text-gray-900 focus:outline-none"
            onClick={toggleMenu}
          >
            {isMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 py-4 border-t border-gray-100">
            <nav className="flex flex-col space-y-4">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/features"
                    className={`text-sm font-medium ${isActive("/features") ? "text-primary-blue" : "text-gray-600"}`}
                    onClick={toggleMenu}
                    state={{ authenticated: true }}
                  >
                    Características
                  </Link>
                  <Link
                    to="/pricing"
                    className={`text-sm font-medium ${isActive("/pricing") ? "text-primary-blue" : "text-gray-600"}`}
                    onClick={toggleMenu}
                    state={{ authenticated: true }}
                  >
                    Precios
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    to="/features"
                    className={`text-sm font-medium ${isActive("/features") ? "text-primary-blue" : "text-gray-600"}`}
                    onClick={toggleMenu}
                  >
                    Características
                  </Link>
                  <Link
                    to="/pricing"
                    className={`text-sm font-medium ${isActive("/pricing") ? "text-primary-blue" : "text-gray-600"}`}
                    onClick={toggleMenu}
                  >
                    Precios
                  </Link>
                </>
              )}
              {isAuthenticated ? (
                <>
                  <Link
                    to="/dashboard"
                    className="text-sm font-medium text-gray-600"
                    onClick={toggleMenu}
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/settings"
                    className="text-sm font-medium text-gray-600"
                    onClick={toggleMenu}
                  >
                    Configuración
                  </Link>
                  <button
                    className="text-sm font-medium text-red-600 text-left"
                    onClick={() => {
                      handleLogout();
                      toggleMenu();
                    }}
                  >
                    Cerrar sesión
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="text-sm font-medium text-gray-600"
                    onClick={toggleMenu}
                  >
                    Iniciar sesión
                  </Link>
                  <Link to="/register" onClick={toggleMenu}>
                    <Button size="sm" className="w-full">
                      Registrarse
                    </Button>
                  </Link>
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;
