# Práctica de Voice Cloning - TTS

Práctica de Sistemas Interactivos Inteligentes sobre **zero-shot voice cloning** utilizando modelos TTS.

## 📋 Descripción

Este proyecto implementa y compara dos modelos de síntesis de voz con capacidad de clonación:

- **XTTS-v2** (Coqui-TTS): Modelo basado en Transformers, zero-shot voice cloning
- **VITS** (Coqui-TTS): Modelo multi-speaker, más rápido que XTTS-v2

Se evalúan mediante métricas objetivas de similitud de voz y se comparan en términos de calidad y rendimiento.

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker instalado
- Make (opcional, pero recomendado)
- Audio de referencia en formato WAV

### Instalación y Ejecución

```bash
# 1. Clonar/descargar el proyecto
cd practica-tts

# 2. Colocar el audio de referencia
# Copiar tu archivo WAV a: data/reference/voz_referencia.wav

# 3. Verificar que el audio está presente
make check-audio

# 4. Construir la imagen Docker
make build

# 5. Ejecutar el pipeline completo
make run
```

## 📁 Estructura del Proyecto

```
practica-tts/
├── src/
│   ├── main.py              # Pipeline principal
│   ├── clone_xtts.py        # Implementación XTTS-v2
│   ├── clone_yourtts.py       
│   └── evaluate.py          # Sistema de métricas
├── data/
│   ├── reference/           # Audio de referencia (entrada)
│   │   └── voz_referencia.wav
│   └── generated/           # Audios generados (salida)
│       ├── xtts/
│       └── yourtts/
├── results/                 # Resultados de evaluación
│   ├── comparison_plot.png
│   ├── comparison_table.csv
│   ├── detailed_results.json
│   └── report.md
├── Dockerfile
├── Makefile
├── requirements.txt
└── README.md
```

## 🎯 Comandos Disponibles

### Comandos principales

```bash
make build        # Construir imagen Docker
make run          # Ejecutar pipeline completo
make evaluate     # Solo evaluar métricas
make clean        # Limpiar audios generados
make clean-all    # Limpiar todo (incluye Docker image)
```

### Comandos individuales por modelo

```bash
make run-xtts     # Solo generar con XTTS-v2
make run-f5tts    # Solo generar con F5-TTS
```

### Comandos de utilidad

```bash
make shell        # Abrir shell en el contenedor
make check-audio  # Verificar audio de referencia
make help         # Mostrar ayuda
```

## 📊 Métricas Implementadas

### Métricas Objetivas

1. **Speaker Similarity** (Resemblyzer)
   - Mide similitud entre embeddings de voz
   - Rango: 0-1 (mayor es mejor)
   - Métrica principal para voice cloning

2. **Audio Quality Metrics**
   - SNR (Signal-to-Noise Ratio)
   - Zero Crossing Rate
   - Duración del audio

### Métricas de Rendimiento

- Tiempo de generación por audio
- Tiempo total de procesamiento
- Latencia (crítica en TTS según el profesor)

## 🔧 Modelos Implementados

### XTTS-v2 (Coqui-TTS)

- **Arquitectura**: Transformer-based
- **Características**:
  - Zero-shot voice cloning nativo
  - Multilingüe (español incluido)
  - Buena velocidad de inferencia
  - Mencionado explícitamente en el enunciado

### F5-TTS

- **Arquitectura**: Flow Matching
- **Características**:
  - Basado en denoising (similar a difusión)
  - "Mejores resultados" según diapositivas del profesor
  - Más lento que modelos no autoregresivos
  - Elimina necesidad de vocoder separado

## 📝 Resultados

Después de ejecutar el pipeline, los resultados se guardan en `results/`:

- `comparison_plot.png`: Gráficos comparativos de similitud
- `comparison_table.csv`: Tabla con métricas por modelo
- `detailed_results.json`: Resultados completos en JSON
- `report.md`: Reporte resumen en Markdown

## 🐳 Uso con Docker (Manual)

Si no usas Make:

```bash
# Construir imagen
docker build -t voice-cloning-tts .

# Ejecutar pipeline completo
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  voice-cloning-tts

# Ejecutar solo evaluación
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  voice-cloning-tts \
  python src/evaluate.py
```

## 📖 Notas Importantes

### Audio de Referencia

- **Formato**: WAV recomendado
- **Duración**: 10-20 segundos (mínimo 5)
- **Calidad**: 16 kHz o 22.05 kHz sample rate
- **Canales**: Mono (1 canal)
- **Contenido**: Habla clara, sin ruido de fondo
- **Ética**: Usar solo voces propias o con permiso explícito

### Idiomas

- **XTTS-v2**: Soporta español nativamente
- **F5-TTS**: Funciona mejor con inglés (por eso los textos están en inglés)

### Requisitos de Hardware

- **CPU**: Funciona en CPU (más lento)
- **GPU**: Recomendado para mayor velocidad (CUDA)
- **RAM**: Mínimo 8GB, recomendado 16GB
- **Espacio**: ~10GB para modelos y dependencias

## 🔍 Troubleshooting

### Problema: Audio no encontrado

```bash
❌ Error: No se encuentra data/reference/voz_referencia.wav
```

**Solución**: Coloca tu archivo WAV en `data/reference/voz_referencia.wav`

### Problema: F5-TTS no disponible

```bash
⚠️ F5-TTS no disponible
```

**Solución**: Es opcional. El proyecto funciona solo con XTTS-v2.

### Problema: Error de memoria

```bash
RuntimeError: CUDA out of memory
```

**Solución**: 
- Reduce el tamaño del batch
- Usa CPU en lugar de GPU
- Cierra otras aplicaciones

## 👨‍🎓 Información Académica

- **Asignatura**: Sistemas Interactivos Inteligentes
- **Práctica**: 3 - TTS y Voice Cloning
- **Objetivo**: Comparar modelos de zero-shot voice cloning
- **Requisitos**: 
  - Mínimo 2 modelos acústicos
  - Al menos 1 métrica objetiva
  - Memoria 500-3000 palabras
  - Entrega en formato Docker

## 📚 Referencias

- [Coqui TTS (XTTS-v2)](https://github.com/coqui-ai/TTS)
- [F5-TTS](https://github.com/SWivid/F5-TTS)
- [Resemblyzer](https://github.com/resemble-ai/Resemblyzer)
- Diapositivas del profesor: Sesión 10, Tema 3

## 📄 Licencia

Este proyecto es material educativo para la asignatura de Sistemas Interactivos Inteligentes.