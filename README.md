# 🏝️ Kiosque Rental — Sistema de Reservas

Sistema web para reserva de quiosques, desenvolvido em Python (Flask) com banco de dados SQLite.

---

## 📁 Estrutura do Projeto

```
kiosque_rental/
├── database/
│   └── kiosque.db          ← Banco de dados SQLite (gerado automaticamente)
├── frontend/
│   ├── css/
│   │   └── style.css       ← Estilos globais
│   ├── js/
│   │   └── main.js         ← Interatividade (disponibilidade, pagamento)
│   └── pages/
│       ├── login.html
│       ├── quiosques.html
│       ├── reserva.html
│       ├── confirmacao.html
│       └── minhas_reservas.html
├── src/
│   ├── app.py              ← Ponto de entrada Flask
│   ├── routes.py           ← Todas as rotas da aplicação
│   └── models.py           ← Banco de dados e queries
├── INICIAR.bat             ← Inicia o sistema (duplo clique)
└── README.md
```

---

## 🚀 Como Iniciar

1. Certifique-se de ter o **Python 3.8+** instalado
2. Dê **duplo clique** em `INICIAR.bat`
3. O sistema instala o Flask automaticamente e abre o navegador
4. Acesse: **http://localhost:5000**

---

## 🔑 Acesso Padrão

| Campo  | Valor |
|--------|-------|
| Login  | `123` |
| Senha  | `123` |

---

## ✅ Funcionalidades

- Login com autenticação
- 4 Quiosques disponíveis para reserva
- Verificação de disponibilidade em tempo real
- Alerta quando a data já está ocupada
- Regras de uso exibidas antes da confirmação
- Pagamento: PIX, Débito, Crédito ou Dinheiro
- Tela de confirmação com resumo completo
- Histórico de reservas com opção de cancelamento

---

## 🛠️ Tecnologias

- **Backend**: Python 3 + Flask
- **Banco de dados**: SQLite
- **Frontend**: HTML5 + CSS3 + JavaScript puro
