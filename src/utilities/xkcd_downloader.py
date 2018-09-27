'''
Created on 25. 9. 2018

@author: miros
'''
import urllib
import urllib.request
import re
import shutil
import ctypes


def download_page(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    return text

def find_image(page, ext):
    images = []
    for line in page.splitlines():
        match = re.search("img src=\"(.*\.{})\".*".format(ext), line)
        if match:
            images.append(match[1])
    return images

def download_image(url, filePath):
    
    image = urllib.request.urlretrieve(url)
    print(image[0])
    shutil.move(image[0], filePath)
    
def changeBG(imagePath):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 3)
    return;
        
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=".", type=str, help="Path of the downloaded image")
    args = parser.parse_args()
    
    
    page = download_page("https://xkcd.com/")
    images = find_image(page,'png')
    download_image('https:' + images[1],args.file)
    changeBG(args.file)
