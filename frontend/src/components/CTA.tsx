
import React from 'react';
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const CTA = () => {
  return (
    <section className="py-20 gradient-bg">
      <div className="container mx-auto px-4 text-center text-white">
        <h2 className="text-3xl md:text-4xl font-bold mb-6">
          ¿Listo para crear presupuestos profesionales?
        </h2>
        <p className="text-lg mb-8 max-w-2xl mx-auto opacity-90">
          Únete a cientos de profesionales que están transformando la forma en que crean
          presupuestos para sus proyectos de software.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link to="/register">
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-primary-dark">
              Comenzar gratis
            </Button>
          </Link>
          <Link to="/contact">
            <Button size="lg" className="bg-white text-primary-dark hover:bg-gray-100">
              Contactar con ventas
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default CTA;
