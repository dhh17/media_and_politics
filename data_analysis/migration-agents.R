require("dplyr")
require("ggplot2")
require("zoo")

group <- function(data, groupBy, facetBy, dateFunction) {
  return (data %>% mutate(date = as.Date(dateFunction(date))) %>% group_by_("date",facetBy,groupBy) %>% count())
}

migration_agents <- read.csv("hs-political-agents-migration.csv",stringsAsFactors = FALSE, col.names=c("queryLemma","name","date","id")) %>% filter(date>as.Date("2014-01-01"))

groupedAgents <- group(migration_agents,"name","name",as.yearqtr) %>% group_by(name) %>% filter(sum(n)>220) %>% ungroup()
ggplot(groupedAgents, aes_string(x="date",y="n",group="name",color="name")) + geom_line() + coord_cartesian(ylim=c(0, 135))


