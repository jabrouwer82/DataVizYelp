library("ggplot2", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")
library("lubridate", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")
options(java.parameters="-Xmx2g")
library(rJava)
library(RJDBC)

jdbcDriver <- JDBC(driverClass="oracle.jdbc.OracleDriver", classPath="/Library/Java/JavaVirtualMachines/jdk1.7.0_45.jdk/Contents/Home/ojdbc6.jar")

# In the following, use your username and password instead of "CS347_prof", "orcl_prof" once you have an Oracle account
possibleError <- tryCatch(
  jdbcConnection <- dbConnect(jdbcDriver, "jdbc:oracle:thin:@128.83.138.158:1521:orcl", "C##cs347_jab5948", "orcl_jab5948"),
error=function(e) e
)
if(!inherits(possibleError, "error")){
  users <- dbGetQuery(jdbcConnection, "select review_count, average_stars from yelper")
  businesses <- dbGetQuery(jdbcConnection, "select stars, city, state, review_count as \"BUSINESS_REVIEW_COUNT\", longitude, latitude, business_open from business")
  dbDisconnect(jdbcConnection)
}
# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}
head(users)
head(businesses)
ggplot(data = users) + geom_histogram(aes(x = REVIEW_COUNT), binwidth=10) + coord_cartesian(xlim=c(0, 500))
ggplot(data = users) + geom_histogram(aes(x = REVIEW_COUNT))
ggplot(data = users) + geom_density(aes(x = REVIEW_COUNT, fill = "gray50")) + coord_cartesian(xlim=c(0, 500))
ggplot(data = users) + geom_density(aes(x = REVIEW_COUNT, fill = "gray50"))
ggplot(users, aes(x = REVIEW_COUNT, y = AVERAGE_STARS)) + geom_point() + coord_cartesian(xlim=c(0, 3000))
b <- c(5, 4, 3, 2, 1)
p1 <- ggplot(subset(businesses, CITY == "Phoenix"), aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Phoenix") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")
p2 <- ggplot(subset(businesses, CITY == "Madison"), aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Madison") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")
p3 <- ggplot(subset(businesses, CITY == "Edinburgh"), aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Edinburgh") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")
p4 <- ggplot(subset(businesses, CITY == "Las Vegas"), aes(x=LONGITUDE, y=LATITUDE, color = STARS)) + geom_point() + ggtitle("Las Vegas") + scale_colour_gradientn(limits = c(1, 5), colours = rainbow(3), breaks=b, labels=format(b))# + theme(legend.position="none")
multiplot(p1, p2, p3, p4, cols=2)

