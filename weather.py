import sys 
 			 #for lcd
import Adafruit_Nokia_LCD as LCD #for lcd
import Adafruit_GPIO.SPI as SPI  #for lcd

from PIL import Image    	 #for lcd
from PIL import ImageDraw        #for lcd
from PIL import ImageFont        #for lcd



import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
import urllib2
import smtplib 
from email.mime.text import MIMEText

USERNAME="xyz@gmail.com"
PASSWORD="your password"
MAILTO="destination@gmail.com"

def lcd_display(T,RH):
	DC = 23
	RST = 24
	SPI_PORT = 0
	SPI_DEVICE = 0
	disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
	disp.begin(contrast=60)
	disp.clear()
	disp.display()
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	font = ImageFont.load_default()
	draw.text((2,10),"temp"+str(T), font=font)
	draw.text((2,30), "punna"+str(RH), font=font)
	disp.image(image)
	disp.display()
	print('Press Ctrl-C to quit.')
#	while True:
#	    	sleep(1.0)

def getSensorData():

        RH,T=Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,4)
    # return dict 
        return (str(RH),str(T))
        RH,T=Adafruit_DHT.getSensorData()
        
#main() function 
def main():
#     sys.argv  
       if len(sys.argv)<2:
               print('Usage: python weather_monitor.py PRIVATE KEY ')
               exit(0)
       print ('Starting...')
       baseURL='https://api.thingspeak.com/update?api_key=%s' % sys.argv[1]
       print (baseURL)
       while True:
              try:
                 
                      RH, T = getSensorData()
                      f=urllib2.urlopen(baseURL+'&field2=%s&field1=%s'%(RH,T))
                      
		      lcd_display(T,RH)
                      print("Humidity"+str(RH)+"%")
                      print("Temperature" +str(T)+"c") 
	              msg = MIMEText('Temperature %s Humidity %s for data logger click the link https://thingspeak.com/channels/451913 ' %(T, RH)))
		      msg['Subject']='Weather Report'
                      msg['From']=USERNAME
                      msg['TO']=MAILTO
                      server = smtplib.SMTP('smtp.gmail.com',587)
                      server.ehlo_or_helo_if_needed()
		      server.starttls()
		      
                      server.ehlo_or_helo_if_needed()
		      
                      server.login("raspikedar@gmail.com","sosswami")
		      server.sendmail("raspikedar@gmail.com", "skmkedar@gmail.com", msg.as_string())
		      server.close()
		      f.close()
		      sleep(15)
		      

              except:   
                      print ('Exiting.')
                      break 

# call main 
if __name__  =='__main__':
    main()    

