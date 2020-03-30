# Load R Packages
library(shiny)
library(RODBC)
require("ggplot2")

# define constants
source("paths.R")
dbDSN <- dbDSN
dbuid <- dbuid
dbpwd <- dbpwd

shinyServer(function(input, output, session) {

  ###################  Retrieve Destiny Data ###############################
  lratio <- reactive({
    conn <- odbcConnect(dbDSN, dbuid, dbpwd)
    # PatientID from URL (Test PatientStudyID <- 4476)
    query <- parseQueryString(session$clientData$url_search)
    PID <- query[['PID']]
    
    SQLStmt = paste("SELECT [PID],[Sample.ID],[Sample.Date],[BCR.ABL.Ratio],[Control.Gene] as [ABL] FROM [udv_PredictDemo_BCRABLratio_V] where PID = '", PID, "'", sep="")
    lratio <- sqlQuery(conn, SQLStmt)
    odbcClose(conn)
    
    # prepare data
    lratio$det <- "detected value"
    lratio$det[lratio$BCR.ABL.Ratio == 0] <- "value below detection limit"
    
    lratio$lratio <- log10(lratio$BCR.ABL.Ratio)
    if (any(!is.na(lratio$ABL)))
        lratio$lql[!is.na(lratio$ABL)] <- log10(3 / lratio$ABL[!is.na(lratio$ABL)] * 100)
    lratio$lratio[which(lratio$BCR.ABL.Ratio == 0)] <- lratio$lql[which(lratio$BCR.ABL.Ratio == 0)]
    #lratio$date <- lratio$Sample.Date
    lratio$time <- as.numeric(difftime(as.POSIXct(lratio$Sample.Date), as.POSIXct(min(lratio$Sample.Date)), units = "days")) / 365 * 12
    return(lratio)
  })

  ###################  render plot: Model prediction ###############################
  output$plot <- renderPlot({
    # Data request
    lratio <- lratio()
    
    # plot
    plot <- ggplot()
    
    plot <- plot +
      geom_point(data = lratio, aes(time, lratio, shape = det), size = 4.0, colour = "#377EB8", fill="#377EB8") +
      scale_shape_manual(values = c('detected value' = 19, 'value below detection limit' = 25, 'detection limit' = 6))
          
    plot <- plot + 
            theme_bw() +
            ggtitle("Molecular Response") +
            scale_y_continuous(name="BCR-ABL / ABL", breaks = -4:2, labels = c('', 'MR5', 'MR4', 'MR3', '1 %', '10 %', '100 %'), limits = c(-4,2)) +
            scale_x_continuous(name="time [month]") +
            theme(plot.title = element_text(hjust = 0.5),
            legend.title = element_blank(),
            legend.background = element_rect(fill = alpha("white", 0)),
            legend.key = element_rect(fill = alpha("white", 0)),
            text = element_text(size = 20),
            plot.margin = unit(c(6, 1, 0.5, 0.5), "lines"),
            legend.position="bottom",
            legend.direction = "vertical")
    
    plot
    
  }, height = 500)
})