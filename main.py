from flask import Flask
from flask import jsonify, render_template, request, make_response
# from db_manager import *
from datetime import datetime



DB_PATH = "main.db"
EXCEL_CONF_PATH = "machines_and_ips.xlsx"

app = Flask(__name__)



@app.route('/')
@app.route('/index/')
def index():


    return render_template('index.html')

#MARK: API
###########################################################################################################
############################################### API #######################################################
###########################################################################################################

# # Endpoint para obter todas as informações das máquinas
# @app.route('/get_all_machines', methods=['GET'])
# def get_items():
#     db_data = db_get_all_machines(DB_PATH)

#     data_dict = {}
#     for data in db_data:
#         id, ip, machine, ready_carts, curing_oven_hours, operator_name = data
#         data_dict[ip] = {
#             'machine': machine,
#             'ready_carts': ready_carts,
#             'curing_oven_hours': curing_oven_hours,
#             'operator_name': operator_name
#         }
        
#     return jsonify(data_dict)

# # Endpoint para obter a informação de uma máquina específica
# @app.route('/get_machine/<tablet_ip>', methods=['GET'])
# def get_item(tablet_ip):
#     db_data = db_get_machine(DB_PATH, tablet_ip)

#     if db_data:
#         id, ip, machine, ready_carts, curing_oven_hours, operator_name = db_data
#         data = {
#             'ip': ip,
#             'machine': machine,
#             'ready_carts': ready_carts,
#             'curing_oven_hours': curing_oven_hours,
#             'operator_name': operator_name
#         }
#         return jsonify(data)
#     else:
#         return jsonify({'error': 'Máquina nao encontrada'}), 404



# # Endpoint para somar um carrinho na quantidade utilizando o IP do tablet
# @app.route('/add_cart', methods=['POST'])
# def add_cart():

#     data = request.get_json()

#     # Extrair os dados
#     operator_name = data.get('operator_name')
#     curing_oven_hours = data.get('curing_oven_hours')

#     client_ip = request.remote_addr
#     client_ip = '10.80.10.43' #MARK: Atenção!! Tenho que comentar, só está para teste

#     message = db_add_cart(DB_PATH, client_ip, operator_name, curing_oven_hours)

#     return jsonify({'message': message})

# # Endpoint para somar um carrinho na quantidade utilizando o IP do tablet
# @app.route('/remove_cart', methods=['POST'])
# def remove_cart():

#     data = request.get_json()

#     # Extrair os dados
#     operator_name = data.get('operator_name')
#     curing_oven_hours = data.get('curing_oven_hours')

#     client_ip = request.remote_addr
#     client_ip = '10.80.10.43' #MARK: Atenção!! Tenho que comentar, só está para teste

#     message = db_remove_cart(DB_PATH, client_ip, operator_name, curing_oven_hours)

#     return jsonify({'message': message})


if __name__ == '__main__':

    # verify_and_create_db(DB_PATH, EXCEL_CONF_PATH)

    app.run(debug=True, host='0.0.0.0')