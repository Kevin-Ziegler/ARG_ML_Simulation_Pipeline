from ete3 import Tree
#from ete3 import resolve_polytomy
#from NormalizeBranchLengths import normalize_branch_lengths
import os
import subprocess

def runProcess(r_script):

	try:
		# Use the 'Rscript' command to execute the R script
		result = subprocess.run(r_script, capture_output = True, text=True)

		# Get the return code (exit status)
		#return_code = result.returncode
		#print(return_code)

		# Print the standard output and standard error
		#print("Standard Output:")
		#print(result.stdout)

		#print("\nStandard Error:")
		#print(result.stderr)

		#print(f"\nReturn Code (Exit Status): {return_code}")
		return result.stdout

	except FileNotFoundError:
		print("Rscript command not found. Please ensure R is installed and in your PATH.")



def RF_Newick_Strings(tree1, tree2):
	t1 = Tree(tree1)
	t2 = Tree(tree2)
	#t1.resolve_polytomy()
	#t2.resolve_polytomy()
	#rf = t1.robinson_foulds(t2, unrooted_trees=True, correct_by_polytomy_size=True)[0]
	rf = t1.robinson_foulds(t2, unrooted_trees=True)[0]

	return rf


def RF_File(infile):
	f = open(infile, 'r')
	lstRF = []
	for line in f:
		sline = line.split()
		if len(sline) < 2:
			continue

		newick1 = sline[0]
		newick2 = sline[1]
		#normalize_newick1 = normalize_branch_lengths(newick1)
		#normalize_newick2 = normalize_branch_lengths(newick2)
		Rcommand = []
		Rcommand.append("Rscript")
		Rcommand.append("/pool/Kevin81/NormalizeWRFTry2/DryadPipeLine/CommandLineRF.r")
		Rcommand.append(newick1)
		Rcommand.append(newick2)

		out = runProcess(Rcommand)
		out = out.split()
		rf = out[1]
		wrf = out[3]
		print(out)
		#rfold = RF_Newick_Strings(sline[0], sline[1])
		#print(rfold)
		#print(wrf)
		lstRF.append(wrf)
	f.close()

	return lstRF

#def use_RF_File_Normalize_r(infile):
#	RCommand

"""
lst = []
lst.append("Rscript")
lst.append("CommandLineRF.r")
lst.append("((((A:.01, (B:.01, C:.3):.1):4, D:.2):6,E:.6):7, F:.5);")
lst.append("((((F:0.1, (A:.1, D:.3):.2):4, C:.2):6,E:.6):7, B:.5);")
#runProcess("CommandLineRF.r ((((A:.01, (B:.01, C:.3):.1):4, D:.2):6,E:.6):7, F:.5); ((((F:0.1, (A:.1, D:.3):.2):4, C:.2):6,E:.6):7, B:.5);")
a = runProcess(lst)

a = a.split()
print(a)"""
