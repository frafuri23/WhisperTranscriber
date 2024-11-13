import whisper
import os

def transcribe_audio(file_path, model_name="base"):
    # Verifica che il file audio esista
    if not os.path.exists(file_path):
        print(f"Errore: il file '{file_path}' non esiste. Controlla il percorso.")
        return

    # Controllo FFmpeg manuale
    os.system(f"ffmpeg -i {file_path} -f null -")

    # Carica il modello Whisper
    print("Caricamento del modello Whisper...")
    model = whisper.load_model(model_name)

    # Trascrive il file audio
    print("Inizio trascrizione...")
    result = model.transcribe(file_path)

    # Stampa la trascrizione
    print("\nTrascrizione completata:")
    print(result["text"])

# Percorso corretto del file audio
audio_file = "Registrazione_audio_prova.wav"

# Avvia la trascrizione
transcribe_audio(audio_file)