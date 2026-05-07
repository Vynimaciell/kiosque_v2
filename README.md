# 🏝️ Kiosque Rental — Sistema de Reservas

> Sistema web completo para aluguel de quiosques ao ar livre, com reserva online, calendário interativo e múltiplas formas de pagamento.

🌐 **Acesse o site:** [https://kiosque-v2.onrender.com](https://kiosque-v2.onrender.com)  
👤 **Login:** `123` | **Senha:** `123`

---

## 📸 Preview

| Login | Quiosques | Reserva |
|---|---|---|
| Tela split com foto temática | Grid com fotos reais | Calendário de intervalo |

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| **Backend** | Python 3 + Flask (Blueprint pattern) |
| **Banco de dados** | SQLite via `sqlite3` nativo (sem ORM) |
| **Frontend** | HTML5 + CSS3 + JavaScript puro |
| **Fontes** | Google Fonts — Playfair Display + DM Sans |
| **Imagens** | Unsplash (URLs diretas) |
| **Deploy** | Render.com |
| **Versionamento** | Git + GitHub |

---

## ✅ Funcionalidades

- 🔐 **Autenticação** com sessão Flask
- 🏖️ **4 Quiosques** com fotos reais, descrição, capacidade e preço
- 📅 **Calendário interativo** com seleção de intervalo de datas (1 dia ou múltiplos dias)
- 🔴 **Dias reservados** aparecem em vermelho automaticamente
- 👁️ **Preview do período** ao passar o mouse antes de confirmar
- 💰 **Cálculo automático** do valor total (diárias × preço)
- 💳 **4 formas de pagamento:** PIX, Débito, Crédito e Dinheiro
- 🎴 **Cartão de crédito visual** que atualiza em tempo real ao digitar
- 🎲 **Gerador de dados aleatórios** para o cartão (demonstração)
- ✅ **Tela de confirmação** com resumo completo da reserva
- 📋 **Minhas Reservas** com histórico e opção de cancelamento
- 📱 **Responsivo** para desktop e mobile

---

## 📁 Estrutura do Projeto

```
kiosque_v2/
├── database/
│   └── kiosque.db              ← SQLite (gerado automaticamente)
├── frontend/
│   ├── css/
│   │   └── style.css           ← Estilos globais com CSS Variables
│   ├── js/
│   │   └── main.js
│   └── pages/
│       ├── login.html
│       ├── quiosques.html
│       ├── reserva.html
│       ├── confirmacao.html
│       └── minhas_reservas.html
├── src/
│   ├── app.py                  ← Entry point Flask
│   ├── routes.py               ← Todas as rotas (Blueprint)
│   └── models.py               ← Banco de dados e queries
├── Procfile                    ← Configuração do Render
├── requirements.txt            ← Dependências Python
├── render.yaml                 ← Config automática do Render
└── INICIAR.bat                 ← Iniciar localmente (Windows)
```

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.8+
- pip

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/Vynimaciell/kiosque_v2.git
cd kiosque_v2

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicie o servidor
cd src
python app.py
```

Ou no Windows, dê duplo clique em **`INICIAR.bat`**

Acesse: **http://localhost:5000**  
Login: `123` | Senha: `123`

---

## 🗄️ Banco de Dados

O banco SQLite é criado automaticamente na primeira execução com:
- Usuário padrão (`123`/`123`)
- 4 quiosques pré-cadastrados
- Reservas demo para demonstração do calendário

### Schema principal
```sql
-- Uma linha por dia reservado (permite verificação de conflitos com BETWEEN)
reservas (
  grupo_id,        -- UUID curto que agrupa dias de uma mesma reserva
  quiosque_id,
  data_reserva,    -- YYYY-MM-DD
  data_inicio,
  data_fim,
  total_dias,
  nome_cliente,
  forma_pagamento,
  status           -- 'confirmada' | 'cancelada'
)
```

---

## ☁️ Deploy

O projeto está hospedado no **Render.com** com deploy automático a cada `git push`.

**Variáveis de ambiente necessárias:**
```
SECRET_KEY=sua_chave_secreta
```

**Start command:**
```
gunicorn --chdir src app:app
```

> ⚠️ No plano gratuito do Render, o servidor dorme após 15min de inatividade. O primeiro acesso pode demorar ~30 segundos para "acordar".

---

## 📄 Licença

MIT License — sinta-se livre para usar e modificar.

---

Desenvolvido com 🌿 e muito café.
