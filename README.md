# NCMCALC - Calculadora de Tributação para Importação

## 📋 Sobre o Projeto

**NCMCALC** é uma calculadora profissional de tributação e rentabilidade para importação no Brasil. A aplicação calcula automaticamente todos os impostos de importação (II, IPI, PIS, COFINS, ICMS) e projeta margens de lucro na revenda, oferecendo uma análise completa de rentabilidade com relatórios exportáveis.

## 🎯 Funcionalidades Principais

### 💰 Cálculo de Impostos
- **Imposto de Importação (II)** - Baseado no código NCM
- **IPI (Imposto sobre Produtos Industrializados)** - Cálculo automático
- **PIS/COFINS** - Contribuições sociais sobre importação
- **ICMS** - Imposto estadual configurável por UF
- **Custos Adicionais** - Armazenagem, marketing e outros

### 📊 Análise de Rentabilidade
- Cálculo automático de **faturamento total**
- **Lucro/prejuízo líquido** em tempo real
- **ROI (Retorno sobre Investimento)**
- **Margem sobre venda e compra**
- **Markup** e indicadores financeiros
- Gráficos interativos comparativos

### 📄 Relatórios e Exportação
- Relatórios completos de rentabilidade
- Exportação em **PDF** profissional
- Histórico de cálculos salvos
- Cenários de análise comparativa

### 🔍 Recursos Avançados
- **Busca inteligente de códigos NCM** por nome do produto
- **Conversão de moedas** em tempo real (USD/BRL)
- Interface responsiva e moderna
- Sistema de autenticação de usuários
- Dashboard com histórico de cálculos

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados principal
- **Flask-Login** - Autenticação de usuários

### Frontend
- **Bootstrap 5** - Framework CSS responsivo
- **Chart.js** - Gráficos interativos
- **Feather Icons** - Iconografia moderna
- **JavaScript Vanilla** - Funcionalidades dinâmicas

### Integrações
- **AwesomeAPI** - Cotações USD/BRL em tempo real
- **Portal Siscomex** - Códigos NCM oficiais (planejado)
- **Banco Central do Brasil** - Cotações alternativas

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.11+
- PostgreSQL (ou usar o banco incluído no Replit)
- Variáveis de ambiente configuradas

### Variáveis de Ambiente Necessárias
```bash
DATABASE_URL=postgresql://usuario:senha@host:porta/banco
SESSION_SECRET=sua_chave_secreta_aqui
```

### Instalação e Execução

1. **Clone o repositório**
```bash
git clone https://github.com/LeandroCostaeSilva/NCMCALC.git
cd NCMCALC
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python main.py
```

4. **Acesse no navegador**
```
http://localhost:5000
```

## 👤 Como Usar

### 1. **Cadastro/Login**
- Crie uma conta ou faça login
- Acesse o dashboard personalizado

### 2. **Nova Calculação**
- Clique em "Nova Calculação"
- Informe os dados do produto:
  - Nome do produto
  - Código NCM (com busca inteligente)
  - Valor CIF em USD
  - País de origem
  - Quantidade

### 3. **Análise de Resultados**
- Visualize todos os impostos calculados
- Informe o preço de venda desejado
- Analise a rentabilidade em tempo real
- Visualize gráficos comparativos

### 4. **Relatórios**
- Gere relatórios completos
- Exporte em PDF profissional
- Salve cenários para comparação

## 📈 Principais Indicadores Calculados

| Sigla | Descrição | Função |
|-------|-----------|--------|
| **PV** | Preço de Venda | Valor unitário de revenda |
| **FT** | Faturamento Total | Receita bruta total |
| **LL/PJ** | Lucro/Prejuízo Líquido | Resultado financeiro |
| **ROI** | Return on Investment | Retorno sobre investimento |
| **CPU** | Custo por Unidade | Custo individual do produto |
| **MSV** | Margem sobre Venda | % de lucro sobre faturamento |
| **MKP** | Markup | Multiplicador de preço |

## 🎯 Público-Alvo

- **Importadores** - Análise de viabilidade de importações
- **Consultores Tributários** - Cálculos precisos para clientes
- **Analistas de Compras** - Avaliação de fornecedores internacionais
- **Empresários** - Planejamento de novos produtos importados

## 🔄 Atualizações Futuras

- [ ] Integração com Portal Siscomex para NCM oficial
- [ ] Calculadora de frete internacional
- [ ] Análise de múltiplos cenários simultâneos
- [ ] API REST para integrações
- [ ] App mobile responsivo
- [ ] Relatórios em Excel/CSV

## 📞 Contato e Suporte

- **Desenvolvedor**: LeandroCostaeSilva
- **GitHub**: [https://github.com/LeandroCostaeSilva](https://github.com/LeandroCostaeSilva)
- **Projeto**: [https://github.com/LeandroCostaeSilva/NCMCALC](https://github.com/LeandroCostaeSilva/NCMCALC)

## 📜 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

**NCMCALC** - Transformando complexidade tributária em decisões inteligentes de importação! 🇧🇷✨