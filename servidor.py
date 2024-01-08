from flask import Flask, render_template, request, jsonify
import pandas as pd 

app = Flask(__name__)
df = pd.read_excel('bank/login.xlsx')
df['password'] = df['password'].astype(str)
df_itens = pd.read_excel('bank/itens.xlsx')

def pegar_itens():
    it=pd.read_excel('bank/itens.xlsx')
    return it.to_dict(orient='records')

def verificar_login(username, password):
    # Verifique se o usuário está presente no DataFrame
    if username not in df['user_name'].values:
        return False

    # Obtenha a senha armazenada no DataFrame
    stored_password = df[df['user_name'] == username]['password'].values[0]

    # Compare a senha armazenada com a senha fornecida
    return password == stored_password

@app.route('/recarregar_usuarios', methods=['GET'])
def recarregar_usuarios():
    # Recarrega os dados do banco de dados e retorna a lista de usuários
    df = pd.read_excel('bank/login.xlsx')
    df['password'] = df['password'].astype(str)

    users = []
    for index, row in df.iterrows():
        user_info = {'name': row['user_name'], 'password': row['password'], 'status': row['func']}
        users.append(user_info)

    return jsonify(users)

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verificar_login(username, password):
            if username =='adm':
                return render_template('adm.html')
            else:
                return render_template('bemvindo.html')
        else:
            error_message = "Senha ou usuário incorretos. Tente novamente."

    return render_template('login.html', error_message=error_message)

@app.route('/excluir_usuario', methods=['POST'])
def excluir_usuario():
    # Obtém o nome do usuário a ser excluído a partir dos dados da solicitação POST
    username = request.form['username']

    # Remove o usuário do DataFrame (ou execute a lógica de exclusão desejada)
    df.drop(df[df['user_name'] == username].index, inplace=True)
    df.to_excel('bank/login.xlsx', index=False)  # Salva as alterações no arquivo Excel

    # Recarrega os dados atualizados após a exclusão
    return recarregar_usuarios()
@app.route('/adm', methods=['GET'])
def adm():
    return render_template('adm.html')


@app.route('/cadastrar_itens', methods=['GET', 'POST'])
def cadastrar_itens():
    global df_itens
    if request.method == 'POST':
        pi = request.form['pi']
        data = request.form['data']
        item = request.form['item']
        quantidade = request.form['quantidade']

        # Verifica se a checkbox "emergencia" está marcada
        emergencia = 'emergencia' in request.form
        em = pd.DataFrame({'PI': [pi], 'Data': [data], 'Item': [item], 'Quantidade': [quantidade], 'Urgencia': [emergencia]})
        df_itens = pd.concat([df_itens, em], ignore_index=True)
        df_itens.to_excel('bank/itens.xlsx', index=False)  # Salva os dados no arquivo Excel
        print('Item cadastrado com sucesso!')

    return render_template('cadastrar_itens.html')

@app.route('/editar_itens', methods=['GET'])
def editar_itens():
    # Lógica para obter os itens do banco de dados ou DataFrame
    # Neste exemplo, usaremos df_itens, mas você deve adaptar conforme necessário

    # Converta os dados do DataFrame para uma lista de dicionários para o template
    lista_itens = pegar_itens()

    # Renderiza o template 'editar_itens.html' com os itens
    return render_template('editar.html', itens=lista_itens)

if __name__ == '__main__':
    app.run(debug=True)