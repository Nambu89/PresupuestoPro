import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional
import os

from app.config import settings

class EmailSender:
    def __init__(self):
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        attachments: Optional[List[tuple]] = None  # Lista de tuplas (filename, content)
    ) -> bool:
        """
        Envía un email con contenido HTML y opcionalmente archivos adjuntos
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Añadir contenido HTML
            msg.attach(MIMEText(html_content, 'html'))
            
            # Añadir archivos adjuntos si existen
            if attachments:
                for filename, content in attachments:
                    attachment = MIMEApplication(content)
                    attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
                    msg.attach(attachment)
            
            # Conectar al servidor SMTP
            if settings.SMTP_TLS:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                
            # Login
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
                
            # Enviar email
            server.sendmail(self.from_email, to_email, msg.as_string())
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error al enviar email: {str(e)}")
            return False
            
    def send_project_email(
        self,
        to_email: str,
        project,
        user,
        pdf_content: Optional[bytes] = None
    ) -> bool:
        """
        Envía un email con información del proyecto y opcionalmente el PDF adjunto
        """
        subject = f"Tu presupuesto para: {project.name}"
        
        # Crear contenido HTML
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4a86e8; color: white; padding: 10px 20px; }}
                .content {{ padding: 20px; border: 1px solid #ddd; }}
                .footer {{ font-size: 12px; color: #777; margin-top: 20px; }}
                .button {{ display: inline-block; background-color: #4a86e8; color: white; 
                           padding: 10px 20px; text-decoration: none; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>PresupuestoPro</h2>
                </div>
                <div class="content">
                    <h3>Hola {user.first_name},</h3>
                    <p>Adjunto encontrarás el presupuesto para tu proyecto: <strong>{project.name}</strong>.</p>
                    
                    <h4>Detalles del Proyecto:</h4>
                    <ul>
                        <li><strong>Nombre:</strong> {project.name}</li>
                        <li><strong>Descripción:</strong> {project.description}</li>
                        <li><strong>Coste Estimado:</strong> {project.estimated_cost} €</li>
                        <li><strong>Duración Estimada:</strong> {project.estimated_duration_weeks} semanas</li>
                    </ul>
                    
                    <p>Puedes acceder a los detalles completos de tu proyecto en tu dashboard:</p>
                    <p><a href="{settings.FRONTEND_URL}/dashboard" class="button">Ver en Dashboard</a></p>
                </div>
                <div class="footer">
                    <p>Este email ha sido enviado desde PresupuestoPro.</p>
                    <p>© 2025 PresupuestoPro. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Preparar adjuntos
        attachments = None
        if pdf_content:
            filename = f"presupuesto_{project.name.replace(' ', '_')}.pdf"
            attachments = [(filename, pdf_content)]
            
        # Enviar email
        return self.send_email(to_email, subject, html_content, attachments)
