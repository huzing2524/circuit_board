# -*- coding: utf-8 -*-
# @Time   : 19-8-9 下午4:02
# @Author : huziying
# @File   : test_3.py

import time

t1 = time.time()
t_list = list()
for i in range(1000000):
    t_list.append(i)  # 0.09662270545959473
    # t_list += [i]  # 0.11090660095214844
print('time', time.time() - t1)
print(t_list[:10])

