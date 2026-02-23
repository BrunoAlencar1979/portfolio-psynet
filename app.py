from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import string

app = Flask(__name__)

# --- CONFIGURAÇÃO DO GOOGLE SHEETS ---
def conectar_planilha():
    # Define o escopo de acesso do Google
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)
    # Abre a planilha pelo nome exato que está no seu Google Drive
    return client.open("PsyNet_Licencas").sheet1 

@app.route('/')
def home():
    return render_template('index.html')

# --- NOVA ROTA: PÁGINA DE TESTE GRÁTIS ---
@app.route('/teste-gratis')
def teste_gratis():
    return render_template('teste_gratis.html')

# --- NOVA ROTA: API QUE GERA A CHAVE MAGICA ---
@app.route('/api/gerar-chave', methods=['POST'])
def gerar_chave():
    try:
        dados = request.json
        nome_oficina = dados.get('nome')
        whatsapp = dados.get('whatsapp')

        if not nome_oficina or not whatsapp:
            return jsonify({'erro': 'Preencha todos os campos!'}), 400

        # Gera uma chave única (Ex: TRIAL-A8F2Z9)
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        chave_nova = f"TRIAL-{codigo}"

        # Calcula a data de vencimento (Hoje + 7 dias) no formato YYYY-MM-DD
        vencimento = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

        # Conecta no Google e salva o Lead na mesma hora!
        planilha = conectar_planilha()
        
        # ATENÇÃO: Ajuste a ordem de acordo com as colunas da sua planilha!
        # Exemplo: [Chave, Vencimento, Plano, Nome Oficina, WhatsApp]
        planilha.append_row([chave_nova, vencimento, "TESTE", nome_oficina, whatsapp])

        return jsonify({
            'sucesso': True,
            'chave': chave_nova,
            'mensagem': 'Chave gerada e registrada com sucesso!'
        })
    except Exception as e:
        print(f"Erro na geração da chave: {e}")
        return jsonify({'erro': 'Ocorreu um erro ao gerar a chave no servidor.'}), 500

if __name__ == '__main__':
    app.run(debug=True)