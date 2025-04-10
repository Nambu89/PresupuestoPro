from typing import Dict, Any, List, Tuple
import random

class AIProjectEstimator:
    """
    Simulador de estimación de presupuestos con IA
    En una implementación real, aquí se conectaría con un servicio de IA/ML
    """
    
    def __init__(self):
        # Definir tarifas por tipo de trabajo (€/hora)
        self.hourly_rates = {
            "frontend": 50,
            "backend": 60,
            "design": 45,
            "project_management": 55,
            "qa": 40,
        }
        
        # Definir componentes comunes de proyectos
        self.common_components = {
            "user_authentication": {"frontend": 16, "backend": 16},
            "admin_dashboard": {"frontend": 40, "backend": 32, "design": 16},
            "public_website": {"frontend": 24, "backend": 16, "design": 16},
            "payment_processing": {"frontend": 16, "backend": 24},
            "file_upload": {"frontend": 8, "backend": 16},
            "reporting": {"frontend": 24, "backend": 32},
            "api_integration": {"backend": 24},
            "real_time_features": {"frontend": 24, "backend": 32},
            "search_functionality": {"frontend": 16, "backend": 24},
            "user_profiles": {"frontend": 16, "backend": 16, "design": 8},
        }
    
    def generate_estimate(self, project_description: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Generar una estimación simulada basada en el nombre y descripción del proyecto
        
        En un sistema real, procesaríamos el texto con NLP para identificar componentes
        """
        # Identificar componentes que podrían ser parte del proyecto
        # Esto simula el análisis de la IA del texto de descripción
        keywords = project_description.lower().split()
        
        # Seleccionar componentes basados en palabras clave
        selected_components = {}
        for component, hours in self.common_components.items():
            # Lógica simple de simulación: si una palabra del componente está en la descripción, inclúyelo
            component_words = component.split("_")
            if any(word in keywords for word in component_words) or random.random() < 0.3:
                selected_components[component] = hours
        
        # Siempre incluir algunos componentes básicos si la selección está vacía
        if not selected_components:
            selected_components = {
                "user_authentication": self.common_components["user_authentication"],
                "public_website": self.common_components["public_website"]
            }
        
        # Calcular las horas por rol
        total_hours_by_role = {}
        for component_hours in selected_components.values():
            for role, hours in component_hours.items():
                total_hours_by_role[role] = total_hours_by_role.get(role, 0) + hours
        
        # Añadir horas para project management y QA
        base_hours = sum(total_hours_by_role.values())
        total_hours_by_role["project_management"] = int(base_hours * 0.15)  # 15% del total
        total_hours_by_role["qa"] = int(base_hours * 0.2)  # 20% del total
        
        # Calcular costos
        costs_by_role = {}
        for role, hours in total_hours_by_role.items():
            rate = self.hourly_rates.get(role, 50)  # Tarifa por defecto si no está definida
            costs_by_role[role] = hours * rate
        
        total_cost = sum(costs_by_role.values())
        total_hours = sum(total_hours_by_role.values())
        
        # Estimar duración en semanas (asumiendo un equipo de 3 personas, cada una trabajando 40h/semana)
        team_capacity_per_week = 3 * 40 * 0.7  # 70% de eficiencia
        estimated_weeks = round(total_hours / team_capacity_per_week)
        
        # Crear una vista previa (versión gratuita)
        preview_data = {
            "estimated_cost": total_cost,
            "estimated_duration_weeks": estimated_weeks,
            "total_hours": total_hours,
        }
        
        # Crear datos completos (versión premium)
        full_data = {
            **preview_data,
            "hours_breakdown": total_hours_by_role,
            "costs_breakdown": costs_by_role,
            "components": list(selected_components.keys()),
            "hourly_rates": self.hourly_rates,
            "risk_assessment": self._generate_risk_assessment(),
            "payment_schedule": self._generate_payment_schedule(total_cost, estimated_weeks),
            "team_composition": self._generate_team_composition(total_hours_by_role),
            "detailed_timeline": self._generate_timeline(selected_components, estimated_weeks),
        }
        
        return preview_data, full_data
    
    def _generate_risk_assessment(self) -> List[Dict[str, Any]]:
        """Genera una evaluación de riesgos ficticia"""
        risks = [
            {"name": "Cambios en los requisitos", "probability": "Media", "impact": "Alto", "mitigation": "Definir alcance claro, incluir buffer para cambios"},
            {"name": "Problemas técnicos", "probability": "Baja", "impact": "Alto", "mitigation": "Realizar pruebas de concepto tempranas"},
            {"name": "Disponibilidad del cliente", "probability": "Media", "impact": "Medio", "mitigation": "Programar reuniones regulares con anticipación"},
            {"name": "Retrasos en integraciones externas", "probability": "Alta", "impact": "Medio", "mitigation": "Comenzar integraciones temprano, tener alternativas"},
        ]
        return risks
    
    def _generate_payment_schedule(self, total_cost: float, weeks: int) -> List[Dict[str, Any]]:
        """Genera un calendario de pagos"""
        if weeks <= 4:
            return [
                {"percentage": 50, "amount": total_cost * 0.5, "description": "Al inicio del proyecto"},
                {"percentage": 50, "amount": total_cost * 0.5, "description": "A la entrega final"}
            ]
        elif weeks <= 12:
            return [
                {"percentage": 30, "amount": total_cost * 0.3, "description": "Al inicio del proyecto"},
                {"percentage": 40, "amount": total_cost * 0.4, "description": "Al completar el desarrollo principal"},
                {"percentage": 30, "amount": total_cost * 0.3, "description": "A la entrega final"}
            ]
        else:
            return [
                {"percentage": 20, "amount": total_cost * 0.2, "description": "Al inicio del proyecto"},
                {"percentage": 20, "amount": total_cost * 0.2, "description": "Al finalizar la fase de diseño"},
                {"percentage": 30, "amount": total_cost * 0.3, "description": "Al completar el desarrollo principal"},
                {"percentage": 20, "amount": total_cost * 0.2, "description": "Al inicio de pruebas de aceptación"},
                {"percentage": 10, "amount": total_cost * 0.1, "description": "A la entrega final"}
            ]
    
    def _generate_team_composition(self, hours_by_role):
        """Genera una sugerencia de composición del equipo"""
        team = []
        for role, hours in hours_by_role.items():
            if hours < 20:
                allocation = 0.25
            elif hours < 40:
                allocation = 0.5
            else:
                allocation = 1.0
                
            team.append({
                "role": role.replace("_", " ").title(),
                "allocation": allocation,
                "hours": hours
            })
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