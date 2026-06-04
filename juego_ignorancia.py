import random

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conecta_bd import *
from ed_categoria import *
from ed_pregunta import *


pantalla = Tk()
pantalla.resizable(1,1)
pantalla.geometry("1200x900")
pantalla.config(background="pink")
pantalla.title("Ignorancia-BD")


seleccion = ()

str_preg = StringVar()
str_res1 = StringVar()
str_res2 = StringVar()
str_res3 = StringVar()
str_res4 = StringVar()
str_sig = StringVar()
str_cat_label = StringVar()

correcto = 0

x1 = 10
x2 = 10
x3 = 10
x4 = 10

turno = 1
juego_terminado = False

WIN_ADVANCES = 9

adv1 = 0
adv2 = 0
adv3 = 0
adv_ignorancia = 0



canvas = Canvas(
    pantalla,
    width=1200,
    height=700,
    bg="RoyalBlue4",
    highlightthickness=0
)

canvas.place(x=0, y=150)



fon = PhotoImage(file=r"./im/PISTA.png")

canvas.create_image(
    0,
    0,
    image=fon,
    anchor=NW
)



def reiniciar_juego():

    global x1, x2, x3, x4
    global adv1, adv2, adv3, adv_ignorancia
    global turno, juego_terminado, seleccion

    x1 = 10
    x2 = 10
    x3 = 10
    x4 = 10

    adv1 = 0
    adv2 = 0
    adv3 = 0
    adv_ignorancia = 0

    turno = 1
    juego_terminado = False
    seleccion = ()

    canvas.coords(j1, x1, 135)
    canvas.coords(j2, x2, 220)
    canvas.coords(j3, x3, 320)
    canvas.coords(bu, x4, 400)

    str_sig.set("jugador 1")

    str_preg.set("")
    str_res1.set("")
    str_res2.set("")
    str_res3.set("")
    str_res4.set("")

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)


def fin_juego(mensaje):

    global juego_terminado

    juego_terminado = True

    repetir = messagebox.askyesno(
        "Fin del juego",
        mensaje + "\n\n¿Deseas jugar otra vez?"
    )

    if repetir:
        reiniciar_juego()


def avanza_jug():

    global x1, x2, x3
    global adv1, adv2, adv3

    if juego_terminado:
        return

    if turno == 1:

        x1 += 100
        adv1 += 1

        canvas.coords(j1, x1, 135)

        if adv1 >= WIN_ADVANCES:
            fin_juego("¡El perro del Jugador 1 ganó!")

    elif turno == 2:

        x2 += 100
        adv2 += 1

        canvas.coords(j2, x2, 220)

        if adv2 >= WIN_ADVANCES:
            fin_juego("¡El perro del Jugador 2 ganó!")

    elif turno == 3:

        x3 += 100
        adv3 += 1

        canvas.coords(j3, x3, 320)

        if adv3 >= WIN_ADVANCES:
            fin_juego("¡El perro del Jugador 3 ganó!")


def mover_ignorancia():

    global x4, adv_ignorancia

    x4 += 100
    adv_ignorancia += 1

    canvas.coords(bu, x4, 400)

    if adv_ignorancia >= WIN_ADVANCES and not juego_terminado:
        fin_juego("¡El perro ignorante ganó! Todos pierden.")


def desactivar_botones():

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)


def opc1():

    desactivar_botones()

    if correcto == 1:
        avanza_jug()
    else:
        mover_ignorancia()


def opc2():

    desactivar_botones()

    if correcto == 2:
        avanza_jug()
    else:
        mover_ignorancia()


def opc3():

    desactivar_botones()

    if correcto == 3:
        avanza_jug()
    else:
        mover_ignorancia()


def opc4():

    desactivar_botones()

    if correcto == 4:
        avanza_jug()
    else:
        mover_ignorancia()


def sel_preg():

    global str_preg, correcto

    tam = len(seleccion)

    if tam != 0:

        n = random.randint(0, tam - 1)

        str_preg.set(seleccion[n][1])

        str_res1.set(seleccion[n][2])
        str_res2.set(seleccion[n][3])
        str_res3.set(seleccion[n][4])
        str_res4.set(seleccion[n][5])

        try:
            correcto = int(seleccion[n][6])
        except:
            correcto = seleccion[n][6]

        if not juego_terminado:

            r1.config(state=NORMAL)
            r2.config(state=NORMAL)
            r3.config(state=NORMAL)
            r4.config(state=NORMAL)

    else:

        str_preg.set("categoria sin preguntas")

        str_res1.set("")
        str_res2.set("")
        str_res3.set("")
        str_res4.set("")

        r1.config(state=DISABLED)
        r2.config(state=DISABLED)
        r3.config(state=DISABLED)
        r4.config(state=DISABLED)


def pregunta(event):

    global seleccion

    cat = event.widget.get()
    cat = str(cat).replace("_", " ")

    str_cat_label.set(cat)

    seleccion = recupera_preguntas(cat)

    sel_preg()


def pregunta_sig():

    global seleccion, turno

    if juego_terminado:
        return

    cat = categorias.get()

    str_cat_label.set(cat)

    seleccion = recupera_preguntas(cat)

    sel_preg()

    turno += 1

    if turno > 3:
        turno = 1

    str_sig.set("jugador " + str(turno))


def edita_categoria():

    manipula_categorias()


L_cats = recupera_categoria()

cats = []

for cat in L_cats:

    cat2 = str(cat[0]).replace(" ", "_")

    cats.append(cat2)



style = ttk.Style()

style.configure(
    "Custom.TCombobox",
    font=("Arial Black", 18, "bold")
)

pantalla.option_add(
    'TComboboxListbox.font',
    ("Arial Black", 18, "bold")
)

eti_cat = Label(
    pantalla,
    bg="#1E293B",
    fg="white",
    text="Categoria",
    font=("Arial Black", 18, "bold")
)

eti_cat.place(x=10, y=10)

categorias = ttk.Combobox(
    pantalla,
    font=("Arial Black", 18, "bold")
)

categorias['values'] = L_cats

categorias.place(x=150, y=10)

categorias.bind("<<ComboboxSelected>>", pregunta)


sig = Button(
    pantalla,
    text="siguiente",
    command=pregunta_sig,
    font=("Arial Black", 14, "bold"),
    bg="#F59E0B",
    fg="white",
    activebackground="#D97706",
    activeforeground="white"
)

sig.place(x=900, y=6)



str_sig.set("jugador 1")

sig_jug = Label(
    pantalla,
    bg="#1E293B",
    fg="white",
    textvariable=str_sig,
    font=("Arial Black", 18, "bold")
)

sig_jug.place(x=500, y=10)


eti = Label(
    pantalla,
    bg="#1E293B",
    fg="white",
    text="Pregunta",
    font=("Arial Black", 18, "bold")
)

eti.place(x=10, y=60)

pre = Entry(
    pantalla,
    textvariable=str_preg,
    font=("Arial Black", 18, "bold"),
    bg="white",
    width=80
)

pre.place(x=150, y=60)


r1 = Button(
    pantalla,
    textvariable=str_res1,
    command=opc1,
    font=("Arial Black", 14, "bold"),
    bg="#334155",
    fg="white",
    activebackground="#475569",
    width=20
)

r1.place(x=100, y=110)

r2 = Button(
    pantalla,
    textvariable=str_res2,
    command=opc2,
    font=("Arial Black", 14, "bold"),
    bg="#334155",
    fg="white",
    activebackground="#475569",
    width=20
)

r2.place(x=360, y=110)

r3 = Button(
    pantalla,
    textvariable=str_res3,
    command=opc3,
    font=("Arial Black", 14, "bold"),
    bg="#334155",
    fg="white",
    activebackground="#475569",
    width=20
)

r3.place(x=620, y=110)

r4 = Button(
    pantalla,
    textvariable=str_res4,
    command=opc4,
    font=("Arial Black", 14, "bold"),
    bg="#334155",
    fg="white",
    activebackground="#475569",
    width=20
)

r4.place(x=880, y=110)



ju1 = PhotoImage(file=r"./im/cerdito 1.png")
ju2 = PhotoImage(file=r"./im/cerdito 2.png")
ju3 = PhotoImage(file=r"./im/cerdito 3.png")
bur = PhotoImage(file=r"./im/cerdito 4.png")


j1 = canvas.create_image(
    10,
    135,
    image=ju1,
    anchor=NW
)

j2 = canvas.create_image(
    10,
    220,
    image=ju2,
    anchor=NW
)

j3 = canvas.create_image(
    10,
    320,
    image=ju3,
    anchor=NW
)

bu = canvas.create_image(
    10,
    400,
    image=bur,
    anchor=NW
)



pantalla.mainloop()

def mostrar_tablero(ganador):

    tabla = Toplevel()
    tabla.title("Tablero de Resultados")
    tabla.geometry("500x350")
    tabla.config(bg="#1E293B")

    Label(
        tabla,
        text="RESULTADOS FINALES",
        font=("Arial Black", 22, "bold"),
        bg="#1E293B",
        fg="#FACC15"
    ).pack(pady=20)

    jugadores = [
        ("Jugador 1", adv1),
        ("Jugador 2", adv2),
        ("Jugador 3", adv3),
        ("Ignorante", adv_ignorancia)
    ]

    for nombre, puntos in jugadores:

        if nombre == ganador:
            color = "#22C55E"
            estado = "GANADOR"
        else:
            color = "#EF4444"
            estado = "PERDEDOR"

        Label(
            tabla,
            text=f"{nombre}  -  {puntos} puntos  -  {estado}",
            font=("Arial Black", 16),
            bg="#334155",
            fg=color,
            width=35,
            pady=8
        ).pack(pady=5)

 