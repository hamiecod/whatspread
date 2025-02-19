import pyautogui
import time
import pandas as pd
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import sys
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap
import argparse
import pyperclip

# Parsing
parser = argparse.ArgumentParser(description="Process start, end and message descriptions")

parser.add_argument('-s', '--start', required=True, help='Start Value')
parser.add_argument('-e', '--end', required=True, help='End Value')

parser.add_argument('message_templates', nargs='*', help='List of message templates')

args = parser.parse_args()

start_from = int(args.start)
end_at = int(args.end)
message_templates = args.message_templates


# default values for microsoft surface pro 9
search_box = (222, 244)
first_match = (452, 395)
chat_box = (1088, 1777)
caption_area = (1063, 1622)

def loadMessage():
    with open((random.choice(message_templates)), 'r') as file:
        message = file.read()
    return message

# OCRs the image and returns text
def ocr(x,y,width,height):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    screenshot = pyautogui.screenshot(region=(x, y,width,height))

    # image enhancements
    gray_screenshot = screenshot.convert('L')
    enhancer = ImageEnhance.Contrast(gray_screenshot)
    gray_screenshot = enhancer.enhance(2)
    filtered_image = gray_screenshot.filter(ImageFilter.MedianFilter(size=3))

    text = pytesseract.image_to_string(filtered_image)

    print(text)

def type_multiline_message(message, contactName, fast=True):
    time.sleep(random.uniform(0.05, 0.25))
    message = message.replace('{{name}}', contactName)

    for char in message:
        if char == '\n':
            if fast == True :
                lines = message.split('\n')
                copied_text = '\n'.join(lines[1:])
                pyperclip.copy(copied_text)
                break

            pyautogui.keyDown('shift')
            pyautogui.press('enter')
            pyautogui.keyUp('shift')

        else:
            pyautogui.write(str(char)

        # simulate occassional typo
        if random.randint(1, 70) == 1:
            typo_char = random.choice('abcdefghijklmnopqrstuvwxyz')
            pyautogui.write(str(typo_char)
            time.sleep(random.uniform(0.1, 0.3))
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.05, 0.2))

        # add random delays
        if char in ['.', ',', '?', '!', ':', ';']:
            time.sleep(random.uniform(0.3, 0.6))
        elif char == ' ':
            time.sleep(random.uniform(0.005, 0.1))
        else:
            time.sleep(random.uniform(0.003, 0.005))

    # in case of fast typing, paste the copied text
    #pyautogui.hotkey('ctrl', 'v')

# moves the mouse like a human
def human_like_move(x, y, min_duration=0.05, max_duration=0.15):
    x += random.randint(-1, 1)
    y += random.randint(-1, 1)

    duration = random.uniform(min_duration, max_duration)
    pyautogui.dragTo(x,y, duration=duration, tween=pyautogui.easeInOutQuad)

# opens the chat of the phone number
def open_chat(phoneNumber):
    # navigate to search box
    human_like_move(search_box[0], search_box[1])
    time.sleep(0.5)

    # clear search box
    pyautogui.tripleClick()
    pyautogui.press("backspace")
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.5)

    # write phone number in search box
    pyautogui.write(str(phoneNumber), interval=random.uniform(0.05, 0.15))

    # wait time for contacts to appear
    time.sleep(1.5)

    # open the first match chat
    human_like_move(first_match[0], first_match[1], 0.3, 1)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.click()

    # go to send box of chat
    human_like_move(chat_box[0], chat_box[1], 0.2, 1)
    pyautogui.click()
    time.sleep(1)

# copies image to clipboard
def copy_image_to_clipboard(image_path):
    app = QApplication(image_path)

    pil_image = Image.open(image_path)

    date = pil_image.convert("RGBA").tobytes("raw", "RGBA")
    qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA_8888)

    clipboard = app.clipboard()
    clipboard.setPixmap(QPixmap.fromImage(qimage))

def text_and_image(image, contactName):
    copy_image_to_clipboard(image)
    pyautogui.hotkey('ctrl', 'v')
    # delay to paste data
    time.sleep(random.uniform(1.2, 1.5))

    # add caption
    pyautogui.dragTo(caption_area[0], caption_area[1], duration=time.uniform(0.2, 0.5))
    pyautogui.click()
    type_multiline_message(loadMessage(), contactName)


def text_only(contactName):
   type_multiline_message(loadMessage(), contactName)

def main():
    # start delay
    time.sleep(2)

    df = pd.read_csv('contacts.csv')
    for i in range(len(df)):

        if i < start_from or i > end_at:
            continue

        contactName = df.at[i, 'name']
        phoneNumber = df.at[i, 'phone']

        open_chat(phoneNumber)

        # if you want to send text and image
        # text_and_image(img_path, contactName)

        text_only(contactName)

        #temporary to paste message (faster send speed)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)

        # Final Step: Sends the message
        pyautogui.press("enter")
        time.sleep(1)

        if random.randint(1,100) == 100 :
            time.sleep(100)

if __name__ == "__main__":
    main()
