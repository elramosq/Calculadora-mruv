import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calcular_mruv():
    """
    Función principal que lee los datos, calcula los faltantes
    y genera las gráficas.
    """
    try:
        # 1. Leer los datos de la interfaz
        # Reemplazamos campos vacíos por None
        v0_str = entry_v0.get()
        vf_str = entry_vf.get()
        a_str = entry_a.get()
        t_str = entry_t.get()
        d_str = entry_d.get()

        v0 = float(v0_str) if v0_str else None
        vf = float(vf_str) if vf_str else None
        a = float(a_str) if a_str else None
        t = float(t_str) if t_str else None
        d = float(d_str) if d_str else None

        # 2. Lógica de cálculo (Necesitamos al menos 3 datos)
        datos_conocidos = sum(x is not None for x in [v0, vf, a, t, d])
        
        if datos_conocidos < 3:
            messagebox.showwarning("Faltan datos", "Por favor, ingrese al menos 3 valores.")
            return

        # Bucle de resolución (resuelve hasta que todos tengan valor)
        for _ in range(3):
            if d is None:
                if v0 is not None and t is not None and a is not None:
                    d = v0 * t + 0.5 * a * (t ** 2)
                elif v0 is not None and vf is not None and t is not None:
                    d = ((v0 + vf) / 2) * t
                elif v0 is not None and vf is not None and a is not None and a != 0:
                    d = (vf ** 2 - v0 ** 2) / (2 * a)

            if vf is None:
                if v0 is not None and a is not None and t is not None:
                    vf = v0 + a * t
                elif v0 is not None and a is not None and d is not None:
                    vf = (v0 ** 2 + 2 * a * d) ** 0.5 # Asume movimiento positivo

            if a is None:
                if v0 is not None and vf is not None and t is not None and t != 0:
                    a = (vf - v0) / t
                elif v0 is not None and vf is not None and d is not None and d != 0:
                    a = (vf ** 2 - v0 ** 2) / (2 * d)
                elif v0 is not None and d is not None and t is not None and t != 0:
                    a = (2 * (d - v0 * t)) / (t ** 2)

            if t is None:
                if v0 is not None and vf is not None and a is not None and a != 0:
                    t = (vf - v0) / a
                elif v0 is not None and vf is not None and d is not None and (v0 + vf) != 0:
                    t = (2 * d) / (v0 + vf)

            if v0 is None:
                if vf is not None and a is not None and t is not None:
                    v0 = vf - a * t
                elif d is not None and a is not None and t is not None and t != 0:
                    v0 = (d - 0.5 * a * (t ** 2)) / t

        # Validar si el tiempo es negativo (Físicamente imposible en este contexto)
        if t is not None and t < 0:
            messagebox.showerror("Error", "El tiempo no puede ser negativo.")
            return

        # Mostrar resultados en la interfaz
        lbl_resultado.config(
            text=f"Resultados:\n"
                 f"Velocidad Inicial (v0) = {v0:.2f} m/s\n"
                 f"Velocidad Final (vf) = {vf:.2f} m/s\n"
                 f"Aceleración (a) = {a:.2f} m/s²\n"
                 f"Tiempo (t) = {t:.2f} s\n"
                 f"Distancia (d) = {d:.2f} m",
            fg="blue"
        )

        # 3. Graficar usando Matplotlib
        graficar_mruv(v0, a, t)

    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor, ingrese solo valores numéricos válidos.")

def graficar_mruv(v0, a, t_final):
    """
    Genera las tres gráficas de cinemática: x-t, v-t, a-t
    """
    # Limpiar el frame de gráficas
    for widget in frame_graficas.winfo_children():
        widget.destroy()

    # Generar arreglo de tiempos desde 0 hasta t_final
    tiempos = np.linspace(0, t_final, 100)
    
    # Ecuaciones del MRUV para las gráficas
    posiciones = v0 * tiempos + 0.5 * a * (tiempos ** 2)
    velocidades = v0 + a * tiempos
    aceleraciones = np.full_like(tiempos, a)

    # Crear figura con 3 subgráficos (1 fila, 3 columnas)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    fig.tight_layout(pad=3.0)

    # Gráfica 1: Posición vs Tiempo
    ax1.plot(tiempos, posiciones, color='green')
    ax1.set_title('Posición vs Tiempo')
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Posición (m)')
    ax1.grid(True)

    # Gráfica 2: Velocidad vs Tiempo
    ax2.plot(tiempos, velocidades, color='blue')
    ax2.set_title('Velocidad vs Tiempo')
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Velocidad (m/s)')
    ax2.grid(True)

    # Gráfica 3: Aceleración vs Tiempo
    ax3.plot(tiempos, aceleraciones, color='red')
    ax3.set_title('Aceleración vs Tiempo')
    ax3.set_xlabel('Tiempo (s)')
    ax3.set_ylabel('Aceleración (m/s²)')
    ax3.grid(True)

    # Integrar la gráfica en la interfaz de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
    canvas.draw()
    canvas.get_tk_widget().pack()

def limpiar_campos():
    entry_v0.delete(0, tk.END)
    entry_vf.delete(0, tk.END)
    entry_a.delete(0, tk.END)
    entry_t.delete(0, tk.END)
    entry_d.delete(0, tk.END)
    lbl_resultado.config(text="Ingrese al menos 3 datos y presione Calcular")
    for widget in frame_graficas.winfo_children():
        widget.destroy()

# ==========================================
# INTERFAZ GRÁFICA (GUI) CON TKINTER
# ==========================================
root = tk.Tk()
root.title("Simulador y Graficador Interactivo MRUV - Proyecto Física")
root.geometry("900x700")
root.configure(padx=20, pady=20)

# Título
tk.Label(root, text="Calculadora y Graficador MRUV", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(root, text="Deje en blanco los campos que desea calcular (mínimo 3 datos).").pack()

# Frame para los inputs
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# Etiquetas y campos de texto
tk.Label(frame_inputs, text="Velocidad Inicial (v0) [m/s]:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_v0 = tk.Entry(frame_inputs, width=15)
entry_v0.grid(row=0, column=1)

tk.Label(frame_inputs, text="Velocidad Final (vf) [m/s]:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_vf = tk.Entry(frame_inputs, width=15)
entry_vf.grid(row=1, column=1)

tk.Label(frame_inputs, text="Aceleración (a) [m/s²]:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_a = tk.Entry(frame_inputs, width=15)
entry_a.grid(row=2, column=1)

tk.Label(frame_inputs, text="Tiempo (t) [s]:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_t = tk.Entry(frame_inputs, width=15)
entry_t.grid(row=3, column=1)

tk.Label(frame_inputs, text="Distancia (d) [m]:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
entry_d = tk.Entry(frame_inputs, width=15)
entry_d.grid(row=4, column=1)

# Botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

btn_calcular = tk.Button(frame_botones, text="Calcular y Graficar", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=calcular_mruv)
btn_calcular.pack(side=tk.LEFT, padx=10)

btn_limpiar = tk.Button(frame_botones, text="Limpiar Todo", font=("Arial", 12), bg="#f44336", fg="white", command=limpiar_campos)
btn_limpiar.pack(side=tk.LEFT, padx=10)

# Etiqueta de resultados
lbl_resultado = tk.Label(root, text="Ingrese al menos 3 datos y presione Calcular", font=("Arial", 12), justify="left")
lbl_resultado.pack(pady=10)

# Frame para las gráficas
frame_graficas = tk.Frame(root)
frame_graficas.pack(fill=tk.BOTH, expand=True)

# Iniciar la aplicación
root.mainloop()