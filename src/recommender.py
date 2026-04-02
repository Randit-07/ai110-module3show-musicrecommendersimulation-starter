from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


WEIGHTS = {
    "artist": 4.0,
    "genre": 1.5,
    "mood": 2.0,
    "tempo_bpm": 1.8,
    "energy": 3.0,
    "valence": 1.2,
    "danceability": 1.0,
    "acousticness": 0.8,
}


def _closeness(value: float, target: float, max_distance: float = 1.0) -> float:
    """Return a normalized similarity score between 0 and 1 based on distance."""
    if max_distance <= 0:
        return 0.0
    distance = abs(value - target)
    score = 1.0 - (distance / max_distance)
    return max(0.0, min(1.0, score))


def _score_song(song: Dict, user: Dict) -> Tuple[float, List[str]]:
    """Compute the weighted recommendation score and human-readable reasons for one song."""
    score = 0.0
    reasons: List[str] = []

    user_artist = user.get("artist") or user.get("favorite_artist")
    if user_artist and song.get("artist") == user_artist:
        score += WEIGHTS["artist"]
        reasons.append("artist match")

    user_genre = user.get("genre")
    if user_genre and song.get("genre") == user_genre:
        score += WEIGHTS["genre"]
        reasons.append("genre match")

    user_mood = user.get("mood")
    if user_mood and song.get("mood") == user_mood:
        score += WEIGHTS["mood"]
        reasons.append("mood match")

    if user.get("energy") is not None:
        energy_close = _closeness(float(song.get("energy", 0.0)), float(user["energy"]))
        score += WEIGHTS["energy"] * energy_close
        reasons.append(f"energy closeness {energy_close:.2f}")

    if user.get("tempo_bpm") is not None:
        # Tempo in music often sits roughly between 60 and 200 BPM.
        tempo_close = _closeness(
            float(song.get("tempo_bpm", 0.0)),
            float(user["tempo_bpm"]),
            max_distance=140.0,
        )
        score += WEIGHTS["tempo_bpm"] * tempo_close
        reasons.append(f"tempo closeness {tempo_close:.2f}")

    if user.get("valence") is not None:
        valence_close = _closeness(float(song.get("valence", 0.0)), float(user["valence"]))
        score += WEIGHTS["valence"] * valence_close
        reasons.append(f"valence closeness {valence_close:.2f}")

    if user.get("danceability") is not None:
        dance_close = _closeness(float(song.get("danceability", 0.0)), float(user["danceability"]))
        score += WEIGHTS["danceability"] * dance_close
        reasons.append(f"danceability closeness {dance_close:.2f}")

    acoustic_target = user.get("acousticness")
    if acoustic_target is None and user.get("likes_acoustic") is not None:
        acoustic_target = 0.85 if bool(user["likes_acoustic"]) else 0.15

    if acoustic_target is not None:
        acoustic_close = _closeness(float(song.get("acousticness", 0.0)), float(acoustic_target))
        score += WEIGHTS["acousticness"] * acoustic_close
        reasons.append(f"acousticness closeness {acoustic_close:.2f}")

    return score, reasons

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    favorite_artist: Optional[str] = None
    target_tempo_bpm: Optional[float] = None
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None
    target_acousticness: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _profile_to_prefs(self, user: UserProfile) -> Dict:
        """Convert a UserProfile object into the functional preference dictionary format."""
        return {
            "artist": user.favorite_artist,
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "tempo_bpm": user.target_tempo_bpm,
            "valence": user.target_valence,
            "danceability": user.target_danceability,
            "acousticness": user.target_acousticness,
            "likes_acoustic": user.likes_acoustic,
        }

    def _song_to_dict(self, song: Song) -> Dict:
        """Convert a Song dataclass instance into a dictionary for shared scoring logic."""
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = self._profile_to_prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda song: _score_song(self._song_to_dict(song), prefs)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prefs = self._profile_to_prefs(user)
        song_dict = self._song_to_dict(song)
        score, reasons = _score_song(song_dict, prefs)
        reason_text = ", ".join(reasons[:4]) if reasons else "baseline similarity"
        return f"Score {score:.2f} because of {reason_text}."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = _score_song(song, user_prefs)
        explanation = "Matched on " + ", ".join(reasons[:4]) if reasons else "General similarity"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
