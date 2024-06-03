# Film ranking

**The final project of NPD 2023/2024**

## Table of contents

1. [Description and project explanation](#1-description-and-project-explanation)

    1.1. [Top Movies Country Rating Analysis](#11-top-movies-country-rating-analysis)

    1.2. [Country Hegemony Analysis Based on Economic and Demographic Metrics](#12-country-hegemony-analysis-based-on-economic-and-demographic-metrics)

    1.3. [Director Career Progression Analysis Based on Film Ratings and Votes](#13-director-career-progression-analysis-based-on-film-ratings-and-votes)
2. [Observations and conclusions for performed analyses](#2-observations-and-conclusions-for-performed-analyses)

    2.1. [Top Movies Country Rating Analysis](#21-top-movies-country-rating-analysis)

    2.2. [Country Hegemony Analysis Based on Economic and Demographic Metrics](#22-country-hegemony-analysis-based-on-economic-and-demographic-metrics)

    2.3. [Director Career Progression Analysis Based on Film Ratings and Votes](#23-director-career-progression-analysis-based-on-film-ratings-and-votes)
2. [How to run the program?](#3-how-to-run-the-program)
3. [How to run the tests?](#4-how-to-run-the-tests)
4. [Profiling](#5-profiling)
5. [How to import the package?](#6-how-to-import-the-package)

![img](img.webp)
*Source: DALL-E, OpenAI*

## 1. Description and project explanation

The Project contains three different analyses of the data from IMDb.

### 1.1. Top Movies Country Rating Analysis.

This analysis aims to evaluate and rank countries based on the average ratings of their top movies. 

The main goal is to generate detailed rankings for different sets of top movies and provide comprehensive results for each category.

**Overview:**

- The analysis processes a merged DataFrame containing movie data.
- It considers multiple sets of top movies (e.g., top 10, top 20, top 50, top 100, and top 200).
- For each set, the analysis calculates the average ratings of the top n movies per country.
- It only includes countries with at least n movies to ensure fair and comparable rankings.
- The results for each set are sorted by average rating and saved as CSV files.

**Outcome:**

The final output consists of CSV files named according to the number of top movies considered (e.g., 1_top_10_ratings_{start_year}_{end_year}.csv) and saved in the results folder.

For each set, the top 10 countries are printed.

### 1.2. Country Hegemony Analysis Based on Economic and Demographic Metrics

This analysis aims to evaluate the hegemony of countries based on various economic and demographic metrics in relation to their movie ratings. 

The main goal is to generate comprehensive rankings and hegemony indicators for countries based on their population, GDP, and GDP per capita.

**Overview:**

- The analysis processes a merged DataFrame containing movie data and calculates impact metrics.
- It generates rankings based on weak and strong impact metrics and merges these with demographic and economic data.
- The analysis computes hegemony indicators for population, GDP, and GDP per capita.
- Results are saved as CSV files for further review and analysis.

**Outcome:**

The final output consists of CSV files named according to the metric considered (e.g., 2_hegemony_{metric}_result_{start_year}_{end_year}.csv) and saved in the results folder.

For each metric and weak or strong impact, the top 10 countries are printed.

### 1.3. Director Career Progression Analysis Based on Film Ratings and Votes.

This analysis focuses on evaluating the career progression of film directors based on the average ratings and the number of votes their films receive over time. 

The main goal is to identify how directors' performance changes throughout their careers by examining different sets of their films.

**Overview:**

- The analysis processes a merged DataFrame containing movie data and focuses on directors with a minimum number of films.
- It considers multiple sets of films (e.g., top 6, 10, 20, 50, 100, 200) to evaluate the career progression.
- For each set, the analysis calculates the difference in average ratings and the number of votes between the first half and the last half of the directors' films.

**Outcome:**

The final output consists of CSV files named according to the number of films considered (e.g., 3_{rating/votes_diff}_10_{start_year}_{end_year}.csv) and saved in the results folder.

For each set, the top 10 directors with the highest rating or votes difference are printed.

## 2. Observations and conclusions from the analyses performed

### 2.1. Top Movies Country Rating Analysis

- The analysis of top movies by country rating shows that the United States consistently ranks high across different sets of top movies.
- We could also observe that for every set of number of top movies, the same countries are present in the top 10, sometimes only in different order.

### 2.2. Country Hegemony Analysis Based on Economic and Demographic Metrics

- High values of strong hegemony are often given to countries with low values of economic and demographic indicators, which is caused by high ratings of films in these countries.
- It can therefore be concluded that small and poor countries (in terms of all analyzed metrics) usually rate the films they watch highly, which proves that the results should be divided into groups of countries that are similar in terms of economics and demographics.

### 2.3. Director Career Progression Analysis Based on Film Ratings and Votes

- The more films of directors are taken into account when calculating the difference in ratings and the number of votes, the smaller the differences between the first and last films are visible (directors with the greatest progress record smaller differences in quality/number of votes than when few films are taken into account).
- Directors who have directed the most films (and therefore are the best) record less progress over the course of their careers than directors who have directed few films (the first ones were poorly rated and the last ones much better).

## 3. How to run the program?

```bash
    python main.py [-h] [-start START_YEAR] [-end END_YEAR] basics_title_data rating_title_data akas_title_data crew_title_data name_people_data countries_name_data population_data gdp_data
```

**Arguments:**

- basics_title_data: path to the file with basic information about the title
- rating_title_data: path to the file with rating information about the title
- akas_title_data: path to the file with alternative titles
- crew_title_data: path to the file with crew information
- name_people_data: path to the file with people names
- countries_name_data: path to the file with countries names
- population_data: path to the file with population data
- gdp_data: path to the file with gdp data
- -start: start year
- -end: end year
- -h: help

**Example:**

```bash
    python app.py -start 1990 -end 2020 ./data/title.basics.tsv ./data/title.ratings.tsv ./data/title.akas.tsv ./data/title.crew.tsv ./data/name.basics.tsv ./data/countries.csv ./data/population.csv ./data/gdp.csv 
```

## 4. How to run the tests?

```bash
    python -m pytest
```

## 5. Profiling

The program is profiled using the `cProfile` module. 
The results are saved in the `profile_results.txt` file.

**Possible improvements based on profiling:**
- The majority of the time is spent on loading data. To improve performance, might consider optimizing the data loading process (using e.g. a more efficient data structure or parallel processing).
- The data processing and merging steps are also time-consuming. To optimize performance, could consider using, for example, chunk processing, or checking to see if there are unnecessary copies of the data are created in memory.
- Pandas' merge function is quite expensive, it may be important to ensure data is properly sorted and indexed before linking to improve performance. It may also be beneficial to combine categorical data instead of strings to speed up the process.
- It may also be beneficial to use int32 instead of int64 for columns with integer data to reduce memory usage.

## 6. How to import the package?

```bash
    import film_ranking
```


**Author:** Marta Solarz, MISMaP UW 2023/2024
