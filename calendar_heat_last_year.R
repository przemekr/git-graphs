#!/usr/bin/env Rscript
repos = commandArgs(trailingOnly=TRUE)

library(knitr)
library(ggplot2)
library(timeSeries)
source("calendarHeat.R")

agregatePerDay <- function(dates, values, f) {
   t = strptime(as.character(dates), format="%F %T")
   ts = timeSeries(values, t)
   by = timeSequence(from=start(ts), to=end(ts), by='day')
   timeSeries::aggregate(ts, by, f)
}


sapply(repos, function(repo) {
       print(repo)
   d <- read.csv(pipe(sprintf(
      "psql ehub -c \"\\copy (
         SELECT commitid,to_char(date, 'YYYY-MM-DD HH24:MI:SS') AS date
         FROM hub_commit, hub_project
         WHERE hub_commit.project_id = hub_project.id
         AND hub_project.name = '%s')
      TO stdout CSV HEADER\"", repo
      )))

   commits = agregatePerDay(d$date, d$commitid, length)

   df = data.frame(time(commits), commits$TS.1)
   names(df) <- c("time", "commits")
   png(sprintf("activity_cal_%s.png", repo))
   calendarHeat(time(commits), commits, varname=repo)
   dev.off()
})
