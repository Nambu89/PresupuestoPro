
import React from 'react';
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { MenuIcon, X } from "lucide-react";

const Navbar = () => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100">
      <div className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-blue to-primary-dark rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">PI</span>
            </div>
            <Link to="/" className="text-xl font-bold text-primary-dark">
              Presupuesto<span className="text-primary-blue">Pro</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-600 hover:text-primary-blue transition-colors">
              Inicio
            </Link>
            <Link to="/features" className="text-gray-600 hover:text-primary-blue transition-colors">
              Características
            </Link>
            <Link to="/pricing" className="text-gray-600 hover:text-primary-blue transition-colors">
              Precios
            </Link>
            <Link to="/login">
              <Button variant="outline" className="mr-2">Iniciar Sesión</Button>
            </Link>
            <Link to="/register">
              <Button>Registrarse</Button>
            </Link>
          </div>

          <div className="md:hidden">
            <button 
              onClick={() => setIsOpen(!isOpen)} 
              className="text-gray-700 focus:outline-none"
            >
              {isOpen ? <X /> : <MenuIcon />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div className="md:hidden mt-4 pb-4 space-y-3">
            <Link to="/" className="block text-gray-600 hover:text-primary-blue transition-colors py-2">
              Inicio
            </Link>
            <Link to="/features" className="block text-gray-600 hover:text-primary-blue transition-colors py-2">
              Características
            </Link>
            <Link to="/pricing" className="block text-gray-600 hover:text-primary-blue transition-colors py-2">
              Precios
            </Link>
            <Link to="/login" className="block py-2">
              <Button variant="outline" className="w-full mb-2">Iniciar Sesión</Button>
            </Link>
            <Link to="/register" className="block py-2">
              <Button className="w-full">Registrarse</Button>
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
