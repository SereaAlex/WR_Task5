import random

def generate_input(filename, num_matrices, min_rows, max_rows, min_cols, max_cols):
    with open(filename, 'w') as file:
        for _ in range(num_matrices):
            rows = random.randint(min_rows, max_rows)
            cols = random.randint(min_cols, max_cols)
            matrix = ''.join([random.choice(['0', '1']) for _ in range(rows*cols)])
            file.write(f"{rows}x{cols}:{matrix}\n")

def read_input(filename):
    matrices = []
    with open(filename, 'r') as file:
        for line in file:
            matrix_str = line.strip().split(':')[1]
            rows, cols = map(int, line.split(':')[0].split('x'))
            matrices.append([list(map(int, matrix_str[i:i+cols])) for i in range(0, len(matrix_str), cols)])
    return matrices

def count_isolated_ones(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    count = 0
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                if (i == 0 or matrix[i-1][j] == 0) and \
                   (i == rows-1 or matrix[i+1][j] == 0) and \
                   (j == 0 or matrix[i][j-1] == 0) and \
                   (j == cols-1 or matrix[i][j+1] == 0):
                    count += 1
    return count

def count_clusters(matrix, size):
    rows = len(matrix)
    cols = len(matrix[0])
    visited = [[False]*cols for _ in range(rows)]
    count = 0

    def dfs(row, col):
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col] or matrix[row][col] == 0:
            return
        visited[row][col] = True
        dfs(row-1, col)
        dfs(row+1, col)
        dfs(row, col-1)
        dfs(row, col+1)

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and matrix[i][j] == 1:
                cluster_size = 0
                dfs(i, j)
                for k in range(rows):
                    for l in range(cols):
                        if visited[k][l]:
                            cluster_size += 1
                            visited[k][l] = False
                if cluster_size == size:
                    count += 1
    return count

def process_matrices(matrices):
    results = []
    for matrix in matrices:
        isolated_ones = count_isolated_ones(matrix)
        clusters_two = count_clusters(matrix, 2)
        clusters_three = count_clusters(matrix, 3)
        results.append((isolated_ones, clusters_two, clusters_three))
    return results

def write_output(filename, results):
    with open(filename, 'w') as file:
        for result in results:
            file.write(' '.join(map(str, result)) + '\n')

if __name__ == "__main__":
    generate_input("mat.in", 10, 5, 10, 5, 10)
    matrices = read_input("mat.in")
    results = process_matrices(matrices)
    write_output("mat.out", results)
