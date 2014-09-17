# server.R

library(shiny)

library("ggplot2")
library("lubridate")
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
  las_vegas <- dbGetQuery(jdbcConnection, "selectselect business.latitude, business.longitude, checkin_info.checkin_time, checkin_info.checkin_count from business join checkin on business.business_id = checkin.business_id join checkin_info on checkin.checkin_id = checkin_info.checkin_info_id where city = 'Las Vegas';")
  dbDisconnect(jdbcConnection)
}

las_vegas_map <- ggmap(get_googlemap("Las Vegas, NV"))

shinyServer(function(input, output) {

  day <- input$day
  hour <- input$hour
  
  checkin_time <- tostring(day) + "-" + tostring(hour)
  
  output$distPlot <- renderPlot({}
    ggplot(subset(las_vegas, CHECKIN_TIME == checkin_time), aes(x=LONGITUDE, y=LATITUDE))) + geom_point(colour=CHECKIN_COUNT)
    
  })
})
