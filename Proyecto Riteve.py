# Proyecto 3: ReTeVe
#? Autores: Camilo José Allón Quesada (2022259515) y Víctor Esteban Azfeifa Portuguez (2023113603)
# Fecha de creación 30/5/23

#!============================================================== Módulos ==========================================================================================================
import os
import pickle
from validate_email import validate_email

# GUI
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#?============================================================= Programa ====================================================================================================
registros = open("numeroscitas.dat", "rb")
datos = pickle.load(registros)

reteve_principal = Tk()
num_cita = datos[0]

elegida = IntVar()
elegida.set(0)

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
    
    #? FUNCIONES AUXILIARES
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
    
    #! Validacion de correo
    #! Envío de correo 
    
    #! Despliegue de frames
    def habilitar_deshabilitar_frame():
        if elegida.get() == 2:
            frame_scrollbar.pack(side = TOP, anchor = W, padx = 10)  # Mostrar el frame scrollabar
            frame_manual.pack_forget() # Ocultar frame manual
            citas_frame.update_idletasks() # Esto de acá ajusta la página cuando se despliegan cada uno de los frames
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            frame_scrollbar.pack_forget()  # Ocultar el frame scrollbar
            frame_manual.pack(side = TOP, anchor = W, padx = 10) # Mostrar frame manual
            citas_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            
    #! Verifcar que solo hayan números
    def solo_numeros(evento):
        texto = evento.widget.get()
        if texto.isdigit() == False or len(texto) > 2:
            evento.widget.delete(0, END)    
        
    #! Activar boton guardar
    def activar_guardar():
        if tipo_revision.get() != 0 and placa.get() and marca.get()  and modelo.get() and propietario.get() and telefono.get() != "" and direccion.get() and elegida.get() != 0 and listbox_vehiculo.curselection():
            boton_guardar_cita.config(state = NORMAL)
        else:
            boton_guardar_cita.config(state = DISABLED)
        
    #? PROGRAMA 
        
    #todo Prueba del scrollbar
    main_frame = Frame(p_citas)
    main_frame.pack(fill = BOTH, expand = 1)
   
    canvas = Canvas(main_frame)
    canvas.pack(side = LEFT, fill = BOTH, expand = 1)
        
    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.bind("<Configure>", lambda e: canvas.config(scrollregion = canvas.bbox("all")))

    citas_frame = Frame(canvas)
    canvas.create_window((0,0), window = citas_frame, anchor = "nw")

    # TODO cambio grande: reacomodé todo para que quepa

    #!Label titulo
    frame_tit = Frame(citas_frame)
    frame_tit.pack(side = TOP, anchor = W)
    config_cita = Label(frame_tit, relief = 'solid',  text ='Programe su cita', font=('Times New Roman', 20), width = 15)
    config_cita.pack(side = LEFT, padx = 5, pady = 5)
    
    #!Label numero de cita
    frame_num = Frame(citas_frame)
    frame_num.pack(padx = 10, pady = 20, side = TOP, anchor = W)
    tit_cita = Label(frame_num, text = "Número de cita:", font = ("Times New Roman", 13, "bold"))
    tit_cita.pack(side = LEFT)
    cita = Label(frame_num, text = str(num_cita), font = ("Times New Roman", 13, "bold"),fg='blue')
    cita.pack(side = LEFT, padx = 150)

    

    #? Check box y su label
    frame_tipo = Frame(citas_frame)
    frame_tipo.pack(side = TOP, anchor = W)
    tipo_lab = Label(frame_tipo, text= 'Elija su tipo de cita:', font = ("Times New Roman", 13, "bold"))
    tipo_lab.pack(side = LEFT, anchor = W, padx = 10)

    p_rev = Checkbutton(frame_tipo, text = "Primera vez", variable = tipo_revision, onvalue = 1, offvalue = 0, height = 5,width = 20,command=valor, font = ("Times New Roman", 13))
    p_rev.pack(side = LEFT, padx = 57)
    reins = Checkbutton(frame_tipo, text = "Reinspección", variable = tipo_revision, onvalue = 2, offvalue = 0, height = 5, width = 20,command=valor, font = ("Times New Roman", 13))
    reins.pack(side = LEFT)

    #? Placa y tit
    
    frame_placa  =Frame(citas_frame)
    frame_placa.pack(side = TOP, anchor = W, pady = 20)
    tit_placa = Label(frame_placa, text = 'Número de placa:', font = ("Times New Roman", 13, "bold"))
    tit_placa.pack(side = LEFT, padx = 10)
    placa = Entry(frame_placa,font=('Times New Roman', 13), width = 8,textvariable = num_placa)
    placa.pack(side = LEFT, padx = 130)
    
    #todo lo que tenga bind es un cambio
    placa.bind("<KeyRelease>", long_placa)
    
    #? Tipo Vehiculo titulo
    #Todo saqué el listbox del frame ya que no es necesario y ayuda a acomodarlo mejor
    frame_vehiculo = Frame(citas_frame)
    frame_vehiculo.pack(side =TOP, anchor = W, padx = 10, pady = 20)
    tit_tcarro = Label(frame_vehiculo, text= 'Tipo de Vehiculo:', font = ("Times New Roman", 13, "bold"))
    tit_tcarro.pack(side = LEFT)
    
    #TODO Lista de posibles vehículos y lugar en la lista
    vehiculos = ["Automovil particular y caraga liviana (menor o igual a 3500 kg)", "Automovil particular y de carga liviana (mayor a 3500 kg pero menor a 8000 kg)", "Vehículo de carga pesada y cabezales (mayor o igual a 8000 kg)", "Taxi", "Autobús, bus o microbús", "Motocicleta", "Equipo especial de obras", "Equipo especial agrícola (maquinaria agrícola)"]
    elemento = 1
    
    listbox_vehiculo = Listbox(frame_vehiculo, height = 2, width = 62, font = ("Times New Roman", 13))
    for vehiculo in vehiculos:
        listbox_vehiculo.insert(elemento, vehiculo)
        elemento += 1
    listbox_vehiculo.pack(side = LEFT, padx = 137)
    
    #TODO poner nota para que el usuario se mueva con las flechas en el listbox
    
    #TODO de acá en adelante son cosas que añado extra
    #? Marca del vehículo
    frame_marca = Frame(citas_frame)
    frame_marca.pack(side = TOP, anchor = W, padx = 10, pady = 20)
    tit_marca = Label(frame_marca, text = "Marca del vehículo:", font = ("Times New Roman", 13, "bold"))
    tit_marca.pack(side = LEFT)
    
    marca = Entry(frame_marca, font = ("Times New Roman", 13), width = 15)
    marca.pack(side = LEFT, padx = 120)
    
    marca.bind("<KeyRelease>", long_marca)
        
    #? Modelo
    frame_modelo = Frame(citas_frame)
    frame_modelo.pack(side =TOP, anchor =W, padx = 10, pady =20)
    tit_modelo = Label(frame_modelo, text = "Modelo del vehículo:", font = ("Times New Roman", 13, "bold"))
    tit_modelo.pack(side = LEFT)
    
    modelo = Entry(frame_modelo, font = ("Times New Roman", 13), width = 15)
    modelo.pack(side =LEFT, padx =110)
    
    modelo.bind("<KeyRelease>", long_modelo)
    
    #? Propietario
    frame_prop =Frame(citas_frame)
    frame_prop.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_prop = Label(frame_prop, font = ("Times New Roman", 13, "bold"), text = "Nombre del propietario:")
    tit_prop.pack(side = LEFT)
    
    propietario = Entry(frame_prop, font = ("Times New Roman", 13), width = 40)
    propietario.pack(side = LEFT, padx = 83)
    
    propietario.bind("<KeyRelease>", long_prop)

    #? Teléfono
    frame_tele = Frame(citas_frame)
    frame_tele.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_telefono = Label(frame_tele, text = "Número de teléfono:", font = ("Times New Roman", 13, "bold"))
    tit_telefono.pack(side = LEFT)
    
    telefono = Entry(frame_tele, font = ("Times New Roman", 13), width = 20)
    telefono.pack(side =LEFT, padx = 115)
    
    telefono.bind("<KeyRelease>", long_telefono)
    
    #? Correo
    frame_correo =Frame(citas_frame)
    frame_correo.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_correo = Label(frame_correo, text = "Correo electrónico:", font = ("Times New Roman", 13, "bold"))
    tit_correo.pack(side = LEFT)
    
    correo = Entry(frame_correo, font = ("Times New Roman", 13), width = 40)
    correo.pack(side =LEFT, padx = 115)
    
    #? Direccion
    frame_dir =Frame(citas_frame)
    frame_dir.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_direccion = Label(frame_dir, text = "Dirección física:", font = ("Times New Roman", 13, "bold"))
    tit_direccion.pack(side = LEFT)
    
    direccion = Entry(frame_dir, font = ("Times New Roman", 13), width = 40)
    direccion.pack(side = LEFT, padx = 140)
    
    direccion.bind("<KeyRelease>", long_direc)
    
    #? Fecha y hora
    frame_fyh =Frame(citas_frame)
    frame_fyh.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_fecha = Label(frame_fyh, text = "Elección de fecha y hora:", font = ("Times New Roman", 13, "bold"))
    tit_fecha.pack(side =LEFT)
    
    manual = Radiobutton(frame_fyh, text = "Manual", font = ("Times New Roman", 13), value = 1, variable = elegida, command = habilitar_deshabilitar_frame)
    manual.pack(side =LEFT, padx = 75)
    
    automatico = Radiobutton(frame_fyh, text = "Automático", font = ("Times New Roman", 13), value  = 2, variable = elegida, command = habilitar_deshabilitar_frame)
    automatico.pack(side = LEFT, padx  =40)
    
    #? Botnes de guardado y de salida
    frame_botones = Frame(citas_frame)
    frame_botones.pack(side = BOTTOM, anchor = CENTER, pady = 10)
    
    boton_aplicar = Button(frame_botones, text = "Aplicar", width = 13, font = ("Times New Roman", 13), bg = "yellow", command = activar_guardar)
    boton_aplicar.pack(side = LEFT)
    
    boton_guardar_cita = Button(frame_botones,text = "Guardar cita", font = ("Times New Roman", 13), width = 13, bg = "light green", state = DISABLED)
    boton_guardar_cita.pack(side = LEFT, padx =  20)
    
    
    #! Fechas manuales
    frame_manual = Frame(citas_frame)
    
    tit_manual = Label(frame_manual, text = "Introduzca fecha y hora:", font = ("Times New Roman", 13, "bold"))
    tit_manual.pack()
    
    #* Activar cuando se haga la configración
    """nota = Label(frame_manual, text = f"La citas están dispobles cada {configuracion[-1]} minutos desde las {configuracion[]} hasta las {configuracion[]}", font = ("Times New Roman", 13))
    nota.pack(side = LEFT)"""
    
    # Frame de fecha
    frame_fecha = Frame(frame_manual)
    frame_fecha.pack(side = TOP, anchor = W)
    
    tit_dia = Label(frame_fecha, text = "Fecha:", font = ("Times New Roman", 13, "bold"))
    tit_dia.pack(side = LEFT)
    
    dia = Entry(frame_fecha, font = ("Times New Roman", 13), width = 2)
    dia.pack(side = LEFT, padx = 5)
    dia.bind("<KeyRelease>", solo_numeros)
    
    slash = Label(frame_fecha, text = "/", font = ("Times New Roman", 13))
    slash.pack(side = LEFT)
    
    mes = Entry(frame_fecha, font = ("Times New Roman", 13), width = 2)
    mes.pack(side = LEFT, padx = 5)
    mes.bind("<KeyRelease>", solo_numeros)
    
    
    # Frame de hora
    frame_hora = Frame(frame_manual)
    frame_hora.pack(side = TOP, anchor = W, pady = 5)
    
    tit_hora = Label(frame_hora, text = "Hora:", font = ("Times New Roman", 13, "bold"))
    tit_hora.pack(side = LEFT)
    
    hora = Entry(frame_hora, font = ("Times New Roman", 13), width = 2)
    hora.pack(side = LEFT, padx = 5)
    hora.bind("<KeyRelease>", solo_numeros)
    
    dos_puntos = Label(frame_hora, text = ":", font = ("Times New Roman", 13))
    dos_puntos.pack(side = LEFT, padx = 5)
    
    mins = Entry(frame_hora, font = ("Times New Roman", 13), width = 2)
    mins.pack(side = LEFT, padx = 5)
    mins.bind("<KeyRelease>", solo_numeros)


    #! Scroll bar (automático)
    # Crear un Frame para contener el Listbox y el Scrollbar
    frame_scrollbar = Frame(citas_frame)
    
    # Label
    tit_automatico = Label(frame_scrollbar, text = "Fechas disponibles:", font = ("Times New Roman", 13, "bold"))
    tit_automatico.pack()

    # Crear el Listbox dentro del Frame
    listbox = Listbox(frame_scrollbar)
    listbox.pack(side=LEFT, fill=BOTH)

    # Crear el Scrollbar y asociarlo al Listbox
    scrollbar = Scrollbar(frame_scrollbar, orient=VERTICAL, command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.config(yscrollcommand=scrollbar.set)

    # Agregar elementos al Listbox
    for i in range(100):
        listbox.insert(END, f"Elemento {i}")
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
