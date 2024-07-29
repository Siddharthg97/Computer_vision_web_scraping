from pathlib import Path
import os
import sys
import glob
from pdf2image import convert_from_path
import numpy as np
import pandas as pd
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageFont, ImageDraw
import pytesseract
import spacy
import cv2
from datetime import datetime
import math


"""# Converting Passport pdf into image"""

# pdf_path = '/app/pruthvi_paddle_integ/POC_TMNS/src/PDF_Text/sample_img.pdf'
# save_path ='/app/pruthvi_paddle_integ/POC_TMNS/src/PDF_Text/' 
# doc = fitz.open(pdf_path)

def convert_paddle_ds(img_path,new_height_flag=False):
    # conda.activate("padocr3")
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

    ocr = PaddleOCR(use_angle_cls=True, page_num=2,show_log=False)
    result = ocr.ocr(img_path, cls=True)
    count = 0
    text_new = ''
    for idx in range(len(result)):
        res = result[idx]
        # print(res)
        for input in res:

            # text_new = " ".join(input[1][0])
            text_new = " ".join([text_new, input[1][0]])
            count = count+1
    # print('***************************************************')
    # print(text_new)
    # print('***************************************************')

    return text_new
# function to clean the first_name
def clean_string(text):
  # Remove trailing spaces
  text = text.rstrip()
  # Remove single or multiple K alphabets
  text = text.replace('KK', '')
  # Remove trailing spaces
  text = text.rstrip()
  return text


def save_pages(pdf_file, dpi=300):
    """
    Save pages from a given pdf file at same location
    """
    pdf_path = str(pdf_file)
    result_final = ''
    result_list = []
    if '.pdf' in pdf_file:
        
        # Check whether the passed file is a pdf or not
        assert str(pdf_file)[-4:] == '.pdf'
        # print("Extracting pages for the pdf file:")
        
        # print(pdf_path)
    
        pdf_name = pdf_path.split(os.sep)[-1].split('.pdf')[0]
        save_path = Path(pdf_path.split(pdf_name)[0])
        # print(pdf_name)
        doc = pdf_name.replace(" ","_")
        # print(doc)
        # print(f"Saving pages to folder: {save_path}")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    
    
        poppler_path=r'C:\Program Files (x86)\poppler-21.03.0\Library\bin'
        # pages = convert_from_path(pdf_file, dpi, fmt="jpeg")  # , thread_count=4)
        if sys.platform.startswith('win'):
            pages = convert_from_path(pdf_path, dpi, fmt="tiff", thread_count=4, poppler_path=poppler_path)
        else:
            pages = convert_from_path(pdf_path, dpi, fmt="tiff", thread_count=4)
        for page in pages:
            w, h = page.size
            if w*h > 20000000:
                dpi = 100
                break
            # filename = save_path / f"{doc[1:]}_page_{img_count}.jpg"
            # page.save(filename, 'JPEG')
    
        if dpi==100:
            if sys.platform.startswith('win'):
                pages = convert_from_path(pdf_path, dpi, fmt="tiff", thread_count=4, poppler_path=poppler_path)
            else:
                pages = convert_from_path(pdf_path, dpi, fmt="tiff", thread_count=4)
    
    
        img_count = 1
        for page in pages:
            filename = save_path / f"{doc}_page_{img_count}.tiff"
            page.save(filename, 'TIFF')
            img_count += 1
        
        # print('save done')
        # print(save_path)
    else:
        pdf_name = pdf_path.split(os.sep)[-1].split('.tiff')[0]
        save_path = Path(pdf_path.split(pdf_name)[0])
    for i in glob.glob(str(save_path)+"/*.tiff"):
        # print(i)
        # ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)
        # result = ocr.ocr(img_path, cls=True) #cls=False as no text is rotated by 180 degrees
        result = convert_paddle_ds(i)
        result = result+' '
        # result.to_excel(i.replace('tiff','xlsx'))
        # with open(i.replace('tiff','txt'), "w") as output:
            # output.write(str(result))
        # print(result)
        result_final = result_final+ result
        # print("Total pages saved:", img_count-1)
        result_final = result_final.strip()
    result_list.append(result_final)
    return result_list
    


    

