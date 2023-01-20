import numpy as np
import pandas as pd

leng, move = map(int, input().split())
body = list(reversed(str(input())))
ctr = list(str(input()))
x = 0
y = 0
c_d = 2
t_x = [0]
t_y = [0]
for m in range (move):
    if (ctr[m] == 'L') & (c_d == 1):
        x -= 1
        c_d = 4
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'R') & (c_d == 1):
        x += 1
        c_d = 2
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'F') & (c_d == 1):
        y += 1
        c_d = 1
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'L') & (c_d == 2):
        y += 1
        c_d = 1
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'R') & (c_d == 2):
        y -= 1
        c_d = 3
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'F') & (c_d == 2):
        x += 1
        c_d = 2
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'L') & (c_d == 3):
        x += 1
        c_d = 2
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'R') & (c_d == 3):
        x -= 1
        c_d = 4
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'F') & (c_d == 3):
        y -= 1
        c_d = 3
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'L') & (c_d == 4):
        y -= 1
        c_d = 3
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'R') & (c_d == 4):
        y += 1
        c_d = 1
        t_x.append(x)
        t_y.append(y)
    elif (ctr[m] == 'F') & (c_d == 4):
        x -= 1
        c_d = 4
        t_x.append(x)
        t_y.append(y)

if leng > move+1:
    for i in range(1, leng-move):
        t_x.insert(0, 0)
        t_y.insert(0, -1*i)

dfxy = pd.DataFrame({ 'y' : t_y, 'x' : t_x })
dfl = pd.DataFrame({'l' : body })
df2 = pd.concat([dfxy, dfl])
df2['as'] = df2['l'].shift(-1*leng)
df3 = df2.drop(['l'], axis = 1)
df4 = df3.dropna()
df5 = df4.sort_values(by = ['y', 'x'], ascending = [False, True])
display(df5)

for i in df5['as']:
    print(i, end='')