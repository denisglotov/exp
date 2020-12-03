from collections import Counter as cntr
import random
import subprocess
import sys

SIZE = 10


def calculateBasins(grid):
  n, basins = len(grid), [u for u in range(len(grid)**2)]

  def find(u): return u if basins[u] == u else find(basins[u])
  def union(u, v): basins[find(u)] = find(v)

  for i in range(n):
    for j in range(n):
      mini, minj = get_min(grid, i, j, n)
      union(i*n + j, mini*n + minj)

  for i in range(n):
    for j in range(n):
      print(find(i*n+j), end='\t')
    print()

  return sorted(cntr(find(u) for u in range(n*n)).values(), reverse=True)


def get_min(grid, i, j, n):
  mini, minj = i, j
  if i > 0   and grid[i-1][j] < grid[mini][minj]: mini, minj = i - 1, j
  if i < n-1 and grid[i+1][j] < grid[mini][minj]: mini, minj = i + 1, j
  if j > 0   and grid[i][j-1] < grid[mini][minj]: mini, minj = i, j - 1
  if j < n-1 and grid[i][j+1] < grid[mini][minj]: mini, minj = i, j + 1
  return mini, minj


def createRandomGrid(n):
  grid = [[0 for i in range(n)] for i in range(n)]
  print(n)
  for i in range(n):
    for j in range(n):
      grid[i][j] = random.randint(0, 100)
      print(grid[i][j], end='\t')
    print()

  return grid


while True:
  print('.', end='')
  stdout = sys.stdout
  with open('grid.txt', 'w') as f:
    sys.stdout = f
    grid = createRandomGrid(SIZE)
  with open('output_py.txt', 'w') as f:
    sys.stdout = f
    calculateBasins(grid)
  sys.stdout = stdout

  with open('grid.txt') as fin:
    res_cxx = subprocess.run(['./a.out'], shell=True, stdin=fin, stdout=subprocess.PIPE, text=True).stdout

  with open('output_py.txt') as fin:
    res_py = fin.read()

  if res_py != res_cxx:
    print('Results mismatch.')
    print(res_cxx)
    break
