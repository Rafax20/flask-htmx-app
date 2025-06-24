import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def agregar_usuario(nombre):
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "usuario" (nombre) VALUES (%s)', (nombre,))
    conn.commit()
    cursor.close()
    conn.close()

def editar_usuario(id_usuario, nuevo_nombre):
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute('UPDATE "usuario" SET nombre = %s WHERE id = %s', (nuevo_nombre, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_usuario(id_usuario):
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "usuario" WHERE id = %s', (id_usuario,))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_usuarios():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, correo FROM "usuario"')
    resultados = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()
    return resultados, headers



def buscar_usuario(nombre):
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM "usuario" WHERE nombre ILIKE %s', (f'%{nombre}%',))
    resultados = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return resultados, headers
