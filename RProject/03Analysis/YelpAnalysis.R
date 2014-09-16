library("ggplot2", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")
library("lubridate", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")
options(java.parameters="-Xmx2g")
library(rJava)
library(RJDBC)
library(png)
library(grid)

jdbcDriver <- JDBC(driverClass="oracle.jdbc.OracleDriver", classPath="/Library/Java/JavaVirtualMachines/jdk1.7.0_45.jdk/Contents/Home/ojdbc6.jar")

# In the following, use your username and password instead of "CS347_prof", "orcl_prof" once you have an Oracle account
possibleError <- tryCatch(
  jdbcConnection <- dbConnect(jdbcDriver, "jdbc:oracle:thin:@128.83.138.158:1521:orcl", "C##cs347_jab5948", "orcl_jab5948"),
  error=function(e) e
)
if(!inherits(possibleError, "error")){
  users <- dbGetQuery(jdbcConnection, "select review_count, average_stars from yelper")
  edinburgh <- dbGetQuery(jdbcConnection, "select stars, review_count as \"BUSINESS_REVIEW_COUNT\", longitude, latitude, business_open from business where city='Edinburgh'")
  las_vegas <- dbGetQuery(jdbcConnection, "select stars, review_count as \"BUSINESS_REVIEW_COUNT\", longitude, latitude, business_open from business where city='Las Vegas'")
  phoenix <- dbGetQuery(jdbcConnection, "select stars, review_count as \"BUSINESS_REVIEW_COUNT\", longitude, latitude, business_open from business where city='Phoenix'")
  madison <- dbGetQuery(jdbcConnection, "select stars, review_count as \"BUSINESS_REVIEW_COUNT\", longitude, latitude, business_open from business where city='Madison'")
  dbDisconnect(jdbcConnection)
}
head(users)
ggplot(data = users, aes(x= REVIEW_COUNT, y=..count..)) +
  geom_histogram(binwidth=2,
                 colour="#56B4E9",
                 fill="#56B4E9") +
  geom_density(fill="red",
               alpha=.2) + 
  geom_vline(aes(xintercept=mean(REVIEW_COUNT))) +
  coord_cartesian(xlim=c(0, 75))

ggplot(data = users, aes(x= REVIEW_COUNT, y=..count..)) +
  geom_histogram(binwidth=2,
                 colour="#56B4E9",
                 fill="#56B4E9") +
  geom_density(fill="red",
               alpha=.2) + 
  coord_cartesian(xlim=c(1000, 8100), ylim=c(0, 10))

ggplot(data = users, aes(x = REVIEW_COUNT)) +
  geom_histogram(aes(y=..count..),
                 binwidth=5,
                 colour="#56B4E9",
                 fill="#56B4E9") + 
  geom_density(fill="red",
               alpha=.2) +
  geom_vline(aes(xintercept=mean(REVIEW_COUNT)))

ggplot(users, aes(x = REVIEW_COUNT, y = AVERAGE_STARS)) +
  geom_point(colour="#56B4E9") +
  geom_hline(aes(yintercept=mean(AVERAGE_STARS))) + 
  coord_cartesian(xlim=c(0, 3000))


phoenix_map = rasterGrob(readPNG("./phoenix_map.png"), interpolate=TRUE)
b = c(1, 2, 3, 4, 5)
ggplot(phoenix, aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Phoenix") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")
ggplot(madison, aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Madison") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")
ggplot(edinburgh, aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Edinburgh") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")
ggplot(las_vegas, aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Las Vegas") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")

