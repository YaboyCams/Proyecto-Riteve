# Proyecto 3: ReTeVe
#? Autores: Camilo José Allón Quesada (2022259515) y Víctor Esteban Azfeifa Portuguez (2023113603)
# Fecha de creación 30/5/23

#!============================================================== Módulos ==========================================================================================================
import os
import pickle
from validate_email import validate_email
import datetime
# GUI
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#?============================================================= Programa ====================================================================================================
registros = open("numeroscitas.dat", "rb")
datos = pickle.load(registros)
registros.close() # No sé si esto es necesario

reteve_principal = Tk()
num_cita = datos[0]

elegida = IntVar()
elegida.set(0)

vehiculos = ["Automovil particular y caraga liviana (menor o igual a 3500 kg)", "Automovil particular y de carga liviana (mayor a 3500 kg pero menor a 8000 kg)", "Vehículo de carga pesada y cabezales (mayor o igual a 8000 kg)", "Taxi", "Autobús, bus o microbús", "Motocicleta", "Equipo especial de obras", "Equipo especial agrícola (maquinaria agrícola)"]


#?============================================================= Secundarias ===================================================================================================
#! Verifcar que solo hayan números
def solo_numeros(evento):
    texto = evento.widget.get()
    if texto.isdigit() == False:
        evento.widget.delete(0, END)
        
#?============================================================= Programar citas =========================================================================================================
def programar_cita():
    p_citas = Toplevel()
    p_citas.title("Programar Cita")
    p_citas.state('zoomed')
    listbox = Listbox(p_citas)
    num_placa = StringVar() 
    tipo_revision = IntVar()
    tipo_vehiculo = Listbox()
    
    #*========================================================= FUNCIONES AUXILIARES ==============================================================================================================
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
                
        
    #! Activar boton guardar
    def activar_guardar():
        if tipo_revision.get() != 0 and placa.get() and marca.get()  and modelo.get() and propietario.get() and telefono.get() != "" and direccion.get() and elegida.get() != 0 and listbox_vehiculo.curselection():
            boton_guardar_cita.config(state = NORMAL)
        else:
            boton_guardar_cita.config(state = DISABLED)
            
    #! Hacer que la ventana se mueva con la rueda del mouse
    def scroll(evento):
        canvas.yview_scroll(int(-1 * (evento.delta / 120)), "units")
        
    #*============================================================== PROGRAMA ==================================================================================================================================================== 
        
    #todo Prueba del scrollbar
    main_frame = Frame(p_citas)
    main_frame.pack(fill = BOTH, expand = 1)
   
    canvas = Canvas(main_frame)
    canvas.pack(side = LEFT, fill = BOTH, expand = 1)
        
    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.bind("<Configure>", lambda e: canvas.config(scrollregion = canvas.bbox("all")))
    scrollbar.bind_all("<MouseWheel>", scroll)

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

    

    #? Check box
    frame_tipo = Frame(citas_frame)
    frame_tipo.pack(side = TOP, anchor = W)
    tipo_lab = Label(frame_tipo, text= 'Elija su tipo de cita:', font = ("Times New Roman", 13, "bold"))
    tipo_lab.pack(side = LEFT, anchor = W, padx = 10)

    p_rev = Checkbutton(frame_tipo, text = "Primera vez", variable = tipo_revision, onvalue = 1, offvalue = 0, height = 5,width = 20,command=valor, font = ("Times New Roman", 13))
    p_rev.pack(side = LEFT, padx = 57)
    reins = Checkbutton(frame_tipo, text = "Reinspección", variable = tipo_revision, onvalue = 2, offvalue = 0, height = 5, width = 20,command=valor, font = ("Times New Roman", 13))
    reins.pack(side = LEFT)

    #? Placa 
    
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
    
#?============================================================= Configuración =========================================================================================================
def configuracion():
    configuracion = Toplevel()
    configuracion.title("Configuración")
    configuracion.state("zoomed")
    #*======================================================== FUNCIONES AUXILIARES =====================================================================================================================
    #! Acutalizar contenido del combo box del final del horario
    def actualizar_opciones(evento):
        seleccionada = combo_horas1.current()
        if seleccionada:
            opciones = combo_horas1["values"][seleccionada + 1:]
            combo_horas2["values"] = opciones
        else:
            combo_horas2["values"] = []
    
    #! Verficar que minutos de revisón estén entre los parámetros
    def tiempo_revision(evento):
        min  = mins_revision.get()
        if not min.isdigit() or not int(min) <= 45:
            evento.widget.delete(0, END)
    
    #! Verificar que dias para reinspeccion cumplan los parámetros 
    def dias_reinspeccion(evento):
        dias = max_dias.get()
        if not dias.isdigit() or not int(dias) <= 60:
            evento.widget.delete(0, END)
    
    #! Verificar si el IVA está entre los parámetros
    def iva_permitido(evento):
        porcentaje = percent_iva.get()
        try:
            porcentaje = float(porcentaje)
            if porcentaje > 20.0:
                evento.widget.delete(0, END)
        except ValueError:
            evento.widget.delete(0, END)
    
    #! Guardar configuración         
    def guardar_config():
        if num_lineas.get() and combo_horas1.get() and combo_horas2.get() and mins_revision.get() and max_dias.get() and num_fallas.get() and percent_iva.get() and entry1.get() and entry2.get and entry3.get() and entry4.get() and entry5.get() and entry6.get() and entry7.get() and entry8.get():
            datos = [lineas.get(), combo_horas1.get(), combo_horas2.get(), dias_rev.get(), fallas_max.get(), iva.get(), [var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]]            
            ajustes = open("configuracion_riteve.dat", "wb")
            pickle.dump(datos, ajustes)
            ajustes.close()
            configuracion.destroy()
            
            
    
    #*======================================================== PROGRAMA PRINCIPAL ===============================================================================================================
        
    titulo_config = Label(configuracion, text = "Configuración", font = ("Times New Roman", 20, "bold"))
    titulo_config.pack(side = TOP, anchor = CENTER)
     
    #? Cantidad de líneas de trabajo
    tit_lineas = Label(configuracion, text = "Cantidad de líneas de trabajo en la estación:", font = ("Times New Roman", 13, "bold"))
    tit_lineas.place(x = 10, y = 50)
    
    lineas = IntVar()
    lineas.set(6)
    num_lineas = Entry(configuracion, textvariable = lineas, font = ("Times New Roman", 13), width = 2)
    num_lineas.place(x = 500, y = 50)
    
    #? Horario
    tit_horario = Label(configuracion, text = "Horario de la estación:", font = ("Times New Roman", 13, "bold"))
    tit_horario.place(x = 10, y = 90)
    
    #* Inicio
    tit_inicio = Label(configuracion, text = "Hora inicial: ", font = ("Times New Roman", 13))
    tit_inicio.place(x = 30, y = 110)
    
    horas_disponibles = []
    contador = 0
    
    while contador != 2:
        if contador == 0:
            horas_disponibles.append("12:00 AM")
        else:
            horas_disponibles.append("12:00 PM")
        for i in range(1,12):
            if contador == 0:
                horas_disponibles.append(str(i) + ":00 AM")
            else:
                horas_disponibles.append(str(i) + ":00 PM")
        contador += 1
            
    combo_horas1 = ttk.Combobox(configuracion, values = horas_disponibles)
    combo_horas1.place(x = 500, y = 110)
    combo_horas1.bind("<<ComboboxSelected>>", actualizar_opciones)
    
    combo_horas1.set("6:00 AM")
    
    #* Final 
    tit_final = Label(configuracion, text = "Hora final: ", font = ("Times New Roman", 13))
    tit_final.place(x = 30, y = 140)
    
    combo_horas2 = ttk.Combobox(configuracion)
    combo_horas2.place(x= 500, y = 140)
    combo_horas2.set("9:00 PM")
    
    #? Minutos por cita
    tit_min = Label(configuracion, text = "Minutos por cita de revisión:", font = ("Times New Roman", 13, "bold"))
    tit_min.place(x = 10, y = 170)
    
    minutos = IntVar()
    minutos.set(25)
    mins_revision = Entry(configuracion, textvariable = minutos, width = 2, font = ("Times New Roman", 13))
    mins_revision.bind("<KeyRelease>", tiempo_revision)
    mins_revision.place(x = 500, y = 170)
    
    
    #? Cantidad máxima de días para reinspección
    tit_dias = Label(configuracion, text = "Cantidad máxima de días para reinspección:", font = ("Times New Roman", 13, "bold"))
    tit_dias.place(x = 10, y = 210)
    
    dias_rev = IntVar()
    dias_rev.set(30)
    max_dias = Entry(configuracion, textvariable = dias_rev, width = 2, font = ("Times New Roman", 13))
    max_dias.bind("<KeyRelease>", dias_reinspeccion)
    max_dias.place(x = 500, y = 210)
    
    #? Cantidad de fallas para sacar vehículo de circulación
    tit_fallas = Label(configuracion, text = "Cantidad de fallas graves para sacar de circulación:", font = ("Times New Roman", 13, "bold"))
    tit_fallas.place(x = 10, y = 250)
    
    fallas_max = IntVar()
    fallas_max.set(4)
    num_fallas = Entry(configuracion, width = 2, textvariable = fallas_max, font = ("Times New Roman", 13))
    num_fallas.bind("<KeyRelease>", solo_numeros)
    num_fallas.place(x = 500, y = 250)
        
    #? IVA
    tit_iva = Label(configuracion, text = "Porcentaje de IVA sobre tarifa:", font = ("Times New Roman", 13, "bold"))
    tit_iva.place(x = 10, y = 290)
    
    iva = DoubleVar()
    iva.set(13.0)
    percent_iva = Entry(configuracion, font = ("Times New Roman", 13), textvariable = iva, width = 5)
    percent_iva.bind("<KeyRelease>", iva_permitido)
    percent_iva.place(x = 500, y = 290)
    
    #? Tabla de tarifas (solo columna derecha es alterable)
    tit_tarifas = Label(configuracion, text = "Tabla de tarifas:", font = ("Times New Roman", 13, "bold"))
    tit_tarifas.place(x = 10, y = 330)
    
    # Tabla
    canvas_tarifa = Canvas(configuracion, width = 800, height = 9 * 50)
    canvas_tarifa.place(y = 360)
    
    
    ancho1 = 600
    ancho2 = 120
    altura = 35
    
    for fila in range(9):
        # Primera columna
        x1 = 0
        y1 = fila * altura
        x2 = x1 + ancho1
        y2 = y1 + altura
        canvas_tarifa.create_rectangle(x1,y1,x2,y2, outline = "black")
        
        # Segunda columna
        x1 = ancho1
        x2 = x1 + ancho2
        canvas_tarifa.create_rectangle(x1,y1,x2,y2, outline = "black")
        
    # Tipos de vehículo y sus precios
    tit_vehiculo = Label(configuracion, text = "Vehiculo", font = ("Times New Roman", 13, "bold"))
    tit_vehiculo.place(x = 250, y = 365)
    tit_tarifa = Label(configuracion, text = "Tarifa", font = ("Times New Roman", 13, "bold"))
    tit_tarifa.place(x = 630, y = 365)
    
    # Primero vehículo
    label1 = Label(configuracion, text = f"{vehiculos[0]}", font = ("Times New Roman", 13))
    label1.place(x = 10, y = 400)
    
    var1 = IntVar()
    var1.set(10920)
    entry1 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var1)
    entry1.place(x = 625, y = 400)
    entry1.bind("<KeyRelease>", solo_numeros)
    
    # Segundo vehículo
    label2 = Label(configuracion, text = f"{vehiculos[1]}", font = ("Times New Roman", 13))
    label2.place(x = 10, y = 435)
    
    var2 = IntVar()
    var2.set(14380)
    entry2 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var2)
    entry2.place(x = 625, y = 435)
    entry2.bind("<KeyRelease>", solo_numeros)
    
    
    # Tercer vehículo
    label3 = Label(configuracion, text = f"{vehiculos[2]}", font = ("Times New Roman", 13))
    label3.place(x = 10, y = 470)
    
    var3 = IntVar()
    var3.set(14380)
    entry3 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var3)
    entry3.place(x = 625, y = 470)
    entry3.bind("<KeyRelease>", solo_numeros)
    
    # Cuarto vehículo 
    label4 = Label(configuracion, text = f"{vehiculos[3]}", font = ("Times New Roman", 13))
    label4.place(x = 10, y = 505)
    
    var4 = IntVar()
    var4.set(11785)
    entry4 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var4)
    entry4.place(x = 625, y = 505)
    entry4.bind("<KeyRelease>", solo_numeros)
    
    # Quinto vehículo
    label5 = Label(configuracion, text = f"{vehiculos[4]}", font = ("Times New Roman", 13))
    label5.place(x = 10, y = 540)
    
    var5 = IntVar()
    var5.set(14380)
    entry5 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var5)
    entry5.place(x = 625, y = 540)
    entry5.bind("<KeyRelease>", solo_numeros)
    
    # Sexto vehículo
    label6 = Label(configuracion, text = f"{vehiculos[5]}", font = ("Times New Roman", 13))
    label6.place(x = 10, y = 575)
    
    var6 = IntVar()
    var6.set(7195)
    entry6 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var6)
    entry6.place(x = 625, y = 575)
    entry6.bind("<KeyRelease>", solo_numeros)
    
    
    # Setimo vehículo
    label7 = Label(configuracion, text = f"{vehiculos[6]}", font = ("Times New Roman", 13))
    label7.place(x = 10, y = 610)
    
    var7 = IntVar()
    var7.set(14380)
    entry7 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var7)
    entry7.place(x = 625, y = 610)
    entry7.bind("<KeyRelease>", solo_numeros)
    
    # Octavo vehículo
    label8 = Label(configuracion, text = f"{vehiculos[7]}", font = ("Times New Roman", 13))
    label8.place(x = 10, y = 645)
    
    var8 = IntVar()
    var8.set(6625)
    entry8 = Entry(configuracion, width = 8, font = ("Times New Roman", 13), textvariable = var8)
    entry8.place(x = 625, y = 645) 
    entry8.bind("<KeyRelease>", solo_numeros)

    y = 400
    for i in vehiculos:
        colon = Label(configuracion, text = "₡", font = ("Times New Roman", 13))
        colon.place(x = 610, y = y)
        y += 35
        
    #? Guardar configuracion
    btn_guardado = Button(configuracion, text = "Aplicar", font = ("Times New Roman", 13), width = 7, bg = "light green", command = guardar_config)
    btn_guardado.place(x = 900, y = 645)
    

    configuracion.mainloop()


#?============================================================= Menú Principal ===================================================================================================


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

Configuracion = Button(reteve_principal, text = "Configuración", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3, command = configuracion)
Configuracion.place(x = 20, y = 400)

Ayuda = Button(reteve_principal,text='Ayuda',font=('Times New Roman', 10),bg = "snow",width = 16, height = 3)
Ayuda.place(x = 20, y = 460)

Acerca_de = Button(reteve_principal,text='Acerca de',font=('Times New Roman', 10),bg = "snow",width = 16, height = 3)
Acerca_de.place(x = 20, y = 520)

Salir = Button(reteve_principal,text='Salir',font=('Times New Roman', 10),bg = "snow",width = 16, height = 3, command = reteve_principal.destroy)
Salir.place(x = 20, y = 580)
reteve_principal.mainloop()
