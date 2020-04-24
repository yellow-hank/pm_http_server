#!/usr/bin/env python
# coding: utf-8

# In[4]:

import sys
import numpy as np
import pandas as pd
from matplotlib import colors
import math
import googlemaps
import os
import requests
import json
from os.path import join, dirname

def route_planning(sLat, sLong, eLat, eLong,pm25):
    # 色溫圖的function(get campus pm2.5)
    airbox = ["x_pos", "y_pos", "pm25"]
    x_pos = [15, 39, 35, 17, 7, 40, 28, 56]
    y_pos = [55, 53, 5, 29, 44, 23, 31, 28]
    # pm25 = [0, 0, 0, 80, 80, 0, 80, 0]
    dic = {"x_pos": x_pos, "y_pos": y_pos, "pm25": pm25}
    airbox = pd.DataFrame(dic)

    x = np.arange(60)
    y = np.arange(60)
    z = np.zeros(3600)
    z = z.reshape(60, 60)

    dist = np.zeros(8)
    total = 0

    for i in x:
        for j in y:
            for k in range(8):
                dist[k] = abs(x_pos[k] - i)**2 + abs(y_pos[k] - j)**2
                if dist[k]!=0:
                    dist[k] = 10000 / dist[k]
                total += dist[k]
            for k in range(8):
                z[j, i] += (dist[k] / total) * pm25[k]
            total = 0

    #傳起點與終點的經緯度，回傳所在的block
    def get_blockNo(latitude , longitude):
        row = 0
        col = 0
        # in range
        if ((22.992500 < latitude) and (latitude < 23.003600) and (120.213255 < longitude) and (longitude < 121.001750)):
            out_of_range = False
            row = np.floor(((latitude - 22.992500) * 1000000) / 1850)
            col = np.floor(((longitude - 120.213255) * 1000000) / 1980)
            block_no = row * 6 + col
            return int(block_no), out_of_range
        # out of range
        else:
            out_south = False
            out_west = False
            out_of_range = True
            if latitude < 22.992500:
                out_south = True
                row = 0
            elif latitude > 23.0036:
                row = 5
            else:
                row = np.floor(((latitude - 22.992500) * 1000000) / 1850)
            if longitude < 120.213255:
                out_west = True
                col = 0
            elif longitude > 121.001750:
                col = 5
            else:
                col = np.floor(((longitude - 120.213255) * 1000000) / 1980)
            block_no = row * 6 + col
            if (block_no == 18) or (block_no == 24):
                block_no = 30
            elif (block_no == 0) or (block_no == 1) or (block_no == 6) or (block_no == 7):
                if out_west:
                    block_no = 12
                else:
                    block_no = 2
            return int(block_no), out_of_range

    class Block():
        def __init__(self, Adj):
            self.pm25 = 0
            self.adj = Adj
            self.reverse = 0
        def add_pm25(self, air):
            self.pm25 = air
        def delete(self, Adj):
            self.adj.remove(Adj)
        def goto(self, Adj):
            self.reverse = Adj

    #無須更新
    def get_dij_block():
        block = []

        # block 0
        t = Block([1, 6])
        block.append(t)

        # block 1
        t = Block([0, 2, 7])
        block.append(t)

        # block 2
        t = Block([1, 3, 8])
        block.append(t)

        # block 3
        t = Block([2, 4, 9])
        block.append(t)

        # block 4
        t = Block([3, 5, 10])
        block.append(t)

        # block 5
        t = Block([4, 11])
        block.append(t)

        # block 6
        t = Block([7, 0, 12])
        block.append(t)

        # block 7
        t = Block([6, 8, 1, 13])
        block.append(t)

        # block 8
        t = Block([7, 9, 2, 14])
        block.append(t)

        # block 9
        t = Block([8, 10, 3, 15])
        block.append(t)

        # block 10
        t = Block([9, 11, 4, 16])
        block.append(t)

        # block 11
        t = Block([10, 5, 17])
        block.append(t)

        # block 12
        t = Block([13, 6, 18])
        block.append(t)

        # block 13
        t = Block([12, 14, 7, 19])
        block.append(t)

        # block 14
        t = Block([13, 15, 8, 20])
        block.append(t)

        # block 15
        t = Block([14, 16, 9, 21])
        block.append(t)

        # block 16
        t = Block([15, 17, 10, 22])
        block.append(t)

        # block 17
        t = Block([16, 11, 23])
        block.append(t)

        # block 18
        t = Block([19, 12, 24])
        block.append(t)

        # block 19
        t = Block([18, 20, 13, 25])
        block.append(t)

        # block 20
        t = Block([19, 21, 14, 26])
        block.append(t)

        # block 21
        t = Block([20, 22, 15, 27])
        block.append(t)

        # block 22
        t = Block([21, 23, 16, 28])
        block.append(t)

        # block 23
        t = Block([22, 17, 29])
        block.append(t)

        # block 24
        t = Block([25, 18, 30])
        block.append(t)

        # block 25
        t = Block([24, 26, 19, 31])
        block.append(t)

        # block 26
        t = Block([25, 27, 20, 32])
        block.append(t)

        # block 27
        t = Block([26, 28, 21, 33])
        block.append(t)

        # block 28
        t = Block([27, 29, 22, 34])
        block.append(t)

        # block 29
        t = Block([28, 23, 35])
        block.append(t)

        # block 30
        t = Block([31, 24])
        block.append(t)

        # block 31
        t = Block([30, 32, 25])
        block.append(t)

        # block 32
        t = Block([31, 33, 26])
        block.append(t)

        # block 33
        t = Block([32, 34, 27])
        block.append(t)

        # block 34
        t = Block([33, 35, 28])
        block.append(t)

        # block 35
        t = Block([34, 29])
        block.append(t)
        return block

    def add_pm25(air_3600, block):
        air = np.zeros(36)
        for i in range(36):
            row = i // 6
            column = i % 6
            temp_sum = 0
            for j in range(10):
                for k in range(10):
                    temp_sum += air_3600[10*row + j][10*column + k]
            if temp_sum / 100 < 35:
                block[i].add_pm25(temp_sum / 100 / 2)
            elif temp_sum < 54:
                block[i].add_pm25(temp_sum / 100)
            elif temp_sum < 150:
                block[i].add_pm25(temp_sum / 100 * 4)
            elif temp_sum < 250:
                block[i].add_pm25(temp_sum / 100 * 8)
            else:
                block[i].add_pm25(temp_sum / 100 * 10)
        return block

    def get_path(start_index, end_index, block):
        if start_index == end_index:
            path = [start_index]
            return path
        else:
            discovered = []  #已經發現的點
            distance = np.zeros(36)
            discovered.append(start_index)
            stop = False

            while stop == False:
                dis = sys.maxsize
                start = 0
                end = 0
                for i in range(len(discovered)):
                    for j in range(len(block[discovered[i]].adj)):
                        temp_dis = distance[discovered[i]] + block[block[discovered[i]].adj[j]].pm25
                        if block[discovered[i]].adj[j] == end_index:
                            dis = temp_dis
                            start = discovered[i]
                            end = block[discovered[i]].adj[j]
                            stop = True
                            break
                        elif (temp_dis < dis) and (block[discovered[i]].adj[j] not in discovered) :
                            dis = temp_dis
                            start = discovered[i]
                            end = block[discovered[i]].adj[j]
                    if stop:
                        break
                if dis != 1000:
                    discovered.append(end)
                    distance[end] = dis
                    block[start].delete(end)
                    block[end].delete(start)
                    block[end].goto(start)
                else:
                    print("沒有路徑")
                    stop = True
                    return -1

            path = []
            path.insert(0, end_index)
            i = end_index
            if stop:
                while i != start_index:
                    path.insert(0, block[i].reverse)
                    i = block[i].reverse
            return path

    class Block_road():
        def __init__(self, road_list):
            self.roadList = road_list
            self.road_dic = {}
            for road in road_list:
                self.road_dic[road] = {}
        def add_end(self, start, des_blk, end):
            self.road_dic[start][des_blk] = end

    #無須更新
    def get_blockList_Road():
        blockList = []

        #block0
        newBlock = Block_road([])
        blockList.append(newBlock)

        #block1
        newBlock = Block_road([])
        blockList.append(newBlock)

        #block2
        newBlock = Block_road([-1, 0, 7, 8, 9, 14, 15])
        newBlock.add_end(0, 3, 1)
        newBlock.add_end(0, 8, 14)
        newBlock.add_end(7, 8, 15)
        newBlock.add_end(8, 8, 15)
        newBlock.add_end(9, 8, 15)
        newBlock.add_end(14, 3, 1)
        newBlock.add_end(15, 3, 9)
        newBlock.add_end(-1, 3, 7)
        newBlock.add_end(-1, 3, 8)
        blockList.append(newBlock)

        #block3
        newBlock = Block_road([-1, 1, 2, 7, 8, 9, 10, 11, 16, 17])
        newBlock.add_end(1, 2, 0)
        newBlock.add_end(1, 4, 10)
        newBlock.add_end(1, 9, 17)
        newBlock.add_end(2, 2, 0)
        newBlock.add_end(2, 4, 10)
        newBlock.add_end(2, 9, 17)
        newBlock.add_end(7, 4, 11)
        newBlock.add_end(7, 9, 16)
        newBlock.add_end(8, 4, 11)
        newBlock.add_end(8, 9, 16)
        newBlock.add_end(9, 4, 11)
        newBlock.add_end(9, 9, 16)
        newBlock.add_end(10, 2, 0)
        newBlock.add_end(10, 9, 17)
        newBlock.add_end(11, 2, 9)
        newBlock.add_end(11, 9, 17)
        newBlock.add_end(16, 2, 9)
        newBlock.add_end(16, 4, 11)
        newBlock.add_end(17, 2, 9)
        newBlock.add_end(17, 4, 11)
        newBlock.add_end(-1, 2, 7)
        newBlock.add_end(-1, 2, 8)
        blockList.append(newBlock)

        #block4
        newBlock = Block_road([3, 4, 5, 10, 11, 12, 18, 19])
        newBlock.add_end(3, 3, 10)
        newBlock.add_end(3, 5, 12)
        newBlock.add_end(3, 10, 19)
        newBlock.add_end(4, 3, 10)
        newBlock.add_end(4, 5, 12)
        newBlock.add_end(4, 10, 19)
        newBlock.add_end(5, 3, 10)
        newBlock.add_end(5, 5, 12)
        newBlock.add_end(5, 10, 19)
        newBlock.add_end(10, 5, 12)
        newBlock.add_end(10, 10, 18)
        newBlock.add_end(11, 5, 12)
        newBlock.add_end(11, 10, 18)
        newBlock.add_end(12, 3, 11)
        newBlock.add_end(12, 10, 19)
        newBlock.add_end(18, 3, 11)
        newBlock.add_end(18, 5, 12)
        newBlock.add_end(19, 3, 11)
        newBlock.add_end(19, 5, 12)
        blockList.append(newBlock)

        #block5
        newBlock = Block_road([6, 12, 20])
        newBlock.add_end(6, 4, 12)
        newBlock.add_end(6, 11, 20)
        newBlock.add_end(12, 11, 20)
        newBlock.add_end(20, 4, 12)
        blockList.append(newBlock)

        #block6
        newBlock = Block_road([])
        blockList.append(newBlock)

        #block7
        newBlock = Block_road([])
        blockList.append(newBlock)

        #block8
        newBlock = Block_road([14, 15, 21, 22, 23, 24, 34])
        newBlock.add_end(14, 7, 21)
        newBlock.add_end(14, 9, 24)
        newBlock.add_end(14, 14, 34)
        newBlock.add_end(15, 7, 21)
        newBlock.add_end(15, 9, 24)
        newBlock.add_end(15, 14, 34)
        newBlock.add_end(21, 2, 14)
        newBlock.add_end(21, 9, 24)
        newBlock.add_end(21, 14, 34)
        newBlock.add_end(22, 2, 14)
        newBlock.add_end(22, 9, 24)
        newBlock.add_end(22, 14, 34)
        newBlock.add_end(23, 2, 14)
        newBlock.add_end(23, 9, 24)
        newBlock.add_end(23, 14, 34)
        newBlock.add_end(24, 2, 15)
        newBlock.add_end(24, 7, 21)
        newBlock.add_end(24, 14, 34)
        newBlock.add_end(34, 2, 14)
        newBlock.add_end(34, 7, 23)
        newBlock.add_end(34, 9, 24)
        blockList.append(newBlock)

        #block9
        newBlock = Block_road([-1, 16, 17, 24, 25, 26, 35, 36])
        newBlock.add_end(16, 8, 24)
        newBlock.add_end(16, 10, 26)
        newBlock.add_end(16, 15, 36)
        newBlock.add_end(17, 8, 24)
        newBlock.add_end(17, 10, 26)
        newBlock.add_end(17, 15, 36)
        newBlock.add_end(24, 3, 16)
        newBlock.add_end(24, 10, 26)
        newBlock.add_end(24, 15, 36)
        newBlock.add_end(25, 3, 17)
        newBlock.add_end(25, 8, 24)
        newBlock.add_end(25, 15, 36)
        newBlock.add_end(26, 3, 17)
        newBlock.add_end(26, 8, 24)
        newBlock.add_end(26, 15, 36)
        newBlock.add_end(35, 3, 16)
        newBlock.add_end(35, 8, 24)
        newBlock.add_end(35, 10, 26)
        newBlock.add_end(36, 3, 16)
        newBlock.add_end(36, 8, 24)
        newBlock.add_end(36, 10, 26)
        newBlock.add_end(-1, 10, 25)
        newBlock.add_end(-1, 15, 35)
        blockList.append(newBlock)

        #block10
        newBlock = Block_road([18, 19, 25, 26, 27, 28, 29, 37, 38])
        newBlock.add_end(18, 9, 25)
        newBlock.add_end(18, 11, 27)
        newBlock.add_end(18, 16, 37)
        newBlock.add_end(19, 9, 25)
        newBlock.add_end(19, 11, 27)
        newBlock.add_end(19, 16, 37)
        newBlock.add_end(25, 4, 18)
        newBlock.add_end(25, 11, 27)
        newBlock.add_end(25, 16, 37)
        newBlock.add_end(26, 4, 19)
        newBlock.add_end(26, 11, 28)
        newBlock.add_end(26, 16, 37)
        newBlock.add_end(27, 4, 19)
        newBlock.add_end(27, 9, 25)
        newBlock.add_end(27, 16, 38)
        newBlock.add_end(28, 4, 19)
        newBlock.add_end(28, 9, 26)
        newBlock.add_end(28, 16, 38)
        newBlock.add_end(29, 4, 19)
        newBlock.add_end(29, 9, 26)
        newBlock.add_end(29, 16, 38)
        newBlock.add_end(37, 4, 19)
        newBlock.add_end(37, 9, 26)
        newBlock.add_end(37, 11, 28)
        newBlock.add_end(38, 4, 19)
        newBlock.add_end(38, 9, 26)
        newBlock.add_end(38, 11, 29)
        blockList.append(newBlock)

        #block11
        newBlock = Block_road([-1, 20, 27, 28, 29, 39, 40, 41])
        newBlock.add_end(20, 10, 28)
        newBlock.add_end(20, 17, 41)
        newBlock.add_end(27, 5, 20)
        newBlock.add_end(27, 17, 41)
        newBlock.add_end(28, 5, 20)
        newBlock.add_end(28, 17, 41)
        newBlock.add_end(29, 5, 20)
        newBlock.add_end(29, 17, 39)
        newBlock.add_end(39, 5, 20)
        newBlock.add_end(39, 10, 29)
        newBlock.add_end(40, 5, 20)
        newBlock.add_end(40, 10, 29)
        newBlock.add_end(41, 5, 20)
        newBlock.add_end(41, 10, 28)
        newBlock.add_end(-1, 10, 27)
        newBlock.add_end(-1, 17, 40)
        blockList.append(newBlock)

        #block12
        newBlock = Block_road([30, 31, 42, 49])
        newBlock.add_end(30, 13, 42)
        newBlock.add_end(30, 18, 49)
        newBlock.add_end(31, 13, 42)
        newBlock.add_end(31, 18, 49)
        newBlock.add_end(42, 6, 31)
        newBlock.add_end(42, 18, 49)
        newBlock.add_end(49, 6, 30)
        newBlock.add_end(49, 13, 42)
        blockList.append(newBlock)

        #block13
        newBlock = Block_road([-1, 32, 33, 42, 43, 44, 50, 51])
        newBlock.add_end(32, 12, 42)
        newBlock.add_end(32, 14, 43)
        newBlock.add_end(32, 19, 51)
        newBlock.add_end(33, 12, 42)
        newBlock.add_end(33, 14, 43)
        newBlock.add_end(33, 19, 51)
        newBlock.add_end(42, 7, 32)
        newBlock.add_end(42, 14, 43)
        newBlock.add_end(42, 19, 51)
        newBlock.add_end(43, 7, 33)
        newBlock.add_end(43, 12, 42)
        newBlock.add_end(43, 19, 51)
        newBlock.add_end(44, 7, 33)
        newBlock.add_end(44, 12, 42)
        newBlock.add_end(44, 19, 51)
        newBlock.add_end(50, 7, 33)
        newBlock.add_end(50, 12, 42)
        newBlock.add_end(50, 14, 44)
        newBlock.add_end(51, 7, 33)
        newBlock.add_end(51, 12, 42)
        newBlock.add_end(51, 14, 44)
        newBlock.add_end(-1, 19, 50)
        blockList.append(newBlock)

        #block14
        newBlock = Block_road([34, 43, 44, 45, 46, 47, 53, 54])
        newBlock.add_end(34, 13, 43)
        newBlock.add_end(34, 15, 45)
        newBlock.add_end(34, 20, 53)
        newBlock.add_end(43, 8, 34)
        newBlock.add_end(43, 15, 45)
        newBlock.add_end(43, 20, 53)
        newBlock.add_end(44, 8, 34)
        newBlock.add_end(44, 15, 45)
        newBlock.add_end(44, 20, 53)
        newBlock.add_end(45, 8, 34)
        newBlock.add_end(45, 13, 43)
        newBlock.add_end(45, 20, 53)
        newBlock.add_end(46, 8, 34)
        newBlock.add_end(46, 13, 43)
        newBlock.add_end(46, 20, 54)
        newBlock.add_end(47, 8, 34)
        newBlock.add_end(47, 13, 43)
        newBlock.add_end(47, 20, 54)
        newBlock.add_end(53, 8, 34)
        newBlock.add_end(53, 13, 44)
        newBlock.add_end(53, 15, 45)
        newBlock.add_end(54, 8, 34)
        newBlock.add_end(54, 13, 46)
        newBlock.add_end(54, 15, 47)
        blockList.append(newBlock)

        #block15
        newBlock = Block_road([-1, 35, 36, 45, 46, 47, 48, 55])
        newBlock.add_end(35, 14, 45)
        newBlock.add_end(35, 16, 48)
        newBlock.add_end(35, 21, 55)
        newBlock.add_end(36, 14, 45)
        newBlock.add_end(36, 16, 48)
        newBlock.add_end(36, 21, 55)
        newBlock.add_end(45, 9, 35)
        newBlock.add_end(45, 16, 48)
        newBlock.add_end(45, 21, 55)
        newBlock.add_end(46, 9, 35)
        newBlock.add_end(46, 16, 48)
        newBlock.add_end(46, 21, 55)
        newBlock.add_end(47, 9, 35)
        newBlock.add_end(47, 16, 48)
        newBlock.add_end(47, 21, 55)
        newBlock.add_end(48, 9, 36)
        newBlock.add_end(48, 14, 47)
        newBlock.add_end(48, 21, 55)
        newBlock.add_end(55, 9, 36)
        newBlock.add_end(55, 14, 47)
        newBlock.add_end(55, 16, 48)
        newBlock.add_end(-1, 14, 46)
        blockList.append(newBlock)

        #block16
        newBlock = Block_road([29, 37, 38, 48, 56, 57])
        newBlock.add_end(29, 10, 29)
        newBlock.add_end(29, 15, 48)
        newBlock.add_end(29, 22, 56)
        newBlock.add_end(37, 15, 48)
        newBlock.add_end(37, 17, 29)
        newBlock.add_end(37, 22, 56)
        newBlock.add_end(38, 15, 48)
        newBlock.add_end(38, 17, 29)
        newBlock.add_end(38, 22, 57)
        newBlock.add_end(48, 10, 37)
        newBlock.add_end(48, 17, 29)
        newBlock.add_end(48, 22, 56)
        newBlock.add_end(56, 10, 37)
        newBlock.add_end(56, 15, 48)
        newBlock.add_end(56, 17, 29)
        newBlock.add_end(57, 10, 38)
        newBlock.add_end(57, 15, 48)
        newBlock.add_end(57, 17, 29)
        blockList.append(newBlock)

        #block17
        newBlock = Block_road([-1, 29, 39, 40, 41, 58, 59, 60])
        newBlock.add_end(29, 11, 29)
        newBlock.add_end(29, 23, 58)
        newBlock.add_end(39, 16, 29)
        newBlock.add_end(39, 23, 58)
        newBlock.add_end(40, 16, 29)
        newBlock.add_end(40, 23, 59)
        newBlock.add_end(41, 16, 29)
        newBlock.add_end(41, 23, 60)
        newBlock.add_end(58, 11, 39)
        newBlock.add_end(58, 16, 29)
        newBlock.add_end(59, 11, 40)
        newBlock.add_end(59, 16, 29)
        newBlock.add_end(60, 11, 41)
        newBlock.add_end(60, 16, 29)
        newBlock.add_end(-1, 23, 59)
        blockList.append(newBlock)

        #block18
        newBlock = Block_road([49, 61, 71])
        newBlock.add_end(49, 19, 61)
        newBlock.add_end(49, 24, 71)
        newBlock.add_end(61, 12, 49)
        newBlock.add_end(61, 24, 71)
        newBlock.add_end(71, 12, 49)
        newBlock.add_end(71, 19, 61)
        blockList.append(newBlock)

        #block19
        newBlock = Block_road([-1, 50, 51, 61, 63, 64, 72, 73, 74])
        newBlock.add_end(50, 18, 61)
        newBlock.add_end(50, 20, 63)
        newBlock.add_end(50, 25, 72)
        newBlock.add_end(51, 18, 61)
        newBlock.add_end(51, 20, 63)
        newBlock.add_end(51, 25, 74)
        newBlock.add_end(61, 13, 50)
        newBlock.add_end(61, 20, 63)
        newBlock.add_end(61, 25, 72)
        newBlock.add_end(63, 13, 51)
        newBlock.add_end(63, 18, 61)
        newBlock.add_end(63, 25, 74)
        newBlock.add_end(64, 13, 51)
        newBlock.add_end(64, 18, 62)
        newBlock.add_end(64, 25, 74)
        newBlock.add_end(72, 13, 50)
        newBlock.add_end(72, 18, 61)
        newBlock.add_end(72, 20, 64)
        newBlock.add_end(73, 13, 51)
        newBlock.add_end(73, 18, 61)
        newBlock.add_end(73, 20, 64)
        newBlock.add_end(74, 13, 51)
        newBlock.add_end(74, 18, 61)
        newBlock.add_end(74, 20, 64)
        newBlock.add_end(-1, 25, 73)
        blockList.append(newBlock)

        #block20
        newBlock = Block_road([-1, 53, 54, 63, 64, 65, 66, 75, 76, 77])
        newBlock.add_end(53, 19, 63)
        newBlock.add_end(53, 21, 65)
        newBlock.add_end(53, 26, 76)
        newBlock.add_end(54, 19, 63)
        newBlock.add_end(54, 21, 65)
        newBlock.add_end(54, 26, 76)
        newBlock.add_end(63, 14, 53)
        newBlock.add_end(63, 21, 65)
        newBlock.add_end(63, 26, 75)
        newBlock.add_end(64, 14, 53)
        newBlock.add_end(64, 21, 65)
        newBlock.add_end(64, 26, 75)
        newBlock.add_end(65, 14, 54)
        newBlock.add_end(65, 19, 63)
        newBlock.add_end(65, 26, 76)
        newBlock.add_end(66, 14, 54)
        newBlock.add_end(66, 19, 63)
        newBlock.add_end(66, 26, 76)
        newBlock.add_end(75, 14, 53)
        newBlock.add_end(75, 19, 64)
        newBlock.add_end(75, 21, 65)
        newBlock.add_end(76, 14, 53)
        newBlock.add_end(76, 19, 63)
        newBlock.add_end(76, 21, 66)
        newBlock.add_end(77, 14, 54)
        newBlock.add_end(77, 19, 63)
        newBlock.add_end(77, 21, 66)
        newBlock.add_end(-1, 26, 77)
        blockList.append(newBlock)

        #block21
        newBlock = Block_road([55, 65, 66, 67, 68, 69, 78])
        newBlock.add_end(55, 20, 65)
        newBlock.add_end(55, 22, 67)
        newBlock.add_end(55, 27, 78)
        newBlock.add_end(65, 15, 55)
        newBlock.add_end(65, 22, 67)
        newBlock.add_end(65, 27, 78)
        newBlock.add_end(66, 15, 55)
        newBlock.add_end(66, 22, 68)
        newBlock.add_end(66, 27, 78)
        newBlock.add_end(67, 15, 55)
        newBlock.add_end(67, 20, 65)
        newBlock.add_end(67, 27, 78)
        newBlock.add_end(68, 15, 55)
        newBlock.add_end(68, 20, 66)
        newBlock.add_end(68, 27, 78)
        newBlock.add_end(69, 15, 55)
        newBlock.add_end(69, 20, 66)
        newBlock.add_end(69, 27, 78)
        newBlock.add_end(78, 15, 55)
        newBlock.add_end(78, 20, 66)
        newBlock.add_end(78, 22, 69)
        blockList.append(newBlock)

        #block22
        newBlock = Block_road([-1, 56, 57, 67, 68, 69, 70, 79, 80, 81])
        newBlock.add_end(56, 21, 67)
        newBlock.add_end(56, 23, 70)
        newBlock.add_end(56, 28, 80)
        newBlock.add_end(57, 21, 68)
        newBlock.add_end(57, 23, 70)
        newBlock.add_end(57, 28, 81)
        newBlock.add_end(67, 16, 56)
        newBlock.add_end(67, 23, 70)
        newBlock.add_end(67, 28, 80)
        newBlock.add_end(68, 16, 56)
        newBlock.add_end(68, 23, 70)
        newBlock.add_end(68, 28, 80)
        newBlock.add_end(69, 16, 56)
        newBlock.add_end(69, 23, 70)
        newBlock.add_end(69, 28, 80)
        newBlock.add_end(70, 16, 57)
        newBlock.add_end(70, 21, 68)
        newBlock.add_end(70, 28, 81)
        newBlock.add_end(79, 16, 56)
        newBlock.add_end(79, 21, 69)
        newBlock.add_end(79, 23, 70)
        newBlock.add_end(80, 16, 56)
        newBlock.add_end(80, 21, 69)
        newBlock.add_end(80, 23, 70)
        newBlock.add_end(81, 16, 56)
        newBlock.add_end(81, 21, 68)
        newBlock.add_end(81, 23, 70)
        newBlock.add_end(-1, 28, 79)
        blockList.append(newBlock)

        #block23
        newBlock = Block_road([58, 59, 60, 70, 82, 106, 108])
        newBlock.add_end(58, 22, 70)
        newBlock.add_end(58, 29, 82)
        newBlock.add_end(59, 22, 70)
        newBlock.add_end(59, 29, 82)
        newBlock.add_end(60, 22, 70)
        newBlock.add_end(60, 29, 106)
        newBlock.add_end(70, 17, 58)
        newBlock.add_end(70, 29, 82)
        newBlock.add_end(82, 17, 59)
        newBlock.add_end(82, 22, 70)
        newBlock.add_end(106, 17, 60)
        newBlock.add_end(106, 22, 70)
        newBlock.add_end(108, 17, 60)
        newBlock.add_end(108, 22, 70)
        newBlock.add_end(108, 29, 106)
        blockList.append(newBlock)

        #block24
        newBlock = Block_road([71, 83, 90])
        newBlock.add_end(71, 25, 83)
        newBlock.add_end(71, 30, 90)
        newBlock.add_end(83, 18, 71)
        newBlock.add_end(83, 30, 90)
        newBlock.add_end(90, 18, 71)
        newBlock.add_end(90, 25, 83)
        blockList.append(newBlock)

        #block25
        newBlock = Block_road([-1, 72, 73, 74, 83, 84, 85, 91])
        newBlock.add_end(72, 24, 83)
        newBlock.add_end(72, 26, 84)
        newBlock.add_end(72, 31, 91)
        newBlock.add_end(73, 24, 83)
        newBlock.add_end(73, 26, 84)
        newBlock.add_end(73, 31, 91)
        newBlock.add_end(74, 24, 83)
        newBlock.add_end(74, 26, 84)
        newBlock.add_end(74, 31, 91)
        newBlock.add_end(83, 19, 74)
        newBlock.add_end(83, 26, 85)
        newBlock.add_end(83, 31, 91)
        newBlock.add_end(84, 19, 74)
        newBlock.add_end(84, 24, 83)
        newBlock.add_end(84, 31, 91)
        newBlock.add_end(85, 19, 74)
        newBlock.add_end(85, 24, 83)
        newBlock.add_end(85, 31, 91)
        newBlock.add_end(91, 19, 74)
        newBlock.add_end(91, 24, 83)
        newBlock.add_end(91, 26, 85)
        newBlock.add_end(-1, 19, 72)
        newBlock.add_end(-1, 19, 73)
        blockList.append(newBlock)

        #block26
        newBlock = Block_road([-1, 75, 76, 77, 84, 85, 86, 92])
        newBlock.add_end(75, 25, 84)
        newBlock.add_end(75, 27, 86)
        newBlock.add_end(75, 32, 92)
        newBlock.add_end(76, 25, 85)
        newBlock.add_end(76, 27, 86)
        newBlock.add_end(76, 32, 92)
        newBlock.add_end(77, 25, 85)
        newBlock.add_end(77, 27, 86)
        newBlock.add_end(77, 32, 92)
        newBlock.add_end(84, 20, 75)
        newBlock.add_end(84, 27, 86)
        newBlock.add_end(84, 32, 92)
        newBlock.add_end(85, 20, 76)
        newBlock.add_end(85, 27, 86)
        newBlock.add_end(85, 32, 92)
        newBlock.add_end(86, 20, 76)
        newBlock.add_end(86, 25, 85)
        newBlock.add_end(86, 32, 92)
        newBlock.add_end(92, 20, 76)
        newBlock.add_end(92, 25, 85)
        newBlock.add_end(92, 27, 86)
        newBlock.add_end(-1, 20, 77)
        blockList.append(newBlock)

        #block27
        newBlock = Block_road([78, 86, 87])
        newBlock.add_end(78, 26, 86)
        newBlock.add_end(78, 28, 87)
        newBlock.add_end(78, 33, 96)#
        newBlock.add_end(86, 21, 78)
        newBlock.add_end(86, 28, 87)
        newBlock.add_end(86, 33, 96)#
        newBlock.add_end(87, 21, 78)
        newBlock.add_end(87, 26, 86)
        newBlock.add_end(87, 33, 96)#
        blockList.append(newBlock)

        #block28
        newBlock = Block_road([-1, 79, 80, 81, 87, 88, 89, 93])
        newBlock.add_end(79, 27, 87)
        newBlock.add_end(79, 29, 89)
        newBlock.add_end(79, 34, 93)
        newBlock.add_end(80, 27, 87)
        newBlock.add_end(80, 29, 89)
        newBlock.add_end(80, 34, 93)
        newBlock.add_end(81, 27, 87)
        newBlock.add_end(81, 29, 88)
        newBlock.add_end(81, 34, 93)
        newBlock.add_end(87, 22, 80)
        newBlock.add_end(87, 29, 89)
        newBlock.add_end(87, 34, 93)
        newBlock.add_end(88, 22, 81)
        newBlock.add_end(88, 27, 87)
        newBlock.add_end(88, 34, 93)
        newBlock.add_end(89, 22, 80)
        newBlock.add_end(89, 27, 87)
        newBlock.add_end(89, 34, 93)
        newBlock.add_end(93, 22, 80)
        newBlock.add_end(93, 27, 87)
        newBlock.add_end(93, 29, 89)
        newBlock.add_end(-1, 22, 79)
        blockList.append(newBlock)

        #block29
        newBlock = Block_road([82, 88, 89, 94, 106, 109])
        newBlock.add_end(82, 28, 88)
        newBlock.add_end(82, 35, 94)
        newBlock.add_end(88, 23, 82)
        newBlock.add_end(88, 35, 94)
        newBlock.add_end(89, 23, 106)
        newBlock.add_end(89, 35, 94)
        newBlock.add_end(94, 23, 106)
        newBlock.add_end(94, 28, 89)
        newBlock.add_end(106, 28, 89)
        newBlock.add_end(106, 35, 94)
        newBlock.add_end(109, 23, 106)
        newBlock.add_end(109, 28, 89)
        newBlock.add_end(109, 35, 94)
        blockList.append(newBlock)

        #block30
        newBlock = Block_road([90, 99, 107])
        newBlock.add_end(90, 31, 105)
        newBlock.add_end(99, 24, 90)
        newBlock.add_end(99, 31, 105)
        newBlock.add_end(107, 24, 90)
        newBlock.add_end(107, 31, 105)
        blockList.append(newBlock)

        #block31
        newBlock = Block_road([91, 95, 105])
        newBlock.add_end(91, 30, 90)
        newBlock.add_end(91, 32, 92)
        newBlock.add_end(95, 25, 91)
        newBlock.add_end(95, 30, 99)
        newBlock.add_end(105, 25, 91)
        newBlock.add_end(105, 30, 99)
        newBlock.add_end(105, 32, 95)
        blockList.append(newBlock)

        #block32
        newBlock = Block_road([92, 95, 96, 100])
        newBlock.add_end(92, 31, 95)
        newBlock.add_end(92, 33, 96)
        newBlock.add_end(95, 26, 92)
        newBlock.add_end(95, 33, 96)
        newBlock.add_end(96, 26, 92)
        newBlock.add_end(96, 31, 95)
        newBlock.add_end(100, 26, 92)
        newBlock.add_end(100, 31, 95)
        newBlock.add_end(100, 33, 96)
        blockList.append(newBlock)

        #block33
        newBlock = Block_road([96, 97, 101])
        newBlock.add_end(96, 27, 86)#
        newBlock.add_end(96, 34, 97)
        newBlock.add_end(97, 27, 86)#
        newBlock.add_end(97, 32, 96)
        newBlock.add_end(101, 27, 86)#
        newBlock.add_end(101, 32, 96)
        newBlock.add_end(101, 34, 97)
        blockList.append(newBlock)

        #block34
        newBlock = Block_road([93, 97, 98, 102])
        newBlock.add_end(93, 33, 97)
        newBlock.add_end(93, 35, 98)
        newBlock.add_end(97, 28, 93)
        newBlock.add_end(97, 35, 98)
        newBlock.add_end(98, 28, 93)
        newBlock.add_end(98, 33, 97)
        newBlock.add_end(102, 28, 93)
        newBlock.add_end(102, 33, 97)
        newBlock.add_end(102, 35, 98)
        blockList.append(newBlock)

        #block35
        newBlock = Block_road([94, 98, 103, 104])
        newBlock.add_end(94, 34, 98)
        newBlock.add_end(98, 29, 94)
        newBlock.add_end(103, 29, 94)
        newBlock.add_end(103, 34, 98)
        newBlock.add_end(104, 29, 94)
        newBlock.add_end(104, 34, 98)
        blockList.append(newBlock)

        Road = {}
        Road[0] = 22.992500, 120.217833
        Road[1] = 22.992500, 120.219990
        Road[2] = 22.992500, 120.220333
        Road[3] = 22.992500, 120.221556
        Road[4] = 22.992500, 120.222538
        Road[5] = 22.992500, 120.223080
        Road[6] = 22.992500, 120.223842
        Road[7] = 22.993662, 120.219195
        Road[8] = 22.993894, 120.219195
        Road[9] = 22.994171, 120.219195
        Road[10] = 22.992817, 120.221175
        Road[11] = 22.993775, 120.221175
        Road[12] = 22.993578, 120.223155
        Road[13] = 22.994373, 120.223155
        Road[14] = 22.994350, 120.218009
        Road[15] = 22.994350, 120.218699
        Road[16] = 22.994350, 120.219988
        Road[17] = 22.994350, 120.220893
        Road[18] = 22.994350, 120.221354
        Road[19] = 22.994350, 120.221762
        Road[20] = 22.994350, 120.223991
        Road[21] = 22.995479, 120.217215
        Road[22] = 22.995706, 120.217215
        Road[23] = 22.995884, 120.217215
        Road[24] = 22.994990, 120.219195
        Road[25] = 22.995438, 120.221175
        Road[26] = 22.996023, 120.221175
        Road[27] = 22.995050, 120.223155
        Road[28] = 22.995885, 120.223155
        Road[29] = 22.996160, 120.223155
        Road[30] = 22.996165, 120.214816
        Road[31] = 22.996200, 120.214821
        Road[32] = 22.996200, 120.215807
        Road[33] = 22.996200, 120.217048
        Road[34] = 22.996200, 120.218150
        Road[35] = 22.996200, 120.219533
        Road[36] = 22.996200, 120.220149
        Road[37] = 22.996200, 120.221935
        Road[38] = 22.996200, 120.222807
        Road[39] = 22.996200, 120.223191
        Road[40] = 22.996200, 120.223850
        Road[41] = 22.996200, 120.224065
        Road[42] = 22.996686, 120.215235
        Road[43] = 22.996425, 120.217215
        Road[44] = 22.997220, 120.217215
        Road[45] = 22.996185, 120.219195
        Road[46] = 22.996527, 120.219195
        Road[47] = 22.996913, 120.219195
        Road[48] = 22.998176, 120.221175
        Road[49] = 22.998050, 120.213906
        Road[50] = 22.998050, 120.215285
        Road[51] = 22.998050, 120.216945
        Road[52] = 22.998050, 120.218031
        Road[53] = 22.998050, 120.218305
        Road[54] = 22.998050, 120.219028
        Road[55] = 22.998050, 120.220310
        Road[56] = 22.998050, 120.222072
        Road[57] = 22.998050, 120.222254
        Road[58] = 22.998050, 120.222884
        Road[59] = 22.998050, 120.223342
        Road[60] = 22.998050, 120.224235
        Road[61] = 22.998457, 120.215235
        Road[62] = 22.999624, 120.215235
        Road[63] = 22.998602, 120.217215
        Road[64] = 22.999757, 120.217215
        Road[65] = 22.998423, 120.219195
        Road[66] = 22.999338, 120.219195
        Road[67] = 22.998189, 120.221175
        Road[68] = 22.998853, 120.221175
        Road[69] = 22.999589, 120.221175
        Road[70] = 22.998287, 120.223155
        Road[71] = 22.999900, 120.214266
        Road[72] = 22.999900, 120.215403
        Road[73] = 22.999845, 120.216600
        Road[74] = 22.999909, 120.216777
        Road[75] = 22.999900, 120.217630
        Road[76] = 22.999900, 120.218456
        Road[77] = 22.999900, 120.219083
        Road[78] = 22.999900, 120.220470
        Road[79] = 22.999900, 120.221945
        Road[80] = 22.999900, 120.222200
        Road[81] = 22.999900, 120.222444
        Road[82] = 22.999900, 120.224118
        Road[83] = 23.001253, 120.215235
        Road[84] = 23.000527, 120.217215
        Road[85] = 23.001065, 120.217215
        Road[86] = 23.000897, 120.219195
        Road[87] = 23.000751, 120.221175
        Road[88] = 22.999983, 120.223155
        Road[89] = 23.000600, 120.223155
        Road[90] = 23.001750, 120.214678
        Road[91] = 23.001750, 120.215512
        Road[92] = 23.001750, 120.218629
        Road[93] = 23.001750, 120.222380
        Road[94] = 23.001750, 120.224563
        Road[95] = 23.003488, 120.217215
        Road[96] = 23.003192, 120.219195
        Road[97] = 23.002925, 120.221175
        Road[98] = 23.002646, 120.223155
        Road[99] = 23.003600, 120.214974
        Road[100] = 23.003600, 120.218800
        Road[101] = 23.003600, 120.220649
        Road[102] = 23.003600, 120.222508
        Road[103] = 23.003600, 120.223814
        Road[104] = 23.003600, 120.224729
        Road[105] = 23.003600, 120.216074
        Road[106] = 22.999900, 120.224424
        Road[107] = 23.004035, 120.213255
        Road[108] = 22.998464, 120.225135
        Road[109] = 23.000547, 120.225135
        return blockList, Road

    def get_start_road(lat, long, path, blockList, Road):
        start_index, start_out_range = get_blockNo(lat, long)   #看要上面call還是這裡call
        start_road = {2:0, 3:1, 4:3, 5:6, 12:30, 23:108, 29:109, 30:107, 31:105, 32:100, 33:101, 34:102, 35:104}
        if start_out_range:
            #print(path)
            return start_road[start_index], path
        else:
            start_road_list = []
            times = []
            for rd in blockList[path[0]].roadList:
                if path[1] in blockList[path[0]].road_dic[rd].keys():
                    start_road_list.append(blockList[path[0]].road_dic[rd][path[1]])
            start_road_list = list(set(start_road_list))
            if len(start_road_list) > 1:
                GOOGLE_PLACES_API_KEY = 
                gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
                for srl in start_road_list:
                    origin = (lat, long)
                    des = Road[srl]
                    result = gmaps.distance_matrix(origins = origin, destinations = des, mode = "walking")
                    duration = result['rows'][0]['elements'][0]['duration']['text']
                    temp = duration.split(" ", 1)
                    times.append(int(temp[0])) #超過60min?
                return start_road_list[times.index(min(times))], path[1:]
            else:
                return start_road_list[0], path[1:]

    def get_pathList(blockList, path, start_road):
        pathList = []
        p = path[0]
        r = start_road
        pathList.append(r)
        for blk in path[1:]:
            r = blockList[p].road_dic[r][blk]
            p = blk
            pathList.append(r)
        return pathList

    start_lat = sLat
    start_long = sLong
    end_lat = eLat
    end_long = eLong
    start_index, start_out_range = get_blockNo(start_lat, start_long)
    end_index, start_out_range = get_blockNo(end_lat, end_long)

    block = get_dij_block()
    block = add_pm25(z, block)
    path = get_path(start_index, end_index, block)

    blockList, Road = get_blockList_Road()
    if len(path) > 2:
        start_road, path = get_start_road(start_lat, start_long, path, blockList, Road)
    pathList = get_pathList(blockList, path, start_road)
    roads = []
    for paths in pathList:
        roads.append(Road[paths])
    return roads

# result = route_planning(22.999904, 120.153379, 22.996792, 120.222442)


# In[ ]:




