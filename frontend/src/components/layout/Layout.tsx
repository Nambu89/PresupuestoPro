import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";

interface LayoutProps {
  children: React.ReactNode;
  hideFooter?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, hideFooter = false }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const location = useLocation();

  useEffect(() => {
    // Comprobar si el usuario está autenticado
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token);

    // Aplicar el tema guardado
    const savedTheme = localStorage.getItem("presupuestopro-ui-theme") || "light";
    const root = window.document.documentElement;
    root.classList.remove("light", "dark", "system");
    root.classList.add(savedTheme);
  }, [location]); // Actualizar cuando cambie la ruta

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar isAuthenticated={isAuthenticated} />
      <main className="flex-grow">{children}</main>
      {!hideFooter && <Footer />}
    </div>
  );
};

export default Layout;
