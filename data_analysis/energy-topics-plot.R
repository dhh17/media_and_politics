require("quanteda")
require("data.table")
require("ggplot2")
require("tidyr")
require("RColorBrewer")
#require("dplyr")

#setwd("~/dhh17/data")

#read the csv file with fread and no encoding problem here! jeee!
articles <- fread("energy-lemmas-yle.csv", header=FALSE, encoding="UTF-8")
column_names <- c("keyword", "timestamp", "article_id", "lemmatized")
colnames(articles) <- column_names

# add the publication year as an auxiliary column for more convenient processing later
articles$year <- substr(articles$timestamp, 1, 4)

# remove the single article that has been dated for 1970
articles <- articles[year != 1970]

topics_lower <- c("aaltovoima", "aurinkokenno", "aurinkovoima", "bioenergia", "bioenergia", "biokaasu", "biovoima",
                  "energiavarat", "fossiiliset", "hiili", "hiilivoima", "kaasu", "kaukolämpö", "lämmitys", "lämmöntuotanto",
                  "lämpölaitos", "lämpövoimala", "lng", "maakaasu", "maalämpö", "öljy", "öljynjalostamo", "polttoaine",
                  "puuenergia", "sähkö", "sähköntuotanto", "sähköverkko", "turve", "turve", "tuulivoima", "uraani", "vesivoima",
                  "vuorovesienergia", "ydinvoima", "aurinkoenergia", "biodiesel", "bioetanoli", "biomassa", "biopolttoaine",
                  "energiajäte", "fuusiovoima")

# construct the quanteda corpus
articles_corp <- corpus(articles, text_field = "lemmatized")
articles_dfm <- dfm(articles_corp, select=topics_lower, groups="year")
articles_dfm_df <- as.data.frame(articles_dfm)

# aggregate topics into somewhat broader categories
aggregate_topics <- c("solar", "hydro", "wind", "bioenergy", "coal", "natural_gas", "oil",
                      "nuclear", "peat", "other_renewables")

aggregated <- data.frame(matrix(0, ncol=length(aggregate_topics), nrow=nrow(articles_dfm_df)))
colnames(aggregated) <- aggregate_topics

aggregated$solar <- articles_dfm_df$aurinkoenergia +
                           articles_dfm_df$aurinkokenno +
                           articles_dfm_df$aurinkovoima
aggregated$hydro <- articles_dfm_df$vesivoima
aggregated$wind <- articles_dfm_df$tuulivoima
aggregated$bioenergy <- articles_dfm_df$biodiesel +
                         articles_dfm_df$bioenergia +
                         articles_dfm_df$bioetanoli +
                         articles_dfm_df$biokaasu +
                         articles_dfm_df$biomassa +
                         articles_dfm_df$biopolttoaine +
                         articles_dfm_df$biovoima +
                         articles_dfm_df$puuenergia
aggregated$coal <- articles_dfm_df$hiili + articles_dfm_df$hiilivoima
aggregated$natural_gas <- articles_dfm_df$maakaasu + articles_dfm_df$kaasu
aggregated$oil <- articles_dfm_df$öljy
aggregated$nuclear <- articles_dfm_df$ydinvoima + articles_dfm_df$uraani
aggregated$peat <- articles_dfm_df$turve
aggregated$other_renewables <- articles_dfm_df$aaltovoima +
                              articles_dfm_df$vuorovesienergia +
                              articles_dfm_df$energiajäte +
                              articles_dfm_df$maalämpö

# compute relative topic occurrence frequencies per year
aggregated_relative <- aggregated / rowSums(aggregated)
aggregated_relative$year <- rownames(articles_dfm_df)

# reshape the data for easier plotting with ggplot2
gathered <- gather(aggregated_relative, topic, count, -year)

#colours <- brewer.pal(ncol(aggregated_relative), "Set3")

#ggplot(data=gathered, aes(x=year, y=count, group=topic, colour=topic)) + geom_line()
ggplot(data=gathered, aes(x=year, y=count, group=topic, fill=topic)) +
       geom_area(position="fill") + ggtitle("Relative media visibility of energy topics (Yle)") +
       labs(x="Year", y="Proportion of mentions")
#ggplot(data=gathered, aes(x=year, y=count, group=topic, fill=colours)) + geom_area(position="fill")
