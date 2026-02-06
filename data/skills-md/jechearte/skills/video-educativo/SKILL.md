---
name: video-educativo
description: |
  Genera videos educativos animados con narración de voz usando Remotion y ElevenLabs.
  Usar cuando el usuario pida crear un video explicativo, tutorial, o educativo sobre cualquier tema.
  Triggers: "crear video", "generar video educativo", "video explicativo", "tutorial animado",
  "video con narración", "explicar con video", "video para enseñar".
---

# Video Educativo - Ecuademy

Genera videos educativos de matemáticas para Ecuademy (academia de matemáticas virtual).

**Skills requeridas:** `/elevenlabs-tts`, `/remotion`

---

## Índice de Tareas (Orden de Ejecución)

El agente DEBE seguir este orden de tareas:

| # | Tarea | Tipo | Sección |
|---|-------|------|---------|
| 1 | Crear estructura del proyecto Remotion | Secuencial | §1 |
| 2 | Crear componente Whiteboard.tsx | Secuencial | §2 |
| 3 | Escribir guiones de cada escena | Secuencial | §3 |
| 4 | Crear planificación visual (PLANIFICACION.md) | Secuencial | §3 |
| 5 | **PAUSA: Esperar aprobación del usuario** | PAUSA | §3.1 |
| 6 | Generar audios con ElevenLabs TTS | Secuencial | §4 |
| 7 | Acelerar audios con ffmpeg | Secuencial | §4 |
| 8 | Transcribir audios con Whisper | Secuencial | §5 |
| 9 | Generar componentes de escenas | Secuencial | §6 |
| 10 | Crear MainComposition.tsx y Root.tsx | Secuencial | §7 |
| 11 | Verificar compilación TypeScript | Secuencial | §8 |
| 12 | Renderizar video | Secuencial | §8 |

---

## §1. Estructura del Proyecto

```
proyecto/
├── public/
│   ├── audio/
│   │   ├── scene1.mp3
│   │   └── ...
│   └── logo_cuadrado_ecuademy.png
├── src/
│   ├── components/
│   │   ├── scenes/
│   │   │   ├── Scene1Problema.tsx
│   │   │   ├── Scene2Datos.tsx
│   │   │   └── ...
│   │   └── shared/
│   │       └── Whiteboard.tsx
│   ├── data/
│   │   ├── scene1_timestamps.json
│   │   └── ...
│   ├── Root.tsx
│   └── MainComposition.tsx
├── scripts/
│   ├── transcribe_audio.py
│   ├── guiones/
│   │   ├── scene1.txt
│   │   └── ...
│   └── PLANIFICACION.md
└── package.json
```

Dependencias necesarias:
```bash
npm install remotion @remotion/cli @remotion/bundler @remotion/renderer @remotion/media-utils @remotion/transitions @remotion/google-fonts react react-dom typescript
```

---

## §2. Componente Whiteboard.tsx

Crear en `src/components/shared/Whiteboard.tsx`:

```typescript
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';

interface WhiteboardProps {
  children: React.ReactNode;
}

export const Whiteboard: React.FC<WhiteboardProps> = ({ children }) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#FAFAFA',
        backgroundImage: `
          linear-gradient(90deg, rgba(200,200,200,0.03) 1px, transparent 1px),
          linear-gradient(rgba(200,200,200,0.03) 1px, transparent 1px)
        `,
        backgroundSize: '20px 20px',
      }}
    >
      {/* Marco superior */}
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 12, backgroundColor: '#146A4B' }} />
      {/* Marco inferior */}
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 12, backgroundColor: '#146A4B' }} />
      {/* Contenido */}
      <div style={{ padding: '30px 60px', height: '100%', boxSizing: 'border-box' }}>
        {children}
      </div>
      {/* Logo Ecuademy */}
      <Img
        src={staticFile('logo_cuadrado_ecuademy.png')}
        style={{ position: 'absolute', bottom: 30, right: 40, width: 70, height: 70, opacity: 0.85 }}
      />
    </AbsoluteFill>
  );
};
```

### Identidad Visual Ecuademy

| Elemento | Color | Uso |
|----------|-------|-----|
| Títulos/Énfasis | `#146A4B` | Verde Ecuademy |
| Texto principal | `#2C3E50` | Texto normal |
| Resultados | `#27AE60` | Verde para respuestas |
| Importante | `#E74C3C` | Rojo para destacar |
| Cajas resaltadas | `#E8F5E9` | Fondo verde claro |

---

## §3. Planificación y Guiones

Planifica el contenido del vídeo. El vídeo debe ayudar al alumno a comprender cómo se resuelve el ejercicio, ten en cuenta que el alumno ya ha intentado resolver el ejercicio y ha tenido dificultados, por lo que explicale todo bien para que lo comprenda. El alumno es un estudiante de secundaria en España, no des por hecho que tiene conocimientos que no tiene.

### Estructura obligatoria del video

1. **Escena 1 - Presentación del problema**: Enunciado completo
2. **Escenas intermedias**: Desarrollo paso a paso
3. **Escena final**: Respuesta y conclusión

### Archivos a crear

1. **Guiones** en `scripts/guiones/sceneN.txt` - Solo texto de narración
2. **Planificación** en `scripts/PLANIFICACION.md` - Descripción visual de cada escena

---

## §3.1. PAUSA: Aprobación de Planificación (OBLIGATORIO)

**IMPORTANTE: El agente DEBE detenerse aquí y esperar la aprobación del usuario.**

Después de crear los guiones y la planificación visual, el agente debe:

1. **Mostrar un resumen** de lo creado:
   - Número de escenas planificadas
   - Duración estimada del video
   - Estructura general del contenido

2. **Indicar los archivos a revisar**:
   - `scripts/PLANIFICACION.md` - Diseño visual detallado de cada escena
   - `scripts/guiones/scene*.txt` - Textos de narración

3. **Preguntar explícitamente al usuario**:
   > "He completado la planificación visual y los guiones. Por favor revisa los archivos:
   > - `scripts/PLANIFICACION.md`
   > - `scripts/guiones/`
   >
   > ¿Está todo correcto? ¿Puedo continuar con la generación de audios y escenas?"
   > ¿Cuánto debo acelerar el vídeo?

4. **Esperar respuesta** antes de continuar con §4.

### Qué revisar en la planificación

El usuario debe verificar:
- Correctitud matemática del problema y solución
- Orden lógico de las escenas
- Descripción clara de elementos visuales
- Posición correcta de figuras, etiquetas y símbolos
- Colores y estilos apropiados

### Continuar solo si

El usuario responde afirmativamente (ej: "ok", "continúa", "aprobado", "sí", "correcto").

Si el usuario indica cambios, el agente debe modificar los guiones/planificación y volver a pedir aprobación.
El usuario indicará cuanto quiere acelerar el audio del vídeo, tenlo en cuenta para el siguiente paso.

---

## §4. Generación de Audio

### Paso 1: Generar con ElevenLabs

Usar `/elevenlabs-tts` para cada guion:
```bash
python3 scripts/generate_audio.py "texto del guion" public/audio/sceneN_original.mp3
```

### Paso 2: Acelerar con ffmpeg

```bash
for f in public/audio/*_original.mp3; do
  output="${f/_original/}"
  ffmpeg -y -i "$f" -filter:a "atempo=1.5" "$output"
done
```

### Paso 3: Obtener duraciones

```bash
# macOS
afinfo public/audio/scene1.mp3 | grep duration

# Linux
ffprobe -i public/audio/scene1.mp3 -show_entries format=duration -v quiet -of csv="p=0"
```

---

## §5. Transcripción con Whisper

Crear `scripts/transcribe_audio.py`:

```python
import whisper, json, glob
from pathlib import Path

model = whisper.load_model("base")

for audio_path in sorted(glob.glob("public/audio/scene*.mp3")):
    if "_original" in audio_path:
        continue
    scene_name = Path(audio_path).stem
    result = model.transcribe(audio_path, language="es", word_timestamps=True)
    words = [{"word": w["word"].strip(), "start": round(w["start"], 2)}
             for seg in result["segments"] if "words" in seg for w in seg["words"]]
    output = {"scene": scene_name, "text": result["text"], "words": words}
    Path("src/data").mkdir(parents=True, exist_ok=True)
    with open(f"src/data/{scene_name}_timestamps.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
```

Ejecutar: `python3 scripts/transcribe_audio.py`

---

## §6. Generación de Escenas

Crear cada componente de escena en `src/components/scenes/` siguiendo el patrón obligatorio.

### Patrón obligatorio para cada escena

```typescript
import { Audio, interpolate, useCurrentFrame, useVideoConfig, staticFile } from 'remotion';
import { loadFont } from '@remotion/google-fonts/Caveat';
import { Whiteboard } from '../shared/Whiteboard';

const { fontFamily: caveat } = loadFont();

export const SceneNNombre: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  const TIMESTAMPS = { /* extraídos de Whisper */ };

  // Fade in simple
  const getOpacity = (start: number) => {
    return interpolate(currentTime, [start, start + 0.3], [0, 1],
      { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  };

  // ✍️ ANIMACIÓN DE ESCRITURA EN PIZARRA
  // Simula que el texto se escribe carácter por carácter
  const writeText = (text: string, start: number, charsPerSecond: number = 15) => {
    const duration = text.length / charsPerSecond;
    const progress = interpolate(currentTime, [start, start + duration], [0, text.length],
      { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
    return text.substring(0, Math.floor(progress));
  };

  return (
    <Whiteboard>
      <Audio src={staticFile('audio/sceneN.mp3')} />
      <svg width="100%" height="100%" viewBox="0 0 1920 1080">
        {/* Contenido con efecto escritura */}
      </svg>
    </Whiteboard>
  );
};
```

### Animación de Escritura en Pizarra

**IMPORTANTE:** Todo texto matemático debe aparecer con efecto de escritura, NO instantáneamente.

#### Función `writeText`

```typescript
// Parámetros:
// - text: El texto a escribir
// - start: Timestamp de inicio (segundos)
// - charsPerSecond: Velocidad de escritura (default: 15 chars/s)

const writeText = (text: string, start: number, charsPerSecond: number = 15) => {
  const duration = text.length / charsPerSecond;
  const progress = interpolate(currentTime, [start, start + duration], [0, text.length],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return text.substring(0, Math.floor(progress));
};
```

#### Uso en SVG

```tsx
// Texto simple
<text x={100} y={200} fontFamily={caveat} fontSize={48} fill="#2C3E50">
  {writeText("y = 2x + 3", TIMESTAMPS.ecuacion)}
</text>

// Ecuación en pasos (cada paso empieza cuando termina el anterior)
const paso1 = "2x + 5 = 11";
const paso2 = "2x = 11 - 5";
const paso3 = "2x = 6";
const paso4 = "x = 3";

<text x={100} y={200}>{writeText(paso1, TIMESTAMPS.paso1)}</text>
<text x={100} y={280}>{writeText(paso2, TIMESTAMPS.paso2)}</text>
<text x={100} y={360}>{writeText(paso3, TIMESTAMPS.paso3)}</text>
<text x={100} y={440}>{writeText(paso4, TIMESTAMPS.resultado, 10)}</text>  {/* más lento */}
```

#### Velocidades recomendadas

| Tipo de contenido | charsPerSecond | Ejemplo |
|-------------------|----------------|---------|
| Títulos | 20-25 | Rápido, impactante |
| Ecuaciones | 12-15 | Velocidad normal |
| Resultados importantes | 8-10 | Lento, énfasis |
| Explicaciones largas | 18-20 | Fluido |

#### Fuente Caveat (estilo manuscrito)

Usar siempre la fuente **Caveat** para simular escritura a mano:

```typescript
import { loadFont } from '@remotion/google-fonts/Caveat';
const { fontFamily: caveat } = loadFont();

// En SVG
<text fontFamily={caveat} fontSize={48}>...</text>

// En HTML/CSS
<p style={{ fontFamily: caveat, fontSize: 48 }}>...</p>
```

---

## §7. Composición Final

Crear `src/MainComposition.tsx`:

```typescript
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

const FPS = 30;
const SCENE_DURATIONS = {
  scene1: Math.ceil(DURACION_AUDIO_1 * FPS) + 15,
  scene2: Math.ceil(DURACION_AUDIO_2 * FPS) + 15,
  // ...
};

export const MainComposition: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.scene1}>
        <Scene1Problema />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: 15})} />
      {/* ... más escenas */}
    </TransitionSeries>
  );
};
```

Crear `src/Root.tsx` y `src/index.ts` para registrar la composición.

---

## §8. Verificación y Renderizado

### Verificar TypeScript
```bash
npx tsc --noEmit
```

### Iniciar Studio (preview)
```bash
npx remotion studio
```

### Renderizar video final
```bash
npx remotion render MainComposition out/video.mp4
```

---

## §9. Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| Audio se corta | Duración en frames < duración audio | `Math.ceil(duracion * fps) + 15` |
| Animaciones antes del audio | Timestamps incorrectos | Verificar JSON de Whisper |
| Fuente no carga | Import incorrecto | `import { loadFont } from '@remotion/google-fonts/Caveat'` |
| SVG cortado | viewBox incorrecto | `viewBox="0 0 1920 1080"` |

---

## Checklist Final

- [ ] §1: Estructura de proyecto creada
- [ ] §2: Whiteboard.tsx creado
- [ ] §3: Guiones y PLANIFICACION.md creados
- [ ] **§3.1: APROBACIÓN DEL USUARIO RECIBIDA** ← OBLIGATORIO
- [ ] §4: Audios generados y acelerados
- [ ] §5: Timestamps extraídos con Whisper
- [ ] §6: Escenas generadas
- [ ] §7: MainComposition y Root creados
- [ ] §8: TypeScript compila sin errores
- [ ] §8: Video renderizado
