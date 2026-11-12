import csv
from typing import List, Dict, Tuple
from dataclasses import asdict, dataclass

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

class Recommender:
    """Recommend Song objects using the same scoring rules as the CLI."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the highest-scoring Song objects."""
        prefs = self._preferences(user)
        ranked = sorted(
            self.songs, key=lambda song: score_song(prefs, asdict(song))[0], reverse=True
        )
        return ranked[:max(0, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain the points a song earned for this user."""
        _, reasons = score_song(self._preferences(user), asdict(song))
        return "; ".join(reasons)

    @staticmethod
    def _preferences(user: UserProfile) -> Dict:
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }


def load_songs(csv_path: str) -> List[Dict]:
    """Read the CSV catalog and convert numeric columns to Python numbers."""
    with open(csv_path, newline="", encoding="utf-8") as catalog:
        songs = list(csv.DictReader(catalog))
    for song in songs:
        song["id"] = int(song["id"])
        for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
            song[field] = float(song[field])
    return songs


def score_song(
    user_prefs: Dict, song: Dict, *, genre_weight: float = 2.0, energy_weight: float = 1.0
) -> Tuple[float, List[str]]:
    """Return a weighted relevance score and its point-by-point explanation."""
    score = 0.0
    reasons = []
    for field, weight in (("genre", genre_weight), ("mood", 1.0)):
        if song[field].strip().casefold() == user_prefs[field].strip().casefold():
            score += weight
            reasons.append(f"{field} match (+{weight:.2f})")

    gap = abs(song["energy"] - user_prefs["energy"])
    energy_points = energy_weight * max(0.0, 1.0 - gap)
    reasons.append(f"energy gap {gap:.2f} (+{energy_points:.2f})")
    return score + energy_points, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    *,
    genre_weight: float = 2.0,
    energy_weight: float = 1.0,
) -> List[Tuple[Dict, float, str]]:
    """Score each song and return up to k results with explanations."""
    results = []
    for song in songs:
        score, reasons = score_song(
            user_prefs, song, genre_weight=genre_weight, energy_weight=energy_weight
        )
        results.append((song, score, "; ".join(reasons)))
    return sorted(results, key=lambda result: result[1], reverse=True)[:max(0, k)]
