setwd(dir.choose())
data<-read.csv(file.choose(getwd()),sep=",",header=T)
cols=length(names(data)) - 10 + length(levels(dat$Category))
out=matrix(ncol=cols,nrow=length(levels(data$filename)))
colnames(out)<-c("Username","filename",levels(dat$Category),"group","lat","lon","alt","date","CamTime")
out<-as.data.frame(out)
for (i in 1:length(levels(data$filename))){
  dat<-subset(data,filename==levels(data$filename)[i])
  out[i,1]<-as.character(unique(dat$Username))
  out[i,2]<-as.character(unique(dat$filename))
  for (j in 1:length(levels(dat$Category))){
    d<- subset(dat,Category==levels(dat$Category)[j])
    if (dim(d)[1] == 0){
      val<-0
    }else
      {
      val=sum(d$count)
    }
    out[i,2+j]<-val
  }
  out[i,3+j]<-median(dat$group)
  out[i,4+j]<-unique(dat$lat)
  out[i,5+j]<-unique(dat$lon)
  out[i,6+j]<-unique(dat$altitude)
  out[i,7+j]<-as.character(unique(dat$datetime))
  out[i,8+j]<-as.character(unique(dat$CamTime))
}
write.csv(out,paste(as.character(unique(dat$Username)),"summary_results.csv",sep="_"),row.names=F)