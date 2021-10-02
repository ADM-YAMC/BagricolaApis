import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {'Sistema': 'Bagricola'}


class Foto(BaseModel):
    foto:str


@app.get("/api/iniciar/{correo}/{clave}")
def iniciar(correo: str,clave:str):
    try:
        passw=""
        user=""
        nombre=""
        idi=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT CorreoAdmin, Clave, NombreAdmin,IdAdmin from IniciarSesion where CorreoAdmin ='"+correo+"' and Clave = '"+clave+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            user = i[0]
            passw=i[1]
            nombre=i[2]
            idi = i[3]
        if correo == user and clave==passw:
            return {"Bienvenido": nombre, "id":idi}
        else:
            return {"ok":False}
    except TypeError:
        return "Error al estraer los datos"

@app.post("/api/RegistroEmpleados/{CedulaEmpleado}/{NombreEmpleado}/{CodigoEmpleado}/{FechaContratacion}/{departamento}/{turno}")
def RegistroEmpleados(CedulaEmpleado: str,NombreEmpleado:str,CodigoEmpleado:str,FechaContratacion:str,FotoEmpleado:Foto,departamento:str, turno:str):
    try:
        cedula = ""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT CedulaEmpleado FROM RegistroEmpleados WHERE CedulaEmpleado = '"+CedulaEmpleado+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            cedula = i[0]
        if CedulaEmpleado == cedula:
            return  {"ok":False}
        else:
            datos = (CedulaEmpleado,NombreEmpleado,CodigoEmpleado,FechaContratacion,FotoEmpleado.foto,departamento, turno)
            sql='''INSERT INTO RegistroEmpleados(CedulaEmpleado,NombreEmpleado,CodigoEmpleado,FechaContratacion,FotoEmpleado,departamento, turno) VALUES(?,?,?,?,?,?,?)'''
            cursor.execute(sql,datos)
            conexion.commit()
            return  {"ok":True}
    except TypeError:
        return "Error al conectar a la base de datos."


@app.post("/api/ActualizarEmpleados/{CedulaEmpleado}/{NombreEmpleado}/{CodigoEmpleado}/{FechaContratacion}/{departamento}/{idu}")
def ActualizarEmpleados(CedulaEmpleado: str,NombreEmpleado:str,CodigoEmpleado:str,FechaContratacion:str,FotoEmpleado:Foto,departamento:str,idu:str):
    conexion = sqlite3.connect("BagricolaDataBase.s3db")
    cursor = conexion.cursor()
    sql="UPDATE RegistroEmpleados SET CedulaEmpleado='"+CedulaEmpleado+"',NombreEmpleado='"+NombreEmpleado+"',CodigoEmpleado='"+CodigoEmpleado+"',FechaContratacion='"+FechaContratacion+"',FotoEmpleado='"+FotoEmpleado.foto+"',departamento='"+departamento+"' WHERE IdUser = '"+idu+"'"
    cursor.execute(sql)
    conexion.commit()
    return  {"ok":True}

@app.delete("/api/EliminarEmpleados/{idu}/{codigo}")
def EliminarEmpleados(idu:str,codigo:str):
    conexion = sqlite3.connect("BagricolaDataBase.s3db")
    cursor = conexion.cursor()
    sql="DELETE FROM RegistroEmpleados WHERE IdUser = '"+idu+"'"
    cursor.execute(sql)
    sql1="DELETE FROM RegistroEntradas WHERE CodigoEmpleado = '"+codigo+"'"
    cursor.execute(sql1)
    sql2="DELETE FROM RegistroSalidas WHERE CodigoEmpleado = '"+codigo+"'"
    cursor.execute(sql2)
    conexion.commit()
    return  {"ok":True}

@app.post("/api/RegistroAdmin/{nombre}/{correo}/{clave}")
def RegistroAdmin(nombre: str,correo:str,clave:str):
    try:
        cor = ""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT CorreoAdmin FROM IniciarSesion WHERE CorreoAdmin = '"+correo+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            cor = i[0]
        if correo == cor:
            return  {"ok":False}
        else:
            datos = (nombre,correo,clave)
            sql='''INSERT INTO IniciarSesion(NombreAdmin,CorreoAdmin,Clave) VALUES(?,?,?)'''
            cursor.execute(sql,datos)
            conexion.commit()
            return  {"ok":True}
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/Registro")
def Registro():
    try:
        datos=[]
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT CedulaEmpleado,NombreEmpleado,CodigoEmpleado,FechaContratacion,FotoEmpleado,IdUser,departamento FROM RegistroEmpleados")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"cedula":i[0],"nombre":i[1],"codigo":i[2],"fecha":i[3],"foto":i[4], "id":i[5],"departamento":i[6]})
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."


@app.get("/api/RegistroEntrar/{fecha}")
def RegistroEntra(fecha:str):
    try:
        datos=[]
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT IdEntrada,NombreEmpleado,CodigoEmpleado,Fecha,Hora FROM RegistroEntradas WHERE Fecha = '"+fecha+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"id":i[0],"nombre":i[1],"codigo":i[2],"fecha":i[3],"hora":i[4]})
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/RegistroEntrarEmpleado/{CodigoEmpleado}")
def RegistroEntrarEmpleado(CodigoEmpleado:str):
    try:
        datos=[]
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT IdEntrada,NombreEmpleado,CodigoEmpleado,Fecha,Hora FROM RegistroEntradas WHERE CodigoEmpleado = '"+CodigoEmpleado+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"id":i[0],"nombre":i[1],"codigo":i[2],"fecha":i[3],"hora":i[4]})
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/RegistroSalir/{fecha}")
def RegistroSalir(fecha:str):
    try:
        datos=[]
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT IdSalida,NombreEmpleado,CodigoEmpleado,Fecha,Hora FROM RegistroSalidas WHERE Fecha = '"+fecha+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"id":i[0],"nombre":i[1],"codigo":i[2],"fecha":i[3],"hora":i[4]})
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/RegistroSalirEmpeado/{CodigoEmpleado}")
def RegistroSalirEmpeado(CodigoEmpleado:str):
    try:
        datos=[]
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT IdSalida,NombreEmpleado,CodigoEmpleado,Fecha,Hora FROM RegistroSalidas WHERE CodigoEmpleado = '"+CodigoEmpleado+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos.append({"id":i[0],"nombre":i[1],"codigo":i[2],"fecha":i[3],"hora":i[4]})
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/CantidadEmpleados")
def CantidadEmpleados():
    try:
        datos=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT count(IdUser) as cantidad FROM RegistroEmpleados")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = i[0]
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."


@app.get("/api/CantidadEmpleadosEntrada/{fecha}")
def CantidadEmpleadosEntrada(fecha:str):
    try:
        datos=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT count(IdEntrada) as cantidad FROM RegistroEntradas WHERE Fecha = '"+fecha+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = i[0]
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/CantidadEmpleadosSalida/{fecha}")
def CantidadEmpleadosSalida(fecha:str):
    try:
        datos=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT count(IdSalida) as cantidad FROM RegistroSalidas WHERE Fecha = '"+fecha+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = i[0]
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/CantidadEntrada/{fecha}/{codigo}")
def CantidadEntrada(fecha:str,codigo:str):
    try:
        datos=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT count(IdEntrada) as cantidad FROM RegistroEntradas WHERE Fecha = '"+fecha+"' and CodigoEmpleado = '"+codigo+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = i[0]
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.get("/api/CantidadSalida/{fecha}/{codigo}")
def CantidadSalida(fecha:str,codigo:str):
    try:
        datos=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT count(IdSalida) as cantidad FROM RegistroSalidas WHERE Fecha = '"+fecha+"' and CodigoEmpleado = '"+codigo+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = i[0]
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."

@app.post("/api/RegistroEntradas/{NombreEmpleado}/{CodigoEmpleado}/{Fecha}/{Hora}")
def RegistroEntradas(NombreEmpleado: str,CodigoEmpleado:str,Fecha:str,Hora:str):
    try:
        codigo=""
        fec=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT CodigoEmpleado FROM RegistroEmpleados WHERE CodigoEmpleado ='"+CodigoEmpleado+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            codigo = i[0]
        if CodigoEmpleado == codigo:
            cursor.execute("SELECT CodigoEmpleado,Fecha FROM RegistroEntradas WHERE CodigoEmpleado ='"+CodigoEmpleado+"' and Fecha='"+Fecha+"'")
            contenido = cursor.fetchall()
            for i in contenido:
                codigo = i[0]
                fec=i[1]
            if CodigoEmpleado == codigo and Fecha == fec:
                return {"ok": False}
            else:
                datos = (NombreEmpleado,CodigoEmpleado,Fecha,Hora)
                sql='''INSERT INTO RegistroEntradas(NombreEmpleado,CodigoEmpleado,Fecha,Hora) VALUES(?,?,?,?)'''
                cursor.execute(sql,datos)
                conexion.commit()
                return {"ok": True}
        else:
            return {"msj":"Error"}
    except TypeError:
        return {"msj":"Error al conectar a la base de datos."}


@app.post("/api/RegistroSalidas/{NombreEmpleado}/{CodigoEmpleado}/{Fecha}/{Hora}")
def RegistroSalidas(NombreEmpleado: str,CodigoEmpleado:str,Fecha:str,Hora:str):
    try:
        codigo=""
        fec=""
        f=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT CodigoEmpleado FROM RegistroEmpleados WHERE CodigoEmpleado ='"+CodigoEmpleado+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            codigo = i[0]
        if CodigoEmpleado == codigo:
            cursor.execute("SELECT CodigoEmpleado,Fecha FROM RegistroSalidas WHERE CodigoEmpleado ='"+CodigoEmpleado+"' and Fecha='"+Fecha+"'")
            contenido = cursor.fetchall()
            for i in contenido:
                codigo = i[0]
                fec=i[1]
            if CodigoEmpleado == codigo and Fecha == fec:
                return {"ok": False}
            else:
                cursor.execute("SELECT Fecha FROM RegistroEntradas WHERE CodigoEmpleado ='"+CodigoEmpleado+"' and Fecha= '"+Fecha+"'")
                contenid = cursor.fetchall()
                for i in contenid:
                    f = i[0]
                if Fecha == f:
                    datos = (NombreEmpleado,CodigoEmpleado,Fecha,Hora)
                    sql='''INSERT INTO RegistroSalidas(NombreEmpleado,CodigoEmpleado,Fecha,Hora) VALUES(?,?,?,?)'''
                    cursor.execute(sql,datos)
                    conexion.commit()
                    return {"ok": True}
                else:
                    return {"msj":"Er"}         
        else:
             return {"msj":"Error"}
    except TypeError:
        return {"msj":"Error al conectar a la base de datos."}


@app.get("/api/obtenerNombreEmp/{codigo}")
def obtenerNombreEmp(codigo:str):
    try:
        datos=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT NombreEmpleado, turno FROM RegistroEmpleados WHERE CodigoEmpleado = '"+codigo+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = {"Nombre":i[0], "Turno":i[1]}
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."


@app.get("/api/RegistroExcusas/{codigoConfirm}")
def registroExcusas(codigoConfirm:str):
    try:
        datos=""
        conexion = sqlite3.connect("BagricolaDataBase.s3db")
        cursor = conexion.cursor()
        cursor.execute("SELECT NombreAdmin, Clave FROM IniciarSesion WHERE Clave = '"+codigoConfirm+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            datos = {"Nombre":i[0], "Clave":i[1]}
        return datos
    except TypeError:
        return "Error al conectar a la base de datos."