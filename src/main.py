"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations_for_profile(profile_name: str, user_prefs: dict, songs: list[dict]) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 70)
    print(f"🎵  PROFILE: {profile_name}")
    print("=" * 70 + "\n")

    for idx, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec

        rank_bar = "▶" if idx == 1 else "▪" if idx <= 3 else "◦"
        score_bar = "█" * int(score) + "░" * (10 - int(score))

        print(f"  {rank_bar} #{idx}  {song['title']}")
        print(f"      Artist: {song['artist']}")
        print(f"      Score: {score:.2f}  [{score_bar}]")
        print(f"      Why: {explanation}")
        print()


def main() -> None:
    songs = load_songs("../data/songs.csv")

    # Diverse baseline profiles + adversarial edge cases from system evaluation.
    stress_test_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.92,
            "tempo_bpm": 132,
            "valence": 0.86,
            "danceability": 0.88,
            "acousticness": 0.10,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.28,
            "tempo_bpm": 78,
            "valence": 0.46,
            "danceability": 0.42,
            "acousticness": 0.85,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.90,
            "tempo_bpm": 148,
            "valence": 0.34,
            "danceability": 0.45,
            "acousticness": 0.08,
            "likes_acoustic": False,
        },
        "Adversarial Conflict: Sad but Hyper": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.90,
            "tempo_bpm": 145,
            "valence": 0.12,
            "danceability": 0.80,
            "acousticness": 0.12,
            "likes_acoustic": False,
        },
        "Adversarial Mismatch: Acoustic Club": {
            "genre": "edm",
            "mood": "chill",
            "energy": 0.82,
            "tempo_bpm": 126,
            "valence": 0.70,
            "danceability": 0.86,
            "acousticness": 0.95,
            "likes_acoustic": True,
        },
    }

    for profile_name, prefs in stress_test_profiles.items():
        print_recommendations_for_profile(profile_name, prefs, songs)


if __name__ == "__main__":
    main()
