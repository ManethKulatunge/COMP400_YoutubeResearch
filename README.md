# Youtube Conspiracy Theory Recommendations

## Goal 

Part of my COMP 400 project where I observe whether the YouTube recommendation system siloes users towards conspiracy theory-related content. 

## Repository Breakdown

data_cleaning - consisting of scripts I used to clean data passed into models

datasets - consists of data sets I used for the text classification process/model

text_classification - consists of notebook and python script related to text classification

breadth_first - code and files related to breadth first selenium scraper

depth_first - code and files related to depth first selenium scraper

## Experiment Summary and Progress

There are broadly two components to my experiment. Web Scraping and Text Classification. I have currently worked on Text Classification where we can pass in text (youtube comments, title etc) that we want to classify and have the model return a label (class value) which tells us if it is a conspiracy or not.

The web scraper will assist me with obtaining suggestions made by the recommendation system and use the aforementioned model to classify the recommended videos
