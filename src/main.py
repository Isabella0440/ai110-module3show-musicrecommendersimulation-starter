"""Run the music recommender and its evaluation from the command line."""

import argparse
from pathlib import Path

from .recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.80},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.90},
    "High-Energy Sad Pop": {"genre": "pop", "mood": "sad", "energy": 0.90},
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Run all four taste profiles.")
    parser.add_argument("--experiment", action="store_true", help="Run the weight shift.")
    args = parser.parse_args()

    catalog_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    songs = load_songs(catalog_path)
    print(f"Loaded songs: {len(songs)}")
    genre_weight, energy_weight = (1.0, 2.0) if args.experiment else (2.0, 1.0)
    if args.experiment:
        print("Weight shift: genre 1.0, mood 1.0, energy up to 2.0")

    profiles = PROFILES if args.all else {"High-Energy Pop": PROFILES["High-Energy Pop"]}
    for name, prefs in profiles.items():
        print(f"\n{name} ({prefs['genre']}, {prefs['mood']}, energy {prefs['energy']:.2f})")
        results = recommend_songs(
            prefs, songs, k=5, genre_weight=genre_weight, energy_weight=energy_weight
        )
        for rank, (song, score, reasons) in enumerate(results, start=1):
            print(f"{rank}. {song['title']} — {score:.2f} | {reasons}")


if __name__ == "__main__":
    main()
