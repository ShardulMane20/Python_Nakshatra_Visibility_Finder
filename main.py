import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3, os, geocoder
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.time import Time
import astropy.units as u
import matplotlib.pyplot as plt

g = geocoder.ip('me')
location = EarthLocation(lat=g.latlng[0], lon=g.latlng[1])
time = Time.now()

def get_nakshatra_data(name):
    conn = sqlite3.connect('nakshatras.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ra, dec, image_path FROM nakshatras WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result

def calculate_altaz(ra, dec):
    star_coord = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame='icrs')
    altaz_frame = AltAz(obstime=time, location=location) # Creats frame foer sepcific altitude and azimuth for the given observation time and loc
    altaz = star_coord.transform_to(altaz_frame) #International Celestial Reference System
    return altaz.alt.deg, altaz.az.deg

def direction_from_azimuth(azimuth):
    if 0 <= azimuth < 45 or 315 <= azimuth < 360:
        return 'North'
    elif 45 <= azimuth < 135:
        return 'East'
    elif 135 <= azimuth < 225:
        return 'South'
    elif 225 <= azimuth < 315:
        return 'West'

def get_all_nakshatras():
    conn = sqlite3.connect('nakshatras.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM nakshatras")
    nakshatras = [row[0] for row in cursor.fetchall()]
    conn.close()
    return nakshatras

def check_visibility():
    nakshatra_name = dropdown_var.get()
    result = get_nakshatra_data(nakshatra_name)

    if result: 
        ra, dec, image_path = result #unpack
        alt, az = calculate_altaz(ra, dec)
        direction = direction_from_azimuth(az)

        result_window = tk.Toplevel(root)
        result_window.title(f"{nakshatra_name} Visibility")
        result_window.geometry("280x350")

        if alt > 0:
            result_text = f"{nakshatra_name} is visible at:\nAltitude: {alt:.1f}°\nAzimuth: {az:.1f}°\nDirection: {direction}"
            result_label = tk.Label(result_window, text=result_text, font=('Arial', 12))
            result_label.pack(pady=10)

            if image_path:
                full_image_path = os.path.join(os.path.dirname(__file__), image_path)
                if os.path.isfile(full_image_path):
                    img = Image.open(full_image_path).resize((200, 200), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img) #Suitable formatting   
                    img_label = tk.Label(result_window, image=img_tk)
                    
                    img_label.image = img_tk  # Keep reference to avoid garbage collection
                    img_label.pack(pady=10) 
                else:
                    tk.Label(result_window, text="Image not available.", font=('Arial', 10)).pack(pady=10)
        else:
            tk.Label(result_window, text=f"{nakshatra_name} is not visible at the moment.", font=('Arial', 12)).pack(pady=10)

    else:
        messagebox.showerror("Error", "Nakshatra not found. Please select a valid Nakshatra.")

def plot_altitude_azimuth():
    conn = sqlite3.connect('nakshatras.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, ra, dec FROM nakshatras")
    nakshatras_data = cursor.fetchall()
    conn.close()

    names, altitudes = [], []
    for name, ra, dec in nakshatras_data:
        alt, az = calculate_altaz(ra, dec)
        if alt > 0:
            names.append(name)
            altitudes.append(alt)
    
    plt.bar(names, altitudes, color='skyblue')
    plt.xlabel('Nakshatras')
    plt.ylabel('Altitude (°)')
    plt.title('Altitude of Visible Nakshatras')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("Nakshatra Finder")
root.geometry("400x300")

bg_image = Image.open("night-sky-stars.jpg").resize((400, 300), Image.LANCZOS)
bg = ImageTk.PhotoImage(bg_image)#Suitable formatting  
bg_label = tk.Label(root, image=bg)
bg_label.place(relwidth=1, relheight=1)

input_frame = tk.Frame(root, bg="#1c1c2b", bd=5)
input_frame.pack(pady=10)

nakshatras = get_all_nakshatras()
dropdown_var = tk.StringVar(input_frame) #Tkinter variable that holds the current value
dropdown_var.set(nakshatras[0]) 
dropdown_menu = tk.OptionMenu(input_frame, dropdown_var, *nakshatras)
dropdown_menu.config(bg="white", fg="black")  
dropdown_menu.pack()

button_style = {'bg': 'white', 'fg': 'black', 'font': ('Arial', 10)}

tk.Button(root, text="Check Visibility", command=check_visibility, **button_style).pack(pady=15)
tk.Button(root, text="Plot Altitudes", command=plot_altitude_azimuth, **button_style).pack(pady=15)

root.mainloop()
