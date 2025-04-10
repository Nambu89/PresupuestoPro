
import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Pricing from "@/components/Pricing";
import CTA from "@/components/CTA";

const PricingPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <div className="container mx-auto px-4 py-16">
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">Nuestros Planes</h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Opciones flexibles para adaptarse a tus necesidades,
              sin sorpresas ni costes ocultos.
            </p>
          </div>
        </div>
        <Pricing />
        <CTA />
      </main>
      <Footer />
    </div>
  );
};

export default PricingPage;
