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
  score = 0
  grid = []
  for line in f:
    grid.append(line[:-1])

  for i in range(0, len(grid)):
    # if i > 5:
    #   exit()
    for j in range(0, len(grid[0])):
      if grid[i][j] != '*':
        continue

      keep = []
      for row in grid:
        keep.append([False for _ in range(0, len(grid[0]))])

      gn = 0
      rn = 0
      print(grid[i-1][j-1], grid[i-1][j], grid[i-1][j+1])
      print(grid[i][j-1], grid[i][j], grid[i][j+1])
      print(grid[i+1][j-1], grid[i+1][j], grid[i+1][j+1])

      if grid[i-1][j-1].isdigit():
        print("tl", end="," )
        rn+=1
      if grid[i-1][j].isdigit():
        print("tm", end="," )
        rn+=1
      if grid[i-1][j+1].isdigit():
        print("tr", end="," )
        rn+=1

      if rn == 1 or rn == 3:
        gn+=1
      elif rn == 2 and grid[i-1][j].isdigit():
        gn+=1
      elif rn == 2:
        gn+=2

      if grid[i][j-1].isdigit():
        print("cl", end="," )
        gn+=1
      if grid[i][j+1].isdigit():
        print("cr", end="," )
        gn+=1

      rn = 0
      if grid[i+1][j-1].isdigit():
        print("bl", end="," )
        rn+=1
      if grid[i+1][j].isdigit():
        print("bm", end="," )
        rn+=1
      if grid[i+1][j+1].isdigit():
        print("br", end="," )
        rn+=1

      if rn == 1 or rn == 3:
        gn+=1
      elif rn == 2 and grid[i+1][j].isdigit():
        gn+=1
      elif rn == 2:
        gn+=2
      print()
      print("gearnum", gn)

      if gn == 2:
        search(grid, i+1, j+1, keep)
        search(grid, i, j+1, keep)
        search(grid, i-1, j+1, keep)
        search(grid, i+1, j, keep)
        search(grid, i-1, j, keep)
        search(grid, i, j-1, keep)
        search(grid, i+1, j-1, keep)
        search(grid, i-1, j-1, keep)

        prod = 1
        for i2 in range(0, len(grid)):
          str = ''
          for j2 in range(0, len(grid[0])):
            if keep[i2][j2]:
              str = str + grid[i2][j2]
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
              prod *=int(n)
        print(f"adding {prod}")
        print()
        score += prod
    print('--------------------')
  print(score)
# 55966
