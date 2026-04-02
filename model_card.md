# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SessionSeed Recommender 1.0**

---

## 2. Intended Use  

This recommender generates top-k song suggestions from a small CSV catalog based on a single user taste profile. It assumes the user has a meaningful "seed" preference from a current listening session, especially around artist, genre, and mood, and then refines results with numeric targets like tempo and energy. This is for classroom exploration, not production use with real users.

---

## 3. How the Model Works  

Each song is scored one-by-one against the user profile. The model gives the largest weight to artist match, then genre and mood matches, then adds distance-based similarity for tempo, energy, valence, danceability, and acousticness. Songs that are closer to the target numeric values get more points than songs that are farther away. After all songs are scored, the model ranks them from highest to lowest and returns the top results with short explanations.

Compared with the starter logic, I implemented a full scoring loop, weighted feature priorities, CSV loading, ranking, and explanation text for why a song was recommended.

---

## 4. Data  

The catalog currently has 26 songs. It includes genres and moods such as pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, afrobeat, metal, country, reggae, edm, r&b, folk, jazz pop, chamber pop, and vocal jazz, with moods ranging from chill/relaxed to intense/aggressive and romantic/wistful.

I expanded the starter dataset by adding additional rows, including Laufey songs and stylistically adjacent artists (for example, Norah Jones and Samara Joy), to improve coverage of softer jazz-pop and acoustic listening styles.

Important gaps still exist: the dataset is small, mostly English-language, and does not represent many regional genres, lyrical themes, or subcultures.

---

## 5. Strengths  

- Works well for users with clear, stable preferences in artist/genre/mood.
- Captures session intent better than a single-feature recommender because it combines categorical and numeric signals.
- Produces transparent output by returning song title, score, and reason text in the CLI.
- Behaves intuitively when numeric targets are coherent (for example, high-energy/high-tempo profiles receive energetic songs).

---

## 6. Limitations and Bias 

- It does not consider lyrics, language, release era, popularity, or cultural context.
- Artist-heavy weighting can over-concentrate recommendations and reduce discovery.
- Small catalog size means some users may get repetitive or weakly relevant results.
- Underrepresented genres will naturally be shown less often, creating exposure bias.
- A single profile cannot represent changing mood within one listening session.

---

## 7. Evaluation  

I evaluated behavior by running the CLI simulation and inspecting whether top recommendations matched the intended profile and scoring priorities. I also checked that recommendation explanations reflected dominant signals (artist match and numeric closeness) and used existing unit tests for baseline recommender behavior.

A notable observation was that strong artist weighting can lift artist matches even when mood differs, which is useful for fan behavior but can conflict with strict vibe matching.

TODO: add 2-3 explicit profile comparison runs (for example, intense rock vs chill lofi vs Laufey-like profile) and document expected versus actual top-k outputs in this section.

---

## 8. Future Work  

- Add preference decay and diversity constraints so top-k results are less repetitive.
- Support multi-objective ranking (for example, 70% preference fit + 30% novelty).
- Introduce optional filters for language, era, or explicit-content preferences.
- Improve explanation quality with per-feature contribution breakdown.
- Expand the catalog substantially and rebalance genre representation.

---

## 9. Personal Reflection  

Building this made it clear that recommendation quality depends as much on feature design and weighting choices as on algorithm structure. A simple weighted scorer can feel surprisingly useful when preferences are clear, but it can also encode strong bias quickly when one feature (like artist) dominates. This project changed how I think about real music apps: ranking is not just "what matches," it is also a policy decision about exploration, fairness, and which user signals are treated as most important.
