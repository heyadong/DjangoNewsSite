from PIL import Image,ImageDraw,ImageFont
import random
import string
import os
import time

class Captcha(object):
    font_path = os.path.join(os.path.dirname(__file__),'simfang.ttf')
    print(font_path)
    #字体文件路径
    number = 4
    size = (100, 40)
    bgcolor = (255, 255, 255) # 背景颜色
    font_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    font_size = 20
    draw_color = (random.randint(0,100),random.randint(100,255),(random.randint(20,255)))
    draw_line = True
    draw_number = 4
    SOURCE_TEXT= list(string.ascii_letters)
    for i in range(0,10):
        SOURCE_TEXT.append(str(i))
    # 生产验证码的文本

    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE_TEXT,cls.draw_number))
    # 干扰线

    @classmethod
    def __gene_line(cls,draw,width,height):
        begin = (random.randint(0,width),random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin,end],fill=cls.draw_color)

    @classmethod
    def __gene_point(cls,draw,point_chance,width,height):
        probability = min(100,max(0,int(point_chance)))
        for w in width:
            for h in height:
                temp = random.randint(0,101)
                if temp <= probability:
                    draw.point((w, h), fill=cls.draw_color)

    @classmethod
    def gene_code(cls):
        width, height = cls.size
        image = Image.new('RGBA',(width,height), cls.bgcolor)
        font = ImageFont.truetype(cls.font_path, cls.font_size)
        draw = ImageDraw.Draw(image) # 生成draw 对象
        text = cls.gene_text()
        font_width,font_height = font.getsize(text)
        draw.text(((width-font_width)/2,(height-font_height)/2),text,fill=cls.draw_color,font=font) # 将text 生成再画布上
        if cls.draw_line:
            for j in range(0,cls.draw_number):
                cls.__gene_line(draw,width=width,height=height)

        return (text, image)







