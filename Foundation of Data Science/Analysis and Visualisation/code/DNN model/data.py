import numpy as np
import random
from sklearn.model_selection import train_test_split

# Generate Range Data
training_x=[]
training_y=[]
temp=[]
flag=True
for line in open('/Users/shenyi/Desktop/group/normalization_moviedata.csv'):
    if flag:
        flag=False
        continue
    temp.append([float(i) for i in line.split(',')])

random.shuffle(temp)
temp_x=[d[1:(len(d)-1)] for d in temp]
temp_y=[d[-1] for d in temp]
X_tr=np.mat(temp_x).reshape((3956,12))
Y_tr=np.mat(temp_y).reshape((3956,1))


X_train, X_test, Y_train, Y_test = train_test_split(X_tr, Y_tr, test_size=0.2, random_state=42)

'''
X_train=X_tr
Y_train=Y_tr
temp=[]
flag=True
for line in open('/Users/shenyi/Desktop/group/testmovie_normalized.csv'):
    if flag:
        flag=False
        continue
    temp.append([float(i) for i in line.split(',')])
random.shuffle(temp)
temp_x=[d[1:(len(d)-1)] for d in temp]
temp_y=[d[-1] for d in temp]
X_test=np.mat(temp_x).reshape((7,12))
Y_test=np.mat(temp_y).reshape((7,1))
'''
