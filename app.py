import whisper
import streamlit as st
import os
import tempfile
import shutil

# Verifica e configurazione di FFmpeg
def ensure_ffmpeg_installed():
    """Verifica se FFmpeg è installato e accessibile."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg non trovato. Assicurati che sia installato e accessibile nel PATH.")

# Funzione per trascrivere l'audio
def transcribe_audio(file_path, model_name="base"):
    """Trascrive un file audio usando Whisper."""
    model = whisper.load_model(model_name)
    result = model.transcribe(file_path)
    return result["text"]

# Inizio dell'app Streamlit
st.title("Trascrizione Audio by Francesco Furioso")

# Caricamento del file audio
audio_file = st.file_uploader("Carica un file audio", type=["wav", "mp3", "m4a"])

if audio_file is not None:
    # Verifica FFmpeg
    try:
        ensure_ffmpeg_installed()
    except RuntimeError as e:
        st.error(f"Errore: {str(e)}")
    else:
        # Salva temporaneamente il file caricato
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as temp_file:
            temp_file.write(audio_file.read())
            temp_file_path = temp_file.name

        st.success(f"File caricato con successo. Inizio trascrizione...")

        # Avvia la trascrizione
        with st.spinner("Trascrizione in corso..."):
            try:
                transcription = transcribe_audio(temp_file_path)
                st.subheader("Trascrizione:")
                st.write(transcription)
            except Exception as e:
                st.error(f"Errore durante la trascrizione: {str(e)}")

        # Pulsante per scaricare la trascrizione
        transcription_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name
        with open(transcription_file_path, "w") as transcription_file:
            transcription_file.write(transcription)

        with open(transcription_file_path, "rb") as file:
            st.download_button(
                label="Scarica la trascrizione",
                data=file,
                file_name="trascrizione.txt",
                mime="text/plain"
            )

        # Rimuove i file temporanei
        os.unlink(temp_file_path)
        os.unlink(transcription_file_path)
