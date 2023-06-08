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

elegida = IntVar()

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

    # TODO cambio grande: reacomodé todo para que quepa

    #!Label titulo
    config_cita = Label(p_citas, relief = 'solid',  text ='Programe su cita', font=('Times New Roman', 20), width = 15)
    config_cita.place(x=10,y=10)
    
    #!Label numero de cita
    tit_cita = Label(p_citas, text = "Número de cita:", font = ("Times New Roman", 13, "bold"))
    tit_cita.place(x = 10, y = 80)
    cita = Label(p_citas, text = str(num_cita), font = ("Times New Roman", 13, "bold"),fg='blue')
    cita.place(x = 250, y = 80)

    #>! PRUEBA
    def valor():
        print(tipo_revision.get())
        
    #! RESTRICCIONES Y VALIDACIONES DE DATOS
    def long_placa(evento):
        entry_placa = placa.get()
        if len(entry_placa) > 8:
            placa_valida = entry_placa[:8]
            placa.delete(0, END)
            placa.insert(0, placa_valida)
    
    def long_marca(evento):
        entry_marca = marca.get()
        if len(entry_marca) > 15:
            marca_valida = entry_marca[:15]
            marca.delete(0, END)
            marca.insert(0, marca_valida)
            
    def long_modelo(evento):
        entry_modelo = modelo.get()
        if len(entry_modelo) > 15:
            modelo_valido = entry_modelo[:15]
            modelo.delete(0, END)
            modelo.insert(0, modelo_valido)
            
    def long_prop(evento):
        entry_propietario = propietario.get()
        if len(entry_propietario) > 40:
            prop_valida = entry_propietario[:40]
            propietario.delete(0, END)
            propietario.insert(0, prop_valida)
            
    def long_telefono(evento):
        entry_telefono = telefono.get()
        if len(entry_telefono) > 20:
            telefono_valida = entry_telefono[:20]
            telefono.delete(0, END)
            telefono.insert(0, telefono_valida)
            
    def long_direc(evento):
        entry_direccion = direccion.get()
        if len(entry_direccion) > 40:
            direccion_valida = entry_direccion[:40]
            direccion.delete(0, END)
            direccion.insert(0, direccion_valida)

    #? Check box y su label
    tipo_lab = Label(p_citas, text= 'Elija su tipo de cita:', font = ("Times New Roman", 13, "bold"))
    tipo_lab.place(x = 10, y = 130)

    p_rev = Checkbutton(p_citas, text = "Primera vez", variable = tipo_revision, onvalue = 1, offvalue = 0, height=5,width = 20,command=valor, font = ("Times New Roman", 13))
    p_rev.place(x = 280, y = 90)
    reins = Checkbutton(p_citas, text = "Reinspección", variable = tipo_revision, onvalue = 2, offvalue = 0, height=5, width = 20,command=valor, font = ("Times New Roman", 13))
    reins.place(x = 440, y = 90)

    #? Placa y tit
    tit_placa = Label(p_citas, text = 'Número de placa:', font = ("Times New Roman", 13, "bold"))
    tit_placa.place(x = 10, y = 180)
    placa = Entry(p_citas,font=('Times New Roman', 13), width = 8,textvariable = num_placa)
    placa.place(x = 250, y = 180)
    
    #todo lo que tenga bind es un cambio
    placa.bind("<KeyRelease>", long_placa)
    
    #? Tipo Vehiculo titulo
    #Todo saqué el listbox del frame ya que no es necesario y ayuda a acomodarlo mejor
    tit_tcarro = Label(p_citas, text= 'Tipo de Vehiculo:', font = ("Times New Roman", 13, "bold"))
    tit_tcarro.place(x = 10, y = 230)
    
    #TODO Lista de posibles vehículos y lugar en la lista
    vehiculos = ["Automovil particular y caraga liviana (menor o igual a 3500 kg)", "Automovil particular y de carga liviana (mayor a 3500 kg pero menor a 8000 kg)", "Vehículo de carga pesada y cabezales (mayor o igual a 8000 kg)", "Taxi", "Autobús, bus o microbús", "Motocicleta", "Equipo especial de obras", "Equipo especial agrícola (maquinaria agrícola)"]
    elemento = 1
    
    listbox_vehiculo = Listbox(p_citas, height = 2, width = 62, font = ("Times New Roman", 13))
    for vehiculo in vehiculos:
        listbox_vehiculo.insert(elemento, vehiculo)
        elemento += 1
    listbox_vehiculo.place(x = 250, y = 230)
    
    #TODO poner nota para que el usuario se mueva con las flechas en el listbox
    
    #TODO de acá en adelante son cosas que añado extra
    #? Marca del vehículo
    tit_marca = Label(p_citas, text = "Marca del vehículo:", font = ("Times New Roman", 13, "bold"))
    tit_marca.place(x = 10, y = 300)
    
    marca = Entry(p_citas, font = ("Times New Roman", 13), width = 15)
    marca.place(x = 250, y = 300)
    
    marca.bind("<KeyRelease>", long_marca)
        
    #? Modelo
    tit_modelo = Label(p_citas, text = "Modelo del vehículo:", font = ("Times New Roman", 13, "bold"))
    tit_modelo.place(x = 10, y = 350)
    
    modelo = Entry(p_citas, font = ("Times New Roman", 13), width = 15)
    modelo.place(x = 250, y = 350)
    
    modelo.bind("<KeyRelease>", long_modelo)
    
    #? Propietario
    tit_prop = Label(p_citas, font = ("Times New Roman", 13, "bold"), text = "Nombre del propietario:")
    tit_prop.place(x = 10, y = 400)
    
    propietario = Entry(p_citas, font = ("Times New Roman", 13), width = 40)
    propietario.place(x = 250, y = 400)
    
    propietario.bind("<KeyRelease>", long_prop)

    #? Teléfono
    tit_telefono = Label(p_citas, text = "Número de teléfono:", font = ("Times New Roman", 13, "bold"))
    tit_telefono.place(x = 10, y = 450)
    
    telefono = Entry(p_citas, font = ("Times New Roman", 13), width = 20)
    telefono.place(x = 250, y = 450)
    
    telefono.bind("<KeyRelease>", long_telefono)
    
    #? Correo
    tit_correo = Label(p_citas, text = "Correo electrónico:", font = ("Times New Roman", 13, "bold"))
    tit_correo.place(x = 10, y = 500)
    
    correo = Entry(p_citas, font = ("Times New Roman", 13), width = 40)
    correo.place(x = 250, y = 500)
    
    #? Direccion
    tit_direccion = Label(p_citas, text = "Dirección física:", font = ("Times New Roman", 13, "bold"))
    tit_direccion.place(x = 10, y = 550)
    
    direccion = Entry(p_citas, font = ("Times New Roman", 13), width = 40)
    direccion.place(x = 250, y = 550)
    
    direccion.bind("<KeyRelease>", long_direc)
    
    #? Fecha y hora
    tit_fecha = Label(p_citas, text = "Elección de fecha y hora:", font = ("Times New Roman", 13, "bold"))
    tit_fecha.place(x = 10, y = 600)
    
    manual = Radiobutton(p_citas, text = "Manual", font = ("Times New Roman", 13), value = 1, variable = elegida)
    manual.place(x = 250, y = 600)
    
    automatico = Radiobutton(p_citas, text = "Automático", font = ("Times New Roman", 13), value  = 2, variable = elegida)
    automatico.place(x = 350, y = 600)
    
    #? Botnes de guardado y de salida
    boton_guardar_cita = Button(p_citas,text = "Guardar cita", font = ("Times New Roman", 13), width = 13, bg = "light green")
    boton_guardar_cita.place(x = 625, y= 650)

    """#! Scroll bar 
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
        listbox.insert(END, f"Elemento {i}")"""
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
