# Proyecto 3: ReTeVe
#? Autores: Camilo José Allón Quesada (2022259515) y Víctor Esteban Azfeifa Portuguez (2023113603)
# Fecha de creación 30/5/23

#!============================================================== Módulos ==========================================================================================================
import os
import pickle
from datetime import datetime
from datetime import timedelta

# Creación propia
from arbol import Nodo
from arbol import Arbol

# GUI
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Correos
from validate_email import validate_email
import ssl
import smtplib 
from email.message import EmailMessage
import re
import smtplib
import logging  
import socket 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
#?============================================================= Programa ====================================================================================================
registros = open("numeroscitas.dat", "rb")
datos = pickle.load(registros)
registros.close() 

#* Cración del árbol binario
arbol_binario = Arbol()
reteve_principal = Tk()

#* Variables globales
global num_cita

global colas_espera
global cola_revision
global historial_citas

global copy

num_cita = datos[0]
historial_citas = datos[1]

for c in historial_citas:
    arbol_binario.agregar(c)
print(historial_citas)
elegida = IntVar()
elegida.set(0)


lf = open('Lista_Fallas.dat','rb')
Diccionario_Fallas = pickle.load(lf)
lf.close()
print(Diccionario_Fallas)
tablero = []

vehiculos = ["Automovil particular y caraga liviana (menor o igual a 3500 kg)", "Automovil particular y de carga liviana (mayor a 3500 kg pero menor a 8000 kg)", "Vehículo de carga pesada y cabezales (mayor o igual a 8000 kg)", "Taxi", "Autobús, bus o microbús", "Motocicleta", "Equipo especial de obras", "Equipo especial agrícola (maquinaria agrícola)"]

#TODO ======================== CAMBIO DE PRUEBA DEVOLVER A [] ==========================
colas_espera = []
#colas_espera = [['ABC123','DEF456'],['GHI789','JKL321'],['MNO654','PQR987'],['STU543','VWX876'],['YZA219','BCD654'],['789GHI','CJS002']]
#TODO ======================== CAMBIO ==========================
cola_revision = {}
copy = []
#TODO ======================== CAMBIO ==========================



#?============================================================= Secundarias ===================================================================================================
#! Verifcar que solo hayan números
def solo_numeros(evento):
    texto = evento.widget.get()
    if texto.isdigit() == False:
        evento.widget.delete(0, END)

#! Validación de correo
def validar_correo(correo):
    isExists = validate_email(correo, verify=True)
    return isExists
def isvalidEmail(email):
    pattern = "^\S+@\S+\.\S+$"
    objs = re.search(pattern, email)
    try:
        if objs.string == email:
            return True
    except:
        return False
    
#! Enviar correo    
def envio_correo(destino,caso,persona,dia, hora):
    email_sender = "emailpython723@gmail.com"
    email_receiver = destino
    email_smtp = "smtp.gmail.com" 
    email_password = "kmhddfxnpxmaylbx"
    asunto = ""
    mensaje = ""
    if caso == "Cita":
        mensaje += "Hola, "+ str(persona) + ". Este es su correo de confirmación de Revisión Técnica Vehícular" + " el día " + dia + " a las " + hora
        asunto += 'Confirmación de cita'
    if caso == "APROBADA":
        mensaje += "Hola, " + str(persona) + ". El siguiente correo es para notificarle los resultados de su Revisión Técnica Vehícular"
        asunto += 'Reusltados Revicion Técnica Vehícular: ' + str(persona)
    if caso == "REINSPECCIÓN":
        mensaje += "Hola, " + str(persona) + ". El siguiente correo es para notificarle los resultados de su Revisión Técnica Vehícular y la necesidad de REINSPECCION"
        asunto += 'Resultados Revicion Técnica Vehícular: ' + str(persona)
    if caso == "SACAR DE CIRCULACIÓN":
        mensaje += "Hola, " + str(persona) + ". El siguiente correo es para notificarle los resultados de su Revisión Técnica Vehícular y que su vehículo debera ser SACADO DE CIRCULACION"
        asunto += 'Reusltados Revicion Técnica Vehícular: ' + str(persona)
    subject = asunto
    body = mensaje
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    #! Envia resultados y Certificado
    if caso == "APROBADA":
        #TODO NOMBRE GENERICO
        with open("Aprobado.pdf","rb") as f:
            file_data = f.read()
            em.add_attachment(file_data, maintype="aplication",subtype="pdf",filename="Aprobado.pdf")
        with open("Certificado.pdf","rb") as f:
            file_data = f.read()
            em.add_attachment(file_data, maintype="aplication",subtype="pdf",filename="Certificado.pdf")
    #! Solo envia resultados
    if caso == "REINSPECCIÓN":
        with open("Reinspección.pdf","rb") as f:
            file_data = f.read()
            em.add_attachment(file_data, maintype="aplication",subtype="pdf",filename="Reinspección.pdf")
    if caso == "SACAR DE CIRCULACION":
        with open("Reprobado.pdf","rb") as f:
            file_data = f.read()
            em.add_attachment(file_data, maintype="aplication",subtype="pdf",filename="Reprobado.pdf")
    if caso == "Cita":
        pass
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
#! Creación de resultados.pdf
def resultados_pdf(estado, cita, graves, leves):
    
    if estado ==  "APROBADA":
        resultados = canvas.Canvas(f"Aprobado.pdf", pagesize = letter)
        resultados.drawString(200,742, "Revisión Técnica: Resultados")
        # Datos
        y = 712
        resultados.drawString(50, y, f"Datos de la cita:")
        y -= 30
        resultados.drawString(80, y, f"- Cita # {cita[1]}")
        y -= 30
        resultados.drawString(80, y, f"- Tipo de cita: {cita[2]}")
        y -= 30
        resultados.drawString(80, y, f"- Número de placa: {cita[4]}")
        y -= 30
        resultados.drawString(80, y, f"- Tipo de vehículo: {cita[3]}")
        y -= 30
        resultados.drawString(80, y, f"- Marca del vehículo: {cita[5]}")
        y -= 30
        resultados.drawString(80, y, f"- Modelo del vehículo: {cita[6]}")
        y -= 30
        resultados.drawString(80, y, f"- Propietario: {cita[7]}")
        y -= 30
        resultados.drawString(80, y, f"- Teléfono: {cita[8]}")
        y -= 30
        resultados.drawString(80, y, f"- Correo electrónico: {cita[9]}")
        y -= 30
        resultados.drawString(80, y, f"- Dirección: {cita[10]}")
        y -= 30
        resultados.drawString(80, y, f"- Fecha y hora de la cita: {cita[0]}")
        y -= 30
        resultados.drawString(80, y, f"- Estado: {cita[11]}")
        resultados.showPage()
        
        # Resultados de la cita
        y = 712
        resultados.drawString(50, y, "Registro de fallas:")
        y -= 30
        if len(graves) != 0:
            resultados.drawString(80, y, "Fallas graves:")
            y -= 30
            for falla in graves:
                resultados.drawString(100, y, f"- {falla}")
                y-= 30
        else:
            resultados.drawString(80, y, "Fallas graves: No hay")
            y -= 30
            
        if len(leves) != 0:
            resultados.drawString(80, y, "Fallas leves:")
            y -= 30
            for falla in leves:
                resultados.drawString(100, y, f"- {falla}")
                y-= 30
        else:
            resultados.drawString(80, y, "Fallas leves: No hay")
            y -= 30
            
        resultados.drawString(50, y, "Veredicto Final:")
        y -= 30
        resultados.drawString(80, y, "¡Felicitaciones! Su vehículo ha aprobado la revisón.")
        y -= 15
        resultados.drawString(80, y, "En el correo se le adjuntará un certificado de tránsito.")
        y -= 30
        resultados.drawString(80, y, "Nos vemos el próximo año. Tenga un buen día.")
            
        resultados.save()
    
    # Reinspección    
    if estado == "REINSPECCIÓN":
        resultados = canvas.Canvas(f"Reinspección.pdf", pagesize = letter)
        resultados.drawString(200,742, "Revisión Técnica: Resultados")
        # Datos
        y = 712
        resultados.drawString(50, y, f"Datos de la cita:")
        y -= 30
        resultados.drawString(80, y, f"- Cita # {cita[1]}")
        y -= 30
        resultados.drawString(80, y, f"- Tipo de cita: {cita[2]}")
        y -= 30
        resultados.drawString(80, y, f"- Número de placa: {cita[4]}")
        y -= 30
        resultados.drawString(80, y, f"- Tipo de vehículo: {cita[3]}")
        y -= 30
        resultados.drawString(80, y, f"- Marca del vehículo: {cita[5]}")
        y -= 30
        resultados.drawString(80, y, f"- Modelo del vehículo: {cita[6]}")
        y -= 30
        resultados.drawString(80, y, f"- Propietario: {cita[7]}")
        y -= 30
        resultados.drawString(80, y, f"- Teléfono: {cita[8]}")
        y -= 30
        resultados.drawString(80, y, f"- Correo electrónico: {cita[9]}")
        y -= 30
        resultados.drawString(80, y, f"- Dirección: {cita[10]}")
        y -= 30
        resultados.drawString(80, y, f"- Fecha y hora de la cita: {cita[0]}")
        y -= 30
        resultados.drawString(80, y, f"- Estado: {cita[11]}")
        resultados.showPage()
        
        # Resultados de la cita
        y = 712
        resultados.drawString(50, y, "Registro de fallas:")
        y -= 30
        if len(graves) != 0:
            resultados.drawString(80, y, "Fallas graves:")
            y -= 30
            for falla in graves:
                resultados.drawString(100, y, f"- {falla}")
                y-= 30
        else:
            resultados.drawString(80, y, "Fallas graves: No hay")
            y -= 30
            
        if len(leves) != 0:
            resultados.drawString(80, y, "Fallas leves:")
            y -= 30
            for falla in leves:
                resultados.drawString(100, y, f"- {falla}")
                y-= 30
        else:
            resultados.drawString(80, y, "Fallas leves: No hay")
            y -= 30
            
        resultados.drawString(50, y, "Veredicto Final:")
        y -= 30
        resultados.drawString(80, y, "Su vehículo no ha pasado la revisón, tiene que hacerle una reinspección.")
        y -= 15
        resultados.drawString(80, y, f"Para pasar su vehículo no debe tener fallas graves, su vehículo tiene {len(graves)}.")
        y -= 30
        resultados.drawString(80, y, "Tenga un buen día.")
            
        resultados.save()
    
    # Sacar de circulación    
    if estado == "SACAR DE CIRCULACIÓN":
        resultados = canvas.Canvas(f"Reprobado.pdf", pagesize = letter)
        resultados.drawString(200,742, "Revisión Técnica: Resultados")
        # Datos
        y = 712
        resultados.drawString(50, y, f"Datos de la cita:")
        y -= 30
        resultados.drawString(80, y, f"- Cita # {cita[1]}")
        y -= 30
        resultados.drawString(80, y, f"- Tipo de cita: {cita[2]}")
        y -= 30
        resultados.drawString(80, y, f"- Número de placa: {cita[4]}")
        y -= 30
        resultados.drawString(80, y, f"- Tipo de vehículo: {cita[3]}")
        y -= 30
        resultados.drawString(80, y, f"- Marca del vehículo: {cita[5]}")
        y -= 30
        resultados.drawString(80, y, f"- Modelo del vehículo: {cita[6]}")
        y -= 30
        resultados.drawString(80, y, f"- Propietario: {cita[7]}")
        y -= 30
        resultados.drawString(80, y, f"- Teléfono: {cita[8]}")
        y -= 30
        resultados.drawString(80, y, f"- Correo electrónico: {cita[9]}")
        y -= 30
        resultados.drawString(80, y, f"- Dirección: {cita[10]}")
        y -= 30
        resultados.drawString(80, y, f"- Fecha y hora de la cita: {cita[0]}")
        y -= 30
        resultados.drawString(80, y, f"- Estado: {cita[11]}")
        resultados.showPage()
        
        # Resultados de la cita
        y = 712
        resultados.drawString(50, y, "Registro de fallas:")
        y -= 30
        if len(graves) != 0:
            resultados.drawString(80, y, "Fallas graves:")
            y -= 30
            for falla in graves:
                resultados.drawString(100, y, f"- {falla}")
                y-= 30
        else:
            resultados.drawString(80, y, "Fallas graves: No hay")
            y -= 30
            
        if len(leves) != 0:
            resultados.drawString(80, y, "Fallas leves:")
            y -= 30
            for falla in leves:
                resultados.drawString(100, y, f"- {falla}")
                y-= 30
        else:
            resultados.drawString(80, y, "Fallas leves: No hay")
            y -= 30
            
        resultados.drawString(50, y, "Veredicto Final:")
        y -= 30
        resultados.drawString(80, y, "Su vehículo no ha pasado la revisón, debe ser sacado de circulación.")
        y -= 15
        resultados.drawString(80, y, f"Su vehículo ha excedido el número de fallas graves máximas.")
        y -= 30
        resultados.drawString(80, y, "Tenga un buen día.")
            
        resultados.save()

#! Creación del certificado    
def certificado_pdf(cita):
    fecha_inicio = cita[0]
    fecha_final = fecha_inicio + timedelta(days = 365)
    
    fecha1_formato = datetime.strftime(fecha_inicio, "%d/%m/%Y")
    fecha2_formato = datetime.strftime(fecha_final, "%d/%m/%Y")
    certificado = canvas.Canvas(f"Certificado.pdf", pagesize = letter)
    certificado.drawString(200, 450, "Certificado de Tránsito")
    
    felicitacion = certificado.beginText(80, 400)
    felicitacion.textLines(f"Se le entrega este certificado a {cita[7]}, dueño del vehículo de placa {cita[4]},\n un {cita[3]} \ny marca {cita[5]}. Este certificado es válido desde {fecha1_formato} hasta el {fecha2_formato}.")
    certificado.drawText(felicitacion)
    certificado.drawString(80, 350,"¡Felicitaciones! Nos veremos el próximo año.")
    certificado.save()
        
        
#?============================================================= Programar citas =========================================================================================================
def programar_cita():
    p_citas = Toplevel()
    p_citas.title("Programar Cita")
    p_citas.state('zoomed')
    
    #! Variables tipo Var
    tipo_revision = IntVar()
    num_placa = StringVar() 
    marca_v = StringVar()
    modelo_v = StringVar()
    usuario = StringVar()
    telefono_u = StringVar()
    correo_u = StringVar()
    direccion_u = StringVar()
        
    #* Frame manual
    mes_elegido = StringVar()
    dia_elegido = StringVar()
    hora_elegido = StringVar()
    min_elegido = StringVar()

    
    #?Configuración
    ajustes = open("configuracion_riteve.dat", "rb")
    config = pickle.load(ajustes)
    ajustes.close()
    
    num_filas = config[0]
    hora_inicio = config[1]
    hora_fin = config[2]
    duracion_cita = config[3]
    
    
    #TODO encontrar la citas de el día actual dentro de un mes
    #? Fecha actual
    fecha_actual = datetime.now()
    con_formato = datetime.strftime(fecha_actual, "%d/%m/%Y  %H:%M:%S")

    anno_actual = fecha_actual.year 
    dia_actual = fecha_actual.day
    mes_actual = fecha_actual.month 
    hora_actual = fecha_actual.hour
    minutos_actual = fecha_actual.minute
    hora_siguiente = hora_actual + 1
    
    if hora_siguiente == 24:
        hora_siguiente = 0

    fecha_uso = datetime(anno_actual, mes_actual, dia_actual, hora_siguiente, 0)

    mes_siguiente = mes_actual + 1
    anno_siguiente = anno_actual

    # En caso de fin de año
    if mes_siguiente == 13:
        mes_siguiente = 1
        anno_siguiente = anno_actual + 1
        
    fecha_limite = datetime(anno_siguiente, mes_siguiente, dia_actual, hora_actual, minutos_actual)
    diferencia = timedelta(minutes = duracion_cita)
    diferencia_provisional = timedelta(minutes = 1)
    citas_disponibles = []
    #! Lista de fechas disponibles
    while fecha_uso < fecha_limite:
        if fecha_uso.hour >= hora_inicio and fecha_uso.hour < hora_fin:
            citas_disponibles.append(fecha_uso)
            fecha_uso += diferencia
        else:
            fecha_uso += diferencia_provisional
            
    # Límite de personas a la misma hora
    for f in citas_disponibles:
        contador = 0
        for c in historial_citas:
            if c[0] == f:
                contador += 1
            if contador == num_filas:
                citas_disponibles.remove(f)
                
    #*========================================================= FUNCIONES AUXILIARES ==============================================================================================================
       
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
        if entry_telefono.isdigit() == False:
            telefono.delete(0, END)
            
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
            mes.delete(0, END)
            dia.delete(0, END)
            hora.delete(0, END)
            mins.delete(0, END)
            frame_scrollbar.pack(side = TOP, anchor = W, padx = 10)  # Mostrar el frame scrollabar
            frame_manual.pack_forget() # Ocultar frame manual
            citas_frame.update_idletasks() # Esto de acá ajusta la página cuando se despliegan cada uno de los frames
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            listbox.selection_clear(0, END)
            frame_scrollbar.pack_forget()  # Ocultar el frame scrollbar
            frame_manual.pack(side = TOP, anchor = W, padx = 10) # Mostrar frame manual
            citas_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
                
        
    #! Activar boton guardar
    def activar_guardar():
        # Definir la variables globales
        global datos_cita
        global formateada_hora
        global formateada_dia
        global fecha_prueba
        if tipo_revision.get() != 0 and placa.get() and marca.get()  and modelo.get() and propietario.get() and telefono.get() != "" and direccion.get() and elegida.get() != 0 and listbox_vehiculo.curselection():
            # PONER OTRAS VALIDACIONES
            if len(marca.get()) < 3:
                messagebox.showerror("", "Marca no válida. Vuelva a intentar.")
                return
            if len(propietario.get()) < 6:
                messagebox.showerror("", "Nombre del propietario no válido. Vuelva a intentar.")
                return
            if len(direccion.get()) < 10:
                messagebox.showerror("", "Dirección no válida. Vuelva a intentar.")
                return
            if len(telefono.get()) < 8:
                messagebox.showerror("", "Teléfono no válido. Vuelva a intentar.")
                return
            if validar_correo(correo.get()) is not True:
                messagebox.showerror("", "Correo no válido. Vuelva a intentar.")
                return
            for c in historial_citas:
                if c[4] == num_placa.get() and tipo_revision.get() == 1 and c[-1] == "REINSPECCIÓN":
                    messagebox.showerror("", "Marque la opción reinspección para continuar.")
                    return
                if c[4] == num_placa.get() and c[-1] == "SACAR DE CIRCULACIÓN":
                    messagebox.showerror("", "Su vehículo debe sacarse de circulación.")
                    return
                if c[4] == num_placa.get() and tipo_revision.get() == 2 and c[-1] != "REINSPECCIÓN":
                    messagebox.showerror("", "Este vehículo todavía no fue autorizado para reinspección.")
                    return
                if c[4] == num_placa.get() and tipo_revision.get() == 1 and c[-1] == "PENDIENTE":
                    messagebox.showerror("", "Placa ya está registrada.")
                    return
            if tipo_revision.get() == 1:
                tipo = "Primera vez"
            else:
                tipo = "Reinspección"
            # Sacar el tipo de vehículo (nombre)
            seleccionados = listbox_vehiculo.curselection()
            vehiculo_elegido = listbox_vehiculo.get(seleccionados[0])
            if elegida.get() == 1: 
                if mes.get() and dia.get() and hora.get() and mins.get():
                    try:
                        fecha_prueba = datetime(anno_actual, int(mes.get()), int(dia.get()), int(hora.get()), int(mins.get()), 0)
                    except ValueError:
                        messagebox.showerror("", "Fecha u hora no existe.")
                        return
                    
                    if fecha_prueba not in citas_disponibles:
                        messagebox.showerror("", "Fecha u hora de cita solicitada inválidas.")
                        return
                    formateada_dia = fecha_prueba.strftime("%d/%m/%Y")
                    formateada_hora = fecha_prueba.strftime("%H:%M:%S")
                    datos_cita = [fecha_prueba, num_cita, tipo, vehiculo_elegido, num_placa.get(), marca_v.get(), modelo_v.get(), usuario.get(), telefono_u.get(), correo_u.get(), direccion_u.get(), "PENDIENTE"]
                    boton_guardar_cita.config(state = NORMAL)
                    print(datos_cita)
            elif listbox.curselection(): 
                hora_seleccionada = listbox.curselection()
                indice = hora_seleccionada[0]
                fecha_prueba = citas_disponibles[indice] 
                formateada_dia = datetime.strftime(fecha_prueba, "%d/%m/%Y") # Esto es para el correo
                formateada_hora = datetime.strftime(fecha_prueba, "%H:%M:%S")
                datos_cita = [fecha_prueba, num_cita, tipo, vehiculo_elegido, num_placa.get(), marca_v.get(), modelo_v.get(), usuario.get(), telefono_u.get(), correo_u.get(), direccion_u.get(), "PENDIENTE"]
                print(datos_cita)
            for c in historial_citas:
                if tipo_revision.get() == 2 and datos_cita[4] == c[4] and c[-1] == "REINSPECCIÓN":
                    primera_fecha = c[0]
                    if fecha_prueba <= primera_fecha:
                        messagebox.showerror("", "Fecha de reinspección debe ser después de la cita de revisión pasada.")
                        return
                    break
            boton_guardar_cita.config(state = NORMAL)
        else:
            boton_guardar_cita.config(state = DISABLED)
            
    def guardar_citas():
        global num_cita
        arbol_binario.agregar(datos_cita)
        # Abrir archivo 
        citas = open("registro_de_citas.dat", "wb")
        arbol_binario.guardar_datos(citas) 
        citas.close()
        historial_citas.append(datos_cita)
        print(historial_citas) 
        registro_num = open("numeroscitas.dat", "wb")
        pickle.dump([num_cita + 1, historial_citas], registro_num)
        registro_num.close()
        # envío de correo
        envio_correo(correo.get(),"Cita",propietario.get(), formateada_dia, formateada_hora) #* Cambiar esto
        
        # Preguntar si se quiere hacer otra cita
        if messagebox.askyesno("", "¿Desea agregar otra cita?") == True:
            p_citas.destroy()
            num_cita += 1
            programar_cita()
        else:
            num_cita += 1
            p_citas.destroy()
            
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
    #! Indicar fecha 
    actual = Label(citas_frame, font = ("Times New Roman", 13, "bold"), text = f"Hora actual: {con_formato}")
    actual.pack(side = TOP, anchor = E)
    
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

    p_rev = Checkbutton(frame_tipo, text = "Primera vez", variable = tipo_revision, onvalue = 1, offvalue = 0, height = 5,width = 20,font = ("Times New Roman", 13))
    p_rev.pack(side = LEFT, padx = 57)
    reins = Checkbutton(frame_tipo, text = "Reinspección", variable = tipo_revision, onvalue = 2, offvalue = 0, height = 5, width = 20,font = ("Times New Roman", 13))
    reins.pack(side = LEFT)

    #? Placa 
    
    frame_placa  =Frame(citas_frame)
    frame_placa.pack(side = TOP, anchor = W, pady = 20)
    tit_placa = Label(frame_placa, text = 'Número de placa:', font = ("Times New Roman", 13, "bold"))
    tit_placa.pack(side = LEFT, padx = 10)
    placa = Entry(frame_placa,font=('Times New Roman', 13), width = 8, textvariable = num_placa)
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
    
    listbox_vehiculo = Listbox(frame_vehiculo, height = 2, width = 62, font = ("Times New Roman", 13), exportselection = False)
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
    
    marca = Entry(frame_marca, font = ("Times New Roman", 13), width = 15, textvariable = marca_v)
    marca.pack(side = LEFT, padx = 120)
    
    marca.bind("<KeyRelease>", long_marca)
        
    #? Modelo
    frame_modelo = Frame(citas_frame)
    frame_modelo.pack(side =TOP, anchor =W, padx = 10, pady =20)
    tit_modelo = Label(frame_modelo, text = "Modelo del vehículo:", font = ("Times New Roman", 13, "bold"))
    tit_modelo.pack(side = LEFT)
    
    modelo = Entry(frame_modelo, font = ("Times New Roman", 13), width = 15, textvariable = modelo_v)
    modelo.pack(side =LEFT, padx =110)
    
    modelo.bind("<KeyRelease>", long_modelo)
    
    #? Propietario
    frame_prop =Frame(citas_frame)
    frame_prop.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_prop = Label(frame_prop, font = ("Times New Roman", 13, "bold"), text = "Nombre del propietario:")
    tit_prop.pack(side = LEFT)
    
    propietario = Entry(frame_prop, font = ("Times New Roman", 13), width = 40, textvariable = usuario)
    propietario.pack(side = LEFT, padx = 83)
    
    propietario.bind("<KeyRelease>", long_prop)

    #? Teléfono
    frame_tele = Frame(citas_frame)
    frame_tele.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_telefono = Label(frame_tele, text = "Número de teléfono:", font = ("Times New Roman", 13, "bold"))
    tit_telefono.pack(side = LEFT)
    
    telefono = Entry(frame_tele, font = ("Times New Roman", 13), width = 20, textvariable = telefono_u)
    telefono.pack(side =LEFT, padx = 115)
    
    telefono.bind("<KeyRelease>", long_telefono)
    
    #? Correo
    frame_correo =Frame(citas_frame)
    frame_correo.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_correo = Label(frame_correo, text = "Correo electrónico:", font = ("Times New Roman", 13, "bold"))
    tit_correo.pack(side = LEFT)
    
    correo = Entry(frame_correo, font = ("Times New Roman", 13), width = 40, textvariable = correo_u)
    correo.pack(side =LEFT, padx = 115)
    
    #? Direccion
    frame_dir =Frame(citas_frame)
    frame_dir.pack(side =TOP, anchor =W, padx = 10, pady = 20)
    tit_direccion = Label(frame_dir, text = "Dirección física:", font = ("Times New Roman", 13, "bold"))
    tit_direccion.pack(side = LEFT)
    
    direccion = Entry(frame_dir, font = ("Times New Roman", 13), width = 40, textvariable = direccion_u)
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
    
    elegida.set(None) # Esto es para que cuando se cierre prgrmar citas no se quede seleccionado uno de los radiobuttons
    #? Botnes de guardado y de salida
    frame_botones = Frame(citas_frame)
    frame_botones.pack(side = BOTTOM, anchor = CENTER, pady = 10)
    
    boton_aplicar = Button(frame_botones, text = "Aplicar", width = 13, font = ("Times New Roman", 13), bg = "yellow", command = activar_guardar)
    boton_aplicar.pack(side = LEFT)
    
    boton_guardar_cita = Button(frame_botones,text = "Guardar", font = ("Times New Roman", 13), width = 13, bg = "light green", state = DISABLED, command = guardar_citas)
    boton_guardar_cita.pack(side = LEFT, padx =  20)
    
    
    #! Fechas manuales
    frame_manual = Frame(citas_frame)
    
    tit_manual = Label(frame_manual, text = "Introduzca fecha y hora:", font = ("Times New Roman", 13, "bold"))
    tit_manual.pack()
    
    # Frame de fecha
    frame_fecha = Frame(frame_manual)
    frame_fecha.pack(side = TOP, anchor = W)
    
    tit_dia = Label(frame_fecha, text = "Fecha:", font = ("Times New Roman", 13, "bold"))
    tit_dia.pack(side = LEFT)
    
    dia = Entry(frame_fecha, font = ("Times New Roman", 13), width = 2, textvariable = dia_elegido)
    dia.pack(side = LEFT, padx = 5)
    dia.bind("<KeyRelease>", solo_numeros)
    
    slash = Label(frame_fecha, text = "/", font = ("Times New Roman", 13))
    slash.pack(side = LEFT)
    
    mes = Entry(frame_fecha, font = ("Times New Roman", 13), width = 2, textvariable = mes_elegido)
    mes.pack(side = LEFT, padx = 5)
    mes.bind("<KeyRelease>", solo_numeros)
    
    
    # Frame de hora
    frame_hora = Frame(frame_manual)
    frame_hora.pack(side = TOP, anchor = W, pady = 5)
    
    tit_hora = Label(frame_hora, text = "Hora:", font = ("Times New Roman", 13, "bold"))
    tit_hora.pack(side = LEFT)
    
    hora = Entry(frame_hora, font = ("Times New Roman", 13), width = 2, textvariable = hora_elegido)
    hora.pack(side = LEFT, padx = 5)
    hora.bind("<KeyRelease>", solo_numeros)
    
    dos_puntos = Label(frame_hora, text = ":", font = ("Times New Roman", 13))
    dos_puntos.pack(side = LEFT, padx = 5)
    
    mins = Entry(frame_hora, font = ("Times New Roman", 13), width = 2, textvariable = min_elegido)
    mins.pack(side = LEFT, padx = 5)
    mins.bind("<KeyRelease>", solo_numeros)


    #! Scroll bar (automático)
    # Crear un Frame para contener el Listbox y el Scrollbar
    frame_scrollbar = Frame(citas_frame)
    
    # Label
    tit_automatico = Label(frame_scrollbar, text = "Fechas disponibles:", font = ("Times New Roman", 13, "bold"))
    tit_automatico.pack()

    # Crear el Listbox dentro del Frame
    listbox = Listbox(frame_scrollbar, exportselection = False, font = ("Times New Roman", 13))
    listbox.pack(side=LEFT, fill=BOTH)

    # Crear el Scrollbar y asociarlo al Listbox
    scrollbar = Scrollbar(frame_scrollbar, orient=VERTICAL, command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.config(yscrollcommand=scrollbar.set)

    # Agregar elementos al Listbox
    for i in citas_disponibles:
        listbox.insert(END, f"{i}")
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
            horafin_correcta = combo_horas2.current() + combo_horas1.current() + 1
            datos = [lineas.get(), combo_horas1.current(), horafin_correcta, minutos.get(), dias_rev.get(), fallas_max.get(), iva.get(), [var1.get(), var2.get(), var3.get(), var4.get(), var5.get(), var6.get(), var7.get(), var8.get()]]
            
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
    
    # combo_horas1.set("6:00 AM")
    
    #* Final 
    tit_final = Label(configuracion, text = "Hora final: ", font = ("Times New Roman", 13))
    tit_final.place(x = 30, y = 140)
    
    combo_horas2 = ttk.Combobox(configuracion)
    combo_horas2.place(x= 500, y = 140)
    # combo_horas2.set("9:00 PM")
    
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

#!============================================================= CRUD =============================================================================================================
def lista_de_fallas():
    fallas_ventana = Toplevel()
    fallas_ventana.title("Lista de Fallas")
    fallas_ventana.state('zoomed')
    codigo = StringVar()
    falla = IntVar()
    crud = IntVar()
    crud.set(0)
    def sacar_texto():
        texto = descripcion.get("1.0", "end-1c")
        if len(texto.strip()) >= 5 and len(texto.strip()) <= 200:
            return texto.strip()
        else:
            return False
    def largo_codigo(evento):
        entry_modelo = codigo.get()
        try:
            entry_modelo = int(entry_modelo)
            if len(str(entry_modelo)) > 5:
                modelo_valido = str(entry_modelo)[:5]
                pedir_codigo.delete(0, END)
                pedir_codigo.insert(0, modelo_valido)
        except ValueError:
            modelo_valido = ''
            pedir_codigo.delete(0, END)
            pedir_codigo.insert(0, modelo_valido)
    def activar_create():
        pedir_codigo.configure(state="normal")
        descripcion.configure(state="normal")
        radio_lleve.configure(state="normal")
        radio_grave.configure(state="normal")
        btn_realizar.configure(state="normal")

        #RESET
        btn_realizar.place_forget()
        guardar_cambio.place_forget()
        pedir_codigo.delete(0, END)
        descripcion.delete("1.0", "end")
        radio_lleve.deselect()
        radio_grave.deselect()

        btn_realizar.place(x=500, y=650)
        btn_realizar.configure(text="Añadir Falla")
    def activar_consultar():
        pedir_codigo.configure(state="normal")
        descripcion.configure(state="normal")
        descripcion.delete("1.0", "end")
        descripcion.configure(state="disabled")
        radio_lleve.configure(state="disabled")
        radio_grave.configure(state="disabled")
        btn_realizar.configure(state="normal")

        #RESET
        btn_realizar.place_forget()
        guardar_cambio.place_forget()
        pedir_codigo.delete(0, END)
        descripcion.delete("1.0", "end")
        radio_lleve.deselect()
        radio_grave.deselect()

        btn_realizar.place(x=500, y=650)
        btn_realizar.configure(text="Consultar Falla")
    def activar_modificar():
        pedir_codigo.configure(state="normal")
        descripcion.configure(state="normal")
        descripcion.delete("1.0", "end")
        descripcion.configure(state="disabled")
        radio_lleve.configure(state="disabled")
        radio_grave.configure(state="disabled")
        btn_realizar.configure(state="normal")

        #RESET
        btn_realizar.place_forget()
        guardar_cambio.place_forget()
        pedir_codigo.delete(0, END)
        descripcion.delete("1.0", "end")
        radio_lleve.deselect()
        radio_grave.deselect()

        btn_realizar.place(x=500, y=650)
        btn_realizar.configure(text="BUSCAR FALLA")
        guardar_cambio.place(x=500, y=750)
    def activar_eliminar():
        pedir_codigo.configure(state="normal")
        descripcion.configure(state="normal")
        descripcion.delete("1.0", "end")
        descripcion.configure(state="disabled")
        radio_lleve.configure(state="disabled")
        radio_grave.configure(state="disabled")
        btn_realizar.configure(state="normal")

        #RESET
        btn_realizar.place_forget()
        guardar_cambio.place_forget()
        pedir_codigo.delete(0, END)
        descripcion.delete("1.0", "end")
        radio_lleve.deselect()
        radio_grave.deselect()

        btn_realizar.place(x=500, y=650)
        btn_realizar.configure(text="ELIMINAR FALLA")

    #ADD
    def añadir_elemento():
        if codigo.get() != "0" and codigo.get() != "":
            validacion = sacar_texto()
            if validacion !=  False:
                print(falla.get())
                if falla.get() == 1 or falla.get() == 2:
                    code = codigo.get()
                    if code not in Diccionario_Fallas:
                        tipo_falla = falla.get()
                        Diccionario_Fallas[code] = (validacion,tipo_falla)
                        with open("Lista_Fallas.dat", "wb") as file:
                            pickle.dump(Diccionario_Fallas,file)
                        messagebox.showinfo("SISTEMA", "SE AGREGO LA FALLA AL SISTEMA.")
                    else:
                        messagebox.showinfo("ERROR", "LA FALLA YA ESTA REGISTRADA.")
                else:
                    messagebox.showinfo("ERROR", "Debe seleccionar el tipo de falla")
            else:
                messagebox.showinfo("ERROR", "La descripcion debe de estar entre 5 a 200 caracteres")
        else:
            messagebox.showinfo("ERROR", "El codigo debe de ser entre el rango de 1 a 9999")
    #CONSULTAR
    def consultar_elemento():
        if codigo.get() != "0" and codigo.get() != "":
            code = codigo.get()
            if code in Diccionario_Fallas:
                info = Diccionario_Fallas[code]
                descripcion.configure(state="normal")
                descripcion.insert("1.0", info[0])
                descripcion.configure(state="disabled")
                if info[1] == 1:
                    falla.set(1)
                else:
                    falla.set(2)
            else:
                messagebox.showinfo("ERROR", "La falla ingresada no esta registrada")
        else:
            messagebox.showinfo("ERROR", "El codigo debe de ser entre el rango de 1 a 9999")
    #MODIFICAR
    def modificar_elemento():
        if codigo.get() != "0" and codigo.get() != "":
            code = codigo.get()
            if code in Diccionario_Fallas:
                info = Diccionario_Fallas[code]
                descripcion.configure(state="normal")
                descripcion.insert("1.0", info[0])
                anterior = info[0] 
                if info[1] == 1:
                    falla.set(1)
                else:
                    falla.set(2)
                pedir_codigo.configure(state="disable")
                radio_lleve.configure(state="normal")
                radio_grave.configure(state="normal")
            else:
                messagebox.showinfo("ERROR", "La falla ingresada no esta registrada")
        else:
            messagebox.showinfo("ERROR", "El codigo debe de ser entre el rango de 1 a 9999")
    def modificar_guardar():
        validacion = sacar_texto()
        if validacion !=  False:
            code = codigo.get()
            tipo_falla = falla.get()
            Diccionario_Fallas[code] = (validacion,tipo_falla)
            with open("Lista_Fallas.dat", "wb") as file:
                pickle.dump(Diccionario_Fallas,file)
            messagebox.showinfo("SISTEMA", "Modificacion Exitosa!")
            activar_modificar()

        else:
            code = codigo.get()
            info = Diccionario_Fallas[code]
            tipo_falla = falla.get()
            anterior = info[0]

            Diccionario_Fallas[code] = (anterior,tipo_falla)
            with open("Lista_Fallas.dat", "wb") as file:
                pickle.dump(Diccionario_Fallas,file)
            messagebox.showinfo("SISTEMA", "Modificacion Exitosa!")
            activar_modificar()     
    #ELIMINAR
    def eliminar_elemento():
        if codigo.get() != "0" and codigo.get() != "":
            code = codigo.get()
            if code in Diccionario_Fallas:
                info = Diccionario_Fallas[code]
                descripcion.configure(state="normal")
                descripcion.insert("1.0", info[0])
                anterior = info[0] 
                if info[1] == 1:
                    falla.set(1)
                else:
                    falla.set(2)
                    pass
#TODO
                print(cola_revision)
                for llave in cola_revision:
                    for informacion in cola_revision[llave]:
                        info = cola_revision[llave][1]
                        if code in info:
                            messagebox.showinfo("SISTEMA", "Hay carros en revision con esta falla por lo que no se puede eliminar")
                            return
#TODO
                x = messagebox.askquestion('FALLA ENCONTRADA','¿Desea confirmar la eliminación de la falla' + str(code)+"?",master= fallas_ventana)
                if x == 'yes':
                    Diccionario_Fallas.pop(code)
                    with open("Lista_Fallas.dat", "wb") as file:
                        pickle.dump(Diccionario_Fallas,file)
                    activar_eliminar()
                else:
                    activar_eliminar()
            else:
                messagebox.showinfo("ERROR", "La falla ingresada no esta registrada, no se puede eliminar")
        else:
            messagebox.showinfo("ERROR", "El codigo debe de ser entre el rango de 1 a 9999")        
    def accion():
        caso = crud.get()
        match caso:
            case 1:
                añadir_elemento()
            case 2:
                consultar_elemento()
            case 3:
                modificar_elemento()
            case 4:
                eliminar_elemento()

                                
    #! Titulo label 

    tit = Label(fallas_ventana, relief = 'solid',  text ='Menu Lista de fallas', font=('Times New Roman', 32), width = 20)
    tit.place(x=10,y=10)
    instruccion_label=Label(fallas_ventana,  text ='Tipo de acción', font=('Times New Roman', 20), width = 15)
    instruccion_label.place(x=10,y=100)

    create = Radiobutton(fallas_ventana, text="Agregar Fallas", variable=crud, value=1, font=("Times New Roman", 13),command=activar_create)
    create.place(x=10, y=200)
    read = Radiobutton(fallas_ventana, text="Consultar Fallas", variable=crud, value=2, font=("Times New Roman", 13),command=activar_consultar)
    read.place(x=10, y=250)
    upload = Radiobutton(fallas_ventana, text="Modificar Fallas", variable=crud, value=3, font=("Times New Roman", 13),command=activar_modificar)
    upload.place(x=10, y=300)
    delete = Radiobutton(fallas_ventana, text="Eliminar Fallas", variable=crud, value=4, font=("Times New Roman", 13),command=activar_eliminar)
    delete.place(x=10, y=350)


    tit_code = Label(fallas_ventana, text ='Introduzca su código', font=('Times New Roman', 20))
    tit_code.place(x=500, y=150)
    pedir_codigo = Entry(fallas_ventana,font=('Times New Roman', 18), width = 15, textvariable=codigo)
    pedir_codigo.place(x=500, y=200)
    pedir_codigo.bind("<KeyRelease>", largo_codigo)

    #!FRAME
    frame_descripcion = Frame(fallas_ventana, width=400, height=200)
    frame_descripcion.place(x=500, y=300)
    #!SCROLLBAR
    scrollbar = Scrollbar(frame_descripcion)
    scrollbar.pack(side="right", fill="y")

    #?Texto box
    tit_descrip = Label(fallas_ventana, text ='Introduzca una descripción', font=('Times New Roman', 20))
    tit_descrip.place(x=500, y=250)
    descripcion = Text(frame_descripcion, height=10, width=40, bg="light cyan", yscrollcommand=scrollbar.set)
    descripcion.pack(side="left", fill="both")
    scrollbar.config(command=descripcion.yview)

    #?
    tfalla = Label(fallas_ventana, text ='Tipo de Falla', font=('Times New Roman', 20))
    tfalla.place(x=500, y=475)
    radio_lleve = Radiobutton(fallas_ventana, text="Leve", variable=falla, value=1, font=("Times New Roman", 13))
    radio_lleve.place(x=500, y=525)
    radio_grave= Radiobutton(fallas_ventana, text="Grave", variable=falla, value=2, font=("Times New Roman", 13))
    radio_grave.place(x=500, y=575)

    btn_realizar = Button(fallas_ventana, text ='', font=('Times New Roman', 20),command=accion)
    guardar_cambio = Button(fallas_ventana, text ='Guardar modificacíon', font=('Times New Roman', 20),command=modificar_guardar)
    
    #?CASOS
    #INICIO
    pedir_codigo.configure(state="disabled")
    descripcion.configure(state="disabled")
    radio_lleve.configure(state="disabled")
    radio_grave.configure(state="disabled")
    btn_realizar.configure(state="disabled")
    guardar_cambio.place_forget()

    fallas_ventana.mainloop()
    
#? ========================================================= TABLERO DE REVISION ==============================================================================================
def tablero_revision():
    revision = Toplevel()
    revision.title("Tablero de Revision")
    revision.geometry("1024x740")

    #FUNCIONES SECUNDARIAS ===============================================================================================================
    def largo_placa(evento):
        entry_modelo = placa.get()
        if len(str(entry_modelo)) > 8:
            modelo_valido = str(entry_modelo)[:8]
            carro.delete(0, END)
            carro.insert(0, modelo_valido)
    def largo_comand(evento):
        entry_modelo = ident.get()
        if len(str(entry_modelo)) > 1:
            modelo_valido = str(entry_modelo)[:1]
            commmando.delete(0, END)
            commmando.insert(0, modelo_valido)
    def validar_comando(evento):
        command = ident.get()
        if command in "FETU":
            match command:
                case "F":
                    F_commando()
                case "E":
                    E_commando()
                case "T":
                    T_commando()
                case "U":
                    U_commando()
                                                                                
        else:
            messagebox.showinfo("Error","Commando No existe") 
    
    #! Hacer que la ventana se mueva con la rueda del mouse
    def scroll(evento):
        canvas.yview_scroll(int(-1 * (evento.delta / 120)), "units")
    #FUNCIONES SECUNDARIAS ===============================================================================================================
    #?CARGA DE DATOS Y FUNCIONAMIENTO ====================================================================================================        
    config = open('configuracion_riteve.dat','rb')
    dat = pickle.load(config)
    config.close()
    lineas = dat[0]
    fallas_max = int(dat[5])

    ident = StringVar()
    placa = StringVar()
    falla = StringVar()   
    
    tablero = []

    #?Label
    tit_label = Label(revision, relief = 'solid',  text ='Revision Vehicular', font=('Times New Roman', 16), width = 20)
    tit_label.place(x=10,y=10)

    #LABEL Y ENTRYS CODIGO
    tit_com = Label(revision,  text ='COMMANDO:', font=('Times New Roman', 16), width = 20)
    tit_com.place(x=0 , y= 500)
    commmando = Entry(revision, font = ("Times New Roman", 13), width = 3, textvariable= ident)
    commmando.place(x=200 , y= 500)
    commmando.bind("<KeyRelease>", largo_comand)
    commmando.bind("<Return>", validar_comando)

    tit_placa = Label(revision,  text ='PLACA:', font=('Times New Roman', 16), width = 20)
    tit_placa.place(x=0 , y= 550)
    carro = Entry(revision, font = ("Times New Roman", 13), width = 8, textvariable=placa)
    carro.place(x=200 , y=  550)
    carro.bind("<KeyRelease>", largo_placa)

    tit_fail = Label(revision,  text ='CODIGO FALLA:', font=('Times New Roman', 16), width = 20)
    tit_fail.place(x=0 , y= 600)
    falla_code = Entry(revision, font = ("Times New Roman", 13), width = 4, textvariable=falla)
    falla_code.place(x=200 , y= 600)

    tit = Label(revision,  text ='INSERTE FRAME:', font=('Times New Roman', 16), width = 20)

    puesto_1 = Label(revision,  text ='Puesto 1:', font=('Times New Roman', 10), width = 10)
    puesto_1.place(x=380 , y= 50)
    puesto_2 = Label(revision,  text ='Puesto 2:', font=('Times New Roman', 10), width = 10)
    puesto_2.place(x=500 , y= 50)
    puesto_3 = Label(revision,  text ='Puesto 3:', font=('Times New Roman', 10), width = 10)
    puesto_3.place(x=620 , y= 50)
    puesto_4 = Label(revision,  text ='Puesto 4:', font=('Times New Roman', 10), width = 10)
    puesto_4.place(x=740 , y= 50)
    puesto_5 = Label(revision,  text ='Puesto 5:', font=('Times New Roman', 10), width = 10)
    puesto_5.place(x=860 , y= 50)


    #!================== ESTO CAMBIA CON FRAME =======================================
    
    frame_scrollbar = Frame(revision)
    frame_scrollbar.place(x = 250, y = 80, width = 730, height = 400)
    
    canvas = Canvas(frame_scrollbar)
    canvas.pack(side = LEFT, fill = BOTH, expand = True)
    
    scrollbar = ttk.Scrollbar(frame_scrollbar, orient = VERTICAL, command=canvas.yview)
    scrollbar.pack(side = RIGHT, fill = Y)
    scrollbar.bind_all("<MouseWheel>", scroll)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    marco_interno = Frame(frame_scrollbar)
    canvas.create_window((0,0), window = marco_interno, anchor = NW)
    
    
    for i in range(lineas):
        frame_linea = Frame(marco_interno)
        frame_linea.pack(side = TOP, anchor = W, pady = 10)
        label= Label(frame_linea, text=f"Línea {i+1}")
        label.pack(side = LEFT, padx = 10)
        fila = []
        for j in range(5):
            estacion = Button(frame_linea, text = "", font=('Times New Roman', 10), width = 7, height = 2, bg = "light green", state = DISABLED)
            estacion.pack(side = LEFT, padx = 35)
            fila.append(estacion)
        tablero.append(fila)
    marco_interno.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    print(copy)
    if copy != []:
        for i,fila in enumerate(copy):
            for j, texto in enumerate(fila):
                boton = tablero[i][j]
                boton.configure(text=texto)
    #!======================================== COMANDOS ==================================
    def T_commando():
        #PRIMERA ENTRADA DE LOS AUTOS
        if cola_revision == {}:
            auto = placa.get()
            confirmacion = False
            for linea in colas_espera:
                if linea == []:
                    pass
                if linea != []:
                    entrar = linea[-1]
                    if auto == entrar:
                        confirmacion = True
                        break
                    else:
                        pass
            if confirmacion == True:
                for i, lineas in enumerate(colas_espera):
                    print(lineas)
                    if lineas:
                        expediente = lineas.pop(-1)
                        print(expediente)
                        cola_revision[expediente] = [1, [], "PENDIENTE"]
                        boton = tablero[i][0]
                        boton.config(text=expediente)
                        pass
                return
            else:
                messagebox.showinfo("ERROR","ESTE AUTOMOVIL NO ESTA PRIMERO EN LA COLA DE ESPERA")
                return

        if cola_revision != {}:
            #! REVISA QUE NO HAY AUTOMOVILES EN LA LINEA 5
            for lista in tablero:
                boton = lista[4]
                lleno = boton.cget("text")
                if lleno == "":
                    pass
                else:
                    messagebox.showinfo("ERROR","HAY AUTOMOVILES EN EL PUESTO 5 Y NO SE PUEDEN MOVER AUTOMOVILES ")
                    return
            #COLA DE ESPERA ☯
            auto = placa.get()
            membresia = False
            for lista in colas_espera:
                if auto in lista:
                    if lista[-1] == auto:
                        membresia = True
                        break
                    else:
                        break
                else:
                    pass
            if membresia == True:
                #! MOVER TEXTO DE ENFRENTE HACIA ATRAS
                Matriz = []
                for listas in tablero:
                    filas = []
                    for botones in listas:
                        texto = botones.cget("text")
                        filas.append(texto)
                    Matriz.append(filas)
                print(Matriz)
                #! MOVER LA NUEVA MATRIZ UN ESPACIO 
                for i in range(len(Matriz)):
                    Matriz[i] = Matriz[i][0:4]
                    Matriz[i].insert(0, "")
                    print(Matriz[i])
                print(Matriz)
                #! ☯☯☯ AUMENTAR ELEMENTOS EN COLA DE REVISION ☯☯☯☯
                for lista in Matriz:
                    for elemento in lista:
                        if elemento in cola_revision:
                            cola_revision[elemento][0] += 1 
                        else:
                            pass
                #! PONER VALORES DE 
                for i,filas in enumerate(Matriz):
                    for j,elemento in enumerate(filas):
                        print(elemento)
                        boton = tablero[i][j]  # Obtener el botón de la matriz tablero en la posición (i, j)
                        boton.config(text=elemento)
                #! Crear expedientes he ingreso nuevos
                for i, lineas in enumerate(colas_espera):
                    print(lineas)
                    if lineas:
                        expediente = lineas.pop(-1)
                        print(expediente)
                        cola_revision[expediente] = [1, [], "PENDIENTE"]
                        boton = tablero[i][0]
                        boton.config(text=expediente)
                        pass
                return
            #!!!!!! COLA DE REVISION
            if auto in cola_revision:
                mover = cola_revision[auto][0]
                #! VER SI EL AUTO VA DE PRIMERO
                """for llave in cola_revision:
                    for info in cola_revision[llave][:1]:
                        if info > mover:
                             messagebox.showinfo("ERROR","ESTE AUTOMOVIL NO ESTA DE PRIMERO EN LA LINEA DE REVISION")
                             return
                        else:
                            pass"""
                #! SACAR LA LISTA DE VEHICULOS 
                #! MOVER TEXTO DE ENFRENTE HACIA ATRAS
                Matriz = []
                for listas in tablero:
                    filas = []
                    for botones in listas:
                        texto = botones.cget("text")
                        filas.append(texto)
                    Matriz.append(filas)

                # MOVER LA NUEVA MATRIZ UN ESPACIO
                for i in range(len(Matriz)):
                    Matriz[i] = Matriz[i][0:4]
                    Matriz[i].insert(0, "")

                # AUMENTAR ELEMENTOS EN COLA DE REVISION
                for lista in Matriz:
                    for elemento in lista:
                        if elemento in cola_revision:
                            cola_revision[elemento][0] += 1

                # PONER VALORES DE LA MATRIZ EN LOS BOTONES
                for i, filas in enumerate(Matriz):
                    for j, elemento in enumerate(filas):
                        boton = tablero[i][j]
                        boton.config(text=elemento)

                # Crear expedientes e ingresar nuevos
                for i, lineas in enumerate(colas_espera):
                    print(lineas)
                    if lineas:
                        expediente = lineas.pop(-1)
                        print(expediente)
                        cola_revision[expediente] = [1, [], "PENDIENTE"]
                        boton = tablero[i][0]
                        boton.config(text=expediente)
                        pass
                return
            else:
                messagebox.showinfo("ERROR","ESTE AUTOMOVIL NO ESTA PRIMERO EN COLA DE ESPERA O REVISION")
                return
            #revisa que vaya de primero en la cola de espera
    def U_commando():
        auto = placa.get()
        for lista in tablero:
            boton = lista[4]
            lleno = boton.cget("text")
            if lleno == "":
                pass
            else:
                messagebox.showinfo("ERROR","HAY AUTOMOVILES EN EL PUESTO 5 Y NO SE PUEDEN MOVER AUTOMOVILES ")
                return
        if auto not in cola_revision:
            messagebox.showinfo("¡ATENCION!","EL AUTO NO SE ENCUENTRA EN LA COLA DE REVISIÓN")
            return
        else:
            for lista in tablero:
                for i,boton in enumerate(lista):
                    texto = boton.cget("text")
                    if texto != auto:
                        pass
                    if texto == auto:
                        b2 = lista[i+1]
                        siguiente = b2.cget("text")
                        if siguiente == "":
                            b2.configure(text="☯")
                            boton.configure(text="")
                            cola_revision[auto][0] += 1
                            print(cola_revision)
                        else:
                            messagebox.showinfo("¡ATENCION!","EL AUTO NO SE PUEDE MOVER AL SIGUIENTE PUESTO DE REVISION")
            for lista in tablero:
                for boton in lista:
                    texto = boton.cget("text")
                    if texto == "☯":
                        boton.configure(text=auto)
    def E_commando():
        asig_falla = falla.get()
        auto = placa.get()
        if asig_falla == "":
            messagebox.showinfo("ERROR","NO INGRESO EL CODIGO DE LA FALLA")
            return
        if asig_falla not in Diccionario_Fallas:
            messagebox.showinfo("ERROR","NO EXISTE FALLA REGISTRADA CON ESE CODIGO")
            return
        if auto not in cola_revision:
            messagebox.showinfo("ERROR","NO PUEDE ASIGNARSE FALLA PORQUE NO ESTA EN REVISION")
            return
        if asig_falla in cola_revision[auto][1]:
            messagebox.showinfo("ERROR","ESTA FALLA YA FUE ASIGNADA")
            return            
        else:
            cola_revision[auto][1] += [asig_falla]
            messagebox.showinfo("EXITO!","SE ASGINO FALLA")
            return print(cola_revision)
    #! SE DEBE CAMBIAR DESPUES PARA LO DE LOS PDF
    def F_commando():
        auto = placa.get()
        if auto not in cola_revision:
            messagebox.showinfo("ERROR","NO PUEDE LA REVISION PORQUE NO ESTA EN EL PUESTO FINAL")
            return
        info = cola_revision[auto]
        contador = info[0]
        if contador != 5:
            messagebox.showinfo("ERROR","NO PUEDE LA REVISION PORQUE NO ESTA EN EL PUESTO FINAL")
            return
        else:
            auto = placa.get()
            for c in historial_citas:
                if c[4] == auto and c[-1] == "PENDIENTE":
                    informacion = c
            #CALCULAR CASOS
            fallas_asig = cola_revision[auto][1]
            # estado = cola_revision[auto][2]
            Leves = []
            Graves = []
            #todo CAMBIOS HECHOS A TABLERO ACÁ
            for lista in tablero:
                for boton in lista:
                    texto = boton.cget("text")
                    if texto == auto:
                        boton.configure(text="")
        
            for codigo in fallas_asig:
                tipo = Diccionario_Fallas[codigo][1]
                descripcion = Diccionario_Fallas[codigo][0]
                if tipo == 1:
                    Leves.append([descripcion,codigo])
                if tipo == 2:
                    Graves.append([descripcion,codigo])
            if len(Graves) > fallas_max: #! cambio a arbol binario va acá
                estado = "SACAR DE CIRCULACIÓN"
                arbol_binario.cambiar_estado(informacion, estado)
                informacion[-1] = estado
                registro_num = open("numeroscitas.dat", "wb")
                pickle.dump([num_cita, historial_citas], registro_num)
                print(historial_citas)
                registro_num.close()
                resultados_pdf(estado, informacion, Graves, Leves)
                envio_correo(informacion[9], estado, informacion[7], 0,0)
            if len(Graves) <= 1 and len(Graves) <= fallas_max:
                estado = "REINSPECCIÓN"
                arbol_binario.cambiar_estado(informacion, estado)
                informacion[-1] = estado
                registro_num = open("numeroscitas.dat", "wb")
                pickle.dump([num_cita, historial_citas], registro_num)
                print(historial_citas)
                registro_num.close()
                resultados_pdf(estado, informacion, Graves, Leves)
                envio_correo(informacion[9], estado, informacion[7], 0,0)
            if len(Graves) == 0:
                estado = "APROBADA"
                arbol_binario.cambiar_estado(informacion, estado)
                informacion[-1] = estado
                registro_num = open("numeroscitas.dat", "wb")
                pickle.dump([num_cita, historial_citas], registro_num)
                print(historial_citas)
                registro_num.close()
                resultados_pdf(estado, informacion, Graves, Leves)
                certificado_pdf(informacion)
                envio_correo(informacion[9], estado, informacion[7], 0,0)
            cola_revision.pop(auto)
            print(cola_revision)
            #todo PONER LO DEL BOTÓN ACÁ
            messagebox.showinfo("", f"VEHÍCULO {auto} HA SALIDO EXISTOSAMENTE DE LA COLA DE ESPERA")

                    
    def buscar_info(auto):
        #CALCULAR CASOS
        for i in range(1, num_cita):
            x = arbol_binario.buscar_nodos(i)
            if x is None:
                continue  # Salta al siguiente ciclo si x es None
            if auto in x:
                return x
            else:
                pass
    def on_closing():
        global copy
        copy = []
        for lista in tablero:
            fila = []
            for boton in lista:
                texto = boton['text']
                fila.append(texto)
            copy.append(fila)
        print(copy)
        revision.destroy()
        return copy


    revision.protocol("WM_DELETE_WINDOW", on_closing)
    revision.mainloop()
    
#?============================================================= Cancelar citas ============================================================================================================
def cancelar_cita():
    c_citas = Toplevel()
    c_citas.title("Cancelar citas")
    c_citas.geometry("350x300")
    
    #* Función para ctivar botón cuando placa y cita tengan algo escrito
    def activacion(evento):
        if len(entry_placa.get()) > 0 and len(entry_cita.get()) > 0:
            boton_cancelar.config(state = NORMAL)
        else:
            boton_cancelar.config(state = DISABLED)
    
    #* Función cancelar
    def cancelar():
        # Validaciones
        if var_placa.get() in cola_revision: 
            messagebox.showerror("", "No se puede eliminar, ya está en revisón.")
            return
        datos_cita = arbol_binario.buscar_nodos(int(var_cita.get()))
        if datos_cita == None:
            messagebox.showerror("","Esta cita no existe. Vuélvalo a intentar.")
            return
        # Cambio
        if var_placa.get() != datos_cita[4]:
            messagebox.showerror("","Esta placa no corresponde a la de la cita. Vuélvalo a intentar.")
            return
        if datos_cita[-1] == "PENDIENTE":
            if messagebox.askyesno("", "¿Está seguro de querer cancelar la cita?") == True:
                arbol_binario.cambiar_estado(datos_cita, "CANCELADA")
                datos_cita[-1] == "CANCELADA"
                registro_num = open("numeroscitas.dat", "wb")
                pickle.dump([num_cita, historial_citas], registro_num)
                print(historial_citas)
                registro_num.close()
                
                # Eliminación de cola de espera en caso de estarlo
                for cola in colas_espera():
                    if var_placa.get() in cola: 
                        indice = cola.index(var_placa.get())
                        cola.pop(indice)
                        
                messagebox.showinfo("","Cita cancelada existosamente.")
                entry_cita.delete(0, END)
                entry_placa.delete(0, END)
            else:
                return
        else:
            messagebox.showerror("", "Cita ya antes cancelada.")
    
    #* Título
    titulo = Label(c_citas, text = "Cancelar citas", font = ('Times New Roman', 20), relief = SOLID, width = 16)
    titulo.pack(side = TOP, anchor = CENTER, pady = 20)
    
    #* Número de cita
    var_cita = StringVar()
    tit_cita = Label(c_citas, text = "Número de cita:", font = ("Times New Roman", 13, "bold"))
    tit_cita.place(x = 20, y = 90)
    entry_cita = Entry(c_citas, width = 8, justify = CENTER, font = ("Times New Roman", 13), textvariable = var_cita)
    entry_cita.place(x = 240, y = 90)
    entry_cita.bind("<KeyRelease>", activacion)
    entry_cita.bind("<KeyRelease>", solo_numeros)
    
    #* Número de placa
    var_placa = StringVar()
    tit_placa = Label(c_citas, text = "Número de placa:", font = ("Times New Roman", 13, "bold"))
    tit_placa.place(x = 20, y = 150)
    entry_placa = Entry(c_citas, width = 8, justify = CENTER, font = ("Times New Roman", 13), textvariable = var_placa)
    entry_placa.place(x = 240, y = 150)
    entry_placa.bind("<KeyRelease>", activacion)
    
    #* Botón de cancelar cita
    boton_cancelar = Button(c_citas, text = "Cancelar", width = 9, font = ("Times New Roman", 13), command = cancelar, state = DISABLED)
    boton_cancelar.pack(side = BOTTOM, anchor = CENTER, pady = 50)
    
    c_citas.mainloop()

#?=========================================================== Ingreso de vehículos =========================================================================================================
def ingreso_vehiculos():
    ingreso = Toplevel()
    ingreso.title("Ingreso de vehículos")
    ingreso.state("zoomed")
    
    # Abrir configuración
    configuracion = open("configuracion_riteve.dat", "rb")
    datos = pickle.load(configuracion)
    configuracion.close()
    
    num_filas = int(datos[0])
    iva = datos[6]
    lista_tarifas = datos[7]
    
    lista_lens = []
    #* Agregar a lista de colas una cola de espera para cada una
    if len(colas_espera) != num_filas:
        lineas_necesarias = num_filas - len(colas_espera)
        for f in range(lineas_necesarias):
            colas_espera.append([])
    print(colas_espera)

    
    #* Ingresar placa a la cola:
    
    #* Función despliegue de información
    def mostrar_info(): #! Hacen falta algunas validaciones
        global lista_labels
        lista_labels = []
        
        # Encontrar cita en el árbol binario
        datos_cita = arbol_binario.buscar_nodos(int(var_cita.get()))
        
        #* Validaciones 
        if datos_cita == None:
            messagebox.showerror("", "Esta cita no existe.")
            return
            
        if datos_cita[-1] == "CANCELADA":
            messagebox.showerror("", "Esta cita fue cancelada.")
            return
        if datos_cita[-1] == "APROBADA":
            messagebox.showerror("", "Este vehículo ya pasó la revisión.")
            return
        
        fecha_cita = datos_cita[0]
        tipo_vehiculo = datos_cita[3]
        marca = datos_cita[5]
        modelo = datos_cita[6]
        propietario = datos_cita[7]
        
        if fecha_cita.year == fecha_actual.year and fecha_cita.month == fecha_actual.month and fecha_cita.day == fecha_actual.day:
            if (fecha_cita - fecha_actual) < timedelta(hours = 1):
                messagebox.showerror("", "No llegó a tiempo para su revisión. Su cita será cancelada para que cree otra.")
                arbol_binario.cambiar_estado(datos_cita, "CANCELADA")
                datos_cita[-1] = "CANCELADA"
                registro_num = open("numeroscitas.dat", "wb")
                pickle.dump([num_cita, historial_citas], registro_num)
                print(historial_citas)
                registro_num.close()
                return
        else:
            messagebox.showerror("", "No se encuentra en la fecha de revisión asignada.")
            return
        
        label_marca1 = Label(ingreso, text = "Marca: ", font = ("Times New Roman", 13, "bold"))
        label_marca2 = Label(ingreso, text = f"{marca}", font = ("Times New Roman", 13))
        lista_labels.append(label_marca1)
        lista_labels.append(label_marca2)
        label_marca1.place(x = 20, y = 270)
        label_marca2.place(x = 240, y = 270)
        
        label_modelo1 = Label(ingreso, text = "Modelo: ", font = ("Times New Roman", 13, "bold"))
        label_modelo2 = Label(ingreso, text = f"{modelo}", font = ("Times New Roman", 13))
        lista_labels.append(label_modelo1)
        lista_labels.append(label_modelo2)
        label_modelo1.place(x = 20, y = 310)
        label_modelo2.place(x = 240, y = 310)
        
        label_prop1 = Label(ingreso, text = "Propietario: ", font = ("Times New Roman", 13, "bold"))
        label_prop2 = Label(ingreso, text = f"{propietario}", font = ("Times New Roman", 13))
        lista_labels.append(label_prop1)
        lista_labels.append(label_prop2)
        label_prop1.place(x = 20, y = 350)
        label_prop2.place(x = 240, y = 350)
        
        # Costo de la revisión
        indice = vehiculos.index(tipo_vehiculo)
        tarifa = int(lista_tarifas[indice])
        precio_total = tarifa + (tarifa * (iva / 100))

        label_precio1 = Label(ingreso, text = "Costo de la revisión: ", font = ("Times New Roman", 13, "bold"))
        label_precio2 = Label(ingreso, text = f"₡ {precio_total}", font = ("Times New Roman", 13))
        lista_labels.append(label_precio1)
        lista_labels.append(label_precio2)
        label_precio1.place(x = 20, y = 390)
        label_precio2.place(x = 240, y = 390)
        
        boton_guardar = Button(ingreso, text = "Ingresar", width = 15, font = ("Times New Roman", 13), command = ingresar_revision)
        boton_guardar.place(x = 100, y = 440)
        lista_labels.append(boton_guardar)
    
    def ingresar_revision():
        global lista_labels
        for cola in colas_espera:
            largo = len(cola)
            lista_lens.append(largo)
        
        largo_minimo = min(lista_lens)
        for cola in colas_espera:
            if len(cola) == largo_minimo:
                cola.append(var_placa.get())
                break
        print(colas_espera)
        messagebox.showinfo("","¡Vehículo ingresado existosamente!")
        for label in lista_labels:
            label.place_forget()
        entry_cita.delete(0, END)
        entry_placa.delete(0, END)
        
    #* Fecha actual
    fecha_actual = datetime.now()
    con_formato = datetime.strftime(fecha_actual, "%d/%m/%Y  %H:%M:%S")
    actual = Label(ingreso, font = ("Times New Roman", 13, "bold"), text = f"Hora actual: {con_formato}")
    actual.pack(side = TOP, anchor = E)
    
    #* Título
    titulo = Label(ingreso, text = "Ingreso de vehículos", font = ("Times New Roman", 20), relief = SOLID, width = 22)
    titulo.pack(side = TOP, anchor = W, pady = 10, padx = 10)

    #* Número de cita
    var_cita = StringVar()
    tit_cita = Label(ingreso, text = "Número de cita:", font = ("Times New Roman", 13, "bold"))
    tit_cita.place(x = 20, y = 90)
    entry_cita = Entry(ingreso, width = 8, justify = CENTER, font = ("Times New Roman", 13), textvariable = var_cita)
    entry_cita.place(x = 240, y = 90)
    #entry_cita.bind("<KeyRelease>", activacion)
    entry_cita.bind("<KeyRelease>", solo_numeros)
    
    #* Número de placa
    var_placa = StringVar()
    tit_placa = Label(ingreso, text = "Número de placa:", font = ("Times New Roman", 13, "bold"))
    tit_placa.place(x = 20, y = 150)
    entry_placa = Entry(ingreso, width = 8, justify = CENTER, font = ("Times New Roman", 13), textvariable = var_placa)
    entry_placa.place(x = 240, y = 150)
    #entry_placa.bind("<KeyRelease>", activacion)
    
    boton_mostrar = Button(ingreso, text = "Mostrar datos", width = 15, font = ("Times New Roman", 13), command = mostrar_info)
    boton_mostrar.place(x = 100, y = 200)

#?============================================================= Menú Principal ====================================================================================================================

reteve_principal.geometry('500x640')
reteve_principal.title('MENU PRINCIPAL')

#! IMAGEN 'Riteve_Nit.png'
img = PhotoImage(file='Riteve_Nit.png')
fondo_menu = Label(reteve_principal, image = img)
fondo_menu.place(x=0, y= 100, relwidth=1)

titulo_riteve = Label(master = reteve_principal, relief = 'solid',  text ='RETEVE', font=('Times New Roman', 32), width = 9)
titulo_riteve.place(x=170,y=30)

Progra_citas = Button(reteve_principal, text = "Programar citas", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3, command = lambda: programar_cita())
Progra_citas.place(x=20,y=100)

Cancel_citas = Button(reteve_principal, text = "Cancelar citas", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3, command = cancelar_cita)
Cancel_citas.place(x=20,y=160)

Ingreso = Button(reteve_principal, text = "Ingreso de vehículos", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3, command = ingreso_vehiculos)
Ingreso.place(x=20,y=220)

Revision = Button(reteve_principal, text = "Tablero de revisión", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3, command = tablero_revision)
Revision.place(x = 20, y = 280)

Lista_fallas = Button(reteve_principal, text = "Lista de fallas", font = ("Times New Roman", 10), bg = "snow",width = 16, height = 3, command = lista_de_fallas)
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
