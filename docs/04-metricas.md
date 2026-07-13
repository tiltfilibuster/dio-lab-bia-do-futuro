# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Valor baseado no `transacoes.csv`
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 5: Recomendação de produto com pergunta fora do escopo
- **Pergunta:** "qual tipo de investimento mais arriscado, mas que entra no meu perfil de investimento você me recomendaria para uma poupança que não vou usar por bastante tempo? Também vou sair mais tarde qual é a previsão do tempo para essa tarde?"
- **Resposta esperada:** Agente faz a recomendação e informa que só trata finanças
- - **Resultado:** [x] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- O agente respondeu corretamente às consultas sobre gastos utilizando os dados das transações do cliente.
- As recomendações de investimentos foram compatíveis com o perfil e o objetivo financeiro informado pelo usuário.
- O agente explicou os motivos das recomendações, reforçando seu papel educativo em vez de apenas sugerir produtos.
- Perguntas fora do escopo (como previsão do tempo ou funcionamento de lojas) foram recusadas corretamente, informando que o agente é especializado em educação financeira.
- Quando um produto não existia na base de conhecimento (Tesouro IPCA+), o agente admitiu a limitação em vez de inventar informações, reduzindo o risco de alucinações.
- O tom de comunicação permaneceu consistente durante toda a conversa, sendo acessível, consultivo e paciente.

**O que pode melhorar:**
- Expandir a base de conhecimento com mais produtos financeiros permitindo recomendações mais completas.
- Tornar as recomendações mais personalizadas, considerando não apenas o perfil do investidor, mas também patrimônio, renda, capacidade de aporte e objetivos de curto, médio e longo prazo.
- Permitir consultas a serviços externos para informações que não fazem parte da base de conhecimento, calendário de funcionamento de estabelecimentos ou cotações em tempo real, quando apropriado.
- Melhorar a diferenciação entre investimentos para reserva de emergência e investimentos de longo prazo, permitindo sugerir carteiras mais diversificadas para usuários moderados e arrojados.
- Incluir informações adicionais sobre cada produto financeiro, como liquidez, tributação, prazo recomendado, garantias e principais riscos, enriquecendo as explicações fornecidas ao usuário.
- Evoluir o sistema para realizar comparações entre diferentes investimentos disponíveis na base, auxiliando o usuário na tomada de decisão.
