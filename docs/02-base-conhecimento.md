# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo                     | Formato | Utilização no Agente                                                                                                                       |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `historico_atendimento.csv` | CSV     | Recupera atendimentos anteriores para manter contexto e evitar repetir recomendações.                                                      |
| `perfil_investidor.json`    | JSON    | Armazena informações pessoais e financeiras do cliente, como perfil de investidor, patrimônio, objetivos e reserva de emergência.          |
| `produtos_financeiros.json` | JSON    | Contém os produtos financeiros disponíveis para recomendação, incluindo categoria, risco, rentabilidade, aporte mínimo e público indicado. |
| `transacoes.csv`            | CSV     | Registra o histórico de transações financeiras do cliente para análise de gastos, receitas e padrões de consumo.                           |

Todos os arquivos são utilizados como base de conhecimento do agente e permanecem armazenados localmente.

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

foi aumentado as opções de 

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Todos os arquivos são carregados automaticamente no início da execução da aplicação utilizando a função `carregar_dados()`. Essa função utiliza `json.load()` para arquivos JSON e `pandas.read_csv()` para arquivos CSV.
Os dados permanecem em memória durante toda a sessão graças ao decorador `@st.cache_data`, reduzindo o tempo de carregamento e evitando leituras repetidas do disco.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Antes de cada pergunta, a aplicação monta dinamicamente um contexto contendo:

* Informações do perfil do cliente;
* Objetivos financeiros;
* Patrimônio e reserva de emergência;
* Histórico de transações;
* Histórico de atendimentos;
* Produtos financeiros disponíveis.

Além disso, o histórico da conversa é armazenado utilizando `st.session_state.messages`, permitindo que o modelo mantenha memória básica durante a sessão.

Todo esse contexto é concatenado ao prompt enviado ao modelo Gemma 4 executado localmente através do Ollama.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
CLIENTE

Nome: João Silva
Idade: 32 anos
Perfil do Investidor: Moderado

Objetivo:
Construir reserva de emergência.

Patrimônio:
R$ 15.000,00

Reserva de Emergência:
R$ 10.000,00

Transações Recentes

03/10 - Supermercado - R$ 450,00
10/10 - Restaurante - R$ 120,00
15/10 - Salário - R$ 5.000,00

Histórico de Atendimentos

Cliente demonstrou interesse em investimentos de baixo risco e solicitou orientações para aumentar sua reserva de emergência.

Produtos Disponíveis

- Tesouro Selic
- CDB com Liquidez Diária
- LCI/LCA
- Fundo Multimercado
- Fundo de Ações

Histórico da Conversa

Usuário: Quanto gastei com alimentação?

Assistente: Você gastou R$ 570,00 com alimentação.

Pergunta Atual

Qual investimento você recomenda?
```
