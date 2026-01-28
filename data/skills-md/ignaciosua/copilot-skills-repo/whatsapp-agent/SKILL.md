---
name: whatsapp-agent
description: "Enviar mensajes de WhatsApp (contactos y grupos) reutilizando las secuencias existentes de macro-agent. Los mensajes se procesan para estar en minúsculas y sin acentos. Comandos: list, send <contacto> <mensaje>." 
---

# WhatsApp Agent

Skill de alto nivel para **enviar mensajes de WhatsApp** usando las secuencias ya configuradas en macro-agent (`~/.copilot/skills/macro-agent/data/sequences`).

## Cuando usarlo
- El usuario pide "manda un WhatsApp a X", "envia mensaje a Marco", "mensaje al grupo".
- Cuando quieras usar secuencias `whatsapp_send_*` ya creadas.

## Comandos
- `list` - Muestra contactos/grupos disponibles (derivados de secuencias `whatsapp_send_*`).
- `send <contacto> <mensaje>` - Envia el mensaje al contacto/grupo. El mensaje se procesa automáticamente: minúsculas y sin acentos.

## Destinatarios actuales (derivados de secuencias existentes)
- marco
- ross
- abril
- amigos_x
- conspiraciones

*(Se detectan automáticamente todos los `whatsapp_send_<nombre>` que existan en macro-agent.)*

## Procesamiento de mensajes
Los mensajes se procesan automáticamente para:
- Convertir a minúsculas
- Eliminar acentos

## Flujo interno (lo que hace este skill)
1. Busca la secuencia `whatsapp_send_<contacto>` en macro-agent.
2. Procesa el mensaje según las reglas establecidas.
3. Ejecuta `seq-run` de macro-agent para abrir WhatsApp y enfocar el chat.
4. Ejecuta `write "<mensaje_procesado>"`.
5. Ejecuta `press enter` para enviar.

## Notas
- Si agregas un nuevo contacto, crea la secuencia en macro-agent con el patron `whatsapp_send_<alias>` y este skill lo reconocera automaticamente.
- Usa nombres simples (sin espacios) en el alias de la secuencia. Puedes usar guiones bajos.
- El skill preserva la voz del usuario y envía mensajes directos.
- **Importante para el LLM**: Separa claramente las instrucciones del usuario (como "manda este mensaje a X") del contenido del mensaje a enviar. No incluyas las instrucciones en el mensaje procesado.
