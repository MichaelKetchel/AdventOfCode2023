data = {'x': [0, 4001], 'm': [2090, 3780], 'a': [0, 4001], 's': [0, 1351]}

# Create a list of all possible values for each variable
x_values = range(data['x'][0], data['x'][1] + 1)
m_values = range(data['m'][0], data['m'][1] + 1)
a_values = range(data['a'][0], data['a'][1] + 1)
s_values = range(data['s'][0], data['s'][1] + 1)

# Create a list of all possible combinations of values for each variable
combinations = [[x, m, a, s] for x in x_values for m in m_values for a in a_values for s in s_values]

# Count the number of unique combinations
unique_combinations = len(set(combinations))

print(f"There are {unique_combinations} unique combinations of x, m, a, and s.")