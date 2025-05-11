def generar_mensaje_ia(datos_lead, tipo="inicial", modo="para_mi"):
    nombre = datos_lead.get("nombre", "there")
    empresa = datos_lead.get("empresa", "")
    sector = datos_lead.get("sector", "your industry")

    if modo == "para_mi":
        remitente = "I"
        servicio = "my AI-driven prospecting services"
    else:
        remitente = "we"
        servicio = "our client’s AI-based sales outreach system"

    if tipo == "inicial":
        asunto = f"Quick idea for {empresa}"
        cuerpo = f"""Hi {nombre},

My name is Stephen and I help companies in {sector} like {empresa} grow using {servicio}.

Would you be open to a quick call next week to explore how this could benefit {empresa}?

Best regards,  
Stephen  
NovaProspectAI"""
    
    elif tipo == "seguimiento":
        asunto = f"Following up on my idea for {empresa}"
        cuerpo = f"""Hi {nombre},

Just wanted to follow up on the message I sent recently about helping {empresa} grow with AI-powered prospecting.

Let me know if you'd like to take a quick look — no pressure at all.

Best,  
Stephen  
NovaProspectAI"""

    elif tipo == "cierre":
        asunto = f"Last note about {empresa}"
        cuerpo = f"""Hi {nombre},

This will be my last message — I thought {empresa} might benefit from a smarter outreach strategy using AI, but I don’t want to be a bother.

If it ever becomes relevant, feel free to reach out. Wishing you success!

Cheers,  
Stephen  
NovaProspectAI"""
    
    else:
        raise ValueError("Tipo de mensaje no válido")

    return asunto, cuerpo