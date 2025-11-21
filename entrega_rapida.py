#!/usr/bin/env python3
"""
ENTREGA CON AUDIOS REALES - Usa TTS de verdad para clonar tu voz
"""
import os
import json
import time

os.environ["COQUI_TOS_AGREED"] = "1"

def main():
    print("\n🎙️ CLONADOR DE VOZ REAL - XTTS + YourTTS\n")
    
    # Crear directorios
    os.makedirs("data/generated/xtts", exist_ok=True)
    os.makedirs("data/generated/yourtts", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    # Verificar audio de referencia
    ref_audio = "data/reference/voz_referencia.wav"
    if not os.path.exists(ref_audio):
        print(f"❌ Falta: {ref_audio}")
        return 1
    
    print(f"✅ Audio de referencia: {ref_audio}\n")
    
    # Textos CORTOS para clonar
    texts = [
        "Hello, this is Lucia speaking.",
        "Voice cloning is amazing.",
        "I love interactive systems."
    ]
    
    # ========== XTTS-v2 ==========
    print("="*60)
    print("🎤 GENERANDO CON XTTS-v2")
    print("="*60 + "\n")
    
    try:
        from TTS.api import TTS
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📍 Device: {device}\n")
        
        print("⏳ Cargando XTTS-v2...")
        tts_xtts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", 
                       gpu=(device=="cuda"), progress_bar=False)
        print("✅ XTTS-v2 listo\n")
        
        for i, text in enumerate(texts, 1):
            output = f"data/generated/xtts/output_{i}.wav"
            print(f"   [{i}/3] {text}")
            
            try:
                tts_xtts.tts_to_file(
                    text=text,
                    speaker_wav=ref_audio,
                    language="en",
                    file_path=output
                )
                print(f"        ✅ {output}\n")
            except Exception as e:
                print(f"        ⚠️  Error: {e}\n")
        
    except Exception as e:
        print(f"❌ Error XTTS: {e}\n")
    
    # ========== YourTTS ==========
    print("="*60)
    print("🎤 GENERANDO CON YourTTS")
    print("="*60 + "\n")
    
    try:
        from TTS.api import TTS
        
        print("⏳ Cargando YourTTS...")
        tts_yourtts = TTS("tts_models/multilingual/multi-dataset/your_tts", 
                          gpu=False, progress_bar=False)
        print("✅ YourTTS listo\n")
        
        for i, text in enumerate(texts, 1):
            output = f"data/generated/yourtts/output_{i}.wav"
            print(f"   [{i}/3] {text}")
            
            try:
                tts_yourtts.tts_to_file(
                    text=text,
                    speaker_wav=ref_audio,
                    language="en",
                    file_path=output
                )
                print(f"        ✅ {output}\n")
            except Exception as e:
                print(f"        ⚠️  Error: {e}\n")
        
    except Exception as e:
        print(f"⚠️  YourTTS no disponible (opcional): {e}\n")
    
    # ========== MÉTRICAS ==========
    print("="*60)
    print("📊 CALCULANDO MÉTRICAS")
    print("="*60 + "\n")
    
    results = {
        "reference_audio": ref_audio,
        "texts_used": texts,
        "models": {}
    }
    
    try:
        from resemblyzer import VoiceEncoder, preprocess_wav
        import librosa
        import numpy as np
        
        encoder = VoiceEncoder()
        print("📍 Codificando audio de referencia...")
        ref_wav = preprocess_wav(ref_audio)
        ref_emb = encoder.embed_utterance(ref_wav)
        
        # Procesar XTTS
        print("\n📊 XTTS-v2 Métricas:")
        xtts_results = []
        for i in range(1, 4):
            file = f"data/generated/xtts/output_{i}.wav"
            if os.path.exists(file):
                gen_wav = preprocess_wav(file)
                gen_emb = encoder.embed_utterance(gen_wav)
                
                similarity = float(np.dot(ref_emb, gen_emb) / (
                    np.linalg.norm(ref_emb) * np.linalg.norm(gen_emb)
                ))
                
                y, sr = librosa.load(file, sr=None)
                snr = float(librosa.feature.rms(y=y).mean())
                zcr = float(librosa.feature.zero_crossing_rate(y)[0].mean())
                duration = float(librosa.get_duration(y=y, sr=sr))
                
                xtts_results.append({
                    "file": f"output_{i}.wav",
                    "speaker_similarity": similarity,
                    "snr": snr,
                    "zcr": zcr,
                    "duration": duration
                })
                
                print(f"  output_{i}: Similitud {similarity:.3f}")
        
        results["models"]["xtts_v2"] = xtts_results
        
        # Procesar YourTTS
        print("\n📊 YourTTS Métricas:")
        yourtts_results = []
        for i in range(1, 4):
            file = f"data/generated/yourtts/output_{i}.wav"
            if os.path.exists(file):
                gen_wav = preprocess_wav(file)
                gen_emb = encoder.embed_utterance(gen_wav)
                
                similarity = float(np.dot(ref_emb, gen_emb) / (
                    np.linalg.norm(ref_emb) * np.linalg.norm(gen_emb)
                ))
                
                y, sr = librosa.load(file, sr=None)
                snr = float(librosa.feature.rms(y=y).mean())
                zcr = float(librosa.feature.zero_crossing_rate(y)[0].mean())
                duration = float(librosa.get_duration(y=y, sr=sr))
                
                yourtts_results.append({
                    "file": f"output_{i}.wav",
                    "speaker_similarity": similarity,
                    "snr": snr,
                    "zcr": zcr,
                    "duration": duration
                })
                
                print(f"  output_{i}: Similitud {similarity:.3f}")
        
        results["models"]["yourtts"] = yourtts_results
        
    except Exception as e:
        print(f"⚠️  Error en métricas: {e}")
    
    # Guardar resultados
    with open("results/detailed_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ COMPLETADO")
    print("="*60)
    print(f"\n📁 Audios XTTS: data/generated/xtts/ ({len(os.listdir('data/generated/xtts'))} archivos)")
    print(f"📁 Audios YourTTS: data/generated/yourtts/ ({len(os.listdir('data/generated/yourtts'))} archivos)")
    print(f"📊 Métricas: results/detailed_results.json\n")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())