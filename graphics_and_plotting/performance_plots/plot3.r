library("ggplot2")
library(plyr)
data <- read.table("winvslinux.txt", header=T)

## Summarizes data.
## Gives count, mean, standard deviation, standard error of the mean, and confidence interval (default 95%).
##   data: a data frame.
##   measurevar: the name of a column that contains the variable to be summariezed
##   groupvars: a vector containing names of columns that contain grouping variables
##   na.rm: a boolean that indicates whether to ignore NA's
##   conf.interval: the percent range of the confidence interval (default is 95%)
summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
    require(plyr)

    # New version of length which can handle NA's: if na.rm==T, don't count them
    length2 <- function (x, na.rm=FALSE) {
        if (na.rm) sum(!is.na(x))
        else       length(x)
    }

    # This is does the summary; it's not easy to understand...
    datac <- ddply(data, groupvars, .drop=.drop,
                   .fun= function(xx, col, na.rm) {
                           c( N    = length2(xx[,col], na.rm=na.rm),
                              mean = mean   (xx[,col], na.rm=na.rm),
                              sd   = sd     (xx[,col], na.rm=na.rm)
                              )
                          },
                    measurevar,
                    na.rm
             )

    # Rename the "mean" column    
    datac <- rename(datac, c("mean"=measurevar))

    datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean

    # Confidence interval multiplier for standard error
    # Calculate t-statistic for confidence interval: 
    # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
    ciMult <- qt(conf.interval/2 + .5, datac$N-1)
    datac$ci <- datac$se * ciMult

    return(datac)
}


#workload\tsample\tmakespan\tdistribution\tjvm
#png("jvm_bar.png")
#mm <- ddply(data, .(Composicao, Carga), summarise, Decorrido = mean(Decorrido))
mm <- summarySE(data, measurevar="makespan", groupvars=c("workload", "synchronization", "so"))
ggplot(mm, aes(x = so, y = log(makespan), fill=so)) + geom_bar(position=position_dodge(.9), stat = "identity", width=.5)  + geom_errorbar(aes(ymin=log(makespan-ci), ymax=log(makespan+ci)),width=.2,position=position_dodge(.3)) + facet_grid(workload~synchronization, scales="free_y") + xlab("Sistema Operacional")
ggsave("win_vs_linux.png", dpi = 250)  


