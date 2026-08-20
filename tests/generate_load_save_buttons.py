from PIL import Image, ImageDraw, ImageFont
import os

def create_enter_save_button(image_path, width=200, height=150):
    img = Image.new('RGB', (width, height), color='orange')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.rectangle([0, 0, width, height], outline='black', width=2)
    draw.text((50, 50), 'Enter save', fill='white', font=font)
    img.save(image_path)

def create_save_name_background_button(image_path, width=600, height=45, bg_color='deepskyblue'):
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, height], outline='white', width=2)
    img.save(image_path)

if __name__ == '__main__':
    enter_button_path = os.path.join("c:\\", "py code", "Parkour game", "pict", "buttons", "enter_save.png") #'c:\py code\Parkour game\pict\buttons\enter_save.png'
    save_bg_button_path = os.path.join("c:\\", "py code", "Parkour game", "pict", "buttons", "save_name_bg.png") #'c:\py code\Parkour game\pict\buttons\save_name_bg.png'
    create_enter_save_button(enter_button_path)
    create_save_name_background_button(save_bg_button_path)