# PopularScienceBookRecommender

Here is the link to my presentation slides:
https://docs.google.com/presentation/d/1nPsGEysm2qXTsfTVbsp452d_3Vsx2KN3tID-S9_xX34/edit#slide=id.g3606f1c2d_30

## Books Worth Reading

I love reading, especially popular science books. I needed a popular science books recommender for years, and now I have it. Once, I deploy, feel free to use it.

## The Dataset

I web-scraped GoodReads resourse for popular science books list, as well as ratings, reviews, and books metadata. I used Selenium and BeautifulSoup libraries for my scraping.

As a starting point I have:
- 300 books titles and authors
- 300 ratings for each book
- 10 genres per book
- 180 genres in total

## Clustering into Subgroups

Using genres information, I performed KMeans clustering of all books I have into 5 categories. Based on genres frequencies I named those subgroups as follows:

- Health and Medicine
- Psychology and Business
- Nature and Biology
- Space and Technology
- History and Philosophy

Those clusters can be used as filters.

## Recommender system

I build two types recommenders: collaborative filtering and hybrid(content + collaborative)

