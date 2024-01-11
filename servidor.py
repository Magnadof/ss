from flask import Flask, render_template, request, jsonify,redirect,url_for
import pandas as pd 


app = Flask(__name__)
df = pd.read_excel('bank/login.xlsx')
df['password'] = df['password'].astype(str)
df_itens = pd.read_excel('bank/itens.xlsx')

def obter_item_por_pi(pi):
    item = df_itens[df_itens['PI'] == pi].to_dict(orient='records')
    return item[0] if item else None




def pegar_itens():
    it=pd.read_excel('bank/itens.xlsx')
    itens=it.to_dict(orient='records')
    return itens

def verificar_login(username, password):
    df
    username=username.lower()
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
            if username.lower() =='adm':
                return render_template('adm.html')
            elif username != 'adm':
                return render_template('bemvindo.html') 
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
        em = pd.DataFrame({'PI': [pi], 'Data': [data], 'Item': [item], 'Quantidade': [quantidade], 'Urgencia': [emergencia],"Status": "Em esperae"})
        df_itens = pd.concat([df_itens, em], ignore_index=True)
        df_itens.to_excel('bank/itens.xlsx', index=False)
        df_itens=pd.read_excel('bank/itens.xlsx')  # Salva os dados no arquivo Excel
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

@app.route('/editar/<pi>', methods=['GET'])

def editar_item(pi):
    item = obter_item_por_pi(int(pi))
 

    if item is not None:
        # Se o item existir, renderiza a página de edição com as informações do item
        print(f"Item encontrado: {item}")
        return render_template('edit_20.html', item=item)
    else:
        # Se o item não for encontrado, redireciona para a página de edição principal
        print("Item não encontrado.")
        return render_template('editar.html')
    


@app.route('/salvar_edicoes', methods=['POST'])
def salvar_edicoes():
    pi = request.form['pi']
    data = request.form['data']
    item = request.form['item']
    quantidade = request.form['quantidade']
    urgencia = 'emergencia' in request.form
    excluir_pi = 'excluir' in request.form
    status = request.form['status']

    # Verifique se a opção "Excluir PI" foi selecionada
    if excluir_pi:
        itens_a_excluir = df_itens[df_itens['PI'] == int(pi)].index
        # Remova esses itens do DataFrame
        df_itens.drop(itens_a_excluir, inplace=True)
    else:
      
        # Atualize as informações do item no DataFrame df_itens
        df_itens.loc[df_itens['PI'] == int(pi), ['Data', 'Item', 'Quantidade', 'Urgencia', 'Status']] = [data, item, quantidade, urgencia, status]

    # Salve as alterações no arquivo Excel
    df_itens.to_excel('bank/itens.xlsx', index=False)

    return redirect(url_for('editar_itens'))


@app.route('/emergencia', methods=['GET'])
def emergencia_status():
    # Filtra os itens de emergência do DataFrame df_itens
    itens_emergencia = df_itens[df_itens['Urgencia'] == True].to_dict(orient='records')

    return render_template('emergencia.html', itens_emergencia=itens_emergencia)


@app.route('/status', methods=['GET'])
def status():
    lista_itens = pegar_itens()
    return render_template('status.html', itens=lista_itens)


if __name__ == '__main__':
    app.run(debug=True)