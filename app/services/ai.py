from typing import Dict, Any, List, Tuple
import random
import json
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class AIProjectEstimator:
    """
    Estimador de presupuestos con IA que utiliza una API externa
    """
    
    def __init__(self):
        # Obtener la clave de API desde variables de entorno
        self.api_key = os.getenv("AI_API_KEY")
        self.api_url = os.getenv("AI_API_URL", "https://api.openai.com/v1/chat/completions")
        
        # Tarifas por defecto en caso de que la API falle
        self.hourly_rates = {
            "frontend": 50,
            "backend": 60,
            "design": 45,
            "project_management": 55,
            "qa": 40,
        }
    
    def generate_estimate(self, project_data: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Generar una estimación utilizando la API de IA externa
        
        Args:
            project_data: Descripción del proyecto, puede incluir nombre, cliente, tipo, etc.
            
        Returns:
            Tupla con (datos_preview, datos_completos)
        """
        try:
            if not self.api_key:
                print("API key no encontrada. Usando estimación simulada.")
                return self._generate_fallback_estimate(project_data)
                
            # Preparar los datos para la API
            prompt = self._prepare_prompt(project_data)
            
            # Llamar a la API
            response = self._call_ai_api(prompt)
            
            # Procesar la respuesta
            if response and 'choices' in response:
                # Extraer el contenido JSON de la respuesta
                try:
                    ai_response = response['choices'][0]['message']['content']
                    # Intentar extraer el JSON de la respuesta
                    json_start = ai_response.find('{')
                    json_end = ai_response.rfind('}')
                    
                    if json_start >= 0 and json_end > json_start:
                        json_str = ai_response[json_start:json_end+1]
                        budget_data = json.loads(json_str)
                        
                        # Asegurarse de que los datos tienen el formato esperado
                        preview_data, full_data = self._process_ai_response(budget_data)
                        return preview_data, full_data
                except Exception as e:
                    print(f"Error al procesar la respuesta de la IA: {e}")
            
            # Si algo falla, usar la estimación de respaldo
            return self._generate_fallback_estimate(project_data)
            
        except Exception as e:
            print(f"Error al generar estimación con IA: {e}")
            return self._generate_fallback_estimate(project_data)
        
    def _call_ai_api(self, prompt: str) -> Dict[str, Any]:
        """
        Realizar la llamada a la API de IA
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres un experto en estimación de presupuestos para proyectos de software. Tu tarea es analizar los requisitos del proyecto y generar un presupuesto detallado. Responde SOLO con el JSON del presupuesto, sin explicaciones adicionales ni preguntas."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            print(f"Enviando solicitud a la API de OpenAI: {self.api_url}")
            print(f"Modelo utilizado: {data['model']}")
            print(f"Headers: {headers}")
            
            response = requests.post(self.api_url, headers=headers, json=data)
            
            # Imprimir información sobre la respuesta
            print(f"Código de estado de la respuesta: {response.status_code}")
            print(f"Respuesta de la API: {response.text[:500]}..." if len(response.text) > 500 else f"Respuesta de la API: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al llamar a la API de IA: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Respuesta de error detallada: {e.response.text}")
            return None
    
    def _prepare_prompt(self, project_data: str) -> str:
        """
        Preparar el prompt para la API de IA
        
        Args:
            project_data: Descripción del proyecto
            
        Returns:
            Prompt formateado para la API
        """
        prompt = f"""
        Actúa como un experto en estimación de presupuestos para proyectos de software.
        Analiza los siguientes requisitos y genera un presupuesto detallado en formato JSON.
        
        DATOS DEL PROYECTO:
        {project_data}
        
        Genera un presupuesto con la siguiente estructura JSON:
        {{
            "project_name": "Nombre del proyecto",
            "total_cost": 0000, // Costo total estimado en euros
            "duration_weeks": 00, // Duración estimada en semanas
            "hourly_rates": {{
                "frontend": 00, // Tarifa por hora para desarrollo frontend
                "backend": 00, // Tarifa por hora para desarrollo backend
                "design": 00, // Tarifa por hora para diseño
                "project_management": 00, // Tarifa por hora para gestión de proyecto
                "qa": 00 // Tarifa por hora para testing y QA
            }},
            "hours_breakdown": {{
                "frontend": 00, // Horas estimadas de desarrollo frontend
                "backend": 00, // Horas estimadas de desarrollo backend
                "design": 00, // Horas estimadas de diseño
                "project_management": 00, // Horas estimadas de gestión de proyecto
                "qa": 00 // Horas estimadas de testing y QA
            }},
            "phases": [
                {{
                    "name": "Fase 1: Nombre de la fase",
                    "description": "Descripción breve de la fase",
                    "duration_weeks": 0, // Duración de esta fase en semanas
                    "cost": 0000 // Costo de esta fase en euros
                }},
                // Más fases según sea necesario
            ],
            "risks": [
                {{
                    "name": "Nombre del riesgo",
                    "probability": 00, // Probabilidad de 0 a 100
                    "impact": 00, // Impacto de 0 a 100
                    "mitigation": "Estrategia de mitigación"
                }},
                // Más riesgos según sea necesario
            ]
        }}
        
        IMPORTANTE: Responde ÚNICAMENTE con el JSON, sin explicaciones adicionales ni preguntas.
        """
        return prompt
        
    def _generate_fallback_estimate(self, project_data: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Generar una estimación de respaldo en caso de que la API falle
        
        Args:
            project_data: Descripción del proyecto
            
        Returns:
            Tupla con (datos_preview, datos_completos)
        """
        # Extraer el nombre del proyecto si está disponible
        project_name = "Proyecto"  # Valor por defecto
        for line in project_data.split('\n'):
            if line.startswith("Nombre del proyecto:"):
                project_name = line.split(":", 1)[1].strip()
                break
        
        # Generar una estimación simulada
        duration_weeks = random.randint(4, 16)
        
        # Generar horas para cada categoría
        hours = {
            "frontend": random.randint(20, 100),
            "backend": random.randint(30, 120),
            "design": random.randint(15, 60),
            "project_management": random.randint(10, 40),
            "qa": random.randint(15, 50)
        }
        
        # Calcular costos
        costs = {}
        total_cost = 0
        for category, hour in hours.items():
            cost = hour * self.hourly_rates[category]
            costs[category] = cost
            total_cost += cost
        
        # Generar fases
        phases = [
            {
                "name": "Fase 1: Análisis y Diseño",
                "description": "Análisis de requisitos y diseño de la solución",
                "duration_weeks": max(1, int(duration_weeks * 0.2)),
                "cost": int(total_cost * 0.2)
            },
            {
                "name": "Fase 2: Desarrollo",
                "description": "Implementación de funcionalidades principales",
                "duration_weeks": max(2, int(duration_weeks * 0.5)),
                "cost": int(total_cost * 0.5)
            },
            {
                "name": "Fase 3: Pruebas y Despliegue",
                "description": "Testing, correcciones y puesta en producción",
                "duration_weeks": max(1, int(duration_weeks * 0.3)),
                "cost": int(total_cost * 0.3)
            }
        ]
        
        # Generar riesgos
        risks = self._generate_fallback_risks()
        
        # Construir la estimación completa
        full_estimate = {
            "project_name": project_name,
            "total_cost": total_cost,
            "duration_weeks": duration_weeks,
            "hourly_rates": self.hourly_rates,
            "hours_breakdown": hours,
            "phases": phases,
            "risks": risks
        }
        
        # Construir la vista previa
        preview = {
            "project_name": project_name,
            "total_cost": total_cost,
            "duration_weeks": duration_weeks,
            "phase_count": len(phases)
        }
        
        return preview, full_estimate
        
    def _generate_fallback_risks(self) -> List[Dict[str, Any]]:
        """
        Generar riesgos de proyecto simulados en caso de que la API falle
        """
        risks = [
            {
                "name": "Cambios en los requisitos",
                "probability": random.randint(20, 80),
                "impact": random.randint(30, 90),
                "mitigation": "Documentación detallada y aprobación formal de requisitos"
            },
            {
                "name": "Retrasos en la entrega",
                "probability": random.randint(20, 70),
                "impact": random.randint(40, 90),
                "mitigation": "Planificación con margen y seguimiento continuo"
            },
            {
                "name": "Problemas técnicos",
                "probability": random.randint(10, 60),
                "impact": random.randint(50, 90),
                "mitigation": "Pruebas continuas y plan de contingencia"
            }
        ]
        
        return risks
    
    def _process_ai_response(self, budget_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Procesar la respuesta de la IA y formatearla correctamente
        
        Args:
            budget_data: Datos del presupuesto generados por la IA
            
        Returns:
            Tupla con (datos_preview, datos_completos)
        """
        try:
            # Asegurarse de que tenemos todos los campos necesarios
            if not all(k in budget_data for k in ['project_name', 'total_cost', 'duration_weeks']):
                print("Respuesta de IA incompleta, usando valores por defecto")
                return self._generate_fallback_estimate(str(budget_data))
            
            # Construir la vista previa
            preview = {
                "project_name": budget_data.get("project_name", "Proyecto"),
                "total_cost": budget_data.get("total_cost", 10000),
                "duration_weeks": budget_data.get("duration_weeks", 8),
                "phase_count": len(budget_data.get("phases", []))
            }
            
            # Si no hay fases, generar algunas
            if "phases" not in budget_data or not budget_data["phases"]:
                print("No se encontraron fases en la respuesta de la IA, generando fases por defecto")
                total_cost = budget_data.get("total_cost", 10000)
                duration_weeks = budget_data.get("duration_weeks", 8)
                
                budget_data["phases"] = [
                    {
                        "name": "Fase 1: Análisis y Diseño",
                        "description": "Análisis de requisitos y diseño de la solución",
                        "duration_weeks": max(1, int(duration_weeks * 0.2)),
                        "cost": int(total_cost * 0.2)
                    },
                    {
                        "name": "Fase 2: Desarrollo",
                        "description": "Implementación de funcionalidades principales",
                        "duration_weeks": max(2, int(duration_weeks * 0.5)),
                        "cost": int(total_cost * 0.5)
                    },
                    {
                        "name": "Fase 3: Pruebas y Despliegue",
                        "description": "Testing, correcciones y puesta en producción",
                        "duration_weeks": max(1, int(duration_weeks * 0.3)),
                        "cost": int(total_cost * 0.3)
                    }
                ]
            
            # Si no hay riesgos, generar algunos
            if "risks" not in budget_data or not budget_data["risks"]:
                print("No se encontraron riesgos en la respuesta de la IA, generando riesgos por defecto")
                budget_data["risks"] = self._generate_fallback_risks()
            
            # Si no hay tarifas por hora, usar las predeterminadas
            if "hourly_rates" not in budget_data or not budget_data["hourly_rates"]:
                print("No se encontraron tarifas por hora en la respuesta de la IA, usando tarifas por defecto")
                budget_data["hourly_rates"] = self.hourly_rates
            
            # Si no hay desglose de horas, generar uno
            if "hours_breakdown" not in budget_data or not budget_data["hours_breakdown"]:
                print("No se encontró desglose de horas en la respuesta de la IA, generando desglose por defecto")
                total_cost = budget_data.get("total_cost", 10000)
                hours = {}
                for category, rate in budget_data.get("hourly_rates", self.hourly_rates).items():
                    # Calcular horas basadas en una distribución aproximada del costo total
                    if category == "frontend":
                        hours[category] = int((total_cost * 0.3) / rate)
                    elif category == "backend":
                        hours[category] = int((total_cost * 0.35) / rate)
                    elif category == "design":
                        hours[category] = int((total_cost * 0.15) / rate)
                    elif category == "project_management":
                        hours[category] = int((total_cost * 0.1) / rate)
                    elif category == "qa":
                        hours[category] = int((total_cost * 0.1) / rate)
                budget_data["hours_breakdown"] = hours
            
            # Generar calendario de pagos si no existe
            if "payment_schedule" not in budget_data or not budget_data["payment_schedule"]:
                print("No se encontró calendario de pagos en la respuesta de la IA, generando calendario por defecto")
                budget_data["payment_schedule"] = self._generate_payment_schedule(
                    budget_data.get("total_cost", 10000),
                    budget_data.get("duration_weeks", 8)
                )
            
            return preview, budget_data
            
        except Exception as e:
            print(f"Error al procesar la respuesta de la IA: {e}")
            return self._generate_fallback_estimate(str(budget_data))
    
    def _generate_payment_schedule(self, total_cost: float, weeks: int) -> List[Dict[str, Any]]:
        """
        Generar un calendario de pagos basado en el costo total y la duración
        """
        payment_schedule = []
        
        # Pago inicial (30%)
        initial_payment = {
            "name": "Pago inicial",
            "percentage": 30,
            "amount": round(total_cost * 0.3, 2),
            "due_date": "Al inicio del proyecto"
        }
        payment_schedule.append(initial_payment)
        
        # Pago intermedio (40%)
        middle_payment = {
            "name": "Pago intermedio",
            "percentage": 40,
            "amount": round(total_cost * 0.4, 2),
            "due_date": f"Semana {max(1, int(weeks/2))}"
        }
        payment_schedule.append(middle_payment)
        
        # Pago final (30%)
        final_payment = {
            "name": "Pago final",
            "percentage": 30,
            "amount": round(total_cost * 0.3, 2),
            "due_date": f"Semana {weeks} (entrega final)"
        }
        payment_schedule.append(final_payment)
        
        return payment_schedule
    
    def generate_project_description(self, project_data: str) -> str:
        """
        Genera una descripción profesional del proyecto utilizando IA
        
        Args:
            project_data: Descripción del proyecto proporcionada por el usuario
            
        Returns:
            Descripción profesional del proyecto
        """
        try:
            if not self.api_key:
                print("API key no encontrada. Usando descripción por defecto.")
                return self._generate_fallback_description(project_data)
                
            # Preparar el prompt para la API
            prompt = f"""
            Actúa como un consultor profesional de TI. A continuación se presenta una descripción de un proyecto proporcionada por un cliente.
            Tu tarea es reescribir esta descripción en un formato profesional y estructurado para incluirla en un presupuesto formal.
            La descripción debe ser clara, concisa y destacar los aspectos técnicos y funcionales más importantes del proyecto.
            
            Descripción original del cliente:
            {project_data}
            
            Genera una descripción profesional de 3-4 párrafos que incluya:
            1. Una introducción general al proyecto
            2. Los objetivos principales
            3. Las funcionalidades clave
            4. Los beneficios esperados o valor añadido
            
            
            IMPORTANTE: Responde ÚNICAMENTE con la descripción profesional, sin explicaciones adicionales ni preguntas.
            """
            
            # Llamar a la API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres un consultor profesional de TI especializado en redactar descripciones de proyectos para presupuestos formales."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            
            if 'choices' in response_json and len(response_json['choices']) > 0:
                description = response_json['choices'][0]['message']['content'].strip()
                return description
            else:
                print("Respuesta de IA incompleta, usando descripción por defecto")
                return self._generate_fallback_description(project_data)
                
        except Exception as e:
            print(f"Error al generar descripción con IA: {e}")
            return self._generate_fallback_description(project_data)
    
    def _generate_fallback_description(self, project_data: str) -> str:
        """
        Genera una descripción de respaldo en caso de que la API falle
        
        Args:
            project_data: Descripción del proyecto proporcionada por el usuario
            
        Returns:
            Descripción de respaldo
        """
        # Extraer tipo de proyecto si está disponible
        project_type = "desarrollo de software"
        for line in project_data.split('\n'):
            if line.startswith("Tipo de proyecto:"):
                project_type = line.split(":", 1)[1].strip().lower()
                break
        
        # Generar una descripción genérica pero profesional
        description = f"""El proyecto consiste en el {project_type} que permitirá optimizar procesos y mejorar la eficiencia operativa. 
        
Se implementará una solución tecnológica adaptada a las necesidades específicas del cliente, siguiendo las mejores prácticas de la industria y utilizando tecnologías modernas. 
        
La solución incluirá todas las funcionalidades solicitadas por el cliente, con un enfoque en la usabilidad, seguridad y escalabilidad. 
        
El resultado final será un sistema robusto que aportará valor añadido al negocio, mejorando la productividad y facilitando la toma de decisiones."""
        
        return description
    
    def _generate_team_composition(self, hours_by_role):
        """Genera una sugerencia de composición del equipo"""
        team = []
        for role, hours in hours_by_role.items():
            if hours > 0:
                if role == "frontend":
                    team.append({"role": "Desarrollador Frontend", "dedication": "Parcial" if hours < 80 else "Completa"})
                elif role == "backend":
                    team.append({"role": "Desarrollador Backend", "dedication": "Parcial" if hours < 80 else "Completa"})
                elif role == "design":
                    team.append({"role": "Diseñador UX/UI", "dedication": "Parcial" if hours < 60 else "Completa"})
                elif role == "project_management":
                    team.append({"role": "Project Manager", "dedication": "Parcial"})
                elif role == "qa":
                    team.append({"role": "QA Tester", "dedication": "Parcial" if hours < 60 else "Completa"})
        return team
    
    def _generate_timeline(self, components, total_weeks):
        """Genera una línea de tiempo para el proyecto"""
        timeline = []
        current_week = 1
        
        # Fase de inicio
        timeline.append({
            "phase": "Inicio y planificación",
            "start_week": current_week,
            "duration_weeks": 1,
            "deliverables": ["Plan de proyecto", "Requisitos detallados"]
        })
        current_week += 1
        
        # Fase de diseño (si hay componentes de diseño)
        has_design = any("design" in comp_hours for comp_hours in components.values())
        if has_design:
            timeline.append({
                "phase": "Diseño de UI/UX",
                "start_week": current_week,
                "duration_weeks": max(1, int(total_weeks * 0.2)),
                "deliverables": ["Mockups", "Prototipos interactivos"]
            })
            current_week += max(1, int(total_weeks * 0.2))
        
        dev_weeks = max(2, int(total_weeks * 0.6))
        timeline.append({
            "phase": "Desarrollo principal",
            "start_week": current_week,
            "duration_weeks": dev_weeks,
            "deliverables": ["Código base", "Componentes principales", "Integraciones"]
        })
        current_week += dev_weeks
        
        # Fase de pruebas
        qa_weeks = max(1, int(total_weeks * 0.2))
        timeline.append({
            "phase": "Pruebas y control de calidad",
            "start_week": current_week,
            "duration_weeks": qa_weeks,
            "deliverables": ["Plan de pruebas", "Informe de errores", "Versión estable"]
        })
        current_week += qa_weeks
        
        # Fase de despliegue
        timeline.append({
            "phase": "Despliegue y entrega",
            "start_week": current_week,
            "duration_weeks": 1,
            "deliverables": ["Documentación", "Código fuente", "Aplicación en producción"]
        })
        
        return timeline