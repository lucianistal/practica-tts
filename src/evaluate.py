import os
import json
import librosa
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import soundfile as sf
import time


REFERENCE = "data/reference/voz_referencia.wav"
GENERATED = {
    "xtts": "data/generated/xtts",
    "yourtts": "data/generated/yourtts"
}

RESULTS_PATH = "results/detailed_results.json"


def compute_similarity(reference_audio, generated_audio):
    """Devuelve la similitud coseno entre embeddings de voz."""
    encoder = VoiceEncoder()

    ref_wav = preprocess_wav(reference_audio)
    gen_wav = preprocess_wav(generated_audio)

    ref_emb = encoder.embed_utterance(ref_wav)
    gen_emb = encoder.embed_utterance(gen_wav)

    similarity = np.dot(ref_emb, gen_emb) / (
        np.linalg.norm(ref_emb) * np.linalg.norm(gen_emb)
    )
    return float(similarity)


def compute_audio_metrics(audio_path):
    """SNR, duración y zero-crossing-rate."""
    y, sr = librosa.load(audio_path, sr=None)

    snr = librosa.feature.rms(y=y).mean()
    zcr = librosa.feature.zero_crossing_rate(y)[0].mean()
    duration = librosa.get_duration(y=y, sr=sr)

    return {
        "snr": float(snr),
        "zcr": float(zcr),
        "duration": float(duration)
    }


def evaluate():
    print("\n📊 Ejecutando evaluación...")

    if not os.path.exists(REFERENCE):
        raise FileNotFoundError("❌ No se encuentra el audio de referencia")

    results = {}

    for model_name, folder in GENERATED.items():
        print(f"\n🔎 Evaluando modelo: {model_name}")

        model_results = []
        wav_files = sorted(Path(folder).glob("*.wav"))

        for file in wav_files:
            print(f" → {file.name}")

            similarity = compute_similarity(REFERENCE, file)
            audio_metrics = compute_audio_metrics(file)

            model_results.append({
                "file": str(file),
                "similarity": similarity,
                **audio_metrics
            })

        results[model_name] = model_results

    os.makedirs("results", exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Resultados guardados en {RESULTS_PATH}")


if __name__ == "__main__":
    evaluate()
