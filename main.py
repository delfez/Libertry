import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        genre TEXT,
        publisher TEXT,
        isbn TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        student_id TEXT UNIQUE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        student_id INTEGER,
        rent_date TEXT,
        return_date TEXT,
        FOREIGN KEY(book_id) REFERENCES books(id),
        FOREIGN KEY(student_id) REFERENCES students(id)
    )''')

    conn.commit()
    conn.close()

init_db()

root = tk.Tk()
root.title("Sistema de Registro de Livros")
root.geometry("1200x600")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=200)

# Abas
aba_livros = tk.Frame(notebook)
aba_alunos = tk.Frame(notebook)
aba_alugar = tk.Frame(notebook)
notebook.add(aba_livros, text="Registro de Livros")
notebook.add(aba_alunos, text="Registro de Alunos")
notebook.add(aba_alugar, text="Alugar Livros")

##########################
# Aba 1 - Registro Livros
##########################
frame_esq_livros = tk.Frame(aba_livros)
frame_esq_livros.pack(side=tk.LEFT, padx=10, pady=10)

frame_dir_livros = tk.Frame(aba_livros)
frame_dir_livros.pack(side=tk.RIGHT, padx=10, pady=10)

def buscar_livros():
    termo = entry_busca.get()
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + termo + '%',))
    resultados = c.fetchall()
    conn.close()

    text_livros.delete('1.0', tk.END)
    for b in resultados:
        text_livros.insert(tk.END, f"ID: {b[0]} | {b[1]} | {b[2]} | {b[3]} | {b[4]} | {b[5]}\n")

def deletar_livro():
    livro_id = entry_id_remover_livro.get()
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id = ?", (livro_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Removido", "Livro removido com sucesso")
    entry_id_remover_livro.delete(0, tk.END)

tk.Label(frame_esq_livros, text="Buscar Livro por Título", font=("Arial", 11)).pack()
entry_busca = tk.Entry(frame_esq_livros, font=("Arial", 11))
entry_busca.pack()
tk.Button(frame_esq_livros, text="Buscar", command=buscar_livros, font=("Arial", 11)).pack()

text_livros = tk.Text(frame_esq_livros, width=80, font=("Arial", 11), height=20)
text_livros.pack()

entry_id_remover_livro = tk.Entry(frame_esq_livros)
tk.Label(frame_esq_livros, text="ID do Livro para Remover").pack()
entry_id_remover_livro.pack()
tk.Button(frame_esq_livros, text="Remover Livro", command=deletar_livro).pack(pady=5)

def registrar_livro():
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, genre, publisher, isbn) VALUES (?, ?, ?, ?, ?)",
              (entry_titulo.get(), entry_autor.get(), entry_genero.get(), entry_editora.get(), entry_isbn.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Livro registrado com sucesso")

    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_genero.delete(0, tk.END)
    entry_editora.delete(0, tk.END)
    entry_isbn.delete(0, tk.END)

tk.Label(frame_dir_livros, text="Registro de Livro").pack()
entry_titulo = tk.Entry(frame_dir_livros)
entry_autor = tk.Entry(frame_dir_livros)
entry_genero = tk.Entry(frame_dir_livros)
entry_editora = tk.Entry(frame_dir_livros)
entry_isbn = tk.Entry(frame_dir_livros)

for label, entry in zip(["Título", "Autor", "Gênero", "Editora", "ISBN"],
                        [entry_titulo, entry_autor, entry_genero, entry_editora, entry_isbn]):
    tk.Label(frame_dir_livros, text=label).pack()
    entry.pack()

tk.Button(frame_dir_livros, text="Registrar Livro", command=registrar_livro).pack(pady=5)

###########################
# Aba 2 - Registro Alunos
###########################
frame_esq_alunos = tk.Frame(aba_alunos)
frame_esq_alunos.pack(side=tk.LEFT, padx=10, pady=10)

frame_dir_alunos = tk.Frame(aba_alunos)
frame_dir_alunos.pack(side=tk.RIGHT, padx=10, pady=10)

def buscar_aluno_nome():
    termo = entry_busca_aluno.get()
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    c.execute('''SELECT s.name, s.student_id, b.title FROM students s
                 LEFT JOIN rentals r ON s.id = r.student_id AND r.return_date IS NULL
                 LEFT JOIN books b ON r.book_id = b.id
                 WHERE s.name LIKE ?''', ('%' + termo + '%',))
    alunos = c.fetchall()
    conn.close()

    text_alunos.delete('1.0', tk.END)
    for a in alunos:
        alugado = a[2] if a[2] else "Nenhum livro alugado"
        text_alunos.insert(tk.END, f"{a[0]} | RA: {a[1]} | Livro: {alugado}\n")

def deletar_aluno():
    aluno_id = entry_id_remover_aluno.get()
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (aluno_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Removido", "Aluno removido com sucesso")
    entry_id_remover_aluno.delete(0, tk.END)

tk.Label(frame_esq_alunos, text="Buscar Aluno por Nome").pack()
entry_busca_aluno = tk.Entry(frame_esq_alunos)
entry_busca_aluno.pack()
tk.Button(frame_esq_alunos, text="Buscar", command=buscar_aluno_nome).pack()

text_alunos = tk.Text(frame_esq_alunos, width=50, height=20)
text_alunos.pack()

entry_id_remover_aluno = tk.Entry(frame_esq_alunos)
tk.Label(frame_esq_alunos, text="ID do Aluno para Remover").pack()
entry_id_remover_aluno.pack()
tk.Button(frame_esq_alunos, text="Remover Aluno", command=deletar_aluno).pack(pady=5)

def registrar_aluno():
    nome = entry_nome.get()
    ra = entry_ra.get()
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (name, student_id) VALUES (?, ?)", (nome, ra))
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno registrado")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "RA já cadastrado")
    conn.close()
    entry_nome.delete(0, tk.END)
    entry_ra.delete(0, tk.END)

tk.Label(frame_dir_alunos, text="Registro de Aluno").pack()
entry_nome = tk.Entry(frame_dir_alunos)
entry_ra = tk.Entry(frame_dir_alunos)
for label, entry in zip(["Nome", "RA"], [entry_nome, entry_ra]):
    tk.Label(frame_dir_alunos, text=label).pack()
    entry.pack()

tk.Button(frame_dir_alunos, text="Registrar Aluno", command=registrar_aluno).pack(pady=5)

#########################
# Aba 3 - Alugar Livros
#########################
frame_esq_alugar = tk.Frame(aba_alugar)
frame_esq_alugar.pack(side=tk.LEFT, padx=10, pady=10)

frame_dir_alugar = tk.Frame(aba_alugar)
frame_dir_alugar.pack(side=tk.RIGHT, padx=10, pady=10)

def listar_alugueis():
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    c.execute('''SELECT s.name, b.title, r.rent_date, r.return_date FROM rentals r
                 JOIN students s ON s.id = r.student_id
                 JOIN books b ON b.id = r.book_id''')
    dados = c.fetchall()
    conn.close()

    text_rent.delete('1.0', tk.END)
    for d in dados:
        text_rent.insert(tk.END, f"{d[0]} alugou '{d[1]}' em {d[2]} (Devolução: {d[3]})\n")

def alugar():
    livro_id = entry_livro_id.get()
    aluno_id = entry_aluno_id.get()
    data_rent = datetime.now().strftime("%d-%m-%Y")
    data_devolucao = entry_devolucao.get()

    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()
    # Verificar se o livro já está alugado
    c.execute("SELECT * FROM rentals WHERE book_id = ? AND return_date IS NULL", (livro_id,))
    if c.fetchone():
        messagebox.showwarning("Indisponível", "Este livro já está alugado.")
    else:
        c.execute("INSERT INTO rentals (book_id, student_id, rent_date, return_date) VALUES (?, ?, ?, ?)",
                  (livro_id, aluno_id, data_rent, data_devolucao))
        conn.commit()
        messagebox.showinfo("Sucesso", "Livro alugado")
    conn.close()

    entry_livro_id.delete(0, tk.END)
    entry_aluno_id.delete(0, tk.END)
    entry_devolucao.delete(0, tk.END)

tk.Label(frame_esq_alugar, text="ID do Livro").pack()
entry_livro_id = tk.Entry(frame_esq_alugar)
entry_livro_id.pack()
tk.Label(frame_esq_alugar, text="ID do Aluno").pack()
entry_aluno_id = tk.Entry(frame_esq_alugar)
entry_aluno_id.pack()
tk.Label(frame_esq_alugar, text="Data de Devolução (DD-MM-YYYY)").pack()
entry_devolucao = tk.Entry(frame_esq_alugar)
entry_devolucao.pack()

tk.Button(frame_esq_alugar, text="Alugar Livro", command=alugar).pack(pady=10)

text_rent = tk.Text(frame_dir_alugar, width=80, height=25)
text_rent.pack()
tk.Button(frame_dir_alugar, text="Mostrar Aluguéis", command=listar_alugueis).pack(pady=5)

root.mainloop()
