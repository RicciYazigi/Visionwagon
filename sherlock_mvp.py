from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
from datetime import datetime

app = FastAPI(title="Sherlock MVP", description="Sistema de análisis de leads", version="1.0.0")

# Modelos de datos
class LeadData(BaseModel):
    nombre: str
    empresa: str
    facturacion_anual: float  # en USD
    empleados: int
    industria: str
    pain_points: List[str]
    presupuesto_marketing: float  # en USD
    canales_actuales: List[str]
    objetivos_principales: List[str]
    urgencia: int  # 1-10
    decision_maker: bool
    
class SherlockResponse(BaseModel):
    lead_id: str
    timestamp: str
    scoring: Dict
    diagnostico: Dict
    recomendaciones: Dict

# Lógica de scoring
def calcular_scoring(lead: LeadData) -> Dict:
    """Calcula el score del lead basado en múltiples factores"""
    
    # Score financiero (0-30 puntos)
    if lead.facturacion_anual >= 1000000:
        score_financiero = 30
    elif lead.facturacion_anual >= 500000:
        score_financiero = 20
    elif lead.facturacion_anual >= 100000:
        score_financiero = 15
    else:
        score_financiero = 5
    
    # Score de tamaño (0-20 puntos)
    if lead.empleados >= 100:
        score_tamano = 20
    elif lead.empleados >= 50:
        score_tamano = 15
    elif lead.empleados >= 10:
        score_tamano = 10
    else:
        score_tamano = 5
    
    # Score de presupuesto marketing (0-25 puntos)
    ratio_marketing = lead.presupuesto_marketing / lead.facturacion_anual if lead.facturacion_anual > 0 else 0
    if ratio_marketing >= 0.1:  # 10% o más
        score_presupuesto = 25
    elif ratio_marketing >= 0.05:  # 5-10%
        score_presupuesto = 20
    elif ratio_marketing >= 0.02:  # 2-5%
        score_presupuesto = 15
    else:
        score_presupuesto = 5
    
    # Score de urgencia (0-15 puntos)
    score_urgencia = (lead.urgencia / 10) * 15
    
    # Score de autoridad (0-10 puntos)
    score_autoridad = 10 if lead.decision_maker else 3
    
    # Score total
    score_total = score_financiero + score_tamano + score_presupuesto + score_urgencia + score_autoridad
    
    # Clasificación
    if score_total >= 80:
        clasificacion = "HOT"
        prioridad = "ALTA"
    elif score_total >= 60:
        clasificacion = "WARM"
        prioridad = "MEDIA"
    elif score_total >= 40:
        clasificacion = "COLD"
        prioridad = "BAJA"
    else:
        clasificacion = "UNQUALIFIED"
        prioridad = "MUY BAJA"
    
    return {
        "score_total": round(score_total, 1),
        "score_financiero": score_financiero,
        "score_tamano": score_tamano,
        "score_presupuesto": score_presupuesto,
        "score_urgencia": round(score_urgencia, 1),
        "score_autoridad": score_autoridad,
        "clasificacion": clasificacion,
        "prioridad": prioridad,
        "porcentaje": round((score_total / 100) * 100, 1)
    }

def generar_diagnostico(lead: LeadData, scoring: Dict) -> Dict:
    """Genera diagnóstico detallado del lead"""
    
    # Análisis de fortalezas
    fortalezas = []
    if scoring["score_financiero"] >= 20:
        fortalezas.append("Empresa con sólida capacidad financiera")
    if scoring["score_tamano"] >= 15:
        fortalezas.append("Organización de tamaño considerable")
    if scoring["score_presupuesto"] >= 20:
        fortalezas.append("Presupuesto de marketing bien dimensionado")
    if scoring["score_urgencia"] >= 10:
        fortalezas.append("Alta urgencia en la necesidad")
    if lead.decision_maker:
        fortalezas.append("Contacto directo con tomador de decisiones")
    
    # Análisis de debilidades
    debilidades = []
    if scoring["score_financiero"] < 15:
        debilidades.append("Capacidad financiera limitada")
    if scoring["score_presupuesto"] < 15:
        debilidades.append("Presupuesto de marketing insuficiente")
    if scoring["score_urgencia"] < 8:
        debilidades.append("Baja urgencia en la implementación")
    if not lead.decision_maker:
        debilidades.append("No es el decisor final")
    
    # Análisis de industria
    industrias_digitales = ["tecnología", "software", "ecommerce", "fintech", "saas"]
    industrias_tradicionales = ["manufactura", "construcción", "agricultura", "retail físico"]
    
    if any(ind in lead.industria.lower() for ind in industrias_digitales):
        perfil_digital = "ALTO - Industria naturalmente digital"
    elif any(ind in lead.industria.lower() for ind in industrias_tradicionales):
        perfil_digital = "MEDIO - Industria en proceso de digitalización"
    else:
        perfil_digital = "VARIABLE - Requiere análisis específico"
    
    # Pain points principales
    pain_analysis = {}
    for pain in lead.pain_points:
        if "lead" in pain.lower() or "cliente" in pain.lower():
            pain_analysis["generación_leads"] = "Crítico"
        elif "conversión" in pain.lower() or "venta" in pain.lower():
            pain_analysis["conversión"] = "Crítico"
        elif "automatización" in pain.lower() or "proceso" in pain.lower():
            pain_analysis["automatización"] = "Importante"
        elif "seguimiento" in pain.lower() or "nurturing" in pain.lower():
            pain_analysis["nurturing"] = "Importante"
    
    return {
        "resumen": f"Lead {scoring['clasificacion']} con {scoring['porcentaje']}% de fit",
        "fortalezas": fortalezas,
        "debilidades": debilidades,
        "perfil_digital": perfil_digital,
        "pain_points_criticos": pain_analysis,
        "potencial_ingresos": lead.presupuesto_marketing * 0.3,  # Estimación conservadora
        "tiempo_estimado_cierre": "2-4 semanas" if scoring["clasificacion"] == "HOT" else "1-3 meses"
    }

def generar_recomendaciones(lead: LeadData, scoring: Dict, diagnostico: Dict) -> Dict:
    """Genera recomendaciones específicas para cada agente"""
    
    # Recomendaciones para Dali (Creatividad/Contenido)
    dali_tasks = []
    if "generación_leads" in diagnostico["pain_points_criticos"]:
        dali_tasks.append("Crear case study específico para su industria")
        dali_tasks.append("Diseñar landing page personalizada")
    if scoring["clasificacion"] in ["HOT", "WARM"]:
        dali_tasks.append("Preparar propuesta visual personalizada")
        dali_tasks.append("Crear demo interactivo del producto")
    
    # Recomendaciones para Zuckerberg (Paid Media)
    zuckerberg_tasks = []
    if scoring["score_presupuesto"] >= 20:
        zuckerberg_tasks.append("Proponer estrategia de LinkedIn Ads B2B")
        zuckerberg_tasks.append("Configurar campañas de retargeting")
    if lead.urgencia >= 7:
        zuckerberg_tasks.append("Implementar campaña de urgencia limitada")
    
    zuckerberg_tasks.append(f"Presupuesto sugerido: ${int(lead.presupuesto_marketing * 0.4)}/mes")
    
    # Recomendaciones para Coach (Seguimiento/Conversión)
    coach_tasks = []
    if scoring["clasificacion"] == "HOT":
        coach_tasks.append("Agendar demo en próximas 48h")
        coach_tasks.append("Preparar propuesta comercial personalizada")
    elif scoring["clasificacion"] == "WARM":
        coach_tasks.append("Secuencia de nurturing de 5 emails")
        coach_tasks.append("Llamada de descubrimiento en 1 semana")
    else:
        coach_tasks.append("Incluir en secuencia de educación mensual")
        coach_tasks.append("Seguimiento trimestral de re-calificación")
    
    # Próximos pasos priorizados
    if scoring["clasificacion"] == "HOT":
        proximos_pasos = [
            "🔥 URGENTE: Coach agenda demo en 24-48h",
            "🎨 Dali prepara propuesta visual personalizada",
            "📱 Zuckerberg configura retargeting inmediato"
        ]
    elif scoring["clasificacion"] == "WARM":
        proximos_pasos = [
            "📞 Coach programa llamada de descubrimiento",
            "🎯 Zuckerberg inicia campaña de nurturing",
            "📄 Dali crea contenido educativo específico"
        ]
    else:
        proximos_pasos = [
            "📧 Coach incluye en secuencia automatizada",
            "📊 Seguimiento mensual de comportamiento",
            "🔄 Re-evaluación en 90 días"
        ]
    
    return {
        "dali": {
            "prioridad": "ALTA" if scoring["clasificacion"] in ["HOT", "WARM"] else "MEDIA",
            "tareas": dali_tasks,
            "deadline": "48h" if scoring["clasificacion"] == "HOT" else "1 semana"
        },
        "zuckerberg": {
            "prioridad": "ALTA" if scoring["score_presupuesto"] >= 20 else "MEDIA",
            "tareas": zuckerberg_tasks,
            "presupuesto_sugerido": int(lead.presupuesto_marketing * 0.4)
        },
        "coach": {
            "prioridad": "CRÍTICA" if scoring["clasificacion"] == "HOT" else "ALTA",
            "tareas": coach_tasks,
            "seguimiento": "Inmediato" if scoring["clasificacion"] == "HOT" else "1-2 semanas"
        },
        "proximos_pasos": proximos_pasos,
        "timeline_estimado": diagnostico["tiempo_estimado_cierre"]
    }

# Endpoints API
@app.get("/")
def root():
    return {"message": "Sherlock MVP - Sistema de análisis de leads", "version": "1.0.0"}

@app.post("/analyze", response_model=SherlockResponse)
def analyze_lead(lead: LeadData):
    """Analiza un lead y retorna scoring, diagnóstico y recomendaciones"""
    
    try:
        # Generar ID único para el lead
        lead_id = f"LEAD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Procesar análisis
        scoring = calcular_scoring(lead)
        diagnostico = generar_diagnostico(lead, scoring)
        recomendaciones = generar_recomendaciones(lead, scoring, diagnostico)
        
        response = SherlockResponse(
            lead_id=lead_id,
            timestamp=datetime.now().isoformat(),
            scoring=scoring,
            diagnostico=diagnostico,
            recomendaciones=recomendaciones
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando lead: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Endpoint para testing rápido
@app.get("/test")
def test_endpoint():
    """Endpoint de prueba con datos de ejemplo"""
    
    sample_lead = LeadData(
        nombre="Ricardo Empresario",
        empresa="TechCorp Solutions",
        facturacion_anual=800000,
        empleados=45,
        industria="tecnología",
        pain_points=["generación de leads", "automatización de procesos"],
        presupuesto_marketing=40000,
        canales_actuales=["Google Ads", "LinkedIn"],
        objetivos_principales=["aumentar leads", "mejorar conversión"],
        urgencia=8,
        decision_maker=True
    )
    
    return analyze_lead(sample_lead)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)