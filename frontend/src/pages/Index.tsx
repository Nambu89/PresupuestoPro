import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import Layout from "@/components/layout/Layout";
import { ArrowRight, CheckCircle, BarChart, FileText, Zap, Users, Brain, Bot, PieChart, Sparkles } from "lucide-react";

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
          
          {/* Tarjeta flotante con presupuesto de ejemplo */}
          <div className="relative mt-16 mb-16">
            <div className="max-w-md mx-auto px-4 sm:px-0">
              <div className="bg-white rounded-xl shadow-xl border border-gray-100 p-6 relative overflow-hidden transform transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-bold">Aplicación Web E-commerce</h3>
                    <p className="text-sm text-gray-500">Presupuesto #12345</p>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-primary-blue">43.000€</div>
                    <p className="text-sm text-gray-500">Total estimado</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-xs text-gray-500">Duración</p>
                    <p className="text-sm font-medium">3 meses</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Equipo</p>
                    <p className="text-sm font-medium">5 personas</p>
                  </div>
                </div>
                <div className="bg-blue-50 rounded-lg p-3">
                  <div className="flex justify-between text-sm mb-1">
                    <span>Desarrollo Frontend</span>
                    <span className="font-medium">16.000€</span>
                  </div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Desarrollo Backend</span>
                    <span className="font-medium">14.500€</span>
                  </div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Diseño UX/UI</span>
                    <span className="font-medium">7.200€</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Pruebas y Despliegue</span>
                    <span className="font-medium">5.300€</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Stats */}
          <div className="mt-16 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 md:gap-8">
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
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-8">
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-lg shadow-md border border-blue-100 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Brain className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-blue-800">Estimación con IA</h3>
              <p className="text-gray-700">
                Nuestra IA analiza tus requisitos y genera estimaciones precisas basadas en datos de proyectos similares.
              </p>
              <div className="mt-4 pt-4 border-t border-blue-100">
                <div className="flex items-center text-sm text-blue-600">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Precisión del 98%</span>
                </div>
                <div className="flex items-center text-sm text-blue-600 mt-1">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Actualización automática</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-lg shadow-md border border-blue-100 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-blue-800">Plantillas profesionales</h3>
              <p className="text-gray-700">
                Elige entre múltiples plantillas diseñadas para diferentes tipos de proyectos y personalízalas a tu gusto.
              </p>
              <div className="mt-4 pt-4 border-t border-blue-100">
                <div className="flex items-center text-sm text-blue-600">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>+20 plantillas disponibles</span>
                </div>
                <div className="flex items-center text-sm text-blue-600 mt-1">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Personalización completa</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-lg shadow-md border border-blue-100 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <PieChart className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-blue-800">Análisis de costes</h3>
              <p className="text-gray-700">
                Visualiza el desglose de costes y optimiza tus presupuestos para maximizar la rentabilidad.
              </p>
              <div className="mt-4 pt-4 border-t border-blue-100">
                <div className="flex items-center text-sm text-blue-600">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Gráficos interactivos</span>
                </div>
                <div className="flex items-center text-sm text-blue-600 mt-1">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Comparativas automáticas</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-lg shadow-md border border-blue-100 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Bot className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-blue-800">Asistente IA Personalizado</h3>
              <p className="text-gray-700">
                Nuestro asistente de IA te ayuda a generar descripciones detalladas de tareas y estimar tiempos con precisión.
              </p>
              <div className="mt-4 pt-4 border-t border-blue-100">
                <div className="flex items-center text-sm text-blue-600">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Sugerencias inteligentes</span>
                </div>
                <div className="flex items-center text-sm text-blue-600 mt-1">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Adaptación a tu industria</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-lg shadow-md border border-blue-100 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Sparkles className="h-6 w-6 text-primary-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-blue-800">Exportación avanzada</h3>
              <p className="text-gray-700">
                Exporta tus presupuestos en múltiples formatos: PDF, Excel, o compártelos directamente por email.
              </p>
              <div className="mt-4 pt-4 border-t border-blue-100">
                <div className="flex items-center text-sm text-blue-600">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>PDF profesional</span>
                </div>
                <div className="flex items-center text-sm text-blue-600 mt-1">
                  <CheckCircle className="h-4 w-4 mr-2" />
                  <span>Envío directo a clientes</span>
                </div>
              </div>
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
