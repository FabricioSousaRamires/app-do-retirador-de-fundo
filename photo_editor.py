import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from rembg import remove
from PIL import Image, ImageTk
import io
import os


# Função para selecionar imagem
def selecionar_imagem():
    caminho = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
    )
    entrada_var.set(caminho)
    # Atualizar as imagens 'Antes' ao selecionar
    if caminho:
        mostrar_antes(caminho)


# Função para aplicar tema (fundo verde)
def aplicar_tema():
    cor_fundo = "#2e7d32"  # Verde escuro
    janela.config(bg=cor_fundo)
    frame_principal.config(bg=cor_fundo)
    label_antes_texto.config(bg=cor_fundo, fg="white")
    label_depois_texto.config(bg=cor_fundo, fg="white")
    label_autor.config(bg=cor_fundo, fg="white")


# Função para remover o fundo com barra de progresso e mostrar imagens antes e depois
def remover_fundo():
    caminho_entrada = entrada_var.get()

    if not caminho_entrada:
        messagebox.showerror("Erro", "Selecione uma imagem primeiro!")
        return

    try:
        progresso['value'] = 0
        janela.update_idletasks()

        with open(caminho_entrada, 'rb') as input_file:
            input_data = input_file.read()

        progresso['value'] = 30
        janela.update_idletasks()

        output_data = remove(input_data)

        progresso['value'] = 70
        janela.update_idletasks()

        output = Image.open(io.BytesIO(output_data))

        pasta, nome_arquivo = os.path.split(caminho_entrada)
        nome_saida = f"{os.path.splitext(nome_arquivo)[0]}_sem_fundo.png"
        caminho_saida = os.path.join(pasta, nome_saida)

        output.save(caminho_saida)

        progresso['value'] = 100
        janela.update_idletasks()

        mostrar_depois(caminho_saida)

        messagebox.showinfo("Sucesso", f"Fundo removido!\nSalvo em:\n{caminho_saida}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        progresso['value'] = 0


def mostrar_antes(caminho):
    img = Image.open(caminho)
    largura_display = 350
    altura_display = 350
    img = img.resize((largura_display, altura_display))
    img_tk = ImageTk.PhotoImage(img)
    label_antes.config(image=img_tk)
    label_antes.image = img_tk
    label_antes_texto.config(text="Antes")
    label_depois.config(image='')  # Limpa depois
    label_depois_texto.config(text="Depois")


def mostrar_depois(caminho):
    img = Image.open(caminho)
    largura_display = 350
    altura_display = 350
    img = img.resize((largura_display, altura_display))
    img_tk = ImageTk.PhotoImage(img)
    label_depois.config(image=img_tk)
    label_depois.image = img_tk
    label_depois_texto.config(text="Depois")


# ---------- INTERFACE ----------

janela = tk.Tk()
janela.title("Photoeditor - Removedor de Fundo")

# Tela cheia
janela.state('zoomed')

# Tema verde
cor_fundo = "#2e7d32"

# Frame principal
frame_principal = tk.Frame(janela, bg=cor_fundo)
frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

# Entrada de imagem
entrada_var = tk.StringVar()

tk.Label(frame_principal, text="Selecione uma imagem:", bg=cor_fundo, fg="white", font=("Arial", 14, "bold")).pack(pady=10)
entrada_entry = tk.Entry(frame_principal, textvariable=entrada_var, width=70, font=("Arial", 12))
entrada_entry.pack(pady=5)

btn_procurar = tk.Button(frame_principal, text="Procurar Imagem", command=selecionar_imagem,
                        bg="#007acc", fg="white", font=("Arial", 12, "bold"), width=20)
btn_procurar.pack(pady=10)

# Frame para imagens antes e depois
frame_imgs = tk.Frame(frame_principal, bg=cor_fundo)
frame_imgs.pack(pady=20)

# Label texto 'Antes' e imagem
label_antes_texto = tk.Label(frame_imgs, text="Antes", bg=cor_fundo, fg="white", font=("Arial", 16, "bold"))
label_antes_texto.grid(row=0, column=0, padx=40, pady=5)

label_depois_texto = tk.Label(frame_imgs, text="Depois", bg=cor_fundo, fg="white", font=("Arial", 16, "bold"))
label_depois_texto.grid(row=0, column=1, padx=40, pady=5)

label_antes = tk.Label(frame_imgs, bg=cor_fundo)
label_antes.grid(row=1, column=0, padx=40, pady=5)

label_depois = tk.Label(frame_imgs, bg=cor_fundo)
label_depois.grid(row=1, column=1, padx=40, pady=5)

# Botão para executar remoção do fundo, logo após as imagens
btn_remover = tk.Button(frame_principal, text="Remover Fundo", command=remover_fundo,
                       bg="#ffc000", fg="black", font=("Arial", 14, "bold"), width=25)
btn_remover.pack(pady=20)

# Barra de progresso
progresso = ttk.Progressbar(frame_principal, orient="horizontal", length=600, mode="determinate")
progresso.pack(pady=10)

# Rodapé com autor
label_autor = tk.Label(frame_principal, text="Autor: @FabricioSousa", bg=cor_fundo, fg="white", font=("Arial", 10, "italic"))
label_autor.pack(side="bottom", pady=10)

# Aplicar tema
aplicar_tema()

# Loop principal
janela.mainloop()
