
import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Features from "@/components/Features";
import CTA from "@/components/CTA";

const FeaturesPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <div className="container mx-auto px-4 py-16">
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">Nuestras Características</h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Descubre las herramientas avanzadas que PresupuestoPro ofrece para
              que puedas crear presupuestos precisos y profesionales.
            </p>
          </div>
        </div>
        <Features />
        <CTA />
      </main>
      <Footer />
    </div>
  );
};

export default FeaturesPage;
