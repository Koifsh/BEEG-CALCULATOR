import csv
with open("./data/excercises.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    reader = list(reader)
    reader.sort()
    data = list(map(lambda x: "".join(x), reader))
data.insert(0,"excercise")
data.insert(0,"Not Selected")
print(data)
with open("./data/excercises.csv", "w") as f:
    f.writelines("%s\n" % i for i in data)