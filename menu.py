import tkinter as tk
from tkinter import ttk
import json
import requests
from PIL import Image, ImageTk
from tkinter import PhotoImage
import customtkinter
import os
import webbrowser
import ctypes
import os
import time
from ctypes import wintypes
from library import winapi
from library import utility
import requests
from tkinter import messagebox


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def register_button():
    webbrowser.open("www.google.com")

def login_button():
    username_text = username_text_input.get()
    password_text = password_text_input.get()

    if len(username_text) > 2 and len(password_text) > 2:

        login_request = requests.get("http://0.0.0.0:8000/api/checkuser/{}/{}/".format(username_text_input.get(),password_text_input.get())).json()
        login_request_status_json = login_request['Status']
        login_request_context_json = login_request['Context']

        print(login_request_status_json)
        print(login_request_context_json)

        if login_request_status_json == 'Error':
            #Removing Old Widgets
            lab.place(x=80, y=900)
            username_label.place(x=80, y=900)
            username_text_input.place(x=80, y=900)
            password_label.place(x=80, y=900)
            password_text_input.place(x=80, y=900)
            registrarse_button.place(x=80, y=900)
            login_button.place(x=80, y=900)

            #New Widgets
            assault_cube_label = customtkinter.CTkLabel(app, text="Assault Cube", fg_color="transparent")
            assault_cube_label.configure(font=("Courier", 45))
            assault_cube_label.place(x=40, y=20)

            game_found_label = customtkinter.CTkLabel(app, text="Game Found : ", fg_color="transparent")
            game_found_label.configure(font=("Courier", 22))
            game_found_label.place(x=75, y=80)

            assault_cube_label_version = customtkinter.CTkLabel(app, text="Current Version : v0.1", fg_color="transparent")
            assault_cube_label_version.configure(font=("Courier", 15))
            assault_cube_label_version.place(x=85, y=120)
            app.config(width=400, height=150)

            game_found_label_status = customtkinter.CTkLabel(app, text="False", fg_color="transparent")
            game_found_label_status.configure(text_color='red')
            game_found_label_status.configure(font=("Courier", 22))
            game_found_label_status.place(x=240 , y=80)

            #Starting Anticheat
            while True:
                time.sleep(2)
                pid = utility.GetProcId("ac_client.exe")
                if pid != None:
                    game_found_label_status.configure(text_color='green',text="test")
                    break
                messagebox.showerror(message="¡ Open the game !", title="Error")

            handle = winapi.OpenProcess(winapi.PROCESS_ALL_ACCESS, 0, ctypes.wintypes.DWORD(pid))
            moduleAddress = utility.GetModuleBaseAddress(pid, "ac_client.exe")

            entity_list_address = moduleAddress + 0x17E0A8
            WeponBullets = utility.FindDMAAddy(handle, entity_list_address, [0x0140], 32)
            WeponExtraBullets = utility.FindDMAAddy(handle, entity_list_address, [0x11C], 32)
            Life = utility.FindDMAAddy(handle, entity_list_address, [0xEC], 32)

            winapi.WriteProcessMemory(handle, WeponBullets, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int),
                                      None)
            winapi.WriteProcessMemory(handle, Life, ctypes.byref(ctypes.c_int(1111)), ctypes.sizeof(ctypes.c_int), None)
            winapi.WriteProcessMemory(handle, WeponExtraBullets, ctypes.byref(ctypes.c_int(1)),
                                      ctypes.sizeof(ctypes.c_int), None)

            while True:
                life_buffer_size = ctypes.sizeof(ctypes.c_int)
                life_buffer = ctypes.create_string_buffer(life_buffer_size)
                ctypes.windll.kernel32.ReadProcessMemory(handle, Life, life_buffer, life_buffer_size, None)
                life_read = ctypes.c_int.from_buffer(life_buffer).value

                wepon_extra_bullets_buffer_size = ctypes.sizeof(ctypes.c_int)
                wepon_extra_bullets_buffer = ctypes.create_string_buffer(wepon_extra_bullets_buffer_size)
                ctypes.windll.kernel32.ReadProcessMemory(handle, WeponExtraBullets, wepon_extra_bullets_buffer,
                                                         wepon_extra_bullets_buffer_size, None)
                wepon_extra_bullets_bullets_read = ctypes.c_int.from_buffer(wepon_extra_bullets_buffer).value

                wepon_bullets_buffer_size = ctypes.sizeof(ctypes.c_int)
                wepon_bullets_buffer = ctypes.create_string_buffer(wepon_bullets_buffer_size)
                ctypes.windll.kernel32.ReadProcessMemory(handle, WeponBullets, wepon_bullets_buffer,
                                                         wepon_bullets_buffer_size, None)
                wepon_bullets_read = ctypes.c_int.from_buffer(wepon_bullets_buffer).value

                print("Life : {}\nWepon Bullet : {}\nExtra Bullets: {}".format(life_read, wepon_bullets_read,
                                                                               wepon_extra_bullets_bullets_read))
                time.sleep(1)

            winapi.CloseHandle(handle)


app = customtkinter.CTk()
app.title("UARR ANTICHEAT")
app.config(width=400, height=600)
app.resizable(False, False)


if os.name == 'nt':
    if False != True:
        img = Image.open("logo.png")
        photo = ImageTk.PhotoImage(img)
        lab = tk.Label(image=photo, borderwidth=0, bg="#242424")
        lab.place(x=100, y=50)

        username_label = customtkinter.CTkLabel(app, text="Username : ", fg_color="transparent")
        username_label.configure(font=("Courier", 17))
        username_label.place(x=80, y=220)

        username_text_input = ttk.Entry()
        username_text_input.place(x=100, y=320, width=220, height=30)

        password_label = customtkinter.CTkLabel(app, text="Password : ", fg_color="transparent")
        password_label.configure(font=("Courier", 17))
        password_label.place(x=80, y=290)

        password_text_input = ttk.Entry()
        password_text_input.place(x=100, y=400, width=220, height=30)

        registrarse_button = customtkinter.CTkButton(app, text="Register", command=register_button)
        registrarse_button.configure(width=85)
        registrarse_button.place(x=80, y=380)

        login_button = customtkinter.CTkButton(app, text="Login", command=login_button)
        login_button.configure(width=85)
        login_button.place(x=170, y=380)

    version_label = customtkinter.CTkLabel(app, text="Version 0.1", fg_color="transparent")
    version_label.configure(font=("Courier", 17))
    version_label.place(x=20, y=445)
else:
    if False != True:
        img = Image.open("logo.png")
        photo = ImageTk.PhotoImage(img)
        lab = tk.Label(image=photo, borderwidth=0,bg="#242424")
        lab.place(x=120, y=50)


        username_label = customtkinter.CTkLabel(app, text="Username : ", fg_color="transparent")
        username_label.configure(font=("Courier", 17))
        username_label.place(x=100, y=290)

        username_text_input = ttk.Entry()
        username_text_input.place(x=100, y=320, width=220,height=30)

        password_label = customtkinter.CTkLabel(app, text="Password : ", fg_color="transparent")
        password_label.configure(font=("Courier", 17))
        password_label.place(x=100, y=370)

        password_text_input = ttk.Entry()
        password_text_input.place(x=100, y=400, width=220,height=30)


        registrarse_button = customtkinter.CTkButton(app, text="Register",command=register_button)
        registrarse_button.configure(width=100)
        registrarse_button.place(x=100, y=480)

        login_button = customtkinter.CTkButton(app, text="Login",command=login_button)
        login_button.configure(width=100)
        login_button.place(x=220, y=480)


    version_label = customtkinter.CTkLabel(app, text="Version 0.1", fg_color="transparent")
    version_label.configure(font=("Courier", 17))
    version_label.place(x=20, y=570)

app.mainloop()


