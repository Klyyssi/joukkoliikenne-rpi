# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 09:22:54 2017

@author: markus
"""
 
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import time
 
import Image
import ImageDraw
import ImageFont

DC = 27
RST = 17
SPI_PORT = 0
SPI_DEVICE = 0

class NokiaLCD:
    def __init__(self):
        self.disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
        self.disp.begin(contrast=60)
        self.disp.clear()
        self.disp.display()
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 8)
        self.image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
        self.draw = ImageDraw.Draw(self.image)
        self.bigFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 9)
    
    def clear(self, x0=0, y0=0, x1=LCD.LCDWIDTH, y1=LCD.LCDHEIGHT):
        self.draw.rectangle((x0, y0, x1, y1), outline=255, fill=255)
        self.disp.display()
    
    def setText(self, text, x=0, y=0):
        self.draw.text((x,y), text, font=self.font)
        self.disp.image(self.image)
        self.disp.display()
    
    def drawTime(self, x=40, y=20):
        self.draw.rectangle((x,y-1,x+50,y+9), outline=255, fill=255)
        self.draw.text((x,y), time.strftime("%H:%M:%S"), font=self.bigFont)
        self.disp.image(self.image)
        self.disp.display()
        