## load ape
library(ape)
#library(treespace)
#library(phytools)
# #library(treespace)
# #treeDist(tree.a,tree.b,lambda = 0,return.lambda.function = FALSE,emphasise.tips = NULL,emphasise.weight = 2)

# #This file is used for find rf between two trees and sending it to a file

# #library(ape)
library(phangorn)
library(TreeDist)

# args = commandArgs(trailingOnly=TRUE)

# #df <- read.table(args[1])

# #print(df)
# tree <- read.tree(text = "(((A,B),(C,D)),E);")
# plot(tree, type = "cladogram", edge.width = 2)





readTableTryCatch <- function(val, outputFile1, outputFile2, popSize) {
    out <- tryCatch(
        {
            # Just to highlight: if you want to use more than one 
            # R expression in the "try" part then you'll have to 
            # use curly brackets.
            # 'tryCatch()' will return the last evaluated expression 
            # in case the "try" part was completed successfully

            #message("This is the 'try' part")
                    #file = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/testFile"
                #file = "/home/kevin/Desktop/Research/LemmonLab/AncestralRecombinationGraphGeneTree/AverageKCDistanceTrees"
                #file = "/home/kevin/Downloads/AverageKCDistanceTrees"
                #print("after read table")
                #print(df)
                #print(length(df$V1))
                #print(length(df$V2))
                #print(length(df$V3))
                #sink(outputFile)
                df <- read.table(val)
                write("", file  = outputFile1, append = FALSE, sep = "")

                #print("before loop")
                for (i in 1:length(df$V1)){
                        #print(i)
                        # test = as.character(df$V2)[i]
                        # test2 = as.character(df$V3)[i]
                        test = as.character(df[i,2])
                        test2 = as.character(df[i,3])
                        #print("print test 1 and 2")
                        #print(test)
                        #print(test2)
                        #print("done printing tests")
                        if(substr(test, nchar(test), nchar(test)) != ";"){
                                tempO = paste("Failed File ", file, sep = "")
                                print(tempO)
                                break
                        }
                        if(substr(test2, nchar(test2), nchar(test2)) != ";"){
                                tempO = paste("Failed File ", file, sep = "")
                                print(tempO)
                                break
                        }


                        secondtree <- read.tree(text = test)
                        firsttree <- read.tree(text = test2)
			#totallength1 = sum(firsttree$edge.length)
			#totallength2 = sum(secondtree$edge.length)
			#firsttree$edge.length = firsttree$edge.length/totallength1
			#secondtree$edge.length = secondtree$edge.length/totallength2

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


			x <- RF.dist(firsttree, secondtree)
			y <- wRF.dist(firsttree, secondtree)
			a <- KendallColijn(firsttree, secondtree)
			b <- TreeDistance(firsttree, secondtree)

			z = paste(x, y, ' ')
			z = paste(z, a, ' ')
			z = paste(z, b, ' ')
			z = paste(z, '', ' ')

			#str(firsttree)
                        #str(secondtree)
                        #if(is.binary(firsttree) & is.binary(secondtree)){
                        #        #x <- treeDist(firsttree, secondtree)
			#	x <- RF.dist(firsttree, secondtree)
			#	firsttree$edge.length <- firsttree$edge.length/(2.0 * as.double(popSize))
			#	y <- wRF.dist(firsttree, secondtree)
			#	#print("y is")
			#	#print(y)
                        #}else{
                        #        x <- 'NotBinary'
			#	y <- 'NotBinary'
                        #}
			#'
                        #print(x)
                        #cat(x)
                        #cat("\n")
                        write(z, file  = outputFile1, append = TRUE, sep = "")
                        #write(y, file  = outputFile2, append = TRUE, sep = "")
                        
			#write(" \n", file  = outputFile1, append = TRUE, sep = "")
                }
                #sink()


            #readLines(con=url, warn=FALSE) 
            # The return value of `readLines()` is the actual value 
            # that will be returned in case there is no condition 
            # (e.g. warning or error). 
            # You don't need to state the return value via `return()` as code 
            # in the "try" part is not wrapped insided a function (unlike that
            # for the condition handlers for warnings and error below)
        },
        error=function(cond) {
            message(paste("Error Reading Table from File: ", val))
            message("Here's the original error message:")
            message(cond)
            # Choose a return value in case of error
            return(NA)
        },
        warning=function(cond) {
            #message(paste("URL caused a warning:", val))
            #message("Here's the original warning message:")
            #message(cond)
            # Choose a return value in case of warning
            return(NULL)
        },
        finally={
        # NOTE:
        # Here goes everything that should be executed at the end,
        # regardless of success or error.
        # If you want more than one expression to be executed, then you 
        # need to wrap them in curly brackets ({...}); otherwise you could
        # just have written 'finally=<expression>' 
            #message(paste("Processed URL:", val))
            #message("Some other message at the end")
        }
    )    
    return(out)
}



args = commandArgs(trailingOnly=TRUE)

text = args[1]
outputfile = args[2]


#dirc = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentKCFiles/"
#dircOutput = "/home/kevin/Desktop/Research/Data/AncestralRecombinationSimulatedData/RentKCOutput/"

dirc = args[1]
dircOutput = args[2]
#lstFileName = paste(dirc, "FileNames.txt", sep = "")
lstFileName = args[3]
popSize = args[4]

lstFiles <- read.table(lstFileName)
for (j in 1:length(lstFiles$V1)){

        file = as.character(lstFiles[j,1])
        #print(file)
        if(file == "FileNames.txt"){
                next
        }
        filec = paste(dirc, file, sep = "")
        outputFile = paste(dircOutput, file, sep = "")
	outputFileWRF = paste(outputFile, "WRF", sep = "")	

	
	#get popscaling parameter

	x="Standard_Sample_10_Pop_8.0_Recomb_8.0_Rep_0_s_0.00000001.phy_m_Rent_KCPrepFile"



	x_split <- strsplit(x, "")[[1]]

	counter = 0
	popscaling = ""
	for (item in x_split) {
        	if(item == "_"){
                	counter = counter + 1
                	next
        	}

        	if(counter == 4){
                	popscaling = paste(popscaling, item, sep = "")
        	}


	}

	scaledpopSize = as.double(popSize) * as.double(popscaling)
        #print("scaledpopSize")
	#print(scaledpopSize)
	c <-readTableTryCatch(filec, outputFile, outputFileWRF, scaledpopSize)
}

# test = "((50:1.04,(38:0.03,39:0.03):1.01):0.35,((31:1.30,(29:0.47,30:0.47):0.83):0.00,((11:0.37,(4:0.05,(3:0.02,5:0.02):0.02):0.32):0.63,((((6:0.02>
# test2 = "((31:1.18,(29:0.47,30:0.47):0.71):0.31,((50:1.18,(38:0.03,39:0.03):1.15):0.00,((((6:0.02,7:0.02):0.38,((10:0.10,(8:0.04,9:0.04):0.06):0.27>
# #firsttree <- read.tree(text = as.character(df$V1[[1]]))


# firsttree <- read.tree(text = test)
# secondtree <- read.tree(text = test2)
# x <- treeDist(firsttree, secondtree)
# print(x)



