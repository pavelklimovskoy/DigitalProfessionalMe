file = open("count")
k = int(file.read()) + 1
file.close()

file = open("count", "w")
file.write(str(k))
file.close()