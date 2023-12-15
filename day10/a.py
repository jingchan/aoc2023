import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)

def bfs(grid, start, visited, queue):
    queue = [(start, 0)]

    max_steps = 0
    while len(queue)> 0:
        print(queue[0])
        pos = queue[0][0]
        tx = pos[0]-1
        ty = pos[1]+0
        cx = pos[0]
        cy = pos[1]
        steps = queue[0][1]
        print('steps', steps)
        max_steps = max(max_steps, steps)

        move = False
        if tx < len(grid) and ty < len(grid[0]) and tx >= 0 and ty >= 0:
            print(grid[cx][cy])
            print(grid[tx][ty])
            if (grid[tx][ty] == '|' or grid[tx][ty] == '7' or grid[tx][ty] == 'F') and (
            grid[cx][cy] == 'S' or  grid[cx][cy] == '|' or grid[cx][cy] == 'J' or grid[cx][cy] == 'L'):
                print(grid[tx][ty])
                if visited[tx][ty] == False:
                    queue.append(((tx, ty), steps+1))
                    visited[tx][ty] = True
                    move = True

        tx = pos[0]+1
        ty = pos[1]+0
        if tx < len(grid) and ty < len(grid[0]) and tx >= 0 and ty >= 0:
            if (grid[tx][ty] == '|' or grid[tx][ty] == 'J' or grid[tx][ty] == 'L') and (
            grid[cx][cy] == 'S' or grid[cx][cy] == '|' or grid[cx][cy] == '7' or grid[cx][cy] == 'F'):
                if visited[tx][ty] == False:
                    queue.append(((tx, ty), steps+1))
                    visited[tx][ty] = True
                    move = True
        tx = pos[0]+0
        ty = pos[1]-1
        if tx < len(grid) and ty < len(grid[0]) and tx >= 0 and ty >= 0:
            if (grid[tx][ty] == '-' or grid[tx][ty] == 'F' or grid[tx][ty] == 'L') and (
            grid[cx][cy] == 'S' or grid[cx][cy] == '-' or grid[cx][cy] == '7' or grid[cx][cy] == 'J'):
                if visited[tx][ty] == False:
                    queue.append(((tx, ty), steps+1))
                    visited[tx][ty] = True
                    move = True
        tx = pos[0]+0
        ty = pos[1]+1
        if tx < len(grid) and ty < len(grid[0]) and tx >= 0 and ty >= 0:
            if (grid[tx][ty] == '-' or grid[tx][ty] == 'J' or grid[tx][ty] == '7') and (
            grid[cx][cy] == 'S' or grid[cx][cy] == '-' or grid[cx][cy] == 'L' or grid[cx][cy] == 'F'):
                if visited[tx][ty] == False:
                    queue.append(((tx, ty), steps+1))
                    visited[tx][ty] = True
                    move = True
        print(queue)
        queue = queue[1:]
    print(max_steps)



    queue.append(start)
    # visited[start] = True

    # while queue:
    #     s = queue.pop(0)
    #     print(s, end=" ")

    #     for i in grid[s]:
    #         if visited[i] == False:
    #             queue.append(i)
    #             visited[i] = True

with open(IN_FILE, "r") as f:
    total =0
    # line = f.readline()
    grid = []
    start = []
    visited = []
    for line in f.readlines():
        grid.append([x for x in line])
        visited.append([False for x in line])


    for i, l in enumerate(grid):
        for j, r in enumerate(l):
            if r == 'S':
                start = (i,j)
                print(i,j)

    print(bfs(grid, start, visited, []))


    # print(grid)


    print(total)
