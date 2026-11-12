# Model Card — VibeFinder 1.0

## 1. Model Name

VibeFinder 1.0.

## 2. Intended Use

This classroom simulator suggests songs that fit a listener's stated genre, mood, and energy. It assumes the listener can describe what they want with one value for each preference. A real streaming service or artist promotion system would need a larger catalog, listener feedback, and validation.

## 3. How the Model Works

Every song earns two points for matching the requested genre and one for matching the mood. It also earns up to one point for being close to the requested energy. A song at the exact energy target earns the full energy point. The simulator ranks songs by total points and shows the reasons for each recommendation.

## 4. Data

The catalog has 18 rows. It keeps all 10 starter tracks and adds eight fictional tracks. The additions introduce metal, folk, salsa, drum and bass, downtempo, and soul. They also add moods such as sad, nostalgic, joyful, and romantic. Each row stores metadata and numeric descriptors. The catalog has no audio, lyrics, listening history, or measurements from real listeners.

## 5. Strengths

Sunrise City leads the happy pop list with 3.98 points. It matches pop and happy and is only 0.02 above the energy target. Midnight Coding leads Chill Lofi for the same reason. Its lower energy fits the idea of background music for studying.

## 6. Limitations and Bias

An exact genre match earns two points, more than any single mood or energy match. In the happy pop run, the low-energy, sad Paper Satellites ranked above the happy, similarly energetic Rooftop Lights because the latter is labeled indie pop. This rule can keep similar tracks from other genres out of view and create a filter bubble when someone repeatedly uses the same profile. The small catalog makes the problem more visible because each label has only a few examples.

## 7. Evaluation

I ran the top five for four profiles using the same catalog. The [README](README.md#sample-recommendation-output) records the terminal output. The fourth profile deliberately asks for sad music with high energy to see what happens when the available tracks match different parts of the request.

| Profiles compared | What changed and why |
| --- | --- |
| High-Energy Pop and Chill Lofi | Sunrise City gives way to Midnight Coding because the second profile asks for chill lofi at half the energy target. |
| High-Energy Pop and Deep Intense Rock | Storm Runner leads Rock. Gym Hero appears in both lists because it is pop and also intense. |
| High-Energy Pop and High-Energy Sad Pop | Paper Satellites moves from third to first because it matches sad, even though its energy is far below the new target. |
| Chill Lofi and Deep Intense Rock | Midnight Coding and Library Rain lead Lofi, while Storm Runner and Thunder in Bloom lead Rock. The two lists share no tracks because genre, mood, and energy all differ. |
| Chill Lofi and High-Energy Sad Pop | Both winners have relatively low energy, but Midnight Coding fits its target and Paper Satellites wins through genre and mood points. |
| Deep Intense Rock and High-Energy Sad Pop | Both have a 0.90 target. Storm Runner drops from first to fifth when its rock and intense bonuses disappear. |

I halved the genre bonus and doubled the energy bonus while keeping the mood bonus at one. For the sad pop profile, Blue Afterimage rose from fourth (1.99) to first (2.98), and Paper Satellites dropped from first (3.44) to third (2.88). This looks more fitting if high energy is essential. With no listener ratings, the experiment shows a change in what the system prioritizes. It does not measure accuracy.

## 8. Future Work

- Allow listeners to prioritize genre, mood, or energy for a particular session.
- Add multiple tags per song so related genres and moods can earn partial credit.
- Compare results with listener feedback and test whether adding a cross-genre pick helps discovery.

## 9. Personal Reflection

*Draft to personalize before submission.*

The biggest learning moment was seeing how a two-point genre bonus could move a low-energy song ahead of a much closer energy match. AI helped turn the idea of an energy gap into a scoring rule and suggested a profile that would stress the weights. I checked the explanations against the actual scores because a result that sounds plausible can still come from the wrong rule.

I was surprised that three features were enough to produce recognizable lists for studying and for high-energy rock. Next I would try giving listeners control over which preference matters most and see whether their chosen weights improve the results.
