from io import BytesIO
import os
import datetime
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Flowable, KeepTogether, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from app.services.ai import AIProjectEstimator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart

class HorizontalLine(Flowable):
    """Dibuja una línea horizontal con color personalizable"""
    def __init__(self, width, height=0.5, color=colors.black):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.height)
        self.canv.line(0, 0, self.width, 0)

class PDFGenerator:
    """
    Generador de PDFs para presupuestos de proyectos
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
        # Colores corporativos (DynamizaTIC)
        self.primary_color = colors.HexColor('#3a86c8')  # Azul principal
        self.secondary_color = colors.HexColor('#6eb5e5')  # Azul secundario
        self.accent_color = colors.HexColor('#0056a3')  # Azul oscuro acento
        self.text_color = colors.HexColor('#333333')  # Texto oscuro
        self.light_bg = colors.HexColor('#f8f9fa')  # Fondo claro
        
        # Instancia del estimador de IA para generar descripciones profesionales
        self.ai_estimator = AIProjectEstimator()
        
        # Crear estilos personalizados
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            fontName='Helvetica-Bold',
            fontSize=22,
            alignment=TA_CENTER,
            textColor=self.primary_color,
            spaceAfter=12
        ))
        
        # Añadir estilos personalizados
        self.styles.add(ParagraphStyle(
            name='ProjectSubtitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            alignment=TA_LEFT,
            textColor=self.secondary_color,
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=TA_LEFT,
            textColor=self.primary_color,
            spaceAfter=8
        ))
        
        # Modificar el estilo Normal existente
        normal_style = self.styles['Normal']
        normal_style.fontSize = 11
        normal_style.alignment = TA_LEFT
        normal_style.textColor = self.text_color
        normal_style.spaceAfter = 6
        
        self.styles.add(ParagraphStyle(
            name='Footer',
            fontName='Helvetica-Oblique',
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.gray
        ))
        
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            fontName='Helvetica-Bold',
            fontSize=11,
            alignment=TA_CENTER,
            textColor=colors.white
        ))
        
        self.styles.add(ParagraphStyle(
            name='TableCell',
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_CENTER
        ))
        
    def _create_header(self, canvas, doc, project):
        """Crea el encabezado del PDF"""
        canvas.saveState()
        
        # Texto del encabezado (título del documento en cada página)
        canvas.setFillColor(self.text_color)
        canvas.setFont('Helvetica', 9)
        
        # Logo pequeño en la esquina superior izquierda
        canvas.setFillColor(self.primary_color)
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(doc.leftMargin, doc.height + doc.topMargin - 10*mm, "PresupuestoPro")
        
        # Título del documento centrado
        canvas.setFillColor(self.text_color)
        canvas.setFont('Helvetica', 9)
        title_text = f"Oferta: {project.name}"
        canvas.drawCentredString(doc.width/2 + doc.leftMargin, doc.height + doc.topMargin - 10*mm, title_text)
        
        canvas.restoreState()
    
    def _create_footer(self, canvas, doc):
        """Crea el pie de página del PDF"""
        canvas.saveState()
        
        # Número de página
        canvas.setFont('Helvetica', 9)
        text = f"Página {doc.page} de 3"
        canvas.drawRightString(doc.width + doc.leftMargin, doc.bottomMargin - 10*mm, text)
        
        # Logo pequeño en la esquina derecha
        if doc.page > 1:  # No mostrar en la portada
            canvas.setFillColor(self.primary_color)
            # Dibujar un pequeño logo en la esquina inferior derecha
            logo_size = 10*mm
            canvas.drawRightString(doc.width + doc.leftMargin, doc.bottomMargin - 20*mm, "PresupuestoPro")
        
        canvas.restoreState()
    
    def generate_project_pdf(self, project, user):
        """
        Genera un PDF para un proyecto específico con diseño mejorado siguiendo el formato de DynamizaTIC
        """
        buffer = BytesIO()
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm
        )
        
        # Función para agregar encabezado y pie de página
        def add_page_elements(canvas, doc):
            if doc.page > 1:  # No mostrar encabezado en la portada
                self._create_header(canvas, doc, project)
            self._create_footer(canvas, doc)
        
        # Contenido del PDF
        content = []
        
        # PORTADA
        # Logo grande centrado
        logo_style = ParagraphStyle(
            'Logo',
            parent=self.styles['Title'],
            fontSize=36,
            alignment=TA_CENTER,
            textColor=self.primary_color,
            spaceAfter=2*cm
        )
        content.append(Paragraph("<b>PresupuestoPro</b>", logo_style))
        
        # Título del documento
        title_style = ParagraphStyle(
            'DocumentTitle',
            parent=self.styles['Title'],
            fontSize=24,
            alignment=TA_CENTER,
            textColor=self.text_color,
            spaceAfter=0.5*cm
        )
        content.append(Paragraph(f"<b>OFERTA DESARROLLO /</b>", title_style))
        content.append(Paragraph(f"<b>{project.name}</b>", title_style))
        
        # Espacio
        content.append(Spacer(1, 3*cm))
        
        # Cliente
        client_style = ParagraphStyle(
            'ClientName',
            parent=self.styles['Title'],
            fontSize=22,
            alignment=TA_CENTER,
            textColor=self.primary_color,
            spaceAfter=1*cm
        )
        
        # Extraer la primera línea como cliente si es posible
        description_parts = project.description.split('\n', 1)
        client_name = description_parts[0] if len(description_parts) > 1 else 'Cliente'
        content.append(Paragraph(f"<b>{client_name}</b>", client_style))
        
        # Fecha
        date_style = ParagraphStyle(
            'Date',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=0.5*cm
        )
        content.append(Spacer(1, 5*cm))
        content.append(Paragraph(f"{datetime.datetime.now().strftime('%d de %B de %Y')}", date_style))
        
        # Información de contacto
        contact_style = ParagraphStyle(
            'Contact',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.gray
        )
        contact_text = f"Servicios Profesionales PresupuestoPro S.L. - email: {user.email}"
        content.append(Spacer(1, 1*cm))
        content.append(Paragraph(contact_text, contact_style))
        
        # Salto de página después de la portada
        content.append(PageBreak())
        
        # ÍNDICE DE CONTENIDO
        toc_title = ParagraphStyle(
            'TOCTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_LEFT,
            textColor=self.text_color,
            fontName='Helvetica-Bold'
        )
        content.append(Paragraph(f"Oferta: {project.name}", toc_title))
        content.append(Spacer(1, 0.5*cm))
        
        content.append(Paragraph("<b>CONTENIDO</b>", self.styles['Normal']))
        content.append(Spacer(1, 0.3*cm))
        
        # Crear tabla de contenido
        toc_data = [
            ["1.", "OBJETO", "2"],
            ["2.", "DESCRIPCIÓN DEL PROYECTO", "2"],
            ["2.1", "FUNCIONALIDADES PRINCIPALES", "3"],
            ["3.", "PLANIFICACIÓN", "3"],
            ["4.", "COSTE", "3"],
            ["5.", "FIRMAS", "3"]
        ]
        
        toc_table = Table(toc_data, colWidths=[0.5*cm, 15*cm, 0.5*cm])
        toc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        content.append(toc_table)
        content.append(PageBreak())
        
        # 1. OBJETO
        section_title = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            alignment=TA_LEFT,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            spaceAfter=0.3*cm
        )
        content.append(Paragraph("1. OBJETO", section_title))
        
        # Extraer la primera línea como cliente si es posible
        description_parts = project.description.split('\n', 1)
        client_name = description_parts[0] if len(description_parts) > 1 else 'Cliente'
        description = description_parts[1] if len(description_parts) > 1 else project.description
        
        content.append(Paragraph(f"{client_name} tiene la necesidad de {project.name} para mejorar sus procesos de negocio.", self.styles['Normal']))
        content.append(Spacer(1, 0.5*cm))
        
        # 2. DESCRIPCIÓN DEL PROYECTO
        content.append(Paragraph("2. DESCRIPCIÓN DEL PROYECTO", section_title))
        
        # Extraer tipo de proyecto si está disponible
        project_type = ""
        for line in description.split('\n'):
            if line.startswith("Tipo de proyecto:"):
                project_type = line.split(":", 1)[1].strip()
                break
        
        # Generar una descripción profesional utilizando IA
        try:
            print("Generando descripción profesional del proyecto con IA...")
            # Utilizar la IA para generar una descripción profesional
            ai_description = self.ai_estimator.generate_project_description(description)
            
            # Verificar si se obtuvo una descripción válida
            if ai_description and len(ai_description) > 50:  # Asegurarse de que la descripción tiene contenido sustancial
                # Formatear la descripción para el PDF
                paragraphs = ai_description.split('\n\n')
                
                # Si hay un tipo de proyecto, mencionarlo primero
                if project_type:
                    content.append(Paragraph(f"Se desarrollará un proyecto de <b>{project_type}</b> con las siguientes características:", self.styles['Normal']))
                    content.append(Spacer(1, 0.2*cm))
                
                # Añadir cada párrafo de la descripción generada por IA
                for paragraph in paragraphs:
                    if paragraph.strip():  # Asegurarse de que el párrafo no está vacío
                        content.append(Paragraph(paragraph.strip(), self.styles['Normal']))
                        content.append(Spacer(1, 0.2*cm))
            else:
                # Si la IA no generó una descripción válida, usar un enfoque alternativo
                if project_type:
                    content.append(Paragraph(f"Se desarrollará un proyecto de <b>{project_type}</b> que permitirá optimizar procesos y mejorar la eficiencia operativa.", self.styles['Normal']))
                else:
                    content.append(Paragraph(f"El proyecto consiste en el desarrollo de una solución tecnológica que permitirá optimizar procesos y mejorar la eficiencia operativa.", self.styles['Normal']))
                content.append(Spacer(1, 0.2*cm))
                content.append(Paragraph(f"La solución se implementará siguiendo las mejores prácticas de la industria y utilizando tecnologías modernas para garantizar un resultado de alta calidad.", self.styles['Normal']))
        except Exception as e:
            print(f"Error al generar descripción con IA: {e}")
            # En caso de error, usar una descripción genérica pero profesional
            content.append(Paragraph(f"El proyecto consiste en el desarrollo de una solución tecnológica adaptada a las necesidades específicas del cliente.", self.styles['Normal']))
            content.append(Spacer(1, 0.2*cm))
            content.append(Paragraph(f"Se implementará siguiendo las mejores prácticas de la industria y utilizando tecnologías modernas para garantizar un resultado de alta calidad.", self.styles['Normal']))
        content.append(Spacer(1, 0.5*cm))
        
        # 2.1 FUNCIONALIDADES PRINCIPALES
        content.append(Paragraph("2.1 FUNCIONALIDADES PRINCIPALES", section_title))
        
        # Extraer funcionalidades si están disponibles
        funcionalidades = ""
        for line in description.split('\n'):
            if line.startswith("Funcionalidades:"):
                funcionalidades = line.split(":", 1)[1].strip()
                break
        
        if funcionalidades:
            # Si hay funcionalidades especificadas, mostrarlas
            content.append(Paragraph("El proyecto incluirá las siguientes funcionalidades principales:", self.styles['Normal']))
            content.append(Spacer(1, 0.2*cm))
            
            # Intentar dividir las funcionalidades en una lista si están separadas por puntos o comas
            if '.' in funcionalidades or ',' in funcionalidades:
                items = [item.strip() for item in funcionalidades.replace('.', ',').split(',') if item.strip()]
                for item in items:
                    if item:
                        content.append(Paragraph(f"• {item}", self.styles['Normal']))
                        content.append(Spacer(1, 0.1*cm))
            else:
                # Si no se pueden dividir, mostrar como texto normal
                content.append(Paragraph(funcionalidades, self.styles['Normal']))
        else:
            # Si no hay funcionalidades especificadas, mostrar un texto genérico
            content.append(Paragraph("El proyecto incluirá todas las funcionalidades necesarias para cumplir con los objetivos establecidos, garantizando una solución completa y eficiente.", self.styles['Normal']))
        content.append(Spacer(1, 0.5*cm))
        
        # 3. PLANIFICACIÓN
        content.append(Paragraph("3. PLANIFICACIÓN", section_title))
        content.append(Paragraph(f"El proyecto se finalizará en {project.estimated_duration_weeks} semanas. Una vez aprobada la oferta se dará fecha de entrega en el entorno de desarrollo.", self.styles['Normal']))
        content.append(Spacer(1, 0.5*cm))
        
        # 4. COSTE
        content.append(Paragraph("4. COSTE", section_title))
        
        # Calcular el coste total con formato de moneda
        coste_total = f"{project.estimated_cost:,.2f}"
        
        content.append(Paragraph(f"El coste total de este evolutivo es de {coste_total} euros, de los cuales el 50% se facturarán con la firma del contrato y el 50% restante después de finalizado el soporte post arranque de 5 días.", self.styles['Normal']))
        content.append(Spacer(1, 0.5*cm))
        
        # 5. FIRMAS
        content.append(Paragraph("5. FIRMAS", section_title))
        
        content.append(Paragraph("Aceptación de la oferta", self.styles['Normal']))
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph("La firma del presente documento supone la aceptación por las partes de su contenido, e implica otorgar al presente documento, a todos los efectos, el carácter de contrato de arrendamiento de servicios profesionales.", self.styles['Normal']))
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph("Vigencia:", self.styles['Normal']))
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph("La presente oferta tiene una vigencia de 1 mes a contar desde su fecha de presentación.", self.styles['Normal']))
        content.append(Spacer(1, 1*cm))
        
        # Extraer el nombre del cliente para la firma
        description_parts = project.description.split('\n', 1)
        client_name = description_parts[0] if len(description_parts) > 1 else 'Cliente'
        
        # Tabla para firmas
        firma_data = [
            [Paragraph(f"<b>Por {user.first_name} {user.last_name}:</b>", self.styles['Normal']), Paragraph(f"<b>Por {client_name}:</b>", self.styles['Normal'])],
            [Paragraph(f"Usuario de PresupuestoPro", self.styles['Normal']), Paragraph(f"Cliente", self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), Paragraph("", self.styles['Normal'])],
            [Paragraph("", self.styles['Normal']), Paragraph("", self.styles['Normal'])],
            [Paragraph("_____________________________", self.styles['Normal']), Paragraph("_____________________________", self.styles['Normal'])],
            [Paragraph("Firma y sello", self.styles['Normal']), Paragraph("Firma y sello", self.styles['Normal'])]
        ]
        
        firma_table = Table(firma_data, colWidths=[doc.width*0.45, doc.width*0.45])
        firma_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (2, 0), (3, 1), 20),  # Espacio para firmar
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 1), (-1, 1), 5),
        ]))
        
        content.append(firma_table)
        content.append(Spacer(1, 0.5*cm))
        
        content.append(Paragraph("Nota: A continuación, incluimos los anexos necesarios para cumplimentar con esta oferta.", self.styles['Normal']))
        
        # Construir el PDF con encabezado y pie de página
        doc.build(content, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
        
        # Obtener el contenido del buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf
