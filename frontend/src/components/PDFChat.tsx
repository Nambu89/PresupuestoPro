import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Loader2, ChevronDown, Edit2, MessageSquare } from 'lucide-react';

const Spinner = ({ size = "default" }: { size?: "sm" | "default" | "lg" }) => {
  const sizeClass = size === "sm" ? "h-4 w-4" : size === "lg" ? "h-8 w-8" : "h-6 w-6";
  return <Loader2 className={`animate-spin ${sizeClass}`} />;
};

interface PDFChatProps {
  projectId: number;
  projectName: string;
  onRequestEdit?: (section?: string) => void;
  onScrollToSection?: (section: string) => void;
}

interface Message {
  text: string;
  sender: 'user' | 'assistant';
  documentReference?: string;
  isModificationRequest?: boolean;
}

interface ModificationData {
  type: 'time' | 'cost' | 'content';
  section: string;
  value?: number;
  unit?: string;
  content?: string;
  originalQuery: string;
}

const PDFChat: React.FC<PDFChatProps> = ({ 
  projectId, 
  projectName, 
  onRequestEdit,
  onScrollToSection 
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [pendingModification, setPendingModification] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const displayName = projectName && projectName !== 'Proyecto' ? projectName : 'este proyecto';
    setMessages([{
      text: `Respecto a tu consulta sobre ${displayName}:

Este proyecto tiene un coste estimado y una duración estimada según el documento.

Para obtener información más específica, puedes preguntar sobre:
- Costes detallados del proyecto
- Plazos y cronograma
- Tecnologías recomendadas
- Equipo necesario
- Riesgos potenciales
- Alternativas más económicas o más rápidas

¿En qué aspecto concreto estás más interesado?`,
      sender: 'assistant'
    }]);
  }, [projectName]);

  // Scroll hacia abajo cuando hay nuevos mensajes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Función para detectar modificaciones en el texto del usuario
  const detectDirectModification = (text: string): ModificationData | null => {
    const userText = text.toLowerCase();
    
    // Mapeo de secciones y sus palabras clave
    const sectionKeywords: {[key: string]: string[]} = {
      '1. OBJETO': ['objeto', 'propósito', 'finalidad', 'objetivo'],
      '2. DESCRIPCIÓN DEL PROYECTO': ['descripción', 'proyecto', 'detalles', 'resumen'],
      '2.1 FUNCIONALIDADES PRINCIPALES': ['funcionalidades', 'características', 'features', 'capacidades'],
      '3. PLANIFICACIÓN': ['planificación', 'cronograma', 'calendario', 'plazo', 'duración', 'tiempo'],
      '4. COSTE': ['coste', 'costo', 'precio', 'presupuesto', 'valor', 'importe'],
      '5. FIRMAS': ['firmas', 'firma', 'firmantes', 'autorización']
    };
    
    // Patrones específicos para duración/plazo
    const durationPatterns = [
      // Patrones para cambiar la duración
      /hay que (?:cambiar|modificar)(?:la|lo)? a ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
      /cambiar(?:la|lo)? a ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
      /modificar(?:la|lo)? a ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
      /(?:la )?duración (?:debe ser|tiene que ser|será|es) ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
      /(?:el )?plazo (?:debe ser|tiene que ser|será|es) ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
      /(?:el )?tiempo (?:debe ser|tiene que ser|será|es) ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
    ];
    
    // Verificar patrones de duración primero
    for (const pattern of durationPatterns) {
      const match = userText.match(pattern);
      if (match && match[1]) {
        const value = parseFloat(match[1].replace(/,/g, '.'));
        const unit = match[2] || 'semanas';
        console.log('Detectada modificación de duración:', value, unit);
        return {
          type: 'time',
          section: '3. PLANIFICACIÓN',
          value: value,
          unit: unit,
          content: `La duración estimada del proyecto es de ${value} ${unit}.`,
          originalQuery: text
        };
      }
    }
    
    // Patrones generales para cualquier modificación numérica
    const generalModificationPatterns = [
      /hay que (?:cambiarlo|modificarlo|actualizarlo|ponerlo) (?:a|por|en) ([0-9.,]+)\s*(€|euros|eur|semanas?|meses?|días?|horas?)?/i,
      /hay que (?:cambiar|modificar|actualizar|poner) (?:a|por|en) ([0-9.,]+)\s*(€|euros|eur|semanas?|meses?|días?|horas?)?/i,
      /(?:cambiar|modificar|actualizar|poner) (?:a|por|en) ([0-9.,]+)\s*(€|euros|eur|semanas?|meses?|días?|horas?)?/i,
    ];
    
    // Verificar patrones generales
    for (const pattern of generalModificationPatterns) {
      const match = userText.match(pattern);
      if (match && match[1]) {
        const value = parseFloat(match[1].replace(/,/g, '.'));
        const unit = match[2] || '';
        
        // Determinar el tipo basado en la unidad o el contexto
        if (unit.match(/€|euros?|eur/i) || userText.includes('coste') || userText.includes('precio') || userText.includes('presupuesto')) {
          console.log('Detectada modificación de coste:', value, unit || '€');
          return {
            type: 'cost',
            section: '4. COSTE',
            value: value,
            unit: '€',
            content: `El coste total estimado para el proyecto es de ${value}€.`,
            originalQuery: text
          };
        } else if (unit.match(/semanas?|meses?|días?|horas?/i) || 
                  userText.includes('plazo') || 
                  userText.includes('duración') || 
                  userText.includes('tiempo') || 
                  userText.includes('planificación') || 
                  userText.includes('sección 3')) {
          console.log('Detectada modificación de tiempo:', value, unit || 'semanas');
          return {
            type: 'time',
            section: '3. PLANIFICACIÓN',
            value: value,
            unit: unit || 'semanas',
            content: `La duración estimada del proyecto es de ${value} ${unit || 'semanas'}.`,
            originalQuery: text
          };
        }
      }
    }
    
    // Patrones específicos para cambio de coste
    const costPatterns = [
      /hay que cambiarlo por ([0-9.,]+)\s*(€|euros|eur)?/i,
      /cambiar(?:\w+)? (?:a|por) ([0-9.,]+)\s*(€|euros|eur)?/i,
      /modificar(?:\w+)? (?:a|por) ([0-9.,]+)\s*(€|euros|eur)?/i,
      /coste(?:\w+)? (?:a|de|por) ([0-9.,]+)\s*(€|euros|eur)?/i,
      /precio(?:\w+)? (?:a|de|por) ([0-9.,]+)\s*(€|euros|eur)?/i,
      /poner(?:\w+)? (?:a|en) ([0-9.,]+)\s*(€|euros|eur)?/i
    ];
    
    // Patrones específicos para plazo/duración
    const timePatterns = [
      /plazo(?:\w+)? (?:a|de|por) ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
      /duración(?:\w+)? (?:a|de|por) ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i,
      /tiempo(?:\w+)? (?:a|de|por) ([0-9.,]+)\s*(semanas?|meses?|días?|horas?)?/i
    ];
    
    // Verificar patrones de coste
    for (const pattern of costPatterns) {
      const match = userText.match(pattern);
      if (match && match[1]) {
        const value = parseFloat(match[1].replace(/,/g, '.'));
        return {
          type: 'cost',
          section: '4. COSTE',
          value: value,
          unit: match[2] || '€',
          content: `El coste total estimado para el proyecto es de ${value}€.`,
          originalQuery: text
        };
      }
    }
    
    // Verificar patrones de tiempo
    for (const pattern of timePatterns) {
      const match = userText.match(pattern);
      if (match && match[1]) {
        const value = parseFloat(match[1].replace(/,/g, '.'));
        const unit = match[2] || 'semanas';
        return {
          type: 'time',
          section: '3. PLANIFICACIÓN',
          value: value,
          unit: unit,
          content: `La duración estimada del proyecto es de ${value} ${unit}.`,
          originalQuery: text
        };
      }
    }
    
    // Detectar si es una solicitud de modificación general
    const modificationIndicators = [
      'modifica', 'cambia', 'actualiza', 'edita', 'ajusta', 'corrige',
      'hay que', 'debe ser', 'debería ser', 'tiene que ser',
      'poner', 'cambiar', 'actualizar', 'modificar'
    ];
    
    const isModificationRequest = modificationIndicators.some(indicator => 
      userText.includes(indicator)
    );
    
    if (!isModificationRequest) return null;
    
    // Identificar la sección mencionada en el texto
    let targetSection = null;
    
    // Buscar palabras clave de secciones
    for (const [section, keywords] of Object.entries(sectionKeywords)) {
      if (keywords.some(keyword => userText.includes(keyword))) {
        targetSection = section;
        break;
      }
    }
    
    // Si no se detectó una sección específica, intentar inferirla
    if (!targetSection) {
      // Detectar si habla de dinero (coste)
      if (userText.match(/[0-9.,]+\s*(€|euros|eur)/i)) {
        targetSection = '4. COSTE';
      }
      // Detectar si habla de tiempo (planificación)
      else if (userText.match(/[0-9.,]+\s*(semanas?|meses?|días?|horas?)/i)) {
        targetSection = '3. PLANIFICACIÓN';
      }
      // Por defecto, asumimos que es una modificación general
      else {
        targetSection = 'general';
      }
    }
    
    // Extraer el contenido a modificar
    const contentMatch = userText.match(/(?:a|en|por|como|con)\s+['"]?([^'"]+)['"]?\s*$/i);
    const newContent = contentMatch ? contentMatch[1].trim() : null;
    
    // Detectar valores numéricos (para coste o tiempo)
    const numberMatch = userText.match(/([0-9.,]+)\s*(€|euros|eur|semanas?|meses?|días?|horas?)?/i);
    let numericValue = null;
    let unit = null;
    
    if (numberMatch) {
      numericValue = parseFloat(numberMatch[1].replace(/,/g, '.'));
      unit = numberMatch[2] || (targetSection === '4. COSTE' ? '€' : 'semanas');
    }
    
    return {
      type: targetSection === '4. COSTE' ? 'cost' : 
            targetSection === '3. PLANIFICACIÓN' ? 'time' : 'content',
      section: targetSection,
      value: numericValue,
      unit: unit,
      content: newContent || text,
      originalQuery: text
    };
  };

  // Función para aplicar modificaciones directamente
  const applyDirectModification = async (modification: ModificationData): Promise<boolean> => {
    try {
      // Obtener el token de autenticación
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No se encontró el token de autenticación');
      }
      
      // Validar que tenemos los datos necesarios
      if (!modification.type) {
        throw new Error('Tipo de modificación no especificado');
      }
      
      if (modification.type === 'time' && !modification.value) {
        throw new Error('Valor de duración no especificado');
      }
      
      if (modification.type === 'cost' && !modification.value) {
        throw new Error('Valor de coste no especificado');
      }
      
      // Preparar los datos para la modificación
      const modificationData = {
        section: modification.section,
        type: modification.type,
        value: modification.value,
        unit: modification.unit,
        content: modification.content
      };
      
      console.log('Aplicando modificación directa:', modificationData);
      
      // Construir la URL correcta para la API
      // Usar la URL base actual y añadir el puerto 8000 para el backend
      const baseUrl = window.location.hostname === 'localhost' ? 'http://localhost:8000' : 
                   `${window.location.protocol}//${window.location.hostname}:8000`;
      const apiUrl = `${baseUrl}/api/v1/projects/${projectId}/edit`;
      
      console.log('URL de la API:', apiUrl);
      console.log('Datos enviados:', JSON.stringify(modificationData));
      
      // Llamar a la API para modificar el documento
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(modificationData),
      });
      
      console.log('Respuesta de la API:', response.status);
      
      // Manejar respuestas no exitosas
      if (!response.ok) {
        let errorMessage = `Error al modificar el documento: ${response.status} ${response.statusText}`;
        
        try {
          const errorData = await response.json();
          console.error('Error detallado:', errorData);
          if (errorData.detail) {
            errorMessage = errorData.detail;
          }
        } catch (e) {
          // Ignorar errores al intentar parsear la respuesta como JSON
        }
        
        throw new Error(errorMessage);
      }
      
      // Si llegamos aquí, la modificación fue exitosa
      const successResponse = await response.json();
      console.log('Modificación aplicada exitosamente:', successResponse);
      
      // Añadir mensaje de confirmación
      setMessages(prev => [...prev, { 
        text: `He actualizado el documento con los cambios solicitados. La sección '${modification.section}' ha sido modificada.`, 
        sender: 'assistant' 
      }]);
      
      return true;
    } catch (error) {
      console.error('Error al aplicar modificación directa:', error);
      
      // Añadir mensaje de error
      setMessages(prev => [...prev, { 
        text: `Lo siento, no he podido aplicar los cambios solicitados. ${error instanceof Error ? error.message : 'Ocurrió un error desconocido'}`, 
        sender: 'assistant' 
      }]);
      
      return false;
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    
    // Añadir mensaje del usuario
    setMessages(prev => [...prev, { text: input, sender: 'user' }]);
    setIsLoading(true);
    
    // Detectar si es una solicitud de modificación directa
    const directModification = detectDirectModification(input);
    
    if (directModification) {
      // Si es una modificación directa, aplicarla inmediatamente
      const success = await applyDirectModification(directModification);
      setIsLoading(false);
      setInput('');
      
      // Si la modificación se aplicó con éxito, no necesitamos continuar
      if (success) return;
    }
    
    // Si no es una modificación directa o falló, seguimos con el flujo normal
    try {
      // Obtener el token de autenticación
      const token = localStorage.getItem('token');
      
      // Llamar a la API para obtener respuesta
      const response = await fetch(`/api/v1/projects/${projectId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // Añadir token de autenticación
        },
        body: JSON.stringify({ query: input }),
      });
      
      if (!response.ok) {
        throw new Error('Error al obtener respuesta');
      }
      
      const data = await response.json();
      
      // Añadir respuesta del asistente
      setMessages(prev => [...prev, { 
        text: data.response, 
        sender: 'assistant',
        documentReference: data.document_reference,
        isModificationRequest: data.is_modification_request
      }]);
      
      // Si hay una referencia a una sección, ofrecer acciones
      if (data.document_reference) {
        // Extraer la sección del documento de la referencia
        const sectionMatch = data.document_reference.match(/'([^']+)'/);
        if (sectionMatch && sectionMatch[1] && onScrollToSection) {
          onScrollToSection(sectionMatch[1]);
        }
      }
      
      // Si es una petición de modificación, guardar la información
      if (data.is_modification_request) {
        // Extraer la sección si existe
        const sectionMatch = data.response.match(/'([^']+)'/);
        const section = sectionMatch ? sectionMatch[1] : null;
        
        // Guardar la información de modificación pendiente
        setPendingModification(section);
      }
    } catch (error) {
      console.error('Error en chat:', error);
      setMessages(prev => [...prev, { 
        text: "Lo siento, ocurrió un error al procesar tu consulta. Por favor, inténtalo de nuevo.", 
        sender: 'assistant' 
      }]);
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };

  return (
    <Card className={`fixed bottom-4 right-4 shadow-lg transition-all duration-300 ${isMinimized ? 'h-12 w-12' : 'h-96 w-80'}`}>
      {isMinimized ? (
        <Button 
          className="w-full h-full rounded-full flex items-center justify-center"
          onClick={() => setIsMinimized(false)}
        >
          <MessageSquare size={24} />
        </Button>
      ) : (
        <>
          <div className="flex justify-between items-center p-3 border-b">
            <h3 className="font-medium">Consulta sobre tu presupuesto</h3>
            <div className="flex space-x-1">
              <Button 
                variant="ghost" 
                size="sm" 
                className="h-6 w-6 p-0" 
                onClick={() => setIsMinimized(true)}
              >
                <ChevronDown size={18} />
              </Button>
            </div>
          </div>
          
          <div className="flex-1 p-3 overflow-y-auto h-[calc(100%-6rem)]">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`mb-3 p-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-100 ml-8'
                    : 'bg-gray-100 mr-8'
                }`}
              >
                {message.text.split('\n').map((line, i) => (
                  <p key={i} className={`text-sm ${i > 0 ? 'mt-1' : ''}`}>
                    {line}
                  </p>
                ))}
                
                {message.isModificationRequest && onRequestEdit && (
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="mt-2 text-xs"
                    onClick={() => {
                      // Si el mensaje tiene sección referenciada, pásala
                      const sectionMatch = message.text.match(/'([^']+)'/);
                      onRequestEdit(sectionMatch ? sectionMatch[1] : undefined);
                    }}
                  >
                    <Edit2 size={12} className="mr-1" /> Editar documento
                  </Button>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="p-3 border-t">
            <div className="flex space-x-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Escribe tu consulta..."
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                disabled={isLoading}
                className="text-sm"
              />
              <Button 
                onClick={handleSendMessage} 
                disabled={isLoading} 
                size="sm"
              >
                {isLoading ? <Spinner size="sm" /> : 'Enviar'}
              </Button>
            </div>
          </div>
        </>
      )}
    </Card>
  );
};

export default PDFChat;