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


df$runInserts  = as.numeric(filter(df$inserts, rep(1/30,30), sides=2))
df$runRemovals = as.numeric(filter(df$removals, rep(1/30,30), sides=2))

p <- ggplot() + 
  geom_point(data = df, aes(x = time, y = runInserts, color = "Inserts"))  +
  geom_point(data = df, aes(x = time, y = runRemovals, color = "Removals"))  +
  stat_smooth(data = df, aes(x = time, y = runInserts)) +
  xlab('date') +
  ylab('files, commits')

print(p)
line <- readline()
