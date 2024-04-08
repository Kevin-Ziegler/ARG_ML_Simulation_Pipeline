import re


# Parse the Newick tree and extract branch lengths
def extract_branch_lengths(tree_str):
	branch_lengths = []
	components = re.split(r'(\(|\)|,|:)', tree_str)
	for i, component in enumerate(components):
		if component == ":":
			branch_lengths.append(float(components[i + 1]))
	return branch_lengths


def normalize_branch_lengths(newick_tree):
	branch_lengths = extract_branch_lengths(newick_tree)

	# Calculate the total branch length
	total_length = sum(branch_lengths)

	# Normalize branch lengths
	normalized_branch_lengths = [length / total_length for length in branch_lengths]
	normalized_tree = construct_newick_tree(newick_tree, normalized_branch_lengths)
	return normalized_tree

# Reconstruct the Newick tree with normalized branch lengths
def construct_newick_tree(tree_str, normalized_lengths):
	components = re.split(r'(\(|\)|,|:)', tree_str)
	new_tree = []
	i = 0
	for component in components:
		if component == ":":
			new_tree.append(":")
			new_tree.append(str(normalized_lengths[i]))
			i += 1
		else:
			new_tree.append(component)
	return "".join(new_tree)

"""
# Example Newick tree with branch lengths
newick_tree = "((A:0.2,B:0.3):0.4,(C:0.5,D:0.6):0.7);"
normalized_newick_tree = normalize_branch_lengths(newick_tree)
print(normalized_newick_tree)
"""

