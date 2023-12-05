import numpy as np
import torch # framework open source de deep learning
from scipy.signal import resample
from transformers import Wav2Vec2ForCTC, Wav2Vec2CTCTokenizer


def transcript(audio, sample_rate=16000):
    # Charge un modèle pré-entraîné Wav2Vec2 pour la tâche CTC depuis Hugging Face Model Hub.
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    tokenizer = Wav2Vec2CTCTokenizer.from_pretrained("facebook/wav2vec2-base-960h")

    # Convert the audio to mono and normalize
    if len(audio.shape) > 1:
        audio = np.mean(audio.numpy(), axis=0)
    audio /= np.max(np.abs(audio))

    # Rééchantillonnez le signal audio à 16 kHz
    # calcule le nombre d'échantillons nécessaires pour obtenir le nouveau taux d'échantillonnage souhaité
    resampled_audio = resample(audio, int(len(audio) * (16000 / sample_rate)))

    # Convertissez le signal rééchantillonné en un tableau NumPy
    # np.expand_dims() permet d'ajouter une dimension à un tableau NumPy
    #pour que le tableau NumPy puisse être utilisé comme entrée pour un modèle PyTorch
    input_values = np.expand_dims(resampled_audio, axis=0)

    # Perform speech recognition
    # gradients ne sont pas calculés. Cela permet d'économiser de la mémoire et de calculer plus rapidement
    with torch.no_grad():
        # convertit le tableau input_values en un tenseur PyTorch
        # calcul des logits pour chaque token
        # logits est utilisé pour calculer la probabilité de chaque token

        logits = model(torch.FloatTensor(input_values)).logits
        # predicted-id est l'indice du token avec la probabilité la plus élevée
        predicted_ids = np.argmax(logits, axis=-1)

    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription
