import os
PATH = os.path.dirname(__file__)
IN_FILE = PATH + '/2.txt'
print(IN_FILE)

cubes = {
  'red': 0,
  'green': 0,
  'blue': 0,
}

with open(IN_FILE, 'r') as f:
  score = 0
  for line in f:
    cubes = {
      'red': 0,
      'green': 0,
      'blue': 0,
    }
    game_index = int(line.split(': ')[0].split(' ')[1])
    game_fail = False
    for round_line in line.split(': ')[1].split('; '):
      for num_color in round_line.split(', '):
        print(num_color)
        num = num_color.split(' ')[0]
        color = num_color.split(' ')[1]
        cubes[color.strip()] = max(cubes[color.strip()], int(num))
    power = cubes['red']*cubes['green']*cubes['blue']
    score = score + power

  print(score)
