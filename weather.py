from tkinter import *
import tkinter as tk
from datetime import *
import requests
from PIL import Image, ImageTk
from configparser import ConfigParser

root=Tk()
root.title("Weather App")
root.geometry("580x450")
root.configure(bg="#FAEBD3")
root.resizable(False,False)

image_icon = tk.PhotoImage(file="Images\logo.png")
root.iconphoto(False,image_icon)

config_file = 'configure.ini'
config_parser = ConfigParser()
config_parser.read(config_file)
api_key = config_parser['api_key']['key']



def getWeather(city):
    
    city= city_text.get()

    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, api_key)

    result = requests.get(url)
    json_data = result.json()
    
    city = json_data['name']
    country = json_data['sys']['country']
    
    origtemp = json_data['main']['temp']
    temp = origtemp - 273.15
    
    icon = json_data['weather'][0]['icon']
    description = json_data['weather'][0]['description']
    
    timezone = json_data['timezone']
    utc_time = datetime.utcnow()
    local_time = utc_time + timedelta(seconds = timezone)
    
    wind_speed = json_data['wind']['speed']
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    
    return (city, country, temp, icon, description, timezone, local_time, wind_speed, pressure, humidity)

def getForecast(city):
    url = ("https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, api_key)) 
    
    result = requests.get(url)
    json_data = result.json()
    
    first_min_temp_data = json_data['list'][0]['main']['temp_min']
    first_min_temp = first_min_temp_data - 273.15
    first_max_temp_data = json_data['list'][0]['main']['temp_max']
    first_max_temp = first_max_temp_data - 273.15
    
    second_min_temp_data = json_data['list'][1]['main']['temp_min']
    second_min_temp = second_min_temp_data - 273.15
    second_max_temp_data = json_data['list'][1]['main']['temp_max']
    second_max_temp = second_max_temp_data - 273.15
    
    return (first_min_temp, first_max_temp, second_min_temp, second_max_temp)

def searchWeather():
    
    city = city_text.get()
    weather = getWeather(city)
    forecast_data = getForecast(city)
    
    
    if weather and forecast_data:
        
        city_info = '{}'.format(weather[1])
        
        temp = '{:.2f} °C'.format(weather[2])
        t.config(text = temp)
        
        humid = '{:.2f}%'.format(weather[9])
        h.config(text = humid)
        
        press = '{:.2f} hPa'.format(weather[8])
        p.config(text = press)
        
        wind = '{:.2f} m/s'.format(weather[7])
        w.config(text = wind)
        
        desc = '{}'.format(weather[4])
        d.config(text = desc.capitalize())
        
        icon_path = 'icons/{}@2x.png'.format(weather[3])
        try:
            icon_img = Image.open(icon_path)
            icon_img = icon_img.resize((150,150), Image.LANCZOS)
            icon_img = ImageTk.PhotoImage(icon_img)
            icon_lbl.configure(image=icon_img)
            print(icon_path)
        except Exception as e:
            print({e})
        
        
        first = datetime.now()
        day1.config(text=first.strftime("%D %A"))
        
        second = first+timedelta(days=1)
        day2.config(text=second.strftime("%d %A"))

        third = first+timedelta(days=2)
        day3.config(text=third.strftime("%d %A"))
        
        day2mintemp = 'Min. Temperature: {:.2f} °C'.format(forecast_data[0])
        day2mintemp_lbl.config(text=day2mintemp)
        
        day2maxtemp = 'Max. Temperature: {:.2f} °C'.format(forecast_data[1])
        day2maxtemp_lbl.config(text=day2maxtemp)
        
        day3mintemp = 'Min. Temperature: {:.2f} °C'.format(forecast_data[2])
        day3mintemp_lbl.config(text=day3mintemp)
        
        day3maxtemp = 'Max. Temperature: {:.2f} °C'.format(forecast_data[3])
        day3maxtemp_lbl.config(text=day3maxtemp)
        
        

#GUI

#Search
searchframe=Frame(root,width=530,height=60,bg="#321E17")
searchframe.place(x=20,y=20)

weat_image=PhotoImage(file="images/Layer 7.png")
weatherimage=Label(root,image=weat_image,bg="#321E17")
weatherimage.place(x=30,y=27)

city_text=tk.Entry(root,justify='center',width=15,font=('poppins',25,'bold'),bg="#321E17",border=0,fg="white")
city_text.place(x=150,y=30)
city_text.focus()

search_icon_image = Image.open("images\Layer 6.png")
resized_search_icon = ImageTk.PhotoImage(search_icon_image.resize((50, 50), resample=Image.NEAREST))

search_icon_button = tk.Button(root, image=resized_search_icon, bg="#321E17", borderwidth=0, command=searchWeather)
search_icon_button.pack()
search_icon_button.place(x=475, y=25)

#main frame

icon_lbl = Label(root, bg = "#faebd3", image = "")
icon_lbl.place(x=50, y=100)

day1 = Label(root,font="helvetica 12 bold",fg="#321E17", text="", bg = "#FAEBD3")
day1.place(x=20,y=90)


#Weather Descriptions
labelframe=Frame(root,width=250,height=115,bg="#321E17")
labelframe.place(x=300,y=115)

label1=Label(root,text="Temperature",font=('Helvetica',11),fg="white",bg="#321E17")
label1.place(x=310,y=120)

label2=Label(root,text="Humidity",font=('Helvetica',11),fg="white",bg="#321E17")
label2.place(x=310,y=140)

label3=Label(root,text="Pressure",font=('Helvetica',11),fg="white",bg="#321E17")
label3.place(x=310,y=160)

label4=Label(root,text="Wind Speed",font=('Helvetica',11),fg="white",bg="#321E17")
label4.place(x=310,y=180)

label5=Label(root,text="Description",font=('Helvetica',11),fg="white",bg="#321E17")
label5.place(x=310,y=200)

#thpwd (temperature, humidity, pressure, wind speed, description)

t=Label(root,font=("Helvetica",11),fg="white",bg="#321E17")
t.place(x=420,y=120)
h=Label(root,font=("Helvetica",11),fg="white",bg="#321E17")
h.place(x=420,y=140)
p=Label(root,font=("Helvetica",11),fg="white",bg="#321E17")
p.place(x=420,y=160)
w=Label(root,font=("Helvetica",11),fg="white",bg="#321E17")
w.place(x=420,y=180)
d=Label(root,font=("Helvetica",11),fg="white",bg="#321E17")
d.place(x=420,y=200)


#BOTTOM
frame=Frame(root,width=1000,height=180,bg="#321E17")
frame.pack(side=BOTTOM)

first_box = Image.open("Images\Rounded Rectangle.png")
resized_first_box = ImageTk.PhotoImage(first_box.resize((250, 137), resample=Image.NEAREST))

first_box_label = tk.Label(root, image=resized_first_box, bg="#321E17")
first_box_label.place(x=30, y=290)

firstframe = Frame(root,width=245,height=132,bg="#321E17")
firstframe.place(x=35,y=295)

day2 = Label(firstframe,bg="#321E17",fg="#fff", font="helvetica 15 bold")
day2.place(x=10,y=5)

day2mintemp_lbl = Label(firstframe,bg="#321E17",fg="#fff", font="helvetica 12", text="")
day2mintemp_lbl.place(x=12,y=40)

day2maxtemp_lbl = Label(firstframe,bg="#321E17",fg="#fff", font="helvetica 12", text="")
day2maxtemp_lbl.place(x=12,y=80)




second_box_label = tk.Label(root, image=resized_first_box, bg="#321E17")
second_box_label.place(x=300, y=290)

secondframe = Frame(root,width=246,height=132,bg="#321E17")
secondframe.place(x=304,y=295)

day3 = Label(secondframe,bg="#321E17",fg="#fff", font="helvetica 15 bold")
day3.place(x=10,y=5)

day3mintemp_lbl = Label(secondframe,bg="#321E17",fg="#fff", font="helvetica 12", text="")
day3mintemp_lbl.place(x=12,y=40)

day3maxtemp_lbl = Label(secondframe,bg="#321E17",fg="#fff", font="helvetica 12", text="")
day3maxtemp_lbl.place(x=12,y=80)




root.mainloop()


