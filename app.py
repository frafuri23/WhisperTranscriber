import whisper
import streamlit as st
import os
import tempfile

def transcribe_audio(file_path, model_name="base"):
    """Trascrive un file audio usando Whisper"""
    model = whisper.load_model(model_name)
    result = model.transcribe(file_path)
    return result["text"]

# Titolo dell'app
st.title("Trascrizione Audio by Francesco Furioso")

# Caricamento del file audio
audio_file = st.file_uploader("Carica un file audio", type=["wav", "mp3", "m4a"])

if audio_file is not None:
    # Salva temporaneamente il file caricato
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as temp_file:
        temp_file.write(audio_file.read())
        temp_file_path = temp_file.name

    st.success(f"File caricato con successo. Inizio trascrizione...")

    # Avvia la trascrizione
    with st.spinner("Trascrizione in corso..."):
        transcription = transcribe_audio(temp_file_path)

    # Mostra la trascrizione
    st.subheader("Trascrizione:")
    st.write(transcription)

    # Salva la trascrizione in un file
    transcription_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name
    with open(transcription_file_path, "w") as transcription_file:
        transcription_file.write(transcription)

    # Pulsante per scaricare la trascrizione
    with open(transcription_file_path, "rb") as file:
        st.download_button(
            label="Scarica la trascrizione",
            data=file,
            file_name="trascrizione.txt",
            mime="text/plain"
        )

    # Rimuove il file temporaneo
    os.unlink(temp_file_path)
