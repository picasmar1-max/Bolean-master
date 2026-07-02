[app]

# (str) Título de tu aplicación
title = Boolean Master

# (str) Nombre del paquete (identificador único en el celular, sin espacios)
package.name = booleanmaster

# (str) Dominio del paquete (se usa junto al nombre, ej: org.test.booleanmaster)
package.domain = org.test

# (str) Dónde están tus archivos de código (. significa la carpeta actual)
source.dir = .

# (list) Extensiones de archivos que debe incluir dentro de la app
source.include_exts = py,png,jpg,kv,atlas

# (str) Versión de tu aplicación
version = 0.1

# (list) ¡SÚPER IMPORTANTE! Aquí le decimos a la app que instale Python, Kivy y Sympy
requirements = python3, kivy, sympy

# (str) Orientación de la pantalla (portrait = vertical, landscape = horizontal)
orientation = portrait

# (bool) Indicar si la aplicación se ejecuta en pantalla completa
fullscreen = 0

# (list) Arquitecturas de procesador para las que se compilará (cubre casi cualquier Android moderno)
android.archs = arm64-v8a, armeabi-v7a

# (int) Versión mínima de Android que soportará (API 21 es Android 5.0)
android.minapi = 21

# (int) Versión de la API de Android con la que se compilará
android.ndk_api = 21

# (bool) Usar el almacenamiento privado de la app para los archivos
android.private_storage = True

[buildozer]
# (int) Nivel de detalles en los textos que muestra al compilar (2 significa mostrar todo)
log_level = 2

# (int) Advertir si se ejecuta como administrador (root)
warn_on_root = 1