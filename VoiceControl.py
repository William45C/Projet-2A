#pip install webrtcvad-wheels
# pip install resemblyzer 
# pip install sounddevice 
# pip install openai-whisper 
# pip install numpy
# pip install resemblyzer --no-deps
# pip install numpy scipy librosa umap-learn



import sounddevice as sd
import numpy as np
import whisper
from resemblyzer import VoiceEncoder, preprocess_wav

SAMPLE_RATE = 16000
RECORD_DURATION = 3  # secondes d'écoute par commande

encoder = VoiceEncoder()
model = whisper.load_model("small")
reference_embedding = None

def enroll(duration=5):
    """Enregistre la voix de référence au lancement."""
    print(f"Parle pendant {duration} secondes pour enregistrer ta voix...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    print("Voix enregistrée !")
    wav = preprocess_wav(audio.flatten(), source_sr=SAMPLE_RATE)
    return encoder.embed_utterance(wav)

def is_my_voice(audio, threshold=0.75):
    """Retourne True si l'audio correspond à la voix de référence."""
    wav = preprocess_wav(audio, source_sr=SAMPLE_RATE)
    embedding = encoder.embed_utterance(wav)
    similarity = np.dot(reference_embedding, embedding)
    print(f"  Similarité voix: {similarity:.2f}")
    return similarity >= threshold

def listen():
    """Écoute, vérifie la voix, et retourne le texte transcrit ou None."""
    audio = sd.rec(int(RECORD_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    audio_flat = audio.flatten()

    """
    if not is_my_voice(audio_flat):
        print("  Voix ignorée (pas la bonne personne)")
        return None
    """
    result = model.transcribe(
        audio_flat,
        language="fr",
        initial_prompt="Commandes de jeu: attaque, objet, fuite, gauche, droite, devant.",
        beam_size=5,
    )
    return result["text"].strip().lower()

def actionVocale(current_state,nbObjets):

    while True:
        print("Parle maintenant...")
        text = listen()
        print("fin")
        if text:
            if current_state == "EXPLORE":
                if "avance" in text.lower():
                    print("tout droit")
                    return 0
                if "droite" in text.lower() or "droit" in text.lower():
                    print("droite")
                    return 1
                if "gauche" in text.lower() or "gouche" in text.lower():
                    print("gauche")
                    return 2
                if "objet" in text.lower():
                    print("objet")
                    return 3
            if current_state == "COMBAT":
                if "attaque" in text.lower():
                    print("utilise attack")
                    return 0
                if "fuite" in text.lower() or "8" in text.lower():
                    print("fuite")
                    return 1
                if "objet" in text.lower():
                    print("utilise objet")
                    return 2
            if current_state == "CHEST":
                if "ouvrir" in text.lower():
                    print("ouvre coffre")
                    return 0
                if "laisser" in text.lower():
                    print("laisse coffre")
                    return 1
            if current_state == "SHOP":
                if "objet 1" in text.lower():
                    print("objet 1")
                    return 0
                if "objet 2" in text.lower():
                    print("objet 2")
                    return 1
                if "objet 3" in text.lower():
                    print("objet 3")
                    return 2
                if "partir" in text.lower():
                    print("part du shop")
                    return 3
            if current_state == "OBJECTS":
                if "objet" in text.lower():
                    try:
                        nbr = int(text.lower().split('objet ')[1][0])
                        if nbr > nbObjets:
                            print("non valable")
                            return nbObjets-1
                        else:
                            print(f"Objet {int(text.lower().split('objet ')[1][0])-1}")
                            return int(text.lower().split('objet ')[1][0])-1
                    except:
                        print(text.lower().split('objet ')[1][0], text.lower().split('objet '))
                if "partir" in text.lower():
                    return nbObjets-1
            print("Commande:", text)