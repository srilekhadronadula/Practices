A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]

def mapper(record):
    matrix, i, j, value = record
    if matrix == "A":
        for k in range(len(B[0])):  
            yield (i, k), ("A", j, value)
    else:
        for k in range(len(A)):  
            yield (k, j), ("B", i, value)

def reducer(key, values):
    row, col = key
    a_values = [(j, value) for matrix, j, value in values if matrix == "A"]
    b_values = [(i, value) for matrix, i, value in values if matrix == "B"]
    
    dot_product = sum(a_value[1] * b_value[1] for a_value in a_values for b_value in b_values if a_value[0] == b_value[0])
    
    yield (row, col, dot_product)

def map_reduce(matrix_A, matrix_B, mapper, reducer):
    intermediate_data = []
    
    for i, row in enumerate(matrix_A):
        for j, value in enumerate(row):
            intermediate_data.extend(mapper(("A", i, j, value)))
    
    for j, col in enumerate(zip(*matrix_B)):
        for i, value in enumerate(col):
            intermediate_data.extend(mapper(("B", i, j, value)))
    
    intermediate_data.sort()
    final_output = []
    
    i = 0
    while i < len(intermediate_data):
        key = intermediate_data[i][0]
        values = []
        while i < len(intermediate_data) and intermediate_data[i][0] == key:
            values.append(intermediate_data[i][1])
            i += 1
        
        for output in reducer(key, values):
            final_output.append(output)
    
    return final_output

output = map_reduce(A, B, mapper, reducer)

for i in range(len(A)):
    row = []
    for j in range(len(B[0])):
        cell = [value for row_, col_, value in output if row_ == i and col_ == j]
        row.append(cell[0] if cell else 0)
    print(row)
