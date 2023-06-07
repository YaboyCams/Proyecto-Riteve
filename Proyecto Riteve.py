# Proyecto 3: ReTeVe
#? Autores: Camilo José Allón Quesada (2022259515) y Víctor Esteban Azfeifa Portuguez (2023113603)
# Fecha de creación 30/5/23

#!============================================================== Módulos ==========================================================================================================
import os
import pickle

# GUI
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#?============================================================= Programa ====================================================================================================
registros = open("numeroscitas.dat", "rb")
datos = pickle.load(registros)

reteve_principal = Tk()
cita = StringVar()
num_cita = datos[0]

#?============================================================= Secundarias ===================================================================================================
def programar_cita():
    p_citas = Toplevel()
    p_citas.geometry('1080x850')
    p_citas.title("Programar Cita")
    p_citas.state('zoomed')
    listbox = Listbox(p_citas)
    num_placa = StringVar() 
    tipo_revision = IntVar()
    tipo_vehiculo = Listbox()

    # Deshabilita el scroll bar por medio de recorrido de widgets
    def deshabilitar_frame(frame_scrollbar):
        for child in frame_scrollbar.winfo_children():
            child.configure(state="disabled")

<<<<<<< HEAD

=======
    # TODO cambio grande: reacomodé todo para que quepa
>>>>>>> 1eb4ae5 (Versión 1.1)

    #!Label titulo
    config_cita = Label(p_citas, relief = 'solid',  text ='Programe su cita', font=('Times New Roman', 32), width = 15)
    config_cita.place(x=10,y=10)
    
    #!Label numero de cita
<<<<<<< HEAD
    etiqueta1 = Label(p_citas, text = "Número de cita:", font = ("Times New Roman", 13, "bold"))
    etiqueta1.place(x = 10, y = 80)
    cita = Label(p_citas, text = str(num_cita + 1 ), font = ("Times New Roman", 13, "bold"),fg='blue')
=======
    etiqueta1 = Label(p_citas, text = "Número de cita", font = ("Times New Roman", 13, "bold"))
    etiqueta1.place(x = 10, y = 80)
    cita = Label(p_citas, text = str(num_cita), font = ("Times New Roman", 13, "bold"),fg='blue')
>>>>>>> 1eb4ae5 (Versión 1.1)
    cita.place(x = 150, y = 80)

    #>! PRUEBA
    def valor():
        print(tipo_revision.get())

    #? Check box y su label
    tipo_lab = Label(p_citas, text= 'Elija su tipo de cita', font = ("Times New Roman", 13, "bold"))
    tipo_lab.place(x = 10, y = 140)

<<<<<<< HEAD
    p_rev = Checkbutton(p_citas, text = "Primera vez", variable = tipo_revision, onvalue = 1, offvalue = 0, height=5,width = 20,command=valor)
    p_rev.place(x = 10, y = 160)
    reins = Checkbutton(p_citas, text = "Reinspección", variable = tipo_revision, onvalue = 2, offvalue = 0, height=5, width = 20,command=valor)
    reins.place(x = 140, y = 160)

    #? Placa y tit
    tit_placa = Label(p_citas, text= 'Ingrese su numero de placa', font = ("Times New Roman", 13, "bold"))
    tit_placa.place(x = 10, y = 240)
    placa = Entry(p_citas,font=('Times New Roman', 18), width = 35,textvariable=num_placa)
    placa.place(x = 10, y = 260)
    
    #? Tipo Vehiculo titulo
    tit_tcarro = Label(p_citas, text= 'Tipo de Vehiculo', font = ("Times New Roman", 13, "bold"))
    tit_tcarro.place(x = 10, y = 300)
    frame_vehiculo = Frame(p_citas)
    frame_vehiculo.place(x = 10, y = 340, width=100, height=50)
    vehiculos_list = StringVar()
    vehiculos_list.set(["Vehiculo Especial","Vehiculo Ligero","Vehiculo Pesado"])
    listbox_vehiculo = Listbox(frame_vehiculo,listvariable=vehiculos_list)
    listbox_vehiculo.pack()

    #? Marca de Vehiculo

    #! Scroll bar 
=======
    p_rev = Checkbutton(p_citas, text = "Primera vez", variable = tipo_revision, onvalue = 1, offvalue = 0, height=5,width = 20,command=valor, font = ("Times New Roman", 13))
    p_rev.place(x = 160, y = 100)
    reins = Checkbutton(p_citas, text = "Reinspección", variable = tipo_revision, onvalue = 2, offvalue = 0, height=5, width = 20,command=valor, font = ("Times New Roman", 13))
    reins.place(x = 320, y = 100)

    #? Placa y tit
    tit_placa = Label(p_citas, text = 'Número de placa', font = ("Times New Roman", 13, "bold"))
    tit_placa.place(x = 10, y = 200)
    placa = Entry(p_citas,font=('Times New Roman', 13), width = 35,textvariable = num_placa)
    placa.place(x = 160, y = 200)
    
    #? Tipo Vehiculo titulo
    #Todo saqué el listbox del frame ya que no es necesario y ayuda a acomodarlo mejor
    tit_tcarro = Label(p_citas, text= 'Tipo de Vehiculo', font = ("Times New Roman", 13, "bold"))
    tit_tcarro.place(x = 10, y = 260)
    
    #TODO Lista de posibles vehículos y lugar en la lista
    vehiculos = ["Automovil particular y caraga liviana (menor o igual a 3500 kg)", "Automovil particular y de carga liviana (mayor a 3500 kg pero menor a 8000 kg)", "Vehículo de carga pesada y cabezales (mayor o igual a 8000 kg)", "Taxi", "Autobús, bus o microbús", "Motocicleta", "Equipo especial de obras", "Equipo especial agrícola (maquinaria agrícola)"]
    elemento = 1
    
    listbox_vehiculo = Listbox(p_citas, height = 2, width = 62, font = ("Times New Roman", 13))
    for vehiculo in vehiculos:
        listbox_vehiculo.insert(elemento, vehiculo)
        elemento += 1
    listbox_vehiculo.place(x = 150, y = 260)
    
    #TODO poner nota para que el usuario se mueva con las flechas en el listbox
    
    #TODO de acá en adelante son cosas que añado extra
    #? Marca del vehículo
    #? Modelo 
    #? Propietario
    #? Teléfono
    #? Correo
    #? Direccion
    #? Fecha y hora


    """#! Scroll bar 
>>>>>>> 1eb4ae5 (Versión 1.1)
    # Crear un Frame para contener el Listbox y el Scrollbar
    frame_scrollbar = Frame(p_citas)
    frame_scrollbar.place(x = 750, y = 50, width=250, height=400)

    # Crear el Listbox dentro del Frame
    listbox = Listbox(frame_scrollbar)
    listbox.pack(side=LEFT, fill=BOTH)

    # Crear el Scrollbar y asociarlo al Listbox
    scrollbar = Scrollbar(frame_scrollbar, orient=VERTICAL, command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.config(yscrollcommand=scrollbar.set)

    # Agregar elementos al Listbox
    for i in range(100):
<<<<<<< HEAD
        listbox.insert(END, f"Elemento {i}")
=======
        listbox.insert(END, f"Elemento {i}")"""
>>>>>>> 1eb4ae5 (Versión 1.1)
    p_citas.mainloop()
#?============================================================= Menu Principal ===================================================================================================


reteve_principal.geometry('500x640')
reteve_principal.title('MENU PRINCIPAL')

#! IMAGEN 'Riteve_Nit.png'

img = PhotoImage(file='Riteve_Nit.png')
fondo_menu = Label(reteve_principal, image = img)
fondo_menu.place(x=0, y=100, relwidth=1)

titulo_riteve = Label(master = reteve_principal, relief = 'solid',  text ='RETEVE', font=('Times New Roman', 32), width = 9)
titulo_riteve.place(x=170,y=30)

Progra_citas = Button(reteve_principal, text = "Programar citas", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3, command = lambda: programar_cita())
Progra_citas.place(x=20,y=100)

Cancel_citas = Button(reteve_principal, text = "Cancelar citas", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3)
Cancel_citas.place(x=20,y=160)

Ingreso = Button(reteve_principal, text = "Ingreso de vehículos", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3)
Ingreso.place(x=20,y=220)

Revision = Button(reteve_principal, text = "Tablero de revisión", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3)
Revision.place(x = 20, y = 280)

Lista_fallas = Button(reteve_principal, text = "Lista de fallas", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3)
Lista_fallas.place(x = 20, y = 340)

Configuracion = Button(reteve_principal, text = "Configuración", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3)
Configuracion.place(x = 20, y = 400)

Ayuda = Button(reteve_principal,text='Ayuda',font=('Times New Roman', 10),bg = "snow",width = 16, height = 3)
Ayuda.place(x = 20, y = 460)

Acerca_de = Button(reteve_principal,text='Acerca de',font=('Times New Roman', 10),bg = "snow",width = 16, height = 3)
Acerca_de.place(x = 20, y = 520)

Salir = Button(reteve_principal,text='Salir',font=('Times New Roman', 10),bg = "snow",width = 16, height = 3, command = reteve_principal.destroy)
Salir.place(x = 20, y = 580)
reteve_principal.mainloop()
