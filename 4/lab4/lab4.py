import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

task = int(input('task: '))
if task == 1:
    mode = int(input('mode: '))
image = Image.open("Tsukuba Circuit.jpg")#"1.png")#"KoLll.bmp")#"lenna.bmp")#"Tsukuba Circuit.jpg")
draw = ImageDraw.Draw(image)
width = image.size[0]
height = image.size[1]
pix = image.load()
image.show('Before processing')
data_hist = []

if task == 1:
    if mode == 1:
        f = int(input('input f:'))
        if f < 0:
            f = 0
        if f > 255:
            f = 255
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]

                mid = (a + b + c) / 3
                S = 0
                if mid < f:
                    S = 0
                else:
                    S = 255
                draw.point((i, j), (S, S, S))
                data_hist.append(S)

    if mode == 2:
        f_min = int(input('input f_min:'))
        f_max = int(input('input f_max:'))
        if f_min < 0:
            f = 0
        if f_min > 255:
            f = 255
        if f_max < 0:
            f = 0
        if f_max > 255:
            f = 255

        if f_min > f_max:
            x = f_max
            f_max = f_min
            f_min = x
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]

                mid = (a + b + c) / 3
                S = 0
                if mid < f_min or mid > f_max:
                    S = 0
                else:
                    S = 255
                draw.point((i, j), (S, S, S))
                data_hist.append(S)
    image.save("ans.jpg", "JPEG")
    image.show('After processing')

elif task == 2:
    im = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(im)
    for i in range(width - 2):
        for j in range(height - 2):

            a1 = pix[i, j][0]
            b1 = pix[i, j][1]
            c1 = pix[i, j][2]
            mid1 = (a1 + b1 + c1) / 3

            a2 = pix[i, j + 1][0]
            b2 = pix[i, j + 1][1]
            c2 = pix[i, j + 1][2]
            mid2 = (a2 + b2 + c2) / 3

            a3 = pix[i, j + 2][0]
            b3 = pix[i, j + 2][1]
            c3 = pix[i, j + 2][2]
            mid3 = (a3 + b3 + c3) / 3

            a4 = pix[i + 1, j][0]
            b4 = pix[i + 1, j][1]
            c4 = pix[i + 1, j][2]
            mid4 = (a4 + b4 + c4) / 3

            a6 = pix[i + 1, j + 2][0]
            b6 = pix[i + 1, j + 2][1]
            c6 = pix[i + 1, j + 2][2]
            mid6 = (a6 + b6 + c6) / 3

            a7 = pix[i + 2, j][0]
            b7 = pix[i + 2, j][1]
            c7 = pix[i + 2, j][2]
            mid7 = (a7 + b7 + c7) / 3

            a8 = pix[i + 2, j + 1][0]
            b8 = pix[i + 2, j + 1][1]
            c8 = pix[i + 2, j + 1][2]
            mid8 = (a8 + b8 + c8) / 3

            a9 = pix[i + 2, j + 2][0]
            b9 = pix[i + 2, j + 2][1]
            c9 = pix[i + 2, j + 2][2]
            mid9 = (a9 + b9 + c9) / 3

            H1 = (- (mid1 + 2 * mid2 + mid3) + (mid7 + 2 * mid8 + mid9))
            H2 = (- (mid1 + 2 * mid4 + mid7) + (mid3 + 2 * mid6 + mid9))

            '''
            H1a = - (a1 + 2 * a4 + a7) + (a3 + 2 * a6 + a9)
            H2a = (a7 + 2 * a8 + a9) - (a1 + 2 * a2 + a3)
            H1b = - (b1 + 2 * b4 + b7) + (b3 + 2 * b6 + b9)
            H2b = (b7 + 2 * b8 + b9) - (b1 + 2 * b2 + b3)
            H1c = - (c1 + 2 * c4 + c7) + (c3 + 2 * c6 + c9)
            H2c = (c7 + 2 * c8 + c9) - (c1 + 2 * c2 + c3)
            '''

            mas = []
            mas.append(mid1 * np.sqrt(2))
            mas.append(2 * mid2)
            mas.append(mid3 * np.sqrt(2))
            mas.append(2 * mid4)
            mas.append(2 * mid6)
            mas.append(mid7 * np.sqrt(2))
            mas.append(2 * mid8)
            mas.append(mid9 * np.sqrt(2))

            if np.max(mas) != 0:
                S = np.sqrt((H1 * H1) + (H2 * H2)) * 255 / np.max(mas)
            else:
                S = np.sqrt((H1 * H1) + (H2 * H2)) * 255

            if S > 255:
                S = 255

            #Sa = np.sqrt(H1a * H1a + H2a * H2a)
            #Sb = np.sqrt(H1b * H1b + H2b * H2b)
            #Sc = np.sqrt(H1c * H1c + H2c * H2c)

            draw.point((i + 1, j + 1), (int(S), int(S), int(S)))
            data_hist.append(S)

    im.save("ans.jpg", "JPEG")
    im.show('After processing')

plt.hist(data_hist, 52, facecolor='green', alpha=0.5)
plt.show()
del draw
