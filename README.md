# 🤖 AI ou Não? - Detector de Imagens do Google Gemini

Uma aplicação web que detecta se uma imagem foi gerada pelo **Google Gemini/Imagen** usando a API do Google Gemini e busca por SynthID.

## 📋 Sobre o Projeto

Esta aplicação permite que usuários façam upload de imagens e recebam uma análise sobre a probabilidade da imagem ter sido gerada especificamente pelo **Google Gemini/Imagen**. O sistema busca pela marca d'água digital **SynthID** (invisível) e analisa características visuais específicas dos modelos de IA do Google.

### 🎯 Foco: Detecção SynthID

**SynthID** é a tecnologia de marca d'água imperceptível do Google incorporada em imagens geradas por seus modelos de IA. O sistema analisa:
- Presença de SynthID (marca d'água digital do Google)
- Padrões de renderização específicos do Imagen/Gemini
- Estilo visual característico dos modelos do Google
- Diferenciação de outros geradores (DALL-E, Midjourney, Stable Diffusion)

### ⚠️ Limitações e Avisos

- **Precisão Limitada**: Esta ferramenta usa IA para analisar IA, portanto não é 100% precisa
- **Estimativa**: Os resultados devem ser interpretados como estimativas, não como certezas absolutas
- **Foco Específico**: Detecta apenas imagens do Google Gemini/Imagen (não outras IAs)
- **SynthID**: A detecção de SynthID depende da capacidade do modelo de identificar padrões imperceptíveis
- **Uso Local**: Esta versão é configurada apenas para execução local

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.x
- Flask
- Google Generative AI (Gemini)
- Flask-CORS
- Pillow (processamento de imagens)

### Frontend
- React 18
- Axios
- CSS3 (design responsivo)

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Node.js 16 ou superior
- npm ou yarn
- Chave da API do Google Gemini

## 🔑 Obter Chave da API Gemini

1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

## 🚀 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd ai_ou_nao
```

### 2. Configurar Backend

```bash
# Navegar para a pasta backend
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variável de ambiente
# Copie o arquivo .env.example para .env
copy .env.example .env

# Edite o arquivo .env e adicione sua chave da API:
# GEMINI_API_KEY=sua_chave_api_aqui
```

### 3. Configurar Frontend

```bash
# Em outro terminal, navegue para a pasta frontend
cd frontend

# Instalar dependências
npm install
```

## ▶️ Executando a Aplicação

### 1. Iniciar o Backend

```bash
# Na pasta backend (com ambiente virtual ativado)
python app.py
```

O backend estará rodando em: http://localhost:5000

### 2. Iniciar o Frontend

```bash
# Na pasta frontend (em outro terminal)
npm start
```

O frontend abrirá automaticamente em: http://localhost:3000

## 💡 Como Usar

1. Acesse http://localhost:3000 no seu navegador
2. Arraste e solte uma imagem na área de upload ou clique em "Escolher arquivo"
3. Clique em "Analisar Imagem"
4. Aguarde alguns segundos pela análise
5. Veja o resultado com:
   - **Probabilidade** (0-100%) de ter sido gerada pelo Google Gemini/Imagen
   - **Classificação** (Muito provável do Google, Provavelmente não é do Google, etc.)
   - **Análise descritiva** explicando se detectou SynthID e outros indicadores específicos do Google

## 🎨 Funcionalidades

- ✅ Upload de imagens por drag-and-drop ou seleção manual
- ✅ Preview da imagem antes da análise
- ✅ Análise usando Google Gemini com foco em SynthID
- ✅ Detecção específica de imagens do Google (não outras IAs)
- ✅ Visualização de probabilidade em gráfico circular
- ✅ Classificação por cores (vermelho = Google Gemini, verde = não é do Google)
- ✅ Análise descritiva dos indicadores incluindo SynthID
- ✅ Interface responsiva e moderna
- ✅ 3 tipos de análise: padrão, rápida e detalhada (POO)

## 📁 Estrutura do Projeto

```
ai_ou_nao/
├── backend/
│   ├── app.py              # Servidor Flask
│   ├── requirements.txt    # Dependências Python
│   ├── .env.example        # Exemplo de variáveis de ambiente
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js          # Componente principal
│   │   ├── App.css         # Estilos
│   │   ├── index.js        # Entry point
│   │   └── index.css
│   ├── package.json
│   └── .gitignore
└── README.md
```

## 🔧 Troubleshooting

### Backend não inicia
- Verifique se o ambiente virtual está ativado
- Confirme se a chave da API está configurada no arquivo `.env`
- Verifique se todas as dependências foram instaladas

### Frontend não conecta ao backend
- Confirme se o backend está rodando na porta 5000
- Verifique erros no console do navegador
- Tente limpar o cache do navegador

### Erro de CORS
- Certifique-se de que o Flask-CORS está instalado
- Verifique se o backend está configurado corretamente

## 🔒 Segurança

- **Nunca compartilhe** sua chave da API do Gemini
- O arquivo `.env` está no `.gitignore` para evitar commits acidentais
- Para produção, implemente autenticação e rate limiting

## 📝 Próximas Melhorias

- [ ] Suporte a múltiplas imagens
- [ ] Histórico de análises
- [ ] Comparação lado a lado
- [ ] Export de relatórios
- [ ] Deploy em produção
- [ ] Autenticação de usuários
- [ ] Melhorias na precisão da detecção

## 📄 Licença

Este projeto é para fins educacionais e de demonstração.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 👨‍💻 Autor

Desenvolvido como projeto de detecção de imagens geradas por IA.

---

**Aviso**: Esta ferramenta fornece estimativas baseadas em análise de IA e não deve ser usada como única fonte de verificação para decisões importantes.
