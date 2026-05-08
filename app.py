import os
import json
import smtplib
from email.mime.text import MIMEText
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# --- CONFIGURAÇÃO DE E-MAIL (NOTIFICAÇÃO) ---
def enviar_alerta_lead(nome, whatsapp):
    # Configurado para usar variáveis de ambiente por segurança
    EMAIL_ORIGEM = os.environ.get('EMAIL_USER') 
    SENHA_APP = os.environ.get('EMAIL_PASS')
    
    if not EMAIL_ORIGEM or not SENHA_APP:
        return # Pula se não houver configuração

    msg = MIMEText(f"Novo Lead no Site PsyNet!\n\nNome: {nome}\nWhatsApp: {whatsapp}")
    msg['Subject'] = f"🚀 Novo Lead: {nome}"
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = EMAIL_ORIGEM # Envia para você mesmo

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ORIGEM, SENHA_APP)
            server.send_message(msg)
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

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
    return client.open_by_key("1chg_cheVeBLPS-7mfsXol77IZ2EfIXTk3nZlg8qpAkk")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/erp')
def erp():
    return render_template('erp.html')

@app.route('/teste-gratis')
def teste_gratis():
    return render_template('teste_gratis.html')

@app.route('/liberar_download', methods=['POST'])
def liberar_download():
    nome = request.form.get('nome')
    whatsapp = request.form.get('whatsapp')
    
    try:
        planilha_mestra = conectar_planilha()
        aba_leads = planilha_mestra.get_worksheet(1)
        data_atual = datetime.now().strftime("%d/%m/%Y")
        
        linha_nova = [nome, whatsapp, data_atual]
        aba_leads.append_row(linha_nova)
        
        # Chamada da nova função de notificação
        enviar_alerta_lead(nome, whatsapp)
        
        return render_template('download_liberado.html', nome=nome)
    except Exception as e:
        print(f"Erro ao processar lead: {e}")
        return render_template('download_liberado.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)