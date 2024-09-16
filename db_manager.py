import pandas as pd
import sqlite3
import os


# def verify_and_create_db(db_path, excel_conf_path):
#     if not os.path.exists(db_path):
#         # Se o arquivo não existir, cria o banco de dados e a tabela
#         conn = sqlite3.connect(db_path)

#         # Criando a tabela no banco de dados principal
#         cursor = conn.cursor()

#         cursor.execute('''
#             CREATE TABLE machine_production (
#                 id INTEGER PRIMARY KEY,
#                 ip TEXT NOT NULL,
#                 machine TEXT NOT NULL,
#                 ready_carts INTEGER DEFAULT 0,
#                 curing_oven_hours FLOAT DEFAULT 0,
#                 operator_name TEXT NOT NULL DEFAULT ""
#             )
#         ''')
#         conn.commit()
#         conn.close()

#         insert_or_update_default_values(db_path, excel_conf_path)

#     else:
#         print("Banco de Dados já existe!")

# def insert_or_update_default_values(db_path, excel_conf_path):

#     df = pd.read_excel(excel_conf_path)


#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Executar consulta SQL para contar o número de linhas
#     cursor.execute(f'SELECT COUNT(*) FROM machine_production')

#     # Obter o resultado da consulta
#     count = cursor.fetchone()[0]

#     # Irá fazer os insert na tabela tablets_ips para a primeira vez que rodar
#     if count == 0: 
#         for index, row in df.iterrows():
#             cursor.execute(
#                 "INSERT INTO machine_production (id, ip, machine) VALUES (?, ?, ?);",
#                 (row["ID"], row["IP"], row["Máquina"])
#             )
#             conn.commit()

#     else: 
#         for index, row in df.iterrows():
#             try:
#                 # Atualizar os registros no banco de dados da tabela tablets_ips
#                 cursor.execute(
#                     """
#                     UPDATE machine_production
#                     SET machine = ?, ip = ?
#                     WHERE id = ?;
#                     """,
#                     (row["Máquina"], row["IP"], row["ID"])
#                 )
#                 conn.commit()

#             except:
#                 # Caso o ID não esteja presente na tabela, ele irá dar um insert
#                 cursor.execute(
#                     "INSERT INTO machine_production (id, ip, machine,) VALUES (?, ?, ?);",
#                     (row["ID"], row["IP"], row["Máquina"])
#                 )
                

#     conn.close()

# def db_get_all_machines(db_path):

#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute('SELECT * FROM machine_production')

#     data = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return data

# def db_get_machine(db_path, machine_ip):

#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute('SELECT id, ip, machine, ready_carts, curing_oven_hours, operator_name FROM machine_production WHERE ip = ?', (machine_ip,))

#     data = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     return data



# def db_add_cart(db_path, machine_ip, operator_name, curing_oven_hours):

#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     try:
#         # Verificar se o IP existe na tabela
#         cursor.execute('SELECT COUNT(*) FROM machine_production WHERE ip = ?', (machine_ip,))
#         count = cursor.fetchone()[0]

#         if count > 0:
#             # Se o IP existe, realizar o UPDATE
#             cursor.execute('''
#                 UPDATE machine_production
#                 SET ready_carts = ready_carts + ?, operator_name = ?, curing_oven_hours = ?
#                 WHERE ip = ?
#                 ''', (1, operator_name, curing_oven_hours, machine_ip)
#             )
#             conn.commit()
#             conn.close()

#             return (f"Atualizado com sucesso o IP {machine_ip} com incremento de 1.")

#         else:
#             conn.close()
#             # Se o IP não existe, tratar a situação
#             return(f"IP {machine_ip} não encontrado na tabela machine_production.")
    
#     except sqlite3.Error as e:
#         conn.close()
#         return (f"Erro ao acessar o banco de dados: {e}")
    
# def db_remove_cart(db_path, machine_ip, operator_name, curing_oven_hours):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     try:
#         # Verificar se o IP existe na tabela
#         cursor.execute('SELECT COUNT(*) FROM machine_production WHERE ip = ?', (machine_ip,))
#         count = cursor.fetchone()[0]

#         if count > 0:
#             # Se o IP existe, realizar o UPDATE
#             cursor.execute('''
#                 UPDATE machine_production
#                 SET ready_carts = ready_carts - ?, operator_name = ?, curing_oven_hours = ?
#                 WHERE ip = ?
#                 ''', (1, operator_name, curing_oven_hours, machine_ip)
#             )
#             conn.commit()
#             conn.close()

#             return (f"Atualizado com sucesso o IP {machine_ip} com decremento de 1.")

#         else:
#             conn.close()
#             # Se o IP não existe, tratar a situação
#             return(f"IP {machine_ip} não encontrado na tabela machine_production.")
    
#     except sqlite3.Error as e:
#         conn.close()
#         return (f"Erro ao acessar o banco de dados: {e}")


