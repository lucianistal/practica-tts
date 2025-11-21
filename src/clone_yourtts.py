"""
YourTTS Voice Cloning - Con protección contra segfaults
"""

import os
import time
import torch
from TTS.api import TTS

class YourTTSCloner:
    def __init__(self):
        """Inicializa YourTTS con protecciones para evitar crashes"""
        device = "cpu"  # ⭐ Forzar CPU para evitar problemas en Mac M1/M2
        print(f"🔧 Inicializando YourTTS en {device}...")
        
        try:
            # Configurar torch para CPU estable
            torch.set_num_threads(1)
            torch.set_grad_enabled(False)
            
            self.tts = TTS(
                "tts_models/multilingual/multi-dataset/your_tts", 
                gpu=False,  # ⭐ Siempre CPU
                progress_bar=False
            )
            
            print("✅ YourTTS cargado correctamente")
            print("ℹ️  YourTTS: Zero-shot voice cloning")
            
        except Exception as e:
            print(f"❌ Error cargando YourTTS: {e}")
            raise
    
    def clone_voice(self, text, reference_audio, output_path, language="en"):
        """Genera audio clonando voz"""
        print(f"\n🎤 Generando con YourTTS: {text[:40]}...")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        start = time.time()
        
        try:
            # ⭐ Protección contra crashes
            with torch.no_grad():
                # Limitar longitud del texto para evitar problemas
                if len(text) > 200:
                    text = text[:200]
                
                self.tts.tts_to_file(
                    text=text,
                    speaker_wav=reference_audio,
                    language=language,
                    file_path=output_path
                )
            
            # Verificar que se creó el archivo
            if os.path.exists(output_path):
                elapsed = time.time() - start
                print(f"✅ YourTTS generado en {elapsed:.1f}s → {output_path}")
                
                return {
                    "success": True,
                    "model": "YourTTS",
                    "output": output_path,
                    "time": elapsed
                }
            else:
                print(f"❌ Archivo no creado: {output_path}")
                return {"success": False, "error": "File not created"}
            
        except Exception as e:
            print(f"❌ Error en YourTTS: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "model": "YourTTS",
                "error": str(e)
            }