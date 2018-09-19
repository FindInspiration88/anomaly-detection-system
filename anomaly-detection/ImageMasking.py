from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def maskApply(picName):
    ktPath = "NLM-MontgomeryCXRSet\\MontgomerySet\\CXR_png\\"
    masksPath = "NLM-MontgomeryCXRSet\\MontgomerySet\\ManualMask\\"

    #Создание объектов изображений томографии и масок
    leftMask = Image.open(masksPath+"leftMask\\"+picName).convert("RGBA")
    rightMask = Image.open(masksPath+"rightMask\\"+picName).convert("RGBA")
    ktPic = Image.open(ktPath+picName).convert("RGB")

    #Перевод масок в трёхмерный массив numpy
    leftMaskArr = np.array(leftMask)
    rightMaskArr = np.array(rightMask)

    #Выделение белых областей масок в булиновском массиве
    doubleMaskBool =np.logical_or(leftMaskArr[...,0] > 250 ,rightMaskArr[...,0] > 250)

    #Создание массива, который будет содержать в себе сдвоенную маску
    transparentMaskArr = leftMaskArr.copy()

    #Перекрашивание белых областей в красный цвет и добавление 50%-ой прозрачности
    transparentMaskArr[doubleMaskBool] = [255,0,0,127]

    #Перевод массива в объект изображения (требуется для склейки изображений)
    transparentMask = Image.fromarray(transparentMaskArr)

    #Наложение маски на изображение
    ktPic.paste(transparentMask,(0, 0),transparentMask)

    #Настройка и открытие окна pyplot
    plt.figure(picName)
    plt.imshow(ktPic)
    plt.show()
