def convert(y, z):
  return n * (n - 1 - z) + y + 1

n = int(input("dimension?:"))

cubes = {}
for i in range(n):
  for j in range(n):
    for k in range(n):
      cubes[(i, j, k)] = 0

skewer = []
for i in range(n):
  for j in range(n):
    skewer.append((i, j))

choose = []
for i in range(n * n):
  for j in range(i, n * n - 1):
    if i != j + 1:
      choose.append([i, j + 1])

sk_all = []
for i in choose:
  for j in choose:
    for k in choose:
      sk_all.append(((skewer[i[0]], skewer[i[1]]),(skewer[j[0]], skewer[j[1]]), (skewer[k[0]], skewer[k[1]])))

score_final = []

for i in sk_all:
  for keys in cubes:
    cubes[keys] = 0
  
  for j in range(n):
    for k in range(2):
      cubes[(j, i[0][k][0], i[0][k][1])] = 1
      cubes[(i[1][k][0], j, i[1][k][1])] = 1
      cubes[(i[2][k][0], i[2][k][1], j)] = 1

  stuck = [k for k, v in cubes.items() if v == 1]
  score = 0
  
  for j in stuck:
    score += convert(j[1], j[2])
  score_final.append(score)

score_final.sort(reverse=True)
print("MAX{}, {}回".format(score_final[0], score_final.count(score_final[0])))
print()
