
points = [(983, 166), (985, 168), (988, 183), (1003, 184)]



for item in points:
    print(item[0])
    print(item[1])
    x = (item[0] - 2)/(1500 - 2)
    y = (item[1] - 2)/(500 - 2)
    item = (x,y)
    print(item[0])
    print(item[1])