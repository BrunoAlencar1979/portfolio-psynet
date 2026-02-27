# 🚀 PsyNet ERP - Versão 50 (SaaS & Desktop Híbrido)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-darkgreen.svg)
![Google API](https://img.shields.io/badge/Cloud-Google_Sheets_API-yellow.svg)
![Gemini AI](https://img.shields.io/badge/AI-Google_Gemini-blueviolet.svg)

O **PsyNet ERP** é um sistema de Gestão Empresarial (ERP) e Ponto de Venda (PDV) desenhado especificamente para Oficinas Mecânicas, Auto Centers e Lojas de Peças. 

Desenvolvido com uma arquitetura híbrida, o sistema roda localmente com alta performance (Desktop) ao mesmo tempo que comunica em tempo real com servidores Cloud (Google API) para validação de licenças SaaS (Software as a Service) e captura inteligente de Leads.

---

## 🏗️ Arquitetura do Sistema

O ecossistema PsyNet é composto por 3 pilares fundamentais:

1. **Client-Side (ERP Desktop):** Aplicação executável (`.exe`) em Python instalada na máquina do cliente, garantindo zero latência no balcão e tolerância a falhas de internet (Modo Offline Temporário).
2. **Web/Landing Page (Flask):** Funil de vendas hospedado na nuvem (Render) que captura Leads e os injeta automaticamente na base de dados central.
3. **Painel Matriz (Mini-CRM):** Dashboard administrativo exclusivo da Software House para gerir chaves de ativação, planos de subscrição e conversão de Leads via integração com a API do WhatsApp.

---

## 🛠️ Stack Tecnológico

* **Linguagem Core:** Python 3
* **Interface Gráfica (GUI):** `customtkinter` (Dark Mode nativo, componentes modernos) e `tkinter` nativo.
* **Banco de Dados Local:** MySQL (`mysql-connector-python`) com queries parametrizadas para prevenção de SQL Injection.
* **Cloud & Segurança:** Autenticação via `oauth2client` e `gspread` através de Service Accounts (JSON Keys).
* **Inteligência Artificial:** Integração com a API do Google Gemini para cotação automatizada de peças.
* **Empacotamento & Deploy:** `auto-py-to-exe` e **Inno Setup** para criação de instaladores comerciais padrão Windows.

---

## 🗄️ Estrutura do Banco de Dados (Relacional)

O motor MySQL gera automaticamente as tabelas na primeira execução (`banco_dados.py`), garantindo a integridade referencial (Foreign Keys e Cascade Deletes):

* `clientes`: Dados cadastrais e fiscais (CPF/CNPJ, CEP automatizado via ViaCEP).
* `veiculos`: Garagem do cliente, vinculada ao `id_cliente`.
* `estoque`: Controlo de inventário com alertas de `qtd_minima`.
* `ordens_servico`: Histórico de manutenção, detalhamento em JSON, status financeiro (saldo devedor) e caminho absoluto do PDF gerado.
* `vendas_balcao`: PDV Expresso para venda de peças sem vínculo a veículos.
* `orcamentos_salvos`: Rascunhos de O.S. serializados em JSON para edição posterior.
* `fornecedores`: Gestão da cadeia de suprimentos com links diretos para a Web e WhatsApp.

---

## 🔒 Segurança e Validação SaaS (Licenciamento)

O PsyNet possui proteção contra pirataria e inadimplência construída sob a infraestrutura do Google Cloud:
* **Validação por Chave:** O sistema lê um ficheiro de configuração local cifrado (`AppData`) e cruza a chave `PSYNET-XXXX` com a base de dados na nuvem através do ID único da planilha (evitando falhas de roteamento de nome).
* **Ronda Silenciosa:** Uma *Thread* em background verifica o status da assinatura a cada 60 segundos.
* **Tolerância a Falhas:** Em caso de queda de internet, o sistema entra em *Modo Offline*, permitindo o trabalho na oficina sem interromper o faturamento.

---

## ✨ Módulos e Funcionalidades Core

1. **Importador em Lote (Data Migration):** Algoritmo com `pandas` capaz de varrer dezenas de ficheiros `.xlsx` e `.csv` simultaneamente, extraindo e padronizando Nomes, Placas e Modelos através de heurística de cabeçalhos.
2. **Gerador de PDF Dinâmico:** Geração de Ordens de Serviço e Recibos com a logomarca do cliente (White-Label) e layout de alto padrão comercial.
3. **Módulo Fiscal (SEFAZ):** Integração via API para emissão automatizada de NF-e a partir de uma O.S. fechada e leitura de XML de fornecedores.
4. **Dashboard Financeiro:** Controlo de Caixa, faturamento diário/mensal e gestão inteligente de inadimplência.
5. **CRM Integrado:** Algoritmo que filtra clientes ausentes (ex: +180 dias sem abrir O.S.) e gera campanhas de retenção via WhatsApp.

---

## 👨‍💻 Autor

**Bruno Alencar** *Estudante de Engenharia da Computação (Multivix) & Desenvolvedor de Software* Focado em criar soluções reais, escaláveis e que resolvem os problemas diários do setor automóvel e comercial.
