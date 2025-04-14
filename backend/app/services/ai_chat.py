from typing import List, Dict, Any, Optional
import json
import os
import re

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
        
        # Mapeo de secciones del documento para referencias
        self.document_sections = {
            "coste": "4. COSTE",
            "costes": "4. COSTE",
            "plazo": "3. PLANIFICACIÓN",
            "plazos": "3. PLANIFICACIÓN",
            "planificación": "3. PLANIFICACIÓN",
            "tecnologías": "2. DESCRIPCIÓN DEL PROYECTO",
            "descripción": "2. DESCRIPCIÓN DEL PROYECTO",
            "funcionalidades": "2.1 FUNCIONALIDADES PRINCIPALES",
            "objeto": "1. OBJETO",
            "firmas": "5. FIRMAS",
        }
        
    def get_response(self, project: Any, query: str) -> Dict[str, Any]:
        """
        Genera una respuesta de IA basada en el proyecto y la consulta del usuario
        """
        # Normalizar la consulta
        query_lower = query.lower()
        
        # Detectar si es una petición de modificación
        is_modification_request = self._is_modification_request(query_lower)
        
        # Determinar el tipo de consulta
        query_type = "general"
        
        # Palabras clave ampliadas para cada tipo de consulta
        query_keywords = {
            "costes": ["coste", "costo", "precio", "valor", "cuánto cuesta", "cuánto vale", "presupuesto", "euros", "€"],
            "plazos": ["plazo", "tiempo", "duración", "cuándo", "cuánto tiempo", "semanas", "meses", "días", "tardaría", "tardará", "calendario", "cronograma", "planificación"],
            "tecnologías": ["tecnología", "tecnologías", "herramientas", "lenguajes", "frameworks", "stack", "programación", "desarrollo"],
            "equipo": ["equipo", "personas", "desarrolladores", "programadores", "diseñadores", "recursos humanos", "personal"],
            "riesgos": ["riesgo", "problema", "dificultad", "obstáculo", "complicación", "desafío", "retos"],
            "alternativas": ["alternativa", "opción", "otra forma", "diferente", "más barato", "más rápido", "económico", "reducir"]
        }
        
        # Detectar el tipo de consulta basado en palabras clave ampliadas
        for key, keywords in query_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                query_type = key
                break
                
        # Si no se detectó ningún tipo específico, verificar con las palabras clave originales
        if query_type == "general":
            for key in self.project_prompts:
                if key in query_lower:
                    query_type = key
                    break
        
        # Detectar si se refiere a una sección específica del documento
        document_reference = self._get_document_reference(query_lower)
        
        # Generar respuesta según el tipo de consulta
        if is_modification_request:
            response = self._generate_modification_response(project, query)
        elif query_type == "costes":
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
        
        # Añadir la referencia al documento si existe
        if document_reference and not is_modification_request:
            response += f"\n\n{document_reference}"
            
        return {
            "response": response,
            "query_type": query_type,
            "project_id": project.id,
            "project_name": project.name,
            "is_modification_request": is_modification_request,
            "document_reference": document_reference
        }
    
    def _is_modification_request(self, query: str) -> bool:
        """Detecta si la consulta es una petición de modificación del documento"""
        modification_keywords = [
            "cambia", "modifica", "actualiza", "edita", "ajusta", 
            "sustituye", "reemplaza", "añade", "agrega", "quita", "elimina"
        ]
        
        return any(keyword in query for keyword in modification_keywords)
    
    def _get_document_reference(self, query: str) -> Optional[str]:
        """Obtiene referencia a la sección del documento relacionada con la consulta"""
        for key, section in self.document_sections.items():
            if key in query:
                return f"Puedes encontrar más información en la sección '{section}' del documento que estás visualizando."
        
        return None
    
    def _generate_modification_response(self, project: Any, query: str) -> str:
        """Genera respuesta para peticiones de modificación"""
        # Detectar la sección que se quiere modificar
        section_to_modify = None
        for key, section in self.document_sections.items():
            if key in query.lower():
                section_to_modify = section
                break
        
        if section_to_modify:
            return f"""
Entiendo que deseas modificar la sección '{section_to_modify}' del documento.

Para realizar cambios en el documento, puedes:

1. Hacer clic en el botón "Editar documento" que aparecerá a continuación
2. Modificar la sección según tus necesidades
3. Guardar los cambios para actualizar el PDF

Alternativamente, puedes indicarme exactamente qué cambios deseas realizar y podré asistirte en la generación del nuevo contenido.
"""
        else:
            return f"""
Entiendo que deseas realizar modificaciones en el documento.

Para ayudarte mejor, ¿podrías especificar qué sección del documento quieres modificar y qué cambios deseas realizar?

Las secciones disponibles son:
- 1. OBJETO
- 2. DESCRIPCIÓN DEL PROYECTO
- 2.1 FUNCIONALIDADES PRINCIPALES
- 3. PLANIFICACIÓN
- 4. COSTE
- 5. FIRMAS
"""
    
    def _generate_cost_response(self, project: Any) -> str:
        """Genera respuesta sobre costes"""
        if project.is_premium and project.full_data:
            # Si es premium, dar información detallada
            cost_details = []
            try:
                # Intentar extraer datos de costes del JSON
                full_data = project.full_data if isinstance(project.full_data, dict) else json.loads(project.full_data)
                
                if "hourly_rates" in full_data:
                    cost_details.append("Tarifas por hora:")
                    for role, rate in full_data["hourly_rates"].items():
                        cost_details.append(f"  - {role}: {rate}€/hora")
                
                if "phases" in full_data:
                    cost_details.append("\nDesglose por fases:")
                    for phase in full_data["phases"]:
                        cost_details.append(f"  - {phase.get('name', 'Fase')}: {phase.get('cost', 0)}€")
            except (json.JSONDecodeError, AttributeError):
                # Si hay error al procesar el JSON, usar enfoque simple
                for key, value in vars(project).items():
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