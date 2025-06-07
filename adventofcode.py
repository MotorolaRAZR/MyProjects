# this shit is so horrible lmfaooo

inputfile = open("/home/grimax/projects/input.txt", "r")

content = inputfile.readlines()
# debug
#print(content)

lline = []
rline = []

for line in content:
    l, r = line.split()
    lline.append(int(l))
    rline.append(int(r))

lline.sort()
rline.sort()

result1 = 0

for i in range(len(lline)):
    result1 += abs(lline[i] - rline[i])

print(result1)

rcounter = {} 
similarity_score = 0
for nums in rline:
    rcounter[i] = rcounter.get(nums, 0) + 1
    print(rcounter)
for nums in lline:
    similarity_score += nums * rcounter.get(nums, 0)

print(similarity_score)