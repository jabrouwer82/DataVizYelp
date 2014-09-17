#ui.R 

library(shiny)

# Define UI for application that plots random distributions 
shinyUI(pageWithSidebar(

  # Application title
  headerPanel("Hello Shiny!"),

  # Sidebar with a slider input for number of observations
  sidebarPanel(
    sliderInput("day", 
                "Day of week (0 is Sunday):", 
                min = 0,
                max = 6, 
                value = 0)
    sliderInput("hour", 
                "Hour of day:", 
                min = 0,
                max = 23, 
                value = 0)
  ),

  # Show a plot of the generated distribution
  mainPanel(
    plotOutput("distPlot")
  )
))