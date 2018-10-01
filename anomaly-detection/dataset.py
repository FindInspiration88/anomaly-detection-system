from PIL import Image
import os, errno
import numpy as np
import subprocess
import math


# Разбить исходное изображение на квадраты 100х100 пикселей
def cutImage(picName, road, pic=None):
    dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir + os.sep)

    # Путь к файлу с исходными изображениями легких
    ktPath = "NLM-MontgomeryCXRSet" + os.sep + "MontgomerySet" + os.sep + "CXR_png" + os.sep
    # Размер области в изображении, которое необходимо разбить
    imageSize = 100
    # Открыть исходное изображение из источника ktPath
    originalImage = Image.open(ktPath + picName)
    # Получить размеры исходного изображения
    (width, height) = originalImage.size

    # кол-во требуемых строчек и стоблцов (целочисленное)
    numRows = math.floor(width / imageSize) + 1
    numCols = math.floor(height / imageSize) + 1

    # Cделать массив из картинки
    if pic == None:
        originalImageArr = np.array(originalImage)
    else:
        originalImageArr = np.array(pic)
    # Попробовать создать директорию с именем road
    try:
        os.makedirs(road)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    os.chdir(road)
    # Разбиение np массива на картинки 100х100
    for row in range(numRows):

        for col in range(numCols):
            littlePic = False
            background = Image.new("RGBA", (100, 100), color=(0, 0, 0, 0))
            top = Image.fromarray(
                originalImageArr[col * imageSize:(col + 1) * imageSize, row * imageSize:(row + 1) * imageSize, ...])
            (topWidth, topHeigth) = top.size
            # Проверяет, если картинка оказалась неполной, использовать наложение предыдущей картинки
            if top.size != (imageSize, imageSize):
                if topHeigth != imageSize and topWidth != imageSize:
                    top = Image.fromarray(originalImageArr[(col - 1) * imageSize + topHeigth:col * imageSize + topHeigth,(row - 1) * imageSize + topWidth:row * imageSize + topWidth, ...])
                    littlePic = True
                if topHeigth > topWidth and littlePic == False:
                    top = Image.fromarray(originalImageArr[col * imageSize:(col + 1) * imageSize, (row-1) * imageSize + topWidth:row * imageSize + topWidth,...])
                    littlePic = False
                if topHeigth < topWidth and littlePic == False:
                    top = Image.fromarray(originalImageArr[(col-1) * imageSize + topHeigth:col * imageSize + topHeigth,row * imageSize:(row+1) * imageSize,...])
                    littlePic = False
            background.paste(top, (0, 0))
            background.save("newImage_" + str(col + 1) + "_" + str(row + 1) + ".png")

