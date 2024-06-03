from PIL import Image, ImageFont, ImageDraw


def creating_func(fullname, course, mark):

    img1 = Image.open('media/image.jpg')
    draw = ImageDraw.Draw(img1)
    W, H = img1.size

    # font
    font = ImageFont.truetype("./media/Orbitron-Black.ttf", 100)
    font_mark = ImageFont.truetype("./media/Orbitron-Medium.ttf", 100)
    _, _, w, h = draw.textbbox((0, 0), fullname, font=font)
    _, _, w1, h1 = draw.textbbox((0, 0), course, font=font)
    _, _, w2, h2 = draw.textbbox((0, 0), mark, font=font)

    # set fullname
    draw.text(
        ((W - w) / 2, H/2+100),
        fullname, fill='#1D2733',
        font=font,
    ),
    # set course
    draw.text(
        ((W - w1) / 2-420, H / 2 + 800),
        course, fill='#1D2733',
        font=font,
    ),
    # set mark
    draw.text(
        ((W-w2) / 2 + 410,H/2 + 800),
        mark,fill='#1D2733',
        font=font,
    ),
    # img.show()
    img1.save(f'media/certificates/{fullname}.png')
    # print('Successfully is cut and saved')


# creating_func('Boburmirzo Axmedov', 'IOT', '82112126')
