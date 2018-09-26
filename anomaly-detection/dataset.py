from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
import subprocess

# Разбить исходное изображение на квадраты 100х100 пикселей
def cutOriginalImage(picName, picWithMask=None, road='source'):
    # Путь к файлу с исходными изображениями легких
    ktPath = "NLM-MontgomeryCXRSet" + os.sep + "MontgomerySet" + os.sep + "CXR_png" + os.sep
    # Размер области в изображении, которое необходимо разбить
    imageSize = 100
    # Открыть исходное изображение из источника ktPath
    originalImage = Image.open(ktPath+picName)
    # Получить размеры исходного изображения
    (width, height) = originalImage.size
    #
    previosImage = Image.new("RGBA", (100,100), color=(0,0,0,0))
    #
    littlePic = False

    #кол-во требуемых строчек и стоблцов (целочисленное)
    numRows = round(width / imageSize)+1
    numCols = round(height / imageSize)+1


    # В зависимости от того что передали сделать массив из картинки
    if picWithMask==None:
        originalImageArr = np.array(originalImage)
    else:
        originalImageArr = np.array(picWithMask)

    # Разбиение np массива на картинки 100х100
    for row in range(numRows):

        for col in range(numCols):
            try:
                background = Image.new("RGBA", (100, 100), color = (0, 0, 0, 0))
                top = Image.fromarray(originalImageArr[col*imageSize:(col+1)*imageSize,row*imageSize:(row+1)*imageSize,...])
                (topWidth,topHeigth) = top.size
                # Проверяет, если картинка оказалась неполной, использовать наложение предыдущей картинки
                if top.size != (imageSize,imageSize):
                    if topHeigth&topWidth != imageSize:
                        previosImage = Image.fromarray(originalImageArr[(col-1) * imageSize:col * imageSize,(row - 1) * imageSize:(row) * imageSize, ...])
                        background.paste(previosImage, (0, 0))
                        littlePic = True
                    if topHeigth > topWidth | littlePic == false:
                        previosImage = Image.fromarray(originalImageArr[col*imageSize:(col+1)*imageSize,(row-1)*imageSize:(row)*imageSize,...])
                        background.paste(previosImage, (0,0))
                        littlePic = False
                    else:
                        previosImage = Image.fromarray(originalImageArr[(col-1)*imageSize:(col)*imageSize,row*imageSize:(row+1)*imageSize,...])
                        background.paste(previosImage, (0, 0))
                        littlePic = False
                background.paste(top, (imageSize-topWidth,imageSize-topHeigth))
                background.save(road+os.sep+"newImage_"+str(col+1)+"_"+str(row+1)+".png")
            except Exception:
                pass

def cutImageWithMask(picName):
    ktPath = "NLM-MontgomeryCXRSet" + os.sep + "MontgomerySet" + os.sep + "CXR_png" + os.sep
    masksPath = "NLM-MontgomeryCXRSet" + os.sep + "MontgomerySet" + os.sep + "ManualMask" + os.sep

    # Создание объектов изображений томографии и масок
    leftMask = Image.open(masksPath + "leftMask" + os.sep + picName).convert("RGBA")
    rightMask = Image.open(masksPath + "rightMask" + os.sep + picName).convert("RGBA")
    ktPic = Image.open(ktPath + picName).convert("RGB")

    # Перевод масок в трёхмерный массив numpy
    leftMaskArr = np.array(leftMask)
    rightMaskArr = np.array(rightMask)

    # Выделение белых областей масок в булиновском массиве
    doubleMaskBool = np.logical_or(leftMaskArr[..., 0] > 250, rightMaskArr[..., 0] > 250)

    # Создание массива, который будет содержать в себе сдвоенную маску
    transparentMaskArr = np.zeros(leftMaskArr.shape, dtype=leftMaskArr.dtype)

    # Перекрашивание белых областей в красный цвет и добавление 50%-ой прозрачности
    transparentMaskArr[doubleMaskBool] = [255, 0, 0, 127]

    # Перевод массива в объект изображения (требуется для склейки изображений)
    transparentMask = Image.fromarray(transparentMaskArr)

    # Наложение маски на изображение
    ktPic.paste(transparentMask, (0, 0), transparentMask)

    # функция разбиения картинки на квадраты 100 на 100
    cutOriginalImage(picName, picWithMask=ktPic, road='target')

