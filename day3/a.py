import re
import os
PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + '/2.txt'
print(IN_FILE)


def search(grid, x, y, keep, left=False):
  if x < 0 or x >= len(grid):
    return
  if y < 0 or y >= len(grid[0]):
    return
  if keep[x][y]:
    return
  if grid[x][y].isdigit():
    keep[x][y] = True
    search(grid, x, y-1, keep, left=True)
    search(grid, x, y+1, keep)
    return
  else:
    return
  # elif grid[x][y] == '.':
  # else:
  #   if not only_h:
  #     search(grid, x-1, y, keep, only_h=True)
  #     search(grid, x+1, y, keep, only_h=True)
  #   search(grid, x, y-1, keep, only_h=True)
  #   search(grid, x, y+1, keep)

with open(IN_FILE, 'r') as f:
  grid = []
  keep = []
  for line in f:
    grid.append(line[:-1])
    keep.append([False for i in range(0, len(line[:-1]))])


  for i in range(0, len(grid)):
    for j in range(0, len(grid[0])):
      if grid[i][j] == '.':
        continue
      if grid[i][j].isdigit():
        continue


      search(grid, i+1, j+1, keep)
      search(grid, i, j+1, keep)
      search(grid, i-1, j+1, keep)
      search(grid, i+1, j, keep)
      search(grid, i-1, j, keep)
      search(grid, i, j-1, keep)
      search(grid, i+1, j-1, keep)
      search(grid, i-1, j-1, keep)

  score = 0
  for i in range(0, len(grid)):
    str = ''
    for j in range(0, len(grid[0])):
      if keep[i][j]:
        c = grid[i][j]
        str = str + c
        # print(c, end='')
      else:
        str = str + '.'
        # print('.', end='')

    # print(','.join(str.split(sep='')))
    # print(str)
    nums = re.compile("\.+").split(str)
    for n in nums:
      if n!= '' and int(n) > 0:
        print(n, end=', ')
        score +=int(n)

    print()
  print(score)
# 559667
