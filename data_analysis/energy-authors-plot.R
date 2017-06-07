require(tidyr)
require(plyr)
require(dplyr)

#setwd("~/dhh17/data")

# read the Yle articles dataset imported through the Yle API for the metadata
articles_with_metadata <- read.csv("articles-yle-energy.csv")

# get a histogram of number of articles per author
articles_per_author <- data.frame(table(articles_with_metadata[articles_with_metadata$authors != "",]$authors))
colnames(articles_per_author) <- c("author", "articles")
articles_per_author$author <- as.character(articles_per_author$author)

# split rows with multiple authors into new rows
new_df <- articles_per_author %>% mutate(author = strsplit(as.character(author), ",")) %>% unnest(author)
# merge/sum the new rows with existing author counts
new_df <- ddply(new_df,.(author),summarize,articles=sum(articles))
articles_per_author <- new_df

# drop the first 30 rows that contain mysterious "Yle *" authors that don't actually match "Yle *"
articles_per_author <- articles_per_author[31:nrow(articles_per_author),]

# drop the other well-behaving generic "Yle *" authors
articles_per_author <- articles_per_author[substr(articles_per_author$author, 1, 4) != "Yle ",]

hist(articles_per_author$articles, breaks=max(articles_per_author$articles),
     main="Number of articles published by a single author\n(energy topics, Yle)",
     xlab="number of articles per author", ylab="authors")
