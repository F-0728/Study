def convert(num):
  if num % 3 == 0:
    if num % 9 == 0:
      return 3 * (num // 9)
    else:
      return 3 * (num // 9) + 3
  else:
    return 3 * (num // 9) + (num % 3)


x = []
y = []
z = []

x_c = []
y_c = []
z_c = []

combination = []
cubes = []
sum_list = []

how_to = []

for i in range(3):
  for j in range(3):
    x.append((9 * i + j + 1, 9 * i + j + 4, 9 * i + j + 7))
for i in range(0, 9):
  y.append((3 * i + 1, 3 * i + 2, 3 * i + 3))
  z.append((i + 1, i + 10, i + 19))

for i in range(8, 0, -1):
  for j in range(i):
    x_c.append((x[8 - i], x[8 - i + j + 1]))
    y_c.append((y[8 - i], y[8 - i + j + 1]))
    z_c.append((z[8 - i], z[8 - i + j + 1]))

for i in range(36):
  for j in range(36):
    for k in range(36):
      combination.append((x_c[i], y_c[j], z_c[k]))

for i in range(46656):
  list = []
  for j in range(3):
  	for k in range(2):
  	  for l in range(3):
  	    list.append(combination[i][j][k][l])
  set_list = set(list)
  cubes.append(set_list)
  
for i in range(46656):
  pts = []
  cubes_set = cubes[i]
  for j in cubes_set:
    pts.append(convert(j))
  pt = sum(pts)
  sum_list.append(pt)

  if pt == 105:
   how_to.append(combination[i])    

sum_list.sort()
set_sum = set(sum_list)

for i in set_sum:
  num = sum_list.count(i)
  if len(str(i)) == 2:
    print(" {}: {}".format(i, num))
  else:
    print("{}: {}".format(i, num))

for i in how_to:
 print(i)


print()
