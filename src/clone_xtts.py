"""
XTTS-v2 Voice Cloning - Versión estable y compatible con Docker
"""

import os
import time
import torch
from TTS.api import TTS

# ⭐ Aceptar términos de servicio automáticamente
os.environ["COQUI_TOS_AGREED"] = "1"

class XTTSCloner:
    def __init__(self):
        """Inicializa XTTS-v2"""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔧 Inicializando XTTS-v2 en {device}...")

        try:
            self.tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                gpu=(device == "cuda"),
                progress_bar=False
            )
            print("✅ XTTS-v2 cargado correctamente")
        except Exception as e:
            print(f"❌ Error inicializando XTTS-v2: {e}")
            raise

    def clone_voice(self, text, reference_audio, output_path, language="en"):
        """Genera audio clonando la voz"""

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        print(f"\n🎤 Generando con XTTS-v2: {text[:50]}...")

        start = time.time()

        try:
            self.tts.tts_to_file(
                text=text,
                speaker_wav=reference_audio,
                language=language,
                file_path=output_path
            )
            elapsed = time.time() - start
            print(f"✅ XTTS generado en {elapsed:.2f}s → {output_path}")

            return {"success": True, "time": elapsed, "output": output_path}

        except Exception as e:
            print(f"❌ Error generando con XTTS-v2: {e}")
            return {"success": False, "error": str(e)}