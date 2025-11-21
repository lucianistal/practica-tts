.PHONY: help build run evaluate clean clean-all shell check-audio

DOCKER_IMAGE = voice-cloning-tts
AUDIO_REF = data/reference/voz_referencia.wav

help:
	@echo "📚 Comandos disponibles:"
	@echo ""
	@echo "  make check-audio  - Verificar audio de referencia"
	@echo "  make build        - Construir imagen Docker"
	@echo "  make run          - Ejecutar pipeline completo"
	@echo "  make evaluate     - Solo evaluar métricas"
	@echo "  make clean        - Limpiar audios generados"
	@echo "  make clean-all    - Limpiar todo (incluye imagen)"
	@echo "  make shell        - Abrir shell en contenedor"
	@echo ""

check-audio:
	@echo "🔍 Verificando audio de referencia..."
	@if [ -f "$(AUDIO_REF)" ]; then \
		echo "✅ Audio encontrado: $(AUDIO_REF)"; \
		ls -lh $(AUDIO_REF); \
	else \
		echo "❌ ERROR: No se encuentra $(AUDIO_REF)"; \
		echo ""; \
		echo "Por favor coloca tu archivo WAV en:"; \
		echo "  $(AUDIO_REF)"; \
		exit 1; \
	fi

build:
	@echo "🔨 Construyendo imagen Docker..."
	docker build -t $(DOCKER_IMAGE) .
	@echo "✅ Imagen construida: $(DOCKER_IMAGE)"

run: check-audio
	@echo "🚀 Ejecutando pipeline completo..."
	docker run --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/results:/app/results \
		$(DOCKER_IMAGE)
	@echo "✅ Pipeline completado. Revisa results/"

evaluate:
	@echo "📊 Ejecutando evaluación..."
	docker run --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/results:/app/results \
		$(DOCKER_IMAGE) \
		python src/evaluate.py

shell:
	@echo "🐚 Abriendo shell en contenedor..."
	docker run --rm -it \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/results:/app/results \
		$(DOCKER_IMAGE) \
		/bin/bash

clean:
	@echo "🧹 Limpiando audios generados..."
	rm -rf data/generated/xtts/*.wav
	rm -rf data/generated/yourtts/*.wav
	rm -rf results/*
	@echo "✅ Limpieza completada"

clean-all: clean
	@echo "🧹 Eliminando imagen Docker..."
	docker rmi $(DOCKER_IMAGE) 2>/dev/null || true
	@echo "✅ Limpieza completa"