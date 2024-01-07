from flask import Flask, render_template, request, jsonify
import pandas as pd 

app = Flask(__name__)
df = pd.read_excel('bank/login.xlsx')
df['password'] = df['password'].astype(str)

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
            return render_template('adm.html')
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


if __name__ == '__main__':
    app.run(debug=True)