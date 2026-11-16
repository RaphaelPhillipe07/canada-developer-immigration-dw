import { ArrowDown, ArrowUpRight, Check, ListOrdered } from 'lucide-react'
import { Flag } from './components'
import { useEffect, useRef } from 'react'
import { BarPanel, DataTable, GroupPanel, PeriodPanel, ScatterPanel } from './charts'
import { format, queries, rank, regions } from './data'
import './analytical-slide.css'

const topics = ['Salário','Comunidade brasileira','Moradia','Salário + comunidade','Chegadas + salário','Salário + moradia','Comunidade + moradia','Comparação entre grupos','Equilíbrio dos indicadores','Cobertura dos dados']
export const analyticalProcessSteps: string[][] = [
  ['Selecionamos as nove províncias com salário publicado para o NOC 21232.','Ordenamos os salários medianos em CAD por hora.','Comparamos o primeiro resultado e os empates seguintes.'],
  ['Agrupamos os imigrantes nascidos no Brasil por jurisdição.','Comparamos os totais censitários de cada comunidade.','Observamos os grupos por período de chegada em Ontario.'],
  ['Usamos a proporção de inquilinos que gastam pelo menos 30% da renda com moradia.','Ordenamos os percentuais das jurisdições.','Identificamos onde o comprometimento é maior.'],
  ['Cruzamos o salário mediano com o tamanho da comunidade brasileira.','Aplicamos os cortes de CAD 45,67/h e 1.122,5 pessoas.','Selecionamos as províncias que atendem aos dois critérios.'],
  ['Consideramos as chegadas de 2011–2021 nas nove províncias com salário.','Separamos as províncias com salário de pelo menos CAD 45,67/h.','Dividimos as chegadas desse grupo pelo total do recorte: 93,3%.'],
  ['Cruzamos o salário com o percentual de moradia inacessível.','Aplicamos salário de pelo menos CAD 45,67/h e moradia de até 33,3%.','Mantivemos as províncias que atendem aos dois limites.'],
  ['Cruzamos comunidade e moradia nas dez províncias.','Aplicamos as medianas de 1.122,5 pessoas e 33,3%.','Identificamos as províncias que atingem os dois cortes.'],
  ['Separamos as cinco maiores e as cinco menores comunidades provinciais.','Calculamos as medianas salariais com os valores disponíveis em cada grupo.','Comparamos as medianas de salário e de moradia inacessível.'],
  ['Normalizamos os três indicadores pela escala min–max.','Atribuímos pesos iguais, favorecendo menor comprometimento com moradia.','Ordenamos as nove províncias com os três indicadores.'],
  ['Conferimos a cobertura salarial de cada jurisdição.','Separamos as quatro sem salário provincial utilizável.','Mantivemos os indicadores censitários e marcamos o salário como “Sem dado”.'],
]

function SlideEvidence({index}:{index:number}) {
  const query=queries[index]
  if(query.chart==='coverage') return <DataTable headers={['Jurisdição','Salário · CAD/h','Brasileiros · pessoas','Moradia · %']} rows={regions.filter(region=>region.salary===null).map(region=>[region.name,'Sem dado',format('community',region.community),format('housing',region.housing)])}/>
  if(query.chart==='groups') return <GroupPanel/>
  if(query.chart==='scatter' && query.xy) return <ScatterPanel xy={query.xy} highlight={query.highlight} presentation/>
  if(query.chart==='periods') return <PeriodPanel/>
  const metric=query.chart==='scatter' ? 'salary' : query.chart
  const ranked=rank(metric)
  return <BarPanel metric={metric} items={metric==='housing' ? [...ranked].reverse() : ranked} presentation/>
}

export function AnalyticalSlide({index,revealed,onReveal}:{index:number;revealed:boolean;onReveal:()=>void}) {
  const answerHeading=useRef<HTMLHeadingElement>(null)
  const wasRevealed=useRef(revealed)
  useEffect(()=>{
    if(revealed && !wasRevealed.current) answerHeading.current?.focus({preventScroll:true})
    wasRevealed.current=revealed
  },[revealed])
  const query=queries[index]
  if(!query) return null
  const current=String(index+1).padStart(2,'0')
  const id=`analytical-${index+1}`
  return <article className={`analytical-slide${revealed ? ' is-revealed' : ' is-question'} analytical-${query.chart}`} aria-labelledby={`${id}-question`}>
    <header className="analytical-top"><a className="analytical-brand" href="#abertura" aria-label="Guia Canadá, abertura"><Flag/><strong>Guia Canadá</strong><span>IFAL · TABD 2026.2</span></a><span className="analytical-count">Consulta <b>{current}</b> de 10</span></header>
    <div className="analytical-main">
      <div className="analytical-question-heading"><p className="analytical-kicker"><span/>{topics[index]}</p><h1 id={`${id}-question`}>{query.title}</h1></div>
      {!revealed ? <div className="analytical-question-action"><button className="analytical-reveal" type="button" onClick={onReveal} aria-controls={`${id}-result`}>Ver resposta <ArrowDown size={18}/></button><span>Uma pergunta. Uma resposta orientada pelos dados.</span></div> : <div id={`${id}-result`} className="analytical-result">
        <div className="analytical-insight">
          <section className="analytical-answer" aria-labelledby={`${id}-answer-label`}><h2 id={`${id}-answer-label`} ref={answerHeading} tabIndex={-1}><Check size={15}/> Resposta</h2><p aria-live="polite">{query.answer}</p></section>
          <p className="analytical-caveat">{query.note}</p>
          <section className="analytical-process" aria-labelledby={`${id}-process`}><h2 id={`${id}-process`}><ListOrdered size={16}/>Como chegamos a esse resultado</h2><ol>{analyticalProcessSteps[index].map((step,stepIndex)=><li key={step}><span aria-hidden="true">{String(stepIndex+1).padStart(2,'0')}</span><p>{step}</p></li>)}</ol></section>
        </div>
        <section className="analytical-evidence" aria-labelledby={`${id}-evidence`}><div className="analytical-evidence-heading"><div><p>Evidência nos dados</p><h2 id={`${id}-evidence`}>{query.evidence}</h2></div><ArrowUpRight size={18} aria-hidden="true"/></div><SlideEvidence index={index}/></section>
      </div>}
    </div>
    <footer className="analytical-source"><span>Fonte e período de referência</span><p>{query.source}</p><span className="analytical-source-mark" aria-hidden="true">CANADÁ / DADOS & PERSPECTIVAS</span></footer>
  </article>
}
