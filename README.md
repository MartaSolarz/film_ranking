# Film ranking

**The final project NYPD 2023/2024**

## Table of contents

1. [Description and project explanation](#description-and-project-explanation)
2. [How to run the program?](#how-to-run-the-program)
3. [How to run the tests?](#how-to-run-the-tests)
4. [Profiling](#profiling)

![img](img.webp)
*Source: DALL-E, OpenAI*

## Description and project explanation

TODO

## How to run the program?

```bash
    python main.py [-h] [-start START_YEAR] [-end END_YEAR] film_data ranking_film_data crew_data
```

**Arguments:**

- film_data: path to the film data file
- ranking_film_data: path to the ranking film data file
- crew_data: path to the crew data file
- -start: start year
- -end: end year
- -h: help

**Example:**

```bash
    python main.py -start 2010 -end 2019 ./data/title.basics.tsv ./data/title.ratings.tsv ./data/title.crew.tsv
```

## How to run the tests?

TODO

## Profiling

TODO

**Marta Solarz, MISMaP UW 2023/2024**