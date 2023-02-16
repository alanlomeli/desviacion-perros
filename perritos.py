import tkinter as tk
import pandas as pd
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy.stats import norm
import urllib.request

datos = pd.read_csv('data.csv')

ventana = tk.Tk()
ventana.title('Perritos guau guau')

canvas = tk.Canvas(ventana, width=500, height=500)
canvas.pack()

def graficar(raza_seleccionada):

    edad_raza_agrupada = datos.groupby('raza')['edad']
    media_grupo = edad_raza_agrupada.mean()
    desviacion_std = edad_raza_agrupada.std()

    media_raza_seleccionada = media_grupo[raza_seleccionada]
    desviacion_raza_seleccionada = desviacion_std[raza_seleccionada]

    if pd.isna(media_raza_seleccionada):
        media_raza_seleccionada = 0
    if pd.isna(desviacion_raza_seleccionada):
        desviacion_raza_seleccionada = 0

    
    x = pd.Series(range(int(media_raza_seleccionada - 3 * desviacion_raza_seleccionada), int(media_raza_seleccionada + 3 * desviacion_raza_seleccionada)))

    # crear distribucion 
    y = norm.pdf(x, media_raza_seleccionada, desviacion_raza_seleccionada)

    # magia
    graf = plt.figure()
    plt.plot(x, y, 'b-', label='Distribucion normal')

    plt.title('Raza {}'.format(raza_seleccionada))
    plt.xlabel('Edad')
    plt.ylabel('Densidad')

    plt.legend(loc='best')
    imagen_seleccionada = datos.loc[datos['raza'] == raza_seleccionada, 'foto(url)'].iloc[0]
    img = Image.open(urllib.request.urlopen(imagen_seleccionada))
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.img = img
    plt.show()



razas = sorted(datos['raza'].astype(str).unique())

raza_seleccionada = tk.StringVar(ventana)
raza_seleccionada.set(razas[0]) 


combobox = tk.OptionMenu(ventana, raza_seleccionada, *razas)
combobox.pack()

boton = tk.Button(ventana, text='Ver distribucion', command=lambda: graficar(raza_seleccionada.get()))
boton.pack()

tk.mainloop()
