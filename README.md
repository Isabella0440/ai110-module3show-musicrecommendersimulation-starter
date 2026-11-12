# Music Recommender Simulation

VibeFinder 1.0 ranks an 18-song catalog for a listener's taste profile and explains the points behind each recommendation.

## How The System Works

Streaming services can combine several kinds of evidence. Collaborative filtering draws on behavior across listeners, such as which tracks people with similar listening histories save. Content-based filtering compares song attributes such as genre, mood, or tempo with a listener's preferences. Spotify describes using plays, skips, and saves to refine its representation of a listener's taste. VibeFinder uses a content-based approach with preferences supplied directly by the listener. [Spotify Engineering](https://engineering.atspotify.com/2023/4/humans-machines-a-look-behind-spotifys-algotorial-playlists) · [Spotify's guide to recommendations](https://www.spotify.com/uk/safetyandprivacy/understanding-recommendations)

- A `Song` stores ID, title, artist, genre, mood, energy, tempo in BPM, valence, danceability, and acousticness. Genre, mood, and energy drive the score. Energy captures intensity, while mood can distinguish a happy song from a sad song at the same energy.
- A `UserProfile` stores favorite genre, favorite mood, target energy, and an acoustic preference field from the starter. The CLI supplies the first three as a dictionary. The acoustic preference has no weight in this recipe.

### Algorithm Recipe

1. Award **2 points** for an exact genre match and **1 point** for an exact mood match, ignoring case and surrounding spaces.
2. Add **`1 − abs(song_energy − target_energy)`** points. Both energy values use a 0–1 scale. A song at 0.82 earns 0.98 energy points for a target of 0.80.
3. Score every song and rank the results from highest to lowest. Take the first five by default and keep catalog order for equal scores. `sorted()` returns a new list, while `.sort()` changes its list in place.

**Data flow** — CSV and taste dictionary → score each song and record reasons → sort by score → show the top five.

The genre bonus can push exact matches ahead of tracks that fit the requested mood and energy better.

## Getting Started

The CLI uses only Python's standard library. Run these commands from the project folder.

```sh
python3 -m src.main
python3 -m src.main --all
python3 -m src.main --all --experiment
```

To run the starter tests, install the development requirements with `python3 -m pip install -r requirements.txt` and run `python3 -m pytest -q`.

## Sample Recommendation Output

```text
Loaded songs: 18

High-Energy Pop (pop, happy, energy 0.80)
1. Sunrise City — 3.98 | genre match (+2.00); mood match (+1.00); energy gap 0.02 (+0.98)
2. Gym Hero — 2.87 | genre match (+2.00); energy gap 0.13 (+0.87)
3. Paper Satellites — 2.54 | genre match (+2.00); energy gap 0.46 (+0.54)
4. Rooftop Lights — 1.96 | mood match (+1.00); energy gap 0.04 (+0.96)
5. Thunder in Bloom — 0.95 | energy gap 0.05 (+0.95)

Chill Lofi (lofi, chill, energy 0.40)
1. Midnight Coding — 3.98 | genre match (+2.00); mood match (+1.00); energy gap 0.02 (+0.98)
2. Library Rain — 3.95 | genre match (+2.00); mood match (+1.00); energy gap 0.05 (+0.95)
3. Focus Flow — 3.00 | genre match (+2.00); energy gap 0.00 (+1.00)
4. Soft Geometry — 1.99 | mood match (+1.00); energy gap 0.01 (+0.99)
5. Spacewalk Thoughts — 1.88 | mood match (+1.00); energy gap 0.12 (+0.88)

Deep Intense Rock (rock, intense, energy 0.90)
1. Storm Runner — 3.99 | genre match (+2.00); mood match (+1.00); energy gap 0.01 (+0.99)
2. Thunder in Bloom — 3.95 | genre match (+2.00); mood match (+1.00); energy gap 0.05 (+0.95)
3. Gym Hero — 1.97 | mood match (+1.00); energy gap 0.03 (+0.97)
4. Glass Avalanche — 1.93 | mood match (+1.00); energy gap 0.07 (+0.93)
5. Blue Afterimage — 0.99 | energy gap 0.01 (+0.99)

High-Energy Sad Pop (pop, sad, energy 0.90)
1. Paper Satellites — 3.44 | genre match (+2.00); mood match (+1.00); energy gap 0.56 (+0.44)
2. Gym Hero — 2.97 | genre match (+2.00); energy gap 0.03 (+0.97)
3. Sunrise City — 2.92 | genre match (+2.00); energy gap 0.08 (+0.92)
4. Blue Afterimage — 1.99 | mood match (+1.00); energy gap 0.01 (+0.99)
5. Storm Runner — 0.99 | energy gap 0.01 (+0.99)
```

## Experiments You Tried

The weight shift halved genre from 2 to 1 and doubled the maximum energy bonus from 1 to 2. Mood stayed at 1 and the maximum total stayed at 4. Rooftop Lights moved from fourth to second for High-Energy Pop. Blue Afterimage moved from fourth to first for High-Energy Sad Pop. The Lofi and Rock profiles retained the same order. The shift better reflects a listener who cares most about intensity, while a listener who wants exact pop may prefer the baseline.

## Limitations and Risks

One label per song makes related styles such as pop and indie pop count as separate categories. Repeated use of the same profile can keep the same genres near the top. The small catalog also limits the available matches.

## Reflection

See the [Model Card](model_card.md) for the evaluation, limitations, and reflection draft.
