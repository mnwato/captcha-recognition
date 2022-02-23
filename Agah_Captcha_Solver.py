import pytesseract
import os
import argparse
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    import Image, ImageOps, ImageEnhance, imread
except ImportError:
    from PIL import Image, ImageOps, ImageEnhance

def solve_captcha(path):

    """
    Convert a captcha image into a text, 
    using PyTesseract Python-wrapper for Tesseract
    Arguments:
        path (str):
            path to the image to be processed
    Return:
        'textualized' image
    """
    image = Image.open(path).convert('RGB')
    image = ImageOps.autocontrast(image)

    filename = "{}.png".format(os.getpid())
    image.save(filename)

    text = pytesseract.image_to_string(Image.open(filename))
    print(text)
    return text

solve_captcha('./Captcha_agah.jpg')

# if __name__ == '__main__':
#     argparser = argparse.ArgumentParser()
#     argparser.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
#     args = vars(argparser.parse_args())
#     path = args["image"]
#     print('-- Resolving')
#     captcha_text = solve_captcha(path)
#     print('-- Result: {}'.format(captcha_text))