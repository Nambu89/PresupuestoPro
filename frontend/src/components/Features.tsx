
import React from 'react';
import { 
  AlignLeft, 
  Download, 
  Mail, 
  MessageCircle, 
  Zap, 
  Lock, 
  FileText
} from 'lucide-react';

const Features = () => {
  const featuresList = [
    {
      icon: <FileText className="h-8 w-8 text-primary-blue" />,
      title: "Presupuestos IA",
      description: "Nuestra IA analiza tu proyecto para generar un presupuesto detallado y preciso.",
      free: true
    },
    {
      icon: <Zap className="h-8 w-8 text-primary-blue" />,
      title: "Resultados Instantáneos",
      description: "Obtén el coste estimado de tu proyecto en segundos.",
      free: true
    },
    {
      icon: <AlignLeft className="h-8 w-8 text-secondary-yellow" />,
      title: "Informe Detallado",
      description: "Accede al desglose completo de tu presupuesto con análisis de costos y plazos.",
      free: false
    },
    {
      icon: <Download className="h-8 w-8 text-secondary-yellow" />,
      title: "Exportar a PDF",
      description: "Descarga tus presupuestos en formato PDF listos para compartir.",
      free: false
    },
    {
      icon: <Mail className="h-8 w-8 text-secondary-yellow" />,
      title: "Envío por Email",
      description: "Envía el presupuesto directamente a tus clientes desde la plataforma.",
      free: false
    },
    {
      icon: <MessageCircle className="h-8 w-8 text-secondary-yellow" />,
      title: "Chat con IA",
      description: "Resuelve dudas y obtén recomendaciones adicionales para tu proyecto.",
      free: false
    },
  ];

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Características Principales</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Descubre las herramientas que tenemos para ayudarte a crear presupuestos profesionales
            con precisión y facilidad.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuresList.map((feature, index) => (
            <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="flex items-center mb-4">
                {feature.icon}
                {feature.free ? (
                  <span className="ml-auto bg-green-100 text-green-800 text-xs font-medium py-1 px-2 rounded">
                    Free
                  </span>
                ) : (
                  <span className="ml-auto flex items-center text-xs font-medium text-gray-500">
                    <Lock className="h-3 w-3 mr-1" /> Premium
                  </span>
                )}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
