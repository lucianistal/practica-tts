FROM python:3.10-slim

LABEL maintainer="Estudiante SII"
LABEL description="Voice Cloning - XTTS-v2"

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV COQUI_TOS_AGREED=1

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Actualizar pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# PyTorch
RUN pip install --no-cache-dir \
    "numpy<2.0" \
    torch==2.1.0 \
    torchaudio==2.1.0

# Audio
RUN pip install --no-cache-dir \
    librosa \
    soundfile \
    resemblyzer

# Utilidades
RUN pip install --no-cache-dir \
    pandas \
    matplotlib \
    tqdm

# Instalar TTS sin dependencias opcionales
RUN pip install --no-cache-dir --no-deps TTS==0.21.1

# Instalar TODAS las dependencias necesarias (CON spacy pero SIN japonés)
RUN pip install --no-cache-dir \
    trainer==0.0.32 \
    "transformers<4.35" \
    cython \
    scipy \
    numba \
    inflect \
    anyascii \
    pyyaml \
    aiohttp \
    flask \
    pysbd \
    coqpit \
    jieba \
    pypinyin \
    hangul-romanize \
    gruut[de,es,fr]==2.2.3 \
    jamo \
    nltk \
    g2pkk \
    bangla \
    bnnumerizer \
    bnunicodenormalizer \
    einops \
    encodec \
    unidecode \
    num2words \
    "spacy<3.9" \
    spacy-legacy \
    spacy-loggers

# Copiar código
COPY src/ ./src/
COPY data/ ./data/

# Crear directorios
RUN mkdir -p \
    data/reference \
    data/generated/xtts \
    results

VOLUME ["/app/data", "/app/results"]

CMD ["python", "src/main.py"]