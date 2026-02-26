import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# --- FUNÇÃO DE CONECTAR NA PLANILHA ---

def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    chave_secreta_servidor = os.environ.get('GOOGLE_CREDENTIALS')
    
    if chave_secreta_servidor:
        credenciais_dict = json.loads(chave_secreta_servidor)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
        
    client = gspread.authorize(creds)
    
    # MUDE APENAS ESTA ÚLTIMA LINHA:
    return client.open_by_key("1chg_cheVeBLPS-7mfsXol77IZ2EfIXTk3nZlg8qpAkk")

# --- ROTA 1: PÁGINA INICIAL (VITRINE PRINCIPAL) ---
@app.route('/')
def index():
    return render_template('index.html')

# --- ROTA 2: PÁGINA DE DOWNLOAD (TESTE GRÁTIS) ---
@app.route('/teste-gratis')
def teste_gratis():
    return render_template('teste_gratis.html')

# --- ROTA 3: RECEBE O FORMULÁRIO E LIBERA O DOWNLOAD ---
@app.route('/liberar_download', methods=['POST'])
def liberar_download():
    nome = request.form.get('nome')
    whatsapp = request.form.get('whatsapp')
    
    try:
        planilha_mestra = conectar_planilha()
        
        # SELECIONA A ABA 2 (Índice 1) que você criou: "Leads_Site"
        aba_leads = planilha_mestra.get_worksheet(1)
        
        data_atual = datetime.now().strftime("%d/%m/%Y")
        
        # Salva o contato de forma limpa apenas com os 3 dados necessários
        linha_nova = [nome, whatsapp, data_atual]
        aba_leads.append_row(linha_nova)
        
        # Leva o cliente para a tela final de sucesso
        return render_template('download_liberado.html', nome=nome)
        
    except Exception as e:
        print(f"Erro ao salvar lead: {e}")
        # Mesmo se der erro no Google, libera o download para o cliente não ficar travado
        return render_template('download_liberado.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)
