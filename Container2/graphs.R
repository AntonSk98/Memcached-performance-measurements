library(lattice)

read.table("output-throughput-latency/stats.csv", header=TRUE) -> csvDataFrameSource
csvDataFrame <- csvDataFrameSource

trellis.device("pdf", file="graph1.pdf", color=T, width=6.5, height=5.0)

xyplot(requests/1000 ~ rate/1000, data = csvDataFrame, xlab = "Rate(k.req)", ylab = "Throughput(k.req/s)", main = "Graph 1", type=c("p","l"))

dev.off() -> null 

trellis.device("pdf", file="graph2.pdf", color=T, width=6.5, height=5.0)

xyplot(latency*60 ~ requests/1000, data = csvDataFrame, xlab = "Throughput(k.req/s)", ylab = "Latency(s)", main = "Graph 2", type=c("p","l"))

dev.off() -> null 
