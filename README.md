---
author:
- Abey Richard Hurtis
bibliography:
- ref.bib
date: 2024-10-16
title: Project Discription
---

# Introduction

The **Data Use in Academia Dataset** is a subset of the Semantic Scholar
Open Research Corpus (S2ORC) [@DataUseinAcademiaDataset] [@lo2020],
comprising over 130 million English-language academic papers across
multiple disciplines, sourced from publishers, open archives like arXiv
and PubMed, and web crawls. To enhance usability and relevance,
restrictions were applied: only articles with an abstract and a parsed
PDF or LaTeX file were included, resulting in approximately 30 million
articles. Additionally, only articles published between 2000 and 2020
were considered. Articles from fields less likely to utilize data from
national statistical systems, such as Biology and Engineering, were
excluded, narrowing the dataset to around 10 million articles. Natural
Language Processing (NLP) techniques were employed to extract the
countries of study and data usage from the text, utilizing two main
approaches: regular expression searches based on ISO3166 country names
and Named Entity Recognition (NER) via the spaCy library.

![Top 80% Countries by number of papers
published](countrry_output.png)

## Questions

-   Which countries or regions are the most frequent sources of academic
    data?

-   What are the papers with the highest outbound and inbound citations?

    -   Analyze citation distribution to identify highly influential
        works.

-   How has publication volume in various fields evolved over time?

    -   Identify fields with the most and least growth over time.

-   Are there trends in annual increases or decreases in publications?

    -   Examine year-over-year changes in publication volume.

-   Which fields of study are most represented by country?

-   Which journals or venues publish the most articles?

## Analysis

### Observing the top Journal and amount of papers published. 

![Top 80% Countries by number of papers
published](top80journals.pdf)

### TODO
1. Create Unique Journal count
2. Sort publication by country and journal
3. Find Median publication by year by country
   
# References