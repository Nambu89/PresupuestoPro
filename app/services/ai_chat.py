from typing import List, Dict, Any, Optional
import json
import os

class AIChat:
    """
    Servicio para gestionar conversaciones con IA sobre presupuestos
    """
    def __init__(self):
        # Aquí se podría inicializar una conexión con un servicio de IA como OpenAI
        # Por ahora, simularemos respuestas para demostración
        self.project_prompts = {
            "costes": "Te proporcionaré información detallada sobre los costes del proyecto, incluyendo desglose por categorías y justificación de cada partida.",
            "plazos": "Te explicaré los plazos estimados para cada fase del proyecto y cómo se ha calculado la duración total.",
            "tecnologías": "Te detallaré las tecnologías recomendadas para este proyecto y por qué son las más adecuadas.",
            "equipo": "Te proporcionaré información sobre el equipo necesario para desarrollar este proyecto.",
            "riesgos": "Te explicaré los posibles riesgos del proyecto y cómo mitigarlos.",
            "alternativas": "Te presentaré alternativas más económicas o más rápidas para este proyecto.",
        }
        
    def get_response(self, project: Any, query: str) -> Dict[str, Any]:
        """
        Genera una respuesta de IA basada en el proyecto y la consulta del usuario
        """
        # Normalizar la consulta
        query_lower = query.lower()
        
        # Determinar el tipo de consulta
        query_type = "general"
        for key in self.project_prompts:
            if key in query_lower:
                query_type = key
                break
        
        # Generar respuesta según el tipo de consulta
        if query_type == "costes":
            response = self._generate_cost_response(project)
        elif query_type == "plazos":
            response = self._generate_timeline_response(project)
        elif query_type == "tecnologías":
            response = self._generate_tech_response(project)
        elif query_type == "equipo":
            response = self._generate_team_response(project)
        elif query_type == "riesgos":
            response = self._generate_risk_response(project)
        elif query_type == "alternativas":
            response = self._generate_alternatives_response(project)
        else:
            response = self._generate_general_response(project, query)
            
        return {
            "response": response,
            "query_type": query_type,
            "project_id": project.id,
            "project_name": project.name
        }
    
    def _generate_cost_response(self, project: Any) -> str:
        """Genera respuesta sobre costes"""
        if project.is_premium and project.full_data:
            # Si es premium, dar información detallada
            cost_details = []
            for key, value in project.full_data.items():
                if isinstance(value, (int, float)) and key.endswith("_cost"):
                    cost_details.append(f"- {key.replace('_', ' ').title()}: {value}€")
            
            cost_breakdown = "\n".join(cost_details) if cost_details else "No hay desglose detallado disponible."
            
            return f"""
            El coste total estimado para el proyecto '{project.name}' es de {project.estimated_cost}€.
            
            Desglose de costes:
            {cost_breakdown}
            
            Este presupuesto incluye todos los recursos necesarios para completar el proyecto según las especificaciones proporcionadas.
            """
        else:
            # Si no es premium, dar información básica
            return f"""
            El coste total estimado para el proyecto '{project.name}' es de {project.estimated_cost}€.
            
            Para obtener un desglose detallado de los costes, te recomiendo actualizar a la versión premium del presupuesto.
            """
    
    def _generate_timeline_response(self, project: Any) -> str:
        """Genera respuesta sobre plazos"""
        return f"""
        La duración estimada para completar el proyecto '{project.name}' es de {project.estimated_duration_weeks} semanas.
        
        Este plazo incluye las siguientes fases:
        - Análisis y planificación: {max(1, int(project.estimated_duration_weeks * 0.2))} semanas
        - Desarrollo: {max(2, int(project.estimated_duration_weeks * 0.5))} semanas
        - Pruebas y correcciones: {max(1, int(project.estimated_duration_weeks * 0.2))} semanas
        - Implementación final: {max(1, int(project.estimated_duration_weeks * 0.1))} semanas
        
        El cronograma puede ajustarse según tus necesidades específicas.
        """
    
    def _generate_tech_response(self, project: Any) -> str:
        """Genera respuesta sobre tecnologías"""
        return f"""
        Para el proyecto '{project.name}', recomendaría las siguientes tecnologías:
        
        - Frontend: React con TypeScript para una interfaz de usuario moderna y mantenible
        - Backend: FastAPI (Python) para un desarrollo rápido y eficiente
        - Base de datos: PostgreSQL para almacenamiento seguro y escalable
        - Infraestructura: Despliegue en la nube con Docker y Kubernetes
        
        Estas tecnologías ofrecen el mejor equilibrio entre rendimiento, escalabilidad y facilidad de mantenimiento para este tipo de proyecto.
        """
    
    def _generate_team_response(self, project: Any) -> str:
        """Genera respuesta sobre equipo necesario"""
        return f"""
        Para completar el proyecto '{project.name}' en el plazo estimado de {project.estimated_duration_weeks} semanas, recomendaría el siguiente equipo:
        
        - 1 Jefe de Proyecto
        - 2 Desarrolladores Frontend
        - 2 Desarrolladores Backend
        - 1 Diseñador UX/UI
        - 1 QA Tester
        
        Este equipo tiene la experiencia y habilidades necesarias para entregar un producto de alta calidad dentro del plazo establecido.
        """
    
    def _generate_risk_response(self, project: Any) -> str:
        """Genera respuesta sobre riesgos"""
        return f"""
        Los principales riesgos identificados para el proyecto '{project.name}' son:
        
        1. Cambios en los requisitos durante el desarrollo
           - Mitigación: Definir claramente el alcance al inicio y establecer un proceso para gestionar cambios
        
        2. Retrasos en la entrega
           - Mitigación: Incluir un margen de seguridad en la planificación y realizar seguimiento semanal
        
        3. Problemas técnicos inesperados
           - Mitigación: Realizar un análisis técnico detallado al inicio y tener un plan de contingencia
        
        4. Disponibilidad de recursos
           - Mitigación: Confirmar la disponibilidad del equipo antes de comenzar y tener recursos de respaldo
        
        Con una gestión adecuada, estos riesgos pueden minimizarse significativamente.
        """
    
    def _generate_alternatives_response(self, project: Any) -> str:
        """Genera respuesta sobre alternativas"""
        cheaper_cost = int(project.estimated_cost * 0.7)
        faster_weeks = max(2, int(project.estimated_duration_weeks * 0.7))
        
        return f"""
        Para el proyecto '{project.name}', puedo ofrecerte las siguientes alternativas:
        
        Opción más económica ({cheaper_cost}€):
        - Reducir el alcance a las funcionalidades esenciales
        - Utilizar plantillas prediseñadas en lugar de diseños personalizados
        - Implementar en fases, priorizando las características más importantes
        
        Opción más rápida ({faster_weeks} semanas):
        - Aumentar el tamaño del equipo de desarrollo
        - Utilizar componentes y bibliotecas existentes
        - Simplificar algunas funcionalidades complejas
        
        Cada alternativa implica ciertos compromisos, pero podemos adaptarnos a tus prioridades específicas.
        """
    
    def _generate_general_response(self, project: Any, query: str) -> str:
        """Genera respuesta general basada en la consulta"""
        return f"""
        Respecto a tu consulta sobre el proyecto '{project.name}':
        
        Este proyecto tiene un coste estimado de {project.estimated_cost}€ y una duración estimada de {project.estimated_duration_weeks} semanas.
        
        Para obtener información más específica, puedes preguntar sobre:
        - Costes detallados del proyecto
        - Plazos y cronograma
        - Tecnologías recomendadas
        - Equipo necesario
        - Riesgos potenciales
        - Alternativas más económicas o más rápidas
        
        ¿En qué aspecto concreto estás más interesado?
        """
