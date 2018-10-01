from ImageMasking import maskApply
from dataset import cutImage

cutImage("MCUCXR_0001_0.png",'source')
cutImage("MCUCXR_0001_0.png",'target', maskApply("MCUCXR_0001_0.png"))
