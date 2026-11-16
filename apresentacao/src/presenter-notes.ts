import { queries, sources } from './data'

export type PresenterNote = {
  heading: string
  intro: string
  steps: string[]
  caveats: string[]
  handoff: string
}

/** Speaker-only prompts. Audience-facing wording and results remain in data.ts. */
export const presenterNotes: Record<string, PresenterNote> = {
  abertura: {
    heading: 'Abertura · Por que fizemos o Guia Canadá',
    intro: 'Somos Eliezir Moreira e Raphael Phillipe, do IFAL, na disciplina TABD 2026.2. Investigamos como três condições variam pelo Canadá para apoiar a pesquisa de desenvolvedores brasileiros.',
    steps: [
      'Apresente os três eixos: remuneração de desenvolvedores, comunidade de imigrantes nascidos no Brasil e comprometimento da renda dos inquilinos com moradia.',
      'Explique o recorte: dez províncias e três territórios. O projeto reúne indicadores por jurisdição em um Data Warehouse e organiza dez consultas analíticas.',
      'Diga que o objetivo é comparar cenários e explicitar critérios; prioridades pessoais continuam necessárias para interpretar os resultados.',
    ],
    caveats: ['Os dados agregam jurisdições, não cidades, vagas ou situações individuais.', 'Os salários usam NOC 21232; a comunidade conta imigrantes nascidos no Brasil, não todos os brasileiros ou descendentes.'],
    handoff: 'Antes de apresentar as respostas, vamos mostrar quais perguntas orientaram a pesquisa.',
  },
  perguntas: {
    heading: 'As dez perguntas da pesquisa',
    intro: 'As perguntas começam pelos indicadores separados e avançam para combinações, grupos, equilíbrio e cobertura dos dados.',
    steps: [
      'Percorra as primeiras três: onde estão os maiores salários, onde vivem os imigrantes e onde a moradia compromete mais a renda.',
      'Explique que as consultas 4 a 7 cruzam indicadores com cortes explícitos. A consulta 5 também considera o período de chegada entre 2011 e 2021.',
      'Feche a sequência: comparação entre grupos na 8, índice de equilíbrio na 9 e ausência de salário comparável na 10.',
      'Use a roda, os números ou as setas para mostrar que cada pergunta terá uma resposta e sua evidência própria.',
    ],
    caveats: ['Os cruzamentos são descritivos e não demonstram que um indicador causou outro.', 'A cobertura muda conforme os indicadores exigidos por cada consulta.'],
    handoff: 'Agora vamos explicar o caminho das fontes até essas respostas.',
  },
  metodo: {
    heading: 'Como chegamos às respostas',
    intro: 'O processo tem quatro etapas: reunir, organizar, consultar e explicar. Mostre o percurso e use o detalhe técnico apenas quando ajudar a justificar uma escolha.',
    steps: [
      `Reunir: ${sources.census} fornece comunidade, chegada e moradia. ${sources.wages} fornece a mediana salarial por hora.`,
      'No extrato de imigração documentado: tabela Statistics Canada 98-10-0307-01, treze DGUIDs provinciais/territoriais, idade total, gênero total e local de nascimento Brazil. As linhas Total – Place of birth são mantidas separadamente para o total de imigrantes.',
      'No extrato salarial documentado: filtrar NOC_21232 e reter registros provinciais. A publicação é o recurso Job Bank 2025, revisado em 19/11/2025, mas o período salarial é 2023–2024; annual_wage_flag = 0 confirma CAD por hora.',
      'A integração documentada é um left join das treze jurisdições censitárias com os salários provinciais por nome inglês normalizado. DGUID e código de região econômica são identificadores distintos; salário regional não substitui salário provincial.',
      'Organizar: alinhar indicadores por província ou território, manter CAD/h, pessoas e percentual e preservar salário ausente como Sem dado. O contrato de visualização usa code, salary, community e housing; esse é um recorte dos campos, não o esquema físico do banco.',
      'Consultar: ordenar valores, analisar períodos de chegada, aplicar os cortes de cada pergunta e comparar grupos. O índice de equilíbrio usa normalização min–max e pesos iguais nos três indicadores.',
      'Explicar: apresentar a pergunta completa, uma resposta direta, um gráfico ou tabela, o critério e a fonte com seu período. Os gráficos devem ser compreendidos sem hover.',
    ],
    caveats: ['Não afirmar que os períodos das duas fontes são o mesmo ano: Censo 2021 e salários 2023–2024. O nome do arquivo salarial 2025 indica a publicação, não o período de medição.', 'O README do extrato documenta imigração, salários e integração; não documenta a linhagem específica do indicador de moradia. Não atribuir moradia à tabela 98-10-0307-01.', 'O material consultado não documenta tabelas físicas, comandos SQL ou ferramenta de ETL do DW; distinguir o processo de integração documentado da implementação física.'],
    handoff: 'Começamos pelos salários medianos, usando somente as províncias com referência provincial disponível.',
  },
  'consulta-1': {
    heading: queries[0].title,
    intro: queries[0].answer,
    steps: [
      'Selecione as nove províncias cujo salário não é nulo e ordene a mediana em ordem decrescente.',
      'Mostre British Columbia em CAD 52,40/h e o empate de Alberta e Ontario em CAD 48,08/h. Saskatchewan aparece em CAD 48,07/h.',
      'Reforce a unidade CAD por hora e a referência Job Bank, NOC 21232, 2023–2024.',
    ],
    caveats: ['Mediana salarial não é remuneração garantida de uma vaga ou profissional.', 'Prince Edward Island e os três territórios não entram no ranking salarial provincial. Ausência não equivale a salário zero.'],
    handoff: 'Salário é um eixo. A próxima pergunta mostra o tamanho da comunidade e o período de chegada.',
  },
  'consulta-2': {
    heading: queries[1].title,
    intro: queries[1].answer,
    steps: [
      'Ordene as jurisdições pelo total de imigrantes nascidos no Brasil. Ontario tem 23.120; Quebec, 9.700; British Columbia, 8.765.',
      'Leia as barras por período de chegada. Em Ontario, 12.070 pertencem ao grupo de 2011–2021, o maior grupo da província.',
      'Diferencie a altura ou comprimento total da barra dos segmentos de chegada. O gráfico destaca as cinco maiores comunidades; a tabela conserva as treze jurisdições.',
    ],
    caveats: ['O universo é o Censo 2021 e pessoas nascidas no Brasil; período de chegada não é uma série anual de entradas.', 'Os totais censitários e a soma dos grupos de chegada podem diferir por arredondamento. Não substituir o total publicado pela soma dos segmentos.'],
    handoff: 'Em seguida, observamos a pressão da moradia sobre os inquilinos.',
  },
  'consulta-3': {
    heading: queries[2].title,
    intro: queries[2].answer,
    steps: [
      'Ordene em sentido decrescente o percentual de inquilinos com moradia inacessível. O recorte censitário inclui as treze jurisdições.',
      'Mostre Ontario em 38,4% e British Columbia em 37,8%. Esses percentuais representam a parcela de inquilinos dentro do universo da tabela.',
      'Explique o limite: moradia é considerada inacessível neste indicador quando o gasto atinge pelo menos 30% da renda.',
    ],
    caveats: ['38,4% não é o percentual médio da renda gasto com moradia; é o percentual de inquilinos que ultrapassa o limite.', 'O indicador não é preço de aluguel e não descreve o orçamento particular de um desenvolvedor. Fonte: Censo 2021.'],
    handoff: 'Agora cruzamos salário e comunidade para encontrar onde as duas condições coincidem.',
  },
  'consulta-4': {
    heading: queries[3].title,
    intro: queries[3].answer,
    steps: [
      'Use a mediana salarial de referência CAD 45,67/h e a mediana de comunidade de 1.122,5 pessoas. A primeira vem dos nove salários; a segunda, das dez províncias.',
      'Entre as províncias com salário disponível, filtre salário maior ou igual a CAD 45,67/h e comunidade maior ou igual a 1.122,5 pessoas.',
      'No gráfico, identifique Quebec, Ontario, Alberta e British Columbia no lado dos dois cortes favoráveis. Os nomes e valores dos destaques apoiam a leitura.',
    ],
    caveats: ['Comunidade numerosa e salário alto são definições relativas aos cortes adotados, não classificações universais.', 'A relação combina Censo 2021 e salários 2023–2024; não representa uma medição simultânea.'],
    handoff: 'A próxima consulta aplica o corte salarial às chegadas mais recentes do Censo.',
  },
  'consulta-5': {
    heading: queries[4].title,
    intro: queries[4].answer,
    steps: [
      'Restrinja às nove províncias com salário disponível e leia o grupo de chegada de 2011–2021, representado pelo quinto período dos dados.',
      'Some 25.830 pessoas em New Brunswick, Quebec, Ontario, Saskatchewan, Alberta e British Columbia, onde salário é pelo menos CAD 45,67/h.',
      'Divida por 27.680 chegadas do mesmo período nas nove províncias: 25.830 ÷ 27.680 × 100 resulta em 93,3% após arredondamento.',
      'Mostre o corte horizontal de salário e a concentração das chegadas nos pontos destacados.',
    ],
    caveats: ['Os 93,3% têm como denominador as chegadas nas nove províncias com salário; não todas as chegadas no Canadá.', 'A chegada ocorreu em 2011–2021; o salário é referência posterior de 2023–2024. Não afirmar que esses salários motivaram a imigração.'],
    handoff: 'Além da comunidade, cruzamos a remuneração com o comprometimento da renda com moradia.',
  },
  'consulta-6': {
    heading: queries[5].title,
    intro: queries[5].answer,
    steps: [
      'Exija salário provincial disponível. Aplique salário maior ou igual a CAD 45,67/h e moradia inacessível menor ou igual a 33,3%.',
      'A referência de 33,3% é a mediana da moradia nas dez províncias; a referência salarial usa nove valores publicados.',
      'Identifique New Brunswick (CAD 45,67/h; 28,0%), Quebec (CAD 45,67/h; 25,2%) e Saskatchewan (CAD 48,07/h; 33,1%). No gráfico, procure salário alto e percentual de moradia menor.',
    ],
    caveats: ['Menor percentual representa menor incidência de comprometimento entre inquilinos do recorte, não aluguel individual mais baixo.', 'Não subtrair um percentual de um salário em CAD/h. São unidades e populações diferentes.'],
    handoff: 'A consulta seguinte cruza comunidade e moradia sem exigir cobertura salarial.',
  },
  'consulta-7': {
    heading: queries[6].title,
    intro: queries[6].answer,
    steps: [
      'Use as dez províncias, excluindo os três territórios deste cruzamento. Como o salário não é exigido, Prince Edward Island participa.',
      'Aplique comunidade maior ou igual a 1.122,5 pessoas e percentual de moradia inacessível maior ou igual a 33,3%. Aqui percentual maior é a condição investigada.',
      'Destaque Ontario, Manitoba, Alberta e British Columbia. Os dois eixos vêm do mesmo Censo 2021.',
    ],
    caveats: ['A direção do corte de moradia é diferente da consulta 6: agora procuramos comunidade numerosa junto de maior incidência de moradia inacessível.', 'O resultado não demonstra que a comunidade brasileira provocou comprometimento habitacional.'],
    handoff: 'Em vez de cortes individuais, vamos comparar dois grupos de províncias.',
  },
  'consulta-8': {
    heading: queries[7].title,
    intro: queries[7].answer,
    steps: [
      'Ordene as dez províncias pelo total da comunidade. As cinco maiores são Ontario, Quebec, British Columbia, Alberta e Manitoba. As cinco menores são Nova Scotia, Saskatchewan, New Brunswick, Newfoundland and Labrador e Prince Edward Island.',
      'Compare medianas dentro dos grupos: salário CAD 48,08/h nas maiores e CAD 44,71/h nas menores; moradia inacessível 34,0% e 32,5%, respectivamente.',
      'Explicite a cobertura salarial: cinco de cinco nas maiores e quatro de cinco nas menores. Prince Edward Island não entra na mediana salarial do segundo grupo.',
      'Leia as duas escalas separadamente; o gráfico compara salário com salário e moradia com moradia.',
    ],
    caveats: ['São medianas das referências provinciais, sem ponderação pelo tamanho da população. A mediana do grupo não é um salário nacional.', 'Diferenças entre grupos são associações descritivas; cobertura desigual deve permanecer visível.'],
    handoff: 'Para combinar os três eixos, a consulta 9 usa um índice com regras explícitas.',
  },
  'consulta-9': {
    heading: queries[8].title,
    intro: queries[8].answer,
    steps: [
      'Restrinja às nove províncias com salário, comunidade e moradia disponíveis. Prince Edward Island e os três territórios não recebem pontuação.',
      'Explique a normalização min–max: salário normalizado = (salário − mínimo) ÷ (máximo − mínimo); comunidade usa a mesma lógica. Para moradia, inverta: (máximo − moradia) ÷ (máximo − mínimo).',
      'No recorte completo, os intervalos são CAD 40,87–52,40/h, 90–23.120 pessoas e 25,2–38,4%. Faça a média dos três componentes com pesos iguais e multiplique por 100.',
      'Mostre Quebec com 61,1/100 e Ontario com 54,2/100. As pontuações são fornecidas no conjunto do projeto; a interface as apresenta.',
    ],
    caveats: ['O índice é relativo ao conjunto e aos pesos escolhidos, não uma probabilidade de sucesso ou nota absoluta de qualidade de vida.', 'Normalização e pesos diferentes poderiam alterar o ranking. Um valor ausente não deve receber zero nem uma pontuação improvisada.'],
    handoff: 'Terminamos verificando onde falta salário provincial comparável.',
  },
  'consulta-10': {
    heading: queries[9].title,
    intro: queries[9].answer,
    steps: [
      'Filtre salary igual a null. As quatro jurisdições são Prince Edward Island, Yukon, Northwest Territories e Nunavut.',
      'Explique que Prince Edward Island tem apenas referência regional no recorte; ela não é tratada como salário provincial comparável.',
      'Leia Sem dado na coluna salarial e os valores censitários preservados: PE tem 85 pessoas e 30,2%; YT, 0 e 24,9%; NT, 10 e 15,6%; NU, 10 e 5,2%.',
      'Ligue essa limitação aos rankings e ao índice: a ausência reduz a cobertura salarial, mas não elimina os dados censitários.',
    ],
    caveats: ['Sem dado não é zero, e os zeros censitários são valores apresentados pela fonte, sujeitos ao seu universo e arredondamento.', 'A tabela não afirma ausência de desenvolvedores, oportunidades ou brasileiros nessas jurisdições.'],
    handoff: 'Com os resultados e os limites expostos, podemos sintetizar o que o projeto permite concluir.',
  },
  conclusoes: {
    heading: 'Conclusões · Comparar exige escolher critérios',
    intro: 'Não existe uma única jurisdição vencedora em todos os eixos. O projeto torna visíveis resultados, critérios e limites para que a comparação seja discutida.',
    steps: [
      'Retome três resultados: British Columbia lidera a mediana salarial; Ontario reúne a maior comunidade e tem maior percentual de moradia inacessível; Quebec lidera o índice com os pesos adotados.',
      'Mostre a contribuição do trabalho de DW: reunir os indicadores no recorte geográfico comum e permitir dez perguntas distintas com respostas apoiadas nos dados.',
      'Relembre os limites: agregação por jurisdição, fontes de períodos diferentes, nove salários provinciais utilizáveis e indicadores que descrevem populações específicas.',
      'Agradeça à turma e ao professor. Na discussão, abra a consulta correspondente e confirme o corte, a unidade e o período antes de interpretar uma diferença.',
    ],
    caveats: ['Os resultados apoiam pesquisa e comparação; não substituem a investigação de uma cidade, vaga ou orçamento pessoal.', 'Evite atualizar verbalmente os valores como se fossem atuais: as referências apresentadas são Censo 2021 e salários 2023–2024.'],
    handoff: 'Obrigado. Podemos discutir qualquer uma das dez perguntas e os critérios usados para respondê-la.',
  },
}
