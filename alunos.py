import sqlite3


def conectar_bd():
    return sqlite3.connect('escola.db')


def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matriculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            curso_id INTEGER,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id),
            FOREIGN KEY (curso_id) REFERENCES cursos (id),
            UNIQUE(aluno_id, curso_id)  -- Evita duplicatas
        )
    ''')
    conn.commit()
    conn.close()


def adicionar_aluno(nome, email):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO alunos (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        print("Aluno adicionado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Email já existe.")
    conn.close()


def adicionar_curso(nome, descricao):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cursos (nome, descricao) VALUES (?, ?)', (nome, descricao))
    conn.commit()
    conn.close()
    print("Curso adicionado com sucesso!")


def matricular_aluno(aluno_id, curso_id):
    conn = conectar_bd()
    cursor = conn.cursor()
  
    cursor.execute('SELECT id FROM alunos WHERE id = ?', (aluno_id,))
    if not cursor.fetchone():
        print("Erro: Aluno não encontrado.")
        conn.close()
        return
    cursor.execute('SELECT id FROM cursos WHERE id = ?', (curso_id,))
    if not cursor.fetchone():
        print("Erro: Curso não encontrado.")
        conn.close()
        return
    try:
        cursor.execute('INSERT INTO matriculas (aluno_id, curso_id) VALUES (?, ?)', (aluno_id, curso_id))
        conn.commit()
        print("Matrícula realizada com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Aluno já matriculado neste curso.")
    conn.close()


def desmatricular_aluno(aluno_id, curso_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM matriculas WHERE aluno_id = ? AND curso_id = ?', (aluno_id, curso_id))
    if cursor.rowcount > 0:
        conn.commit()
        print("Desmatrícula realizada com sucesso!")
    else:
        print("Erro: Matrícula não encontrada.")
    conn.close()


def listar_alunos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alunos')
    alunos = cursor.fetchall()
    conn.close()
    if alunos:
        print("\nLista de Alunos:")
        for aluno in alunos:
            print(f"ID: {aluno[0]}, Nome: {aluno[1]}, Email: {aluno[2]}")
    else:
        print("Nenhum aluno encontrado.")


def listar_cursos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cursos')
    cursos = cursor.fetchall()
    conn.close()
    if cursos:
        print("\nLista de Cursos:")
        for curso in cursos:
            print(f"ID: {curso[0]}, Nome: {curso[1]}, Descrição: {curso[2]}")
    else:
        print("Nenhum curso encontrado.")


def listar_alunos_curso(curso_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT alunos.id, alunos.nome, alunos.email
        FROM alunos
        JOIN matriculas ON alunos.id = matriculas.aluno_id
        WHERE matriculas.curso_id = ?
    ''', (curso_id,))
    alunos = cursor.fetchall()
    conn.close()
    if alunos:
        print(f"\nAlunos matriculados no curso {curso_id}:")
        for aluno in alunos:
            print(f"ID: {aluno[0]}, Nome: {aluno[1]}, Email: {aluno[2]}")
    else:
        print("Nenhum aluno matriculado neste curso.")


def listar_cursos_aluno(aluno_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cursos.id, cursos.nome, cursos.descricao
        FROM cursos
        JOIN matriculas ON cursos.id = matriculas.curso_id
        WHERE matriculas.aluno_id = ?
    ''', (aluno_id,))
    cursos = cursor.fetchall()
    conn.close()
    if cursos:
        print(f"\nCursos do aluno {aluno_id}:")
        for curso in cursos:
            print(f"ID: {curso[0]}, Nome: {curso[1]}, Descrição: {curso[2]}")
    else:
        print("Nenhum curso encontrado para este aluno.")


def menu():
    criar_tabelas()  
    while True:
        print("\n--- Sistema de Gerenciamento de Alunos e Cursos ---")
        print("1. Adicionar Aluno")
        print("2. Adicionar Curso")
        print("3. Matricular Aluno em Curso")
        print("4. Desmatricular Aluno de Curso")
        print("5. Listar Alunos")
        print("6. Listar Cursos")
        print("7. Listar Alunos de um Curso")
        print("8. Listar Cursos de um Aluno")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            nome = input("Nome do aluno: ")
            email = input("Email do aluno: ")
            adicionar_aluno(nome, email)
        elif opcao == '2':
            nome = input("Nome do curso: ")
            descricao = input("Descrição do curso: ")
            adicionar_curso(nome, descricao)
        elif opcao == '3':
            aluno_id = int(input("ID do aluno: "))
            curso_id = int(input("ID do curso: "))
            matricular_aluno(aluno_id, curso_id)
        elif opcao == '4':
            aluno_id = int(input("ID do aluno: "))
            curso_id = int(input("ID do curso: "))
            desmatricular_aluno(aluno_id, curso_id)
        elif opcao == '5':
            listar_alunos()
        elif opcao == '6':
            listar_cursos()
        elif opcao == '7':
            curso_id = int(input("ID do curso: "))
            listar_alunos_curso(curso_id)
        elif opcao == '8':
            aluno_id = int(input("ID do aluno: "))
            listar_cursos_aluno(aluno_id)
        elif opcao == '9':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()