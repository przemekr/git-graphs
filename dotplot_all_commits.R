library(ggplot2)
library(timeSeries)

agregatePerDay <- function(dates, values, f) {
   t = strptime(dates, format="%F %T %z")
   ts = timeSeries(values, t)
   by = timeSequence(from=start(ts), to=end(ts), by='day')
   timeSeries::aggregate(ts, by, f)
}

d = read.csv("data.csv", quote="'")

commits       = agregatePerDay(d$Date, d$Commit, length)
files         = agregatePerDay(d$Date, d$Files, sum)
removals      = agregatePerDay(d$Date, d$Delete, sum)
inserts       = agregatePerDay(d$Date, d$Insert, sum)

df = data.frame(time(commits), commits$TS.1, files$TS.1, inserts$TS.1, removals$TS.1)
names(df) <- c("time", "commits", "files", "inserts", "removals")
print(df)



p <- ggplot() + 
  geom_point(data = df, aes(x = time, y = commits, color = "Commits"), size=2.5)   +
  geom_point(data = df, aes(x = time, y = log(files),   color = "Files"))  +
  geom_point(data = df, aes(x = time, y = log(inserts), color = "Inserts"))  +
  geom_point(data = df, aes(x = time, y = log(removals), color = "Removals"))  +
  xlab('date') +
  ylab('files, commits')

print(p)
line <- readline()
