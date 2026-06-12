# processing/normalization/utils.py

import unicodedata
import re
from datetime import datetime

def normalize_title(title: str) -> str:
    """
    Normalise un titre pour le matching :
    - passage en minuscules
    - suppression des accents
    - suppression des caractères spéciaux (garde alphanumeric + espaces)
    - nettoyage des espaces multiples
    """
    if not title or not isinstance(title, str):
        return ""
    
    # Passage en minuscules
    title = title.lower()
    
    # Suppression des accents
    title = "".join(
        c for c in unicodedata.normalize("NFD", title)
        if unicodedata.category(c) != "Mn"
    )
    
    # Suppression des caractères spéciaux
    title = re.sub(r"[^a-z0-9\s]", " ", title)
    
    # Nettoyage des espaces
    title = re.sub(r"\s+", " ", title).strip()
    
    return title

def parse_iso_date(date_str: str) -> str:
    """
    Assure qu'une date est au format YYYY-MM-DD.
    Si seulement l'année est fournie, ajoute -01-01.
    """
    if not date_str or not isinstance(date_str, str):
        return None
        
    date_str = date_str.strip()
    
    # Format YYYY
    if re.match(r"^\d{4}$", date_str):
        return f"{date_str}-01-01"
    
    # Format YYYY-MM-DD (déjà correct ou presque)
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", date_str)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        
    return None

def scale_score(score: any, max_val: float = 10.0) -> float:
    """
    Ramène un score sur une échelle de 0 à 10.
    Gère les pourcentages (ex: "85%").
    """
    if score is None:
        return None
        
    try:
        if isinstance(score, str):
            score = score.replace("%", "").strip()
            val = float(score)
            if "%" in score or val > 10: # Probablement sur 100
                return round(val / 10, 1)
            return round(val, 1)
        
        val = float(score)
        if val > 10: # Probablement sur 100
            return round(val / 10, 1)
        return round(val, 1)
    except:
        return None
