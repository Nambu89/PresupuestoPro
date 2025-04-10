import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import Layout from "@/components/layout/Layout";
import { ArrowRight, CheckCircle, BarChart, FileText, Zap, Users } from "lucide-react";

const Index = () => {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-gray-50 to-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
            Crea presupuestos profesionales <br className="hidden md:block" />
            <span className="text-primary-blue">con inteligencia artificial</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
            Genera presupuestos detallados para tus proyectos en minutos, no en horas. 
            Nuestra IA analiza tus requisitos y crea estimaciones precisas.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link to="/register">
              <Button size="lg" className="w-full sm:w-auto">Comenzar gratis</Button>
            </Link>
            <Link to="/features">
              <Button variant="outline" size="lg" className="w-full sm:w-auto">Ver características</Button>
            </Link>
          </div>
          
          {/* Hero Image */}
          <div className="mt-16 max-w-5xl mx-auto rounded-lg shadow-xl overflow-hidden">
            <img 
              src="/images/dashboard-preview.png" 
              alt="PresupuestoPro Dashboard" 
              className="w-full h-auto"
              onError={(e) => {
                // Fallback si la imagen no existe
                e.currentTarget.src = "https://placehold.co/1200x600/e6f7ff/0099ff?text=PresupuestoPro+Dashboard";
              }}
            />
          </div>
          
          {/* Stats */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
              <div className="text-3xl font-bold text-primary-blue mb-2">+500</div>
              <div className="text-gray-600">Presupuestos generados</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
              <div className="text-3xl font-bold text-primary-blue mb-2">98%</div>
              <div className="text-gray-600">Precisión en estimaciones</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
              <div className="text-3xl font-bold text-primary-blue mb-2">4.9/5</div>
              <div className="text-gray-600">Valoración de usuarios</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Todo lo que necesitas para presupuestar</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              PresupuestoPro combina la potencia de la IA con herramientas profesionales para crear presupuestos detallados y precisos.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Estimación con IA</h3>
              <p className="text-gray-600">
                Nuestra IA analiza tus requisitos y genera estimaciones precisas basadas en datos de proyectos similares.
              </p>
            </div>
            
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Plantillas profesionales</h3>
              <p className="text-gray-600">
                Elige entre múltiples plantillas diseñadas para diferentes tipos de proyectos y personalízalas a tu gusto.
              </p>
            </div>
            
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <BarChart className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Análisis de costes</h3>
              <p className="text-gray-600">
                Visualiza el desglose de costes y optimiza tus presupuestos para maximizar la rentabilidad.
              </p>
            </div>
            
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Users className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Colaboración en equipo</h3>
              <p className="text-gray-600">
                Trabaja con tu equipo en tiempo real, comparte presupuestos y recibe feedback instantáneo.
              </p>
            </div>
            
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <CheckCircle className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Exportación avanzada</h3>
              <p className="text-gray-600">
                Exporta tus presupuestos en múltiples formatos: PDF, Excel, o compártelos directamente por email.
              </p>
            </div>
            
            <div className="bg-gray-50 p-6 rounded-lg">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <ArrowRight className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Y mucho más</h3>
              <p className="text-gray-600">
                Descubre todas las funcionalidades que PresupuestoPro tiene para ofrecer a tu negocio.
              </p>
              <Link to="/features" className="text-primary-blue font-medium mt-2 inline-block hover:underline">
                Ver todas las características
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-blue text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">Comienza a crear presupuestos profesionales hoy</h2>
          <p className="text-xl mb-10 max-w-3xl mx-auto opacity-90">
            Únete a cientos de profesionales que ya confían en PresupuestoPro para sus proyectos.
          </p>
          <Link to="/register">
            <Button size="lg" variant="secondary" className="bg-white text-primary-blue hover:bg-gray-100">
              Registrarse gratis
            </Button>
          </Link>
        </div>
      </section>
    </Layout>
  );
};

export default Index;
