import { useEffect, useState } from 'react'
import { ArrowRight, BookOpen, Coins, MapPin, Scale, Users } from 'lucide-react'
import { AnalyticalSlide } from './AnalyticalSlide'
import { OpeningPreview } from './OpeningPreview'
import { QuestionsPreview } from './QuestionsPreview'
import { MethodPreview } from './MethodPreview'
import { Flag } from './components'
import { format, queries, regionsByCode, sources } from './data'
import { pageIndex, presentationPages } from './presentation-model'
import { PresentationControls } from './PresentationControls'
import './presentation.css'

function Conclusions(){
 const [view,setView]=useState<'findings'|'sources'>('findings')
 return <main className="conclusion-slide" aria-labelledby="conclusion-title"><header className="conclusion-top"><a href="#abertura"><Flag/><strong>Guia Canadá</strong><span>IFAL · TABD 2026.2</span></a><span>Conclusões · 14 de 14</span></header><div className="conclusion-heading"><p>O que os dados nos mostram</p><h1 id="conclusion-title">Três perspectivas.<br/><em>Nenhuma escolha universal.</em></h1><p>Os indicadores mudam conforme o lugar — e a melhor comparação depende das prioridades e dos limites do recorte.</p></div><div className="conclusion-tabs" role="group" aria-label="Conteúdo das conclusões"><button type="button" aria-pressed={view==='findings'} onClick={()=>setView('findings')}>Principais resultados</button><button type="button" aria-pressed={view==='sources'} onClick={()=>setView('sources')}><BookOpen size={15}/> Fontes e limites</button></div>{view==='findings'?<div className="conclusion-content"><div className="conclusion-findings">{[{icon:Coins,label:'Maior salário mediano',place:'British Columbia',value:format('salary',regionsByCode.BC.salary),detail:'NOC 21232 · 2023–2024'},{icon:Users,label:'Maior comunidade brasileira',place:'Ontario',value:format('community',regionsByCode.ON.community),detail:'pessoas nascidas no Brasil · Censo 2021'},{icon:Scale,label:'Maior pontuação de equilíbrio',place:'Quebec',value:format('score',regionsByCode.QC.score),detail:'três indicadores · pesos iguais'}].map(({icon:Icon,label,place,value,detail})=><article key={label}><Icon size={24}/><p>{label}</p><h2>{place}</h2><strong>{value}</strong><small>{detail}</small></article>)}</div><div className="conclusion-takeaway"><MapPin size={21}/><p>Compare os indicadores em conjunto. Uma vantagem salarial pode coexistir com maior comprometimento da renda com moradia.</p></div></div>:<section className="conclusion-sources" aria-label="Fontes e limites da pesquisa"><div><a href="https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/dt-td/index-eng.cfm" target="_blank" rel="noreferrer"><b>{sources.census}</b><span>Comunidade brasileira, períodos de chegada e indicador de moradia.</span><ArrowRight size={16}/></a><a href="https://www.jobbank.gc.ca/trend-analysis/search-wages" target="_blank" rel="noreferrer"><b>{sources.wages}</b><span>Publicação de 2025; referência salarial de 2023–2024.</span><ArrowRight size={16}/></a></div><ul><li><b>Períodos diferentes.</b> A análise é descritiva e não estabelece causalidade.</li><li><b>Recorte geográfico.</b> Resultados por jurisdição não descrevem todas as cidades.</li><li><b>Cobertura salarial.</b> Quatro jurisdições permanecem como “Sem dado”.</li><li><b>Índice de equilíbrio.</b> A pontuação depende da normalização e dos pesos escolhidos.</li></ul></section>}<footer className="conclusion-credits"><p>Eliezir Moreira e Raphael Phillipe · IFAL · TABD 2026.2</p><p>{sources.census} · {sources.wages}</p><small>Foto da abertura: Kowshik Roy Sagor / Unsplash · Mapa: Natural Earth · Bandeiras: Wikimedia Commons e Steven Skelton</small></footer></main>
}

export function Presentation({page}:{page:string}){
 const [answers,setAnswers]=useState<Record<number,boolean>>({})
 const index=pageIndex(page)
 const queryMatch=/^consulta-(\d+)$/.exec(page)
 const queryIndex=queryMatch?Number(queryMatch[1])-1:-1
 const revealed=queryIndex>=0&&Boolean(answers[queryIndex])
 useEffect(()=>{
  document.title=`Guia Canadá · ${presentationPages[index]?.title??'Apresentação'}`
  window.scrollTo({top:0,behavior:'instant'})
 },[page,index])
 function reveal(){if(queryIndex>=0)setAnswers(value=>({...value,[queryIndex]:true}))}
 function next(){
  if(page==='metodo'){window.dispatchEvent(new CustomEvent('guia-method-step',{detail:1}));return}
  const nextPage=presentationPages[index+1];if(nextPage)location.hash=nextPage.id
 }
 function previous(){
  if(page==='metodo'){window.dispatchEvent(new CustomEvent('guia-method-step',{detail:-1}));return}
  const previousPage=presentationPages[index-1];if(previousPage)location.hash=previousPage.id
 }
 useEffect(()=>{
  if(typeof BroadcastChannel==='undefined')return
  const channel=new BroadcastChannel('guia-canada-live')
  const send=()=>channel.postMessage({type:'state',page,revealed})
  channel.onmessage=event=>{
   const message=event.data
   if(message?.type==='request-state')send()
   else if(message?.type==='navigate'&&presentationPages.some(item=>item.id===message.page))location.hash=message.page
   else if(message?.type==='action'){
    if(message.action==='previous')previous()
    else if(message.action==='reveal')reveal()
    else if(message.action==='next'){if(queryIndex>=0&&!revealed)reveal();else next()}
   }
  }
  send()
  return()=>channel.close()
 },[page,revealed,index,queryIndex])
 return <div className={`presentation-app presentation-page-${page} ${queryIndex>=0?'presentation-analytical':''}`}>
  {page==='abertura'&&<OpeningPreview/>}
  {page==='perguntas'&&<QuestionsPreview/>}
  {page==='metodo'&&<MethodPreview/>}
  {queryIndex>=0&&queryIndex<queries.length&&<main id="presentation-query" tabIndex={-1}><AnalyticalSlide key={queryIndex} index={queryIndex} revealed={revealed} onReveal={reveal}/></main>}
  {page==='conclusoes'&&<Conclusions/>}
  <PresentationControls page={page} revealed={revealed} onReveal={queryIndex>=0?reveal:undefined} onNext={next} onPrevious={previous}/>
 </div>
}
