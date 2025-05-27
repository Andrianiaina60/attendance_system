import logging
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_face_encoding(image_path, model_name="Facenet"):
    """
    Extrait les caractéristiques du visage à partir d’une image.
    
    Args:
        image_path (str): Chemin vers l'image contenant le visage.
        model_name (str): Modèle DeepFace à utiliser pour l'extraction (Facenet par défaut).
    
    Returns:
        numpy.ndarray | None: L'encodage facial sous forme de vecteur si réussi, sinon None.
    """
    try:
        logger.debug(f"Extraction des caractéristiques faciales de {image_path}")

        # Extraction des caractéristiques faciales
        embeddings = DeepFace.represent(image_path, model_name=model_name, enforce_detection=False)
        
        if not embeddings or not isinstance(embeddings, list) or "embedding" not in embeddings[0]:
            logger.warning(f"Aucun encodage facial détecté dans l'image : {image_path}")
            return None

        face_encoding = np.array(embeddings[0]["embedding"], dtype=np.float32)
        logger.debug(f"Encodage du visage extrait : {face_encoding}")

        return face_encoding

    except Exception as e:
        logger.error(f"Erreur d'extraction du visage pour {image_path}: {e}")
        return None

def verify_identity(new_encoding, stored_encoding, threshold=0.6):
    """
    Vérifie si l'identité de la personne dans l'image correspond à celle stockée.
    
    Args:
        new_encoding (numpy.ndarray): L'encodage du visage extrait de l'image actuelle.
        stored_encoding (list | numpy.ndarray): L'encodage facial stocké pour comparaison.
        threshold (float): Le seuil de similarité pour déterminer si les visages correspondent.
    
    Returns:
        tuple(bool, float): (True si les visages sont similaires, False sinon, avec le score de similarité)
    """
    try:
        if not isinstance(new_encoding, np.ndarray):
            raise ValueError("new_encoding doit être un tableau numpy valide.")
        
        if isinstance(stored_encoding, list):
            stored_encoding = np.array(stored_encoding, dtype=np.float32)

        if not isinstance(stored_encoding, np.ndarray):
            raise ValueError("stored_encoding doit être un tableau numpy valide.")

        # Vérification de la dimension des encodages
        if new_encoding.shape != stored_encoding.shape:
            raise ValueError(f"Les encodages doivent avoir la même dimension. "
                             f"Reçu {new_encoding.shape} et {stored_encoding.shape}")

        # Calcul de la similarité cosinus
        similarity = 1 - cosine(new_encoding, stored_encoding)
        logger.debug(f"Score de similarité cosinus: {similarity}")

        return similarity >= threshold, similarity

    except Exception as e:
        logger.error(f"Erreur pendant la vérification: {e}")
        return False, 0.0
