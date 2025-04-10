
import React from 'react';
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

const Pricing = () => {
  const plans = [
    {
      name: "Free",
      price: "0€",
      description: "Para explorar la plataforma",
      features: [
        "Creación de presupuestos con IA",
        "Estimación de costes",
        "Almacenamiento de 5 presupuestos",
        "Acceso móvil y desktop",
      ],
      buttonText: "Comenzar gratis",
      popular: false,
      buttonVariant: "outline" as const,
    },
    {
      name: "Premium",
      price: "5€",
      description: "Desbloquea todas las funciones",
      features: [
        "Todo lo del plan Free",
        "Informes completos y detallados",
        "Exportación a PDF",
        "Envío por email",
        "Personalización del informe",
        "Chat con IA para consultas",
        "Almacenamiento ilimitado",
        "Soporte prioritario"
      ],
      buttonText: "Obtener Premium",
      popular: true,
      buttonVariant: "default" as const,
    }
  ];

  return (
    <section className="py-16" id="pricing">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Precios Simples y Transparentes</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Elige el plan que mejor se adapte a tus necesidades. ¡Solo pagas por lo que realmente necesitas!
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan) => (
            <div 
              key={plan.name} 
              className={`rounded-2xl p-8 bg-white border ${
                plan.popular ? 'border-primary-blue shadow-lg' : 'border-gray-200'
              }`}
            >
              {plan.popular && (
                <div className="mb-4">
                  <span className="bg-blue-100 text-primary-blue text-sm font-medium py-1 px-3 rounded-full">
                    Más popular
                  </span>
                </div>
              )}
              <h3 className="text-2xl font-bold">{plan.name}</h3>
              <div className="mt-4 mb-6">
                <span className="text-4xl font-bold">{plan.price}</span>
                {plan.name === "Premium" && <span className="text-gray-500 ml-2">por informe</span>}
              </div>
              <p className="text-gray-600 mb-6">{plan.description}</p>
              <Button 
                variant={plan.buttonVariant} 
                className="w-full mb-8"
              >
                {plan.buttonText}
              </Button>
              <ul className="space-y-3">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-start">
                    <Check className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Pricing;
