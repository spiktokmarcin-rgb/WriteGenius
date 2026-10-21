# Scientific Foundations & Research Bibliography 📚

WriteGenius and the broader **ContentGenius** initiative (in continuous development since 2022) are grounded in empirical linguistics, statistical stylometry, and quantitative readability research. 

This document details the peer-reviewed publications, foundational papers, and mathematical formulas underpinning WriteGenius's multi-lingual European evaluation engine.

---

## 1. Slavic & Polish Readability Research

### Foundational Paper: Walery Pisarek (1969)
* **Citation:** Pisarek, W. (1969). *Jak mierzyć czytelność tekstu* [How to measure text readability]. *Zeszyty Prasoznawcze*, 10(4), 35–46.
* **Core Contribution:** Empirically established that English readability metrics (which treat words with 3+ syllables as complex) yield invalid scores for Slavic languages due to synthetic inflection. In Polish, words with **4 or more syllables ($B \ge 4$)** constitute the true cognitive threshold for difficulty.
* **Formula Implemented:**
  $$W = \frac{T}{Z} + \frac{B_{4+}}{T} \times 100$$
  where $T$ = total words, $Z$ = total sentences, $B_{4+}$ = words with 4+ syllables.

```bibtex
@article{pisarek1969czytelnosc,
  author    = {Walery Pisarek},
  title     = {Jak mierzy{\'c} czytelno{\'s}{\'c} tekstu},
  journal   = {Zeszyty Prasoznawcze},
  volume    = {10},
  number    = {4},
  pages     = {35--46},
  year      = {1969},
  publisher = {Krakowski O{\'s}rodek Bada{\'n} Prasoznawczych}
}
```

### Computational Readability in Polish: Broda et al. (LREC 2014)
* **Citation:** Broda, B., Nitoń, B., Gruszczyński, W., & Ogrodniczuk, M. (2014). *Measuring Readability of Polish Texts: A New Computational Approach*. In *Proceedings of the Ninth International Conference on Language Resources and Evaluation (LREC'14)*, Reykjavik, Iceland, pp. 3118–3122.
* **Core Contribution:** Demonstrates the necessity of syllable-level nucleus detection (accounting for palatal glides such as *i* before vowels: *ia, ie, io, iu, ią, ię*) rather than raw orthographic vowel counts when automating Polish linguistic metrics.

```bibtex
@inproceedings{broda2014measuring,
  author    = {Bartosz Broda and Bart{\l}omiej Nito{\'n} and W{\l}odzimierz Gruszczy{\'n}ski and Maciej Ogrodniczuk},
  title     = {Measuring Readability of Polish Texts: A New Computational Approach},
  booktitle = {Proceedings of the Ninth International Conference on Language Resources and Evaluation (LREC'14)},
  pages     = {3118--3122},
  year      = {2014},
  address   = {Reykjavik, Iceland}
}
```

---

## 2. Classical International Readability Formulas

### Flesch Reading Ease (1948)
* **Citation:** Flesch, R. (1948). *A new readability yardstick*. *Journal of Applied Psychology*, 32(3), 221–233.
* **WriteGenius Implementation:** Implements baseline English coefficients as well as European calibrations (Amstad 1978 for German, Kandel-Moles 1958 for French, Fernandez-Huerta 1959 for Spanish).

```bibtex
@article{flesch1948new,
  author    = {Rudolf Flesch},
  title     = {A new readability yardstick},
  journal   = {Journal of Applied Psychology},
  volume    = {32},
  number    = {3},
  pages     = {221--233},
  year      = {1948},
  doi       = {10.1037/h0057532}
}
```

### Flesch-Kincaid Grade Level (1975)
* **Citation:** Kincaid, J. P., Fishburne, R. P., Rogers, R. L., & Chissom, B. S. (1975). *Derivation of new readability formulas (Automated Readability Index, Fog Count, and Flesch Reading Ease Formula) for Navy enlisted personnel*. Research Branch Report 8-75, Chief of Naval Technical Training, Naval Air Station Memphis.
* **Formula:**
  $$\text{FKGL} = 0.39 \left(\frac{\text{Total Words}}{\text{Total Sentences}}\right) + 11.8 \left(\frac{\text{Total Syllables}}{\text{Total Words}}\right) - 15.59$$

```bibtex
@techreport{kincaid1975derivation,
  author      = {J. Peter Kincaid and Robert P. Fishburne and Richard L. Rogers and Brad S. Chissom},
  title       = {Derivation of new readability formulas for Navy enlisted personnel},
  institution = {Chief of Naval Technical Training, Naval Air Station Memphis},
  year        = {1975},
  number      = {Research Branch Report 8-75}
}
```

### Gunning Fog Index (1952)
* **Citation:** Gunning, R. (1952). *The Technique of Clear Writing*. McGraw-Hill International.
* **Formula:**
  $$\text{FOG} = 0.4 \left[ \left(\frac{\text{Words}}{\text{Sentences}}\right) + 100 \left(\frac{\text{Complex Words}}{\text{Words}}\right) \right]$$

```bibtex
@book{gunning1952technique,
  author    = {Robert Gunning},
  title     = {The Technique of Clear Writing},
  publisher = {McGraw-Hill},
  year      = {1952},
  address   = {New York}
}
```

### Coleman-Liau Index (1975)
* **Citation:** Coleman, E. B., & Liau, T. L. (1975). *A computer readability formula designed for machine scoring*. *Journal of Applied Psychology*, 60(2), 283–284.
* **Formula:**
  $$\text{CLI} = 0.0588 \times L - 0.296 \times S - 15.8$$
  where $L$ = average number of letters per 100 words, $S$ = average number of sentences per 100 words.

```bibtex
@article{coleman1975computer,
  author  = {E. B. Coleman and T. L. Liau},
  title   = {A computer readability formula designed for machine scoring},
  journal = {Journal of Applied Psychology},
  volume  = {60},
  number  = {2},
  pages   = {283--284},
  year    = {1975},
  doi     = {10.1037/h0076540}
}
```

### Automated Readability Index (ARI, 1967)
* **Citation:** Smith, E. A., & Senter, R. J. (1967). *Automated Readability Index*. Technical Report AMRL-TR-66-220, Aerospace Medical Research Laboratories, Wright-Patterson Air Force Base.

```bibtex
@techreport{smith1967automated,
  author      = {E. A. Smith and R. J. Senter},
  title       = {Automated Readability Index},
  institution = {Aerospace Medical Research Laboratories, Wright-Patterson AFB},
  year        = {1967},
  number      = {AMRL-TR-66-220}
}
```

---

## 3. Statistical Lexical Diversity & Stylometry

### Guiraud's Root TTR Index (1954)
* **Citation:** Guiraud, P. (1954). *Les caractères statistiques du vocabulaire: Essai de méthodologie*. Presses Universitaires de France, Paris.
* **Core Contribution:** Overcomes the sample-size dependency of the standard Type-Token Ratio (TTR) by computing:
  $$R = \frac{V}{\sqrt{N}}$$
  where $V$ is vocabulary richness (unique types) and $N$ is total token count.

```bibtex
@book{guiraud1954caracteres,
  author    = {Pierre Guiraud},
  title     = {Les caract{\`e}res statistiques du vocabulaire: Essai de m{\'e}thodologie},
  publisher = {Presses Universitaires de France},
  year      = {1954},
  address   = {Paris}
}
```

### Yule's Lexical Characteristics & Hapax Legomena (1944)
* **Citation:** Yule, G. U. (1944). *The Statistical Study of Literary Vocabulary*. Cambridge University Press.
* **Core Contribution:** Establishes mathematical properties of words occurring exactly once (*hapax legomena*) as stable indicators of authorial vocabulary breadth and syntactic variation.

```bibtex
@book{yule1944statistical,
  author    = {George Udny Yule},
  title     = {The Statistical Study of Literary Vocabulary},
  publisher = {Cambridge University Press},
  year      = {1944},
  address   = {Cambridge}
}
```

---

## 4. Sentiment & Contextual Negation Shift

### Opinion Mining & Lexical Polarity (Pang & Lee 2008)
* **Citation:** Pang, B., & Lee, L. (2008). *Opinion Mining and Sentiment Analysis*. *Foundations and Trends in Information Retrieval*, 2(1–2), 1–135.
* **Core Contribution:** Documents the necessity of local window-based negation shifting (flipping valence when modal negations appear within a 3-token horizon: e.g. *nie jest dobry* / *not good*) and intensifier scaling (*bardzo*, *extremely*).

```bibtex
@article{pang2008opinion,
  author  = {Bo Pang and Lillian Lee},
  title   = {Opinion Mining and Sentiment Analysis},
  journal = {Foundations and Trends in Information Retrieval},
  volume  = {2},
  number  = {1--2},
  pages   = {1--135},
  year    = {2008},
  doi     = {10.1561/1500000011}
}
```

---

## 5. ContentGenius & WriteGenius Technical Reports (2022–2026)

WriteGenius represents the open-source evaluation core of the broader **ContentGenius** initiative (commenced in 2022). ContentGenius was created to establish empirical evidence that AI-assisted content can match and exceed human-authored text in information density, semantic depth, and readability without relying on generative filler.

To cite the WriteGenius project directly:

```bibtex
@software{writegenius2026,
  author    = {WriteGenius Contributors},
  title     = {WriteGenius: Multilingual Natural Language Processing \& Readability Engine for European Languages},
  year      = {2026},
  url       = {https://github.com/spiktokmarcin-rgb/WriteGenius},
  note      = {Open-source evaluation core of the ContentGenius ecosystem (est. 2022)}
}
```
