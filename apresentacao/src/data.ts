export type Region = {
  code: string; name: string; salary: number | null; community: number;
  housing: number; periods: number[]; score: number | null; tile: [number, number];
}

const rows: [string, string, number | null, number, number, number[], number | null, [number, number]][] = [
  ['NL','Newfoundland and Labrador',43.75,90,32.5,[0,0,0,40,50],23.2251,[9,2]],
  ['PE','Prince Edward Island',null,85,30.2,[10,0,0,10,60],null,[9,4]],
  ['NS','Nova Scotia',40.87,435,34.7,[25,10,25,75,305],9.8428,[9,5]],
  ['NB','New Brunswick',45.67,240,28,[0,15,10,15,205],40.3566,[8,4]],
  ['QC','Quebec',45.67,9700,25.2,[305,365,625,3115,5285],61.1196,[7,3]],
  ['ON','Ontario',48.08,23120,38.4,[1570,1115,2950,5420,12070],54.1775,[6,4]],
  ['MB','Manitoba',41.03,1810,33.5,[90,55,35,135,1495],15.3258,[5,3]],
  ['SK','Saskatchewan',48.07,380,33.1,[15,60,25,65,220],34.6188,[4,3]],
  ['AB','Alberta',48.08,3800,34,[220,160,320,1110,1985],37.3251,[3,3]],
  ['BC','British Columbia',52.4,8765,37.8,[505,250,530,1410,6065],47.4046,[2,3]],
  ['YT','Yukon',null,0,24.9,[0,0,0,0,0],null,[1,2]],
  ['NT','Northwest Territories',null,10,15.6,[0,0,10,0,0],null,[3,2]],
  ['NU','Nunavut',null,10,5.2,[0,0,0,0,0],null,[5,1]],
]

export const regions: Region[] = rows.map(([code,name,salary,community,housing,periods,score,tile]) => ({code,name,salary,community,housing,periods,score,tile}))
export const regionsByCode = Object.fromEntries(regions.map(region => [region.code, region]))
export const periods = ['Antes de 1980','1980–1990','1991–2000','2001–2010','2011–2021']
export const metrics = {
  salary: {label:'Salário', title:'Salário mediano', unit:'CAD/h', scale:60},
  community: {label:'Comunidade', title:'Imigrantes nascidos no Brasil', unit:'pessoas', scale:25000},
  housing: {label:'Moradia', title:'Inquilinos com moradia inacessível', unit:'%', scale:50},
} as const
export type Metric = keyof typeof metrics
export const metricKeys = Object.keys(metrics) as Metric[]
export type Priority = Metric | 'score'
export const sources = {
  census: 'Statistics Canada · Censo 2021',
  wages: 'Job Bank · NOC 21232 · 2023–2024',
}
export const priorityLabels: Record<Priority,string> = {salary:'Salário',community:'Comunidade',housing:'Moradia',score:'Equilíbrio'}
const number = (value: number, digits = 0) => value.toLocaleString('pt-BR',{minimumFractionDigits:digits,maximumFractionDigits:digits})
export function format(metric: Priority, value: number | null) {
  if (value === null) return 'Sem dado'
  if (metric === 'salary') return `CAD ${number(value,2)}/h`
  if (metric === 'housing') return `${number(value,1)}%`
  if (metric === 'score') return `${number(value,1)}/100`
  return number(value)
}
export function rank(metric: Priority) {
  return regions.filter(region => region[metric] !== null).sort((a,b) => {
    const difference = (a[metric] ?? 0) - (b[metric] ?? 0)
    return (metric === 'housing' ? difference : -difference) || a.name.localeCompare(b.name)
  })
}

type Query = {title:string; answer:string; note:string; evidence:string; source:string; chart:Metric | 'periods' | 'score' | 'coverage' | 'groups' | 'scatter'; xy?:[Metric | 'arrivals',Metric]; highlight?:string[]}
export const queries: Query[] = [
  {title:'Onde estão os maiores salários medianos?',answer:'British Columbia lidera com CAD 52,40/h.',note:'Alberta e Ontario empatam em CAD 48,08/h. Há nove salários provinciais publicados.',evidence:'Salário mediano por província · CAD/h',source:sources.wages,chart:'salary'},
  {title:'Onde moram os imigrantes brasileiros e quando chegaram?',answer:'Ontario reúne 23.120 imigrantes nascidos no Brasil. O maior grupo na província chegou entre 2011 e 2021.',note:'Quebec (9.700) e British Columbia (8.765) vêm em seguida no total de imigrantes.',evidence:'Imigrantes nascidos no Brasil por período de chegada',source:sources.census,chart:'periods'},
  {title:'Onde a moradia pesa mais na renda dos inquilinos?',answer:'Ontario (38,4%) e British Columbia (37,8%) têm os maiores percentuais.',note:'O indicador conta os inquilinos que gastam pelo menos 30% da renda com moradia no universo da tabela.',evidence:'Inquilinos com moradia inacessível · %',source:sources.census,chart:'housing'},
  {title:'Onde salário alto e comunidade brasileira numerosa coincidem?',answer:'Quebec, Ontario, Alberta e British Columbia atendem aos dois critérios.',note:'Os cortes são as medianas de referência: CAD 45,67/h e 1.122,5 pessoas.',evidence:'Comunidade brasileira × salário mediano',source:`${sources.wages} · ${sources.census}`,chart:'scatter',xy:['community','salary'],highlight:['QC','ON','AB','BC']},
  {title:'Como as chegadas entre 2011 e 2021 se distribuem por salário?',answer:'93,3% das chegadas ocorreram nas províncias com salário mediano de pelo menos CAD 45,67/h.',note:'O percentual considera nove províncias com salários disponíveis. O período de chegada vem do Censo 2021 e a referência salarial é de 2023–2024.',evidence:'Chegadas em 2011–2021 × salário mediano',source:`${sources.wages} · ${sources.census}`,chart:'scatter',xy:['arrivals','salary'],highlight:['NB','QC','ON','SK','AB','BC']},
  {title:'Onde há salário alto e menor comprometimento com moradia?',answer:'New Brunswick, Quebec e Saskatchewan atendem aos dois critérios.',note:'Os cortes são salário mediano de pelo menos CAD 45,67/h e inacessibilidade habitacional de até 33,3%.',evidence:'Inacessibilidade habitacional × salário mediano',source:`${sources.wages} · ${sources.census}`,chart:'scatter',xy:['housing','salary'],highlight:['NB','QC','SK']},
  {title:'Onde comunidade numerosa e moradia menos acessível coincidem?',answer:'Ontario, Manitoba, Alberta e British Columbia atingem as duas medianas de referência.',note:'O recorte inclui dez províncias. Os cortes são 1.122,5 pessoas e 33,3% de inacessibilidade habitacional.',evidence:'Comunidade brasileira × inacessibilidade habitacional',source:sources.census,chart:'scatter',xy:['community','housing'],highlight:['ON','MB','AB','BC']},
  {title:'Como se comparam os grupos com maior e menor presença brasileira?',answer:'O grupo das cinco maiores comunidades tem medianas mais altas em salário e inacessibilidade habitacional.',note:'O grupo com as menores comunidades tem dados salariais para quatro de suas cinco províncias.',evidence:'Medianas por grupo de presença brasileira',source:`${sources.wages} · ${sources.census}`,chart:'groups'},
  {title:'Quais províncias equilibram os três indicadores?',answer:'Quebec lidera com 61,1/100, seguido de Ontario com 54,2/100.',note:'O índice usa normalização min–max, pesos iguais e pontuação maior para menor comprometimento com moradia.',evidence:'Pontuação de equilíbrio · escala de 0 a 100',source:`${sources.wages} · ${sources.census}`,chart:'score'},
  {title:'Quais jurisdições não têm salário provincial utilizável?',answer:'Prince Edward Island, Yukon, Northwest Territories e Nunavut.',note:'Prince Edward Island tem apenas referência regional. Os indicadores censitários continuam disponíveis para as quatro jurisdições.',evidence:'Cobertura salarial e dados censitários disponíveis',source:`${sources.wages} · ${sources.census}`,chart:'coverage'},
]

export const tips = [
  ['Compare o salário com suas despesas','Use a mediana horária como referência e estime aluguel, transporte e outras despesas para o cenário que pretende avaliar.'],
  ['Pesquise a cidade em que pretende morar','O painel agrega dados por jurisdição. Condições de emprego e moradia podem variar entre cidades da mesma província.'],
  ['Confira as datas de cada fonte','Comunidade e moradia vêm do Censo 2021. Os salários representam o período 2023–2024.'],
  ['Considere o tamanho do recorte','O salário corresponde ao grupo NOC 21232. Pesquise também a nomenclatura usada em vagas compatíveis com sua experiência.'],
  ['Leia “sem dado” como ausência de cobertura','Quatro jurisdições não têm salário provincial comparável neste conjunto.'],
  ['Use a comunidade como um ponto de partida','O total censitário ajuda a escolher onde buscar associações, redes profissionais e informações locais.'],
  ['Entenda o indicador de moradia','A taxa indica a parcela de inquilinos que gasta pelo menos 30% da renda com moradia, dentro do universo da tabela.'],
  ['Compare opções com critérios diferentes','Uma jurisdição pode aparecer bem em salário e ter uma proporção alta de inquilinos com moradia inacessível.'],
  ['Abra as fontes antes de tomar decisões','Use as referências oficiais para confirmar a cobertura e procurar atualizações.'],
  ['Monte sua própria lista de prioridades','Compare dois lugares de cada vez e registre quais aspectos têm mais peso para você.'],
]
