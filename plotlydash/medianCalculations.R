
## packages
library(ggplot2)
require(readr)

##Berechnung des Medians und der Quantile
slideFunct <- function(data, window, step){
  total <- ceiling(max(as.numeric(data$TIME),na.rm=T)) + window
  spots <- seq(from = window/2, to=(total-window/2), by=step)
  nr.Pat <- c()

  temp <- data[which(data$TIME >= spots[1] - window/2 & data$TIME < spots[1] + window/2),]
  temp$LRATIO <- ifelse( temp$ND==1,temp$lQL,temp$LRATIO)
  temp <- tapply(temp$LRATIO,temp$PatID,median)
  temp <- temp[!is.na(temp)]
  result <- quantile(temp,c(.05,.25,0.5,0.75, 0.95))
  nr.Pat <- length(temp)

    for(i in 2:length(spots)){
    temp <- data[which(data$TIME >= spots[i] - window/2 & data$TIME < spots[i] + window/2),]
    temp$LRATIO <- ifelse( temp$ND==1,temp$lQL,temp$LRATIO)
    temp <- tapply(temp$LRATIO,temp$PatID,median)
    temp <- temp[!is.na(temp)]
  
    result <- rbind(result,quantile(temp,c(.05,.25,0.5,0.75, 0.95)))
    nr.Pat <- c(nr.Pat,length(temp))
  }
  result <- data.frame(result)
  colnames(result) <- c( "5%",  "25%", "50%", "75%", "95%")
  result$TIME = spots
  result$nr.Pat <- nr.Pat
  result <- reshape2::melt(result,id.vars = c("TIME","nr.Pat"), measure.vars= c("5%",  "25%", "50%", "75%", "95%"),
                           variable.name = "quantile")
  colnames(result) <- c("TIME","Nr.Pat","quantile","LRATIO") 
  
  return(result)
}


#### Berechnung der geglaetteten Kurven und Ausgabe der Graphik 
plot.movingwindowquantile <- function(data,window = 3,step = 1){
  
  movingmean <- slideFunct(data = data, window = window, step = step)

  movingmean <- movingmean[movingmean$Nr.Pat>=10,]
 
  nr.pat <- unique(movingmean[,c("TIME","Nr.Pat")])
  
  movingmeanQuantiles <- data.frame(
    TIME=movingmean[movingmean$quantile=="25%","TIME"],
    quantile25=movingmean[movingmean$quantile=="25%","LRATIO"],
    quantile50=movingmean[movingmean$quantile=="50%","LRATIO"],
    quantile75=movingmean[movingmean$quantile=="75%","LRATIO"]
  )
  
  
  tempplot <-  ggplot(movingmeanQuantiles) + 
    geom_smooth(aes(x=TIME,y=quantile50),se=F,color='black') +
    geom_smooth(aes(x=TIME,y=quantile25),se=F,color='gray65') +
    geom_smooth(aes(x=TIME,y=quantile75),se=F,color='gray65') 
  
  #ggplot_build(tempplot)
  
  ggplot() +
    geom_ribbon(aes(ymin=ggplot_build(tempplot)$data[[2]]$y,ymax=ggplot_build(tempplot)$data[[1]]$y, x=ggplot_build(tempplot)$data[[1]]$x), alpha = 0.3,fill='gray65')+
    geom_ribbon(aes(ymin=ggplot_build(tempplot)$data[[1]]$y,ymax=ggplot_build(tempplot)$data[[3]]$y, x=ggplot_build(tempplot)$data[[1]]$x), alpha = 0.3,fill='gray65')+
   
    geom_line(aes(x=ggplot_build(tempplot)$data[[1]]$x,y=ggplot_build(tempplot)$data[[1]]$y),color='black',size=1) +
    geom_line(aes(x=ggplot_build(tempplot)$data[[2]]$x,y=ggplot_build(tempplot)$data[[2]]$y),color='gray65') +
    geom_line(aes(x=ggplot_build(tempplot)$data[[3]]$x,y=ggplot_build(tempplot)$data[[3]]$y),color='gray65') +
    
  # geom_point(aes(x=data[data$PatID==unique(data$PatID)[2],"TIME"],y=data[data$PatID==unique(data$PatID)[2],"LRATIO"]),color='darkred') +
   # geom_line(aes(x=data[data$PatID==unique(data$PatID)[2],"TIME"],y=data[data$PatID==unique(data$PatID)[2],"LRATIO"]),color='darkred') +
    
    coord_cartesian(ylim = c(-4, 2)) +
    xlab("time [months]") + 
    ylab(expression("log"[10]*"(BCR-ABL1/ABL1)")) +
  
    ggtitle("moving median") +
    # Layout
    theme_bw() +
    # Position der Legende
    theme(legend.position = "bottom",
          plot.title = element_text(size=20),
          axis.title = element_text(size=20),
          axis.text = element_text(size=18),
          legend.text = element_text(size=20))
}

#### Berechnung der geglaetteten Kurven und Ausgabe der Daten
data.movingwindowquantile <- function(data,window = 3,step = 1){
  
  movingmean <- slideFunct(data = data, window = window, step = step)
  movingmean <- movingmean[movingmean$Nr.Pat>=10,]
 
  nr.pat <- unique(movingmean[,c("TIME","Nr.Pat")])
  
  movingmeanQuantiles <- data.frame(
    TIME=movingmean[movingmean$quantile=="25%","TIME"],
    quantile25=movingmean[movingmean$quantile=="25%","LRATIO"],
    quantile50=movingmean[movingmean$quantile=="50%","LRATIO"],
    quantile75=movingmean[movingmean$quantile=="75%","LRATIO"]
  )
  
  
  tempplot <-  ggplot(movingmeanQuantiles) + 
    geom_smooth(aes(x=TIME,y=quantile50),se=F,color='black') +
    geom_smooth(aes(x=TIME,y=quantile25),se=F,color='gray65') +
    geom_smooth(aes(x=TIME,y=quantile75),se=F,color='gray65') 
  
 return(
   data.frame(
     Time = ggplot_build(tempplot)$data[[1]]$x,
     Median = ggplot_build(tempplot)$data[[1]]$y, 
     Quantile25 = ggplot_build(tempplot)$data[[2]]$y,
     Quantile75 = ggplot_build(tempplot)$data[[3]]$y))
}


### Daten vom Subprozess einlesen:
args <- commandArgs(trailingOnly = TRUE)
file <- args[1]
data_in <- read.csv(file, sep = ';')

### Aufruf zur Ausgabe der berechneten geglaetteten Kurven:
#write.table(data.movingwindowquantile(data_in,window = 3,step = 1),file= "table.csv",row.names=F)

out = data.movingwindowquantile(data_in,window = 3,step = 1)
write(format_csv(out), stdout())
### Ausgabe der Graphik
#plot.movingwindowquantile(data_in,window = 3,step = 1)
#plot.movingwindowquantile(dataNordCML006,window = 3,step = 1)




### Vergleich von geglaettetem und ungeglaettetem Median:
# movingmean <- slideFunct(data = dataENEST1st, window = window, step = step)
# movingmean <- movingmean[movingmean$Nr.Pat>=10,]
# movingmeanQuantiles <- data.frame(
#   TIME=movingmean[movingmean$quantile=="25%","TIME"],
#   quantile25=movingmean[movingmean$quantile=="25%","LRATIO"],
#   quantile50=movingmean[movingmean$quantile=="50%","LRATIO"],
#   quantile75=movingmean[movingmean$quantile=="75%","LRATIO"]
# )
# 
# plot(Median~Time,data = data.movingwindowquantile(dataENEST1st,window = 3,step = 1),type="l")
# lines(quantile50~TIME,data=movingmeanQuantiles,col="red")


