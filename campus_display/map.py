import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import colors

def create_picture(pm25):
    airbox = ["x_pos", "y_pos", "pm25"]
    x_pos = [10, 33, 27, 12, 3, 34, 22, 47]                 # 測站的x座標
    y_pos = [56, 54, 5, 30, 45, 25, 32, 30]                 # 測站的y座標
    dic = {"x_pos": x_pos, "y_pos": y_pos, "pm25": pm25}
    airbox = pd.DataFrame(dic)

    x = np.arange(50)
    y = np.arange(60)
    z = np.zeros(3000)
    z = z.reshape(60, 50)

    dist = np.zeros(8)
    total = 0

    # 計算各點之空氣品質
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
            
    # 把角落設成vmin, vmax(尚未找到contour設定vmin, vmax之方法)
    z[0,0] = 0   
    z[59,49] = 150
            
    # 繪圖和設定plt
    plt.figure(figsize=(7, 6))
    norm = colors.Normalize(vmin=0, vmax=150)
    plt.axis('equal')
    plt.axis('off')
    Colors=('#00FF00','#FFFF00','#FFBB00','#FF8800','#FF5511','#FF5511','#FF0000','#FF0000','#CC0000','#CC0000','#7700FF')
    plt.contourf(x, y, z, norm=norm, colors=Colors, extend='max')
    plt.colorbar()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    #plt.show()
    plt.savefig("pm25.png", dpi = 300)
    plt.clf()

    # 設定plt
    plt.figure(figsize=(7, 6))
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)    #去掉上邊框
    ax.spines['bottom'].set_visible(False) #去掉下邊框
    ax.spines['left'].set_visible(False)   #去掉左邊框
    ax.spines['right'].set_visible(False)  #去掉右邊框

    # 疊成大地圖和pm2.5分布圖
    img1 = Image.open('NCKU(black)ver3.jpg')
    img1 = img1.convert('RGBA')
    img2 = Image.open('pm25.png')
    img2 = img2.convert('RGBA')
    img2 = img2.resize((2100, 1800),Image.ANTIALIAS)
    img2 = Image.blend(img2, img1, 0.3)
    #plt.imshow(img2)

    # 疊文字
    img3 = Image.open('NCKU(word)ver2.png')
    img3 = img3.convert('RGBA')
    width3 , height3 = img3.size
    img3_resize = img3.resize((width3, height3))
    resultPicture = Image.new('RGBA', img3.size, (0, 0, 0, 0))
    resultPicture.paste(img2,(0,0))
    resultPicture.paste(img3_resize, (0, 0), img3_resize)
    plt.imshow(resultPicture)
    plt.savefig("result.png", dpi = 300)
    plt.clf()