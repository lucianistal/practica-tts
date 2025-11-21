"""
Pipeline principal para Voice Cloning
Compara XTTS-v2 vs YourTTS (ambos con clonación REAL)
"""

import os
import sys
from pathlib import Path

try:
    from clone_xtts import XTTSCloner
    from clone_yourtts import YourTTSCloner
    from evaluate import evaluate
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)


# Configuración
REFERENCE_AUDIO = "data/reference/voz_referencia.wav"
OUTPUT_DIR_XTTS = "data/generated/xtts"
OUTPUT_DIR_YOURTTS = "data/generated/yourtts"

# Textos en INGLÉS (los modelos funcionan mejor)
TEST_TEXTS = [
    "Hello, this is Lucia speaking.",
    "Voice cloning is amazing.",
    "I love interactive systems."
]


def check_audio_exists():
    """Verifica que exista el audio de referencia"""
    if not os.path.exists(REFERENCE_AUDIO):
        print(f"❌ ERROR: No se encuentra el audio de referencia")
        print(f"   Esperado en: {REFERENCE_AUDIO}")
        print(f"\n💡 Descarga un audio de muestra con:")
        print(f"   bash download_sample_audio.sh")
        return False
    
    print(f"✅ Audio de referencia encontrado: {REFERENCE_AUDIO}")
    return True


def generate_with_xtts():
    """Genera audios con XTTS-v2"""
    print("\n" + "="*60)
    print("🎙️  GENERANDO CON XTTS-v2 (Coqui-TTS)")
    print("="*60)
    
    try:
        cloner = XTTSCloner()
        
        for i, text in enumerate(TEST_TEXTS, 1):
            output_path = f"{OUTPUT_DIR_XTTS}/output_{i}.wav"
            result = cloner.clone_voice(text, REFERENCE_AUDIO, output_path, language="en")
            
            if not result["success"]:
                print(f"⚠️  Fallo en audio {i}")
        
        print("\n✅ XTTS-v2 completado")
        
    except Exception as e:
        print(f"\n❌ Error en XTTS-v2: {e}")
        raise


def generate_with_yourtts():
    """Genera audios con YourTTS"""
    print("\n" + "="*60)
    print("🎙️  GENERANDO CON YourTTS (Coqui-TTS)")
    print("="*60)
    
    try:
        cloner = YourTTSCloner()
        
        for i, text in enumerate(TEST_TEXTS, 1):
            output_path = f"{OUTPUT_DIR_YOURTTS}/output_{i}.wav"
            result = cloner.clone_voice(text, REFERENCE_AUDIO, output_path, language="en")
            
            if not result["success"]:
                print(f"⚠️  Fallo en audio {i}")
        
        print("\n✅ YourTTS completado")
        
    except Exception as e:
        print(f"\n❌ Error en YourTTS: {e}")
        raise


def run_evaluation():
    """Ejecuta la evaluación de métricas"""
    print("\n" + "="*60)
    print("📊 EVALUANDO RESULTADOS")
    print("="*60)
    
    try:
        evaluate()
        print("\n✅ Evaluación completada")
        print("📁 Resultados guardados en: results/")
        
    except Exception as e:
        print(f"\n❌ Error en evaluación: {e}")
        raise


def main():
    """Pipeline principal"""
    print("\n" + "="*60)
    print("🚀 PIPELINE DE VOICE CLONING")
    print("   Modelo: XTTS-v2")
    print("   Idioma: Inglés")
    print("="*60)
    
    # 1. Verificar audio de referencia
    if not check_audio_exists():
        return 1
    
    # 2. Generar con XTTS-v2
    try:
        generate_with_xtts()
    except Exception as e:
        print(f"\n❌ XTTS-v2 falló: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # YourTTS DESHABILITADO - da segfault en Mac M1/M2
    print("\n" + "="*60)
    print("ℹ️  YourTTS deshabilitado (incompatible con Mac ARM)")
    print("="*60)
    
    # 3. Evaluar resultados
    try:
        run_evaluation()
    except Exception as e:
        print(f"\n⚠️  Evaluación falló: {e}")
    
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETADO")
    print("="*60)
    print("\n📊 Revisa los resultados en:")
    print("   - data/generated/xtts/")
    print("   - results/detailed_results.json")
    print("")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
