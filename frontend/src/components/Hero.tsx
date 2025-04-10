
import React from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { FileText, Zap, Lock } from "lucide-react";

const Hero = () => {
  return (
    <section className="container mx-auto px-4 py-16 md:py-24">
      <div className="flex flex-col md:flex-row items-center">
        <div className="md:w-1/2 mb-10 md:mb-0">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 tracking-tight">
            Presupuestos de software{" "}
            <span className="gradient-text">impulsados por IA</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 mb-8">
            Genera presupuestos profesionales para tus proyectos de software en minutos.
            Preciso, completo y personalizado para tus necesidades específicas.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <Link to="/register">
              <Button size="lg" className="w-full sm:w-auto">
                Comenzar gratis
              </Button>
            </Link>
            <Link to="/features">
              <Button size="lg" variant="outline" className="w-full sm:w-auto">
                Ver características
              </Button>
            </Link>
          </div>
        </div>
        <div className="md:w-1/2 md:pl-10">
          <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 animate-float">
            <div className="mb-4 flex justify-between items-center">
              <h3 className="text-lg font-medium">Presupuesto: App de Gestión</h3>
              <span className="text-secondary-green font-semibold">Vista previa</span>
            </div>
            <div className="space-y-4 mb-4">
              <div className="flex items-center">
                <FileText className="h-5 w-5 text-primary-blue mr-2" />
                <span className="text-gray-700">Coste estimado: 12.500 €</span>
              </div>
              <div className="flex items-center">
                <Zap className="h-5 w-5 text-primary-blue mr-2" />
                <span className="text-gray-700">Duración: 12 semanas</span>
              </div>
              <div className="flex items-center">
                <Lock className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-gray-400">Desglose detallado (Bloqueado)</span>
              </div>
            </div>
            <Button className="w-full">Desbloquear informe completo</Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
