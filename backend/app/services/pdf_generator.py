from io import BytesIO
import os
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Flowable, KeepTogether
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
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
        # Colores corporativos
        self.primary_color = colors.HexColor('#1a73e8')  # Azul principal
        self.secondary_color = colors.HexColor('#4285f4')  # Azul secundario
        self.accent_color = colors.HexColor('#fbbc04')  # Amarillo acento
        self.text_color = colors.HexColor('#202124')  # Texto oscuro
        self.light_bg = colors.HexColor('#f8f9fa')  # Fondo claro
        
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
        
        # Logo y nombre de la empresa
        # Simulamos un logo con un rectángulo azul y texto
        canvas.setFillColor(self.primary_color)
        canvas.rect(doc.leftMargin, doc.height + doc.topMargin - 20*mm, 25*mm, 15*mm, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 14)
        canvas.drawString(doc.leftMargin + 5*mm, doc.height + doc.topMargin - 10*mm, "PP")
        
        # Nombre de la empresa
        canvas.setFillColor(self.text_color)
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawString(doc.leftMargin + 30*mm, doc.height + doc.topMargin - 10*mm, "PresupuestoPro")
        
        # Línea separadora
        canvas.setStrokeColor(self.primary_color)
        canvas.setLineWidth(1)
        canvas.line(doc.leftMargin, doc.height + doc.topMargin - 25*mm, 
                   doc.width + doc.leftMargin, doc.height + doc.topMargin - 25*mm)
        
        # Número de página
        canvas.setFont('Helvetica', 9)
        text = f"Página {doc.page}"
        canvas.drawRightString(doc.width + doc.leftMargin, doc.bottomMargin - 10*mm, text)
        
        canvas.restoreState()
    
    def _create_footer(self, canvas, doc):
        """Crea el pie de página del PDF"""
        canvas.saveState()
        
        # Línea separadora
        canvas.setStrokeColor(self.primary_color)
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.bottomMargin - 5*mm, 
                   doc.width + doc.leftMargin, doc.bottomMargin - 5*mm)
        
        # Texto del pie de página
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        footer_text = f"Documento generado por PresupuestoPro el {datetime.datetime.now().strftime('%d/%m/%Y')}"
        canvas.drawCentredString(doc.width/2 + doc.leftMargin, doc.bottomMargin - 15*mm, footer_text)
        
        canvas.restoreState()
    
    def generate_project_pdf(self, project, user):
        """
        Genera un PDF para un proyecto específico con diseño mejorado
        """
        buffer = BytesIO()
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm
        )
        
        # Función para agregar encabezado y pie de página
        def add_page_elements(canvas, doc):
            self._create_header(canvas, doc, project)
            self._create_footer(canvas, doc)
        
        # Contenido del PDF
        content = []
        
        # Título del presupuesto
        content.append(Paragraph(f"Presupuesto: {project.name}", self.styles['CustomTitle']))
        content.append(HorizontalLine(doc.width, 1, self.accent_color))
        content.append(Spacer(1, 0.8*cm))
        
        # Información del cliente y fecha
        client_data = [
            [
                Paragraph("<b>CLIENTE</b>", self.styles['TableHeader']),
                Paragraph("<b>FECHA</b>", self.styles['TableHeader']),
                Paragraph("<b>REFERENCIA</b>", self.styles['TableHeader'])
            ],
            [
                Paragraph(f"{user.first_name} {user.last_name}<br/>{user.email}", self.styles['TableCell']),
                Paragraph(f"{datetime.datetime.now().strftime('%d/%m/%Y')}", self.styles['TableCell']),
                Paragraph(f"PRO-{project.id:04d}", self.styles['TableCell'])
            ]
        ]
        
        client_table = Table(client_data, colWidths=[doc.width/3.0]*3)
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (2, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        content.append(client_table)
        content.append(Spacer(1, 0.8*cm))
        
        # Detalles del proyecto
        content.append(Paragraph("Detalles del Proyecto", self.styles['SectionTitle']))
        content.append(HorizontalLine(doc.width, 0.5, self.secondary_color))
        content.append(Spacer(1, 0.3*cm))
        
        # Extraer la primera línea como cliente si es posible
        description_parts = project.description.split('\n', 1)
        client_name = description_parts[0] if len(description_parts) > 1 else ''
        description = description_parts[1] if len(description_parts) > 1 else project.description
        
        content.append(Paragraph(f"<b>Cliente:</b> {client_name}", self.styles['Normal']))
        content.append(Paragraph(f"<b>Descripción:</b> {description}", self.styles['Normal']))
        content.append(Spacer(1, 0.5*cm))
        
        # Estimaciones
        content.append(Paragraph("Estimaciones", self.styles['SectionTitle']))
        content.append(HorizontalLine(doc.width, 0.5, self.secondary_color))
        content.append(Spacer(1, 0.3*cm))
        
        # Tabla de estimaciones
        data = [
            [Paragraph("<b>Concepto</b>", self.styles['TableHeader']), 
             Paragraph("<b>Valor</b>", self.styles['TableHeader'])],
        ]
        
        # Añadir datos básicos
        data.append([Paragraph("Coste Estimado", self.styles['TableCell']), 
                     Paragraph(f"{project.estimated_cost:,.2f} €", self.styles['TableCell'])])
        data.append([Paragraph("Duración Estimada", self.styles['TableCell']), 
                     Paragraph(f"{project.estimated_duration_weeks} semanas", self.styles['TableCell'])])
        
        # Si es premium, agregar más detalles
        if hasattr(project, 'full_data') and project.full_data:
            for key, value in project.full_data.items():
                if key not in ["estimated_cost", "estimated_duration_weeks"]:
                    if isinstance(value, (int, float)) and key.endswith("_cost"):
                        data.append([Paragraph(key.replace("_", " ").title(), self.styles['TableCell']), 
                                     Paragraph(f"{value:,.2f} €", self.styles['TableCell'])])
                    else:
                        data.append([Paragraph(key.replace("_", " ").title(), self.styles['TableCell']), 
                                     Paragraph(str(value), self.styles['TableCell'])])
        
        # Crear tabla con estilo mejorado
        table = Table(data, colWidths=[doc.width*0.6, doc.width*0.4])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.light_bg, colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        content.append(table)
        content.append(Spacer(1, 0.8*cm))
        
        # Notas y condiciones
        content.append(Paragraph("Notas y Condiciones", self.styles['SectionTitle']))
        content.append(HorizontalLine(doc.width, 0.5, self.secondary_color))
        content.append(Spacer(1, 0.3*cm))
        
        notes = [
            "Este presupuesto es una estimación basada en la información proporcionada.",
            "Los costes finales pueden variar según los requisitos específicos del proyecto.",
            "La validez de este presupuesto es de 30 días a partir de la fecha de emisión.",
            "El tiempo de entrega puede variar según la disponibilidad y complejidad del proyecto.",
            "Los pagos se realizarán según el calendario acordado: 40% al inicio, 30% a mitad del proyecto y 30% a la entrega."
        ]
        
        for note in notes:
            content.append(Paragraph(f"• {note}", self.styles['Normal']))
            content.append(Spacer(1, 0.2*cm))
        
        # Construir el PDF con encabezado y pie de página
        doc.build(content, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
        
        # Obtener el contenido del buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf
