import os
PATH = os.path.dirname(__file__)
IN_FILE = PATH + '/2.txt'
print(IN_FILE)

cubes = {
  'red': 12,
  'green': 13,
  'blue': 14,
}

with open(IN_FILE, 'r') as f:
  score = 0
  for line in f:
    game_index = int(line.split(': ')[0].split(' ')[1])
    game_fail = False
    for round_line in line.split(': ')[1].split('; '):
      for num_color in round_line.split(', '):
        print(num_color)
        num = num_color.split(' ')[0]
        color = num_color.split(' ')[1]
        if cubes[color.strip()] < int(num):
          game_fail = True
          break
      if game_fail:
        break
    if not game_fail:
      score = score + game_index

  print(score)
