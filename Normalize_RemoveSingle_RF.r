#library(tictoc)
#tic()
library(ape)
library(phangorn)
library(TreeDist)
#toc()

args = commandArgs(trailingOnly=TRUE)

file = args[1]
#print(file)
df <- read.table(file)
#print(lstNewick)
#tic()
for (i in 1:length(df$V1)){

	newickIqtree = as.character(df[i,1])
	newickSimulation = as.character(df[i,2])
	
	#print(newickIqtree)
	#print(newickSimulation)	

	firsttree <- read.tree(text = newickIqtree )
	secondtree <- read.tree(text = newickSimulation )

	firsttree <- collapse.singles(firsttree)
	secondtree <- collapse.singles(secondtree)
	


	totallength1 = sum(firsttree$edge.length)
	totallength2 = sum(secondtree$edge.length)

        if(totallength1 != 0){
                firsttree$edge.length = firsttree$edge.length/totallength1
        }
        if(totallength2 != 0){
                secondtree$edge.length = secondtree$edge.length/totallength2
        }


	#firsttree$edge.length = firsttree$edge.length/totallength1
	#secondtree$edge.length = secondtree$edge.length/totallength2


	x <- RF.dist(firsttree, secondtree)
	y <- wRF.dist(firsttree, secondtree)
	a <- KendallColijn(firsttree, secondtree)
	b <- TreeDistance(firsttree, secondtree)

	z = paste(x, y, ' ')
	z = paste(z, a, ' ')
	z = paste(z, b, ' ')
	z = paste(z, '\n', ' ')

	cat(z)
}
#toc()
