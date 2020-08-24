import time
import sys
import pyautogui
import re
import mouse
import pytesseract
import msvcrt
import keyboard
from PIL import Image, ImageEnhance, ImageFilter

def get_pos(name):
    pos = input('point the '+name+' and press enter')
    return pyautogui.position()

def init_data(d):
    d.item.x, d.item.y = get_pos('item icon')
    d.price.x, d.price.y = get_pos('price chan')
    d.quantity.x, d.quantity.y = get_pos('quantity chan')
    d.sell.x, d.sell.y = get_pos('sell button')
    d.lot_1.x, d.lot_1.y = get_pos("lot 1 'K'")
    d.lot_10.x, d.lot_10.y = get_pos("lot 10 'K'")
    d.lot_100.x, d.lot_100.y = get_pos("lot 100 'K'")

def get_im(d):
    pic = pyautogui.screenshot(region=(d.quantity.x - 25, d.quantity.y - 15, 50, 30))
    pic.save('im/quantity.png')
    pic = pyautogui.screenshot(region=(d.lot_1.x - 100, d.lot_1.y - 20, 90, 40))
    pic.save('im/lot_1.png')
    pic = pyautogui.screenshot(region=(d.lot_10.x - 100, d.lot_10.y - 20, 90, 40))
    pic.save('im/lot_10.png')
    pic = pyautogui.screenshot(region=(d.lot_100.x - 100, d.lot_100.y - 20, 90, 40))
    pic.save('im/lot_100.png')

def get_number(file_name, en, th):
    string = read_data(file_name, en, th)
    string = re.sub('\D', '', string)
    index_list = []
    del index_list[:]
    for i, x in enumerate(string):
        if x.isdigit() == True:
            index_list.append(i)
    #if not index_list and en < 15:
    #    return get_number(file_name, en + 10, th)
    if not index_list:
        return 0
    start = index_list[0]
    end = index_list[-1] + 1
    number = string[start:end]
    #print(en)
    return number

def read_data(file_name, en, th):
    img = Image.open(file_name).convert('L')
    img = img.point(lambda p: p > th and 255)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(float(en))
    img.save('im/greyscale.png')
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    #TESSDATA_PREFIX:'C:/Program Files/Tesseract-OCR/tessdata'
    customconf = r'-c tessedit_char_whitelist=" 01234567859" --psm 6'
    return (pytesseract.image_to_string('im/greyscale.png', config=customconf))

def print_data(d):
    print('\nquantity =', int(get_number('im/quantity.png', -100, 90)))
    print('lot 1    =', int(get_number('im/lot_1.png', -100, 90)))
    print('lot 10   =', int(get_number('im/lot_10.png', -100, 90)))
    print('lot 100  =', int(get_number('im/lot_100.png', -100, 90)))

def action(d):
    get_im(d)
    qu = int(get_number('im/quantity.png', -100, 90))
    l1 = int(get_number('im/lot_1.png', -100, 90))
    l10 = int(get_number('im/lot_10.png', -100, 90))
    l100 = int(get_number('im/lot_100.png', -100, 90))
    print (qu, l1, l10, l100)
    if l1 == 0 and l10 == 0 and l100 == 0:
        pyautogui.click(d.item.x, d.item.y)
        return (0)
    if qu == 100:
        price = l100-1
    elif qu == 10:
        price = l10 - 1
    else:
        price = l1-1
    if price <= 0:
        return (0)
    pyautogui.click(d.price.x, d.price.y, clicks = 2, interval = 0.2)
    pyautogui.write(str(price), interval = 0.05)
    for i in range(1,10):
        pyautogui.click(d.sell.x, d.sell.y, interval = 0.2)
    #time.sleep(1)
    return (0)

class pos():
    x = 0
    y = 0

class data():
    item = pos()
    price = pos()
    quantity = pos()
    sell = pos()
    lot_1 = pos()
    lot_10 = pos()
    lot_100 = pos()

if __name__ == "__main__":
    d = data()
    init_data(d)
    get_im(d)
    print_data(d)
    ex = input('correct data ? y/n\n')
    if ex != 'y':
        sys.exit()
    print('\npress esc to quit')
    while ex != 1:
        ex = action(d)
        if keyboard.is_pressed('escape') == True:
            print('exiting...')
            ex = 1