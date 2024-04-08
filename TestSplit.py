def split_file(input_file, output_name, n):
	with open(input_file, 'r') as file:
		lines = file.readlines()

	# Initialize subfiles as a list of empty lists
	subfiles = [[] for _ in range(n)]

	# Distribute lines to subfiles sequentially
	for i, line in enumerate(lines):
		subfiles[i % n].append(line)

	# Write the subfiles
	for i, subfile_lines in enumerate(subfiles):
		te = ""
		if i < 10:
			te = "0" + str(i)
		else:
			te = str(i)
		subfile_name = output_name + te
		with open(subfile_name, 'w') as subfile:
			subfile.writelines(subfile_lines)

# Example usage:
#input_file = "your_input_file.txt"
#input_file = "/pool/Kevin81/BackUpDrivesPaper/Oct_16_2020_100k/Tsinfer/ListTreeFiles.txt"
#output_name = "output_"
#n = 30
#split_file(input_file, output_name, n)


