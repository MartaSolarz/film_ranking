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

Project contains three different analysis of the data from IMDb.

1. **Top 10 countries based on the N the best rated movies.**

## How to run the program?

```bash
    python main.py [-h] [-start START_YEAR] [-end END_YEAR] basics_title_data rating_title_data akas_title_data countries_name_data
```

**Arguments:**

- basics_title_data: path to the file with basic information about the title
- rating_title_data: path to the file with rating information about the title
- akas_title_data: path to the file with alternative titles
- countries_name_data: path to the file with countries names
- -start: start year
- -end: end year
- -h: help

**Example:**

```bash
    python main.py -start 2010 -end 2019 ./data/title.basics.tsv ./data/title.ratings.tsv ./data/title.akas.tsv ./data/countries.csv
```

## How to run the tests?

TODO

## Profiling

TODO

**Marta Solarz, MISMaP UW 2023/2024**