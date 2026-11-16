import { useEffect, useRef, useState, type CSSProperties } from 'react'
import { motion, useReducedMotion } from 'motion/react'
import { ArrowLeft, ArrowRight, BarChart3, Check, Coins, Database, FileSearch, House, Layers3, Maximize, Minimize, Presentation, Scale, ScatterChart, Users } from 'lucide-react'
import { Flag } from './components'
import { sources } from './data'
import './method.css'

const designs=[
 {id:'a',code:'A1',name:'Fluxo visual',description:'A original refinada: fontes, Data Warehouse, análises e apresentação em um fluxo ilustrado.'},
 {id:'b',code:'A2',name:'Visão técnica',description:'O mesmo caminho, com contrato de dados, cobertura e lógica analítica explícitos.'},
 {id:'c',code:'A3',name:'Rastreabilidade',description:'Entrada → regra → saída: uma visão de como justificamos cada transformação.'},
]
const steps=[
 {title:'Reunir',label:'Fontes oficiais',icon:FileSearch,summary:'Duas fontes. Três indicadores.',detail:'Partimos de dados oficiais sobre remuneração, imigração e habitação para investigar as diferenças entre as jurisdições.',items:[['Statistics Canada','Censo 2021: imigrantes nascidos no Brasil, período de chegada e moradia.'],['Job Bank','NOC 21232: salário mediano em CAD/h, referência de 2023–2024.']]},
 {title:'Organizar',label:'Data Warehouse',icon:Database,summary:'Três fatos. Uma dimensão geográfica em comum.',detail:'O modelo Oracle separa salários, imigração e habitação em três fatos. A dimensão conformada dim_provincia conecta os temas, preservando seus grãos e períodos próprios.',items:[['Recorte comum','dim_provincia é compartilhada pelos três fatos. O modelo documenta dez dimensões e três tabelas de staging.'],['Ausência preservada','O status diferencia salário provincial, apenas regional e indisponível. Ausência não é convertida em zero.']]},
 {title:'Consultar',label:'Consultas analíticas',icon:Layers3,summary:'Transformar perguntas em comparações.',detail:'As dez consultas investigam rankings, períodos de chegada e combinações entre salário, comunidade e comprometimento com moradia.',items:[['Critérios explícitos','Cruzamentos usam cortes de referência; cada consulta explica quais.'],['Índice de equilíbrio','Normalização min–max, pesos iguais e menor comprometimento com moradia como fator favorável.']]},
 {title:'Explicar',label:'Evidências e resultados',icon:Presentation,summary:'Uma pergunta. Uma resposta. Uma evidência.',detail:'Apresentamos uma resposta direta, acompanhada de gráfico ou tabela e da explicação de como chegamos ao resultado.',items:[['Leitura sem hover','Valores, unidades e destaques precisam fazer sentido para quem está assistindo.'],['Transparência','Cada resultado informa recorte, método, fonte e período de referência.']]},
]
const number=(n:number)=>String(n).padStart(2,'0')
const technical=[
 {title:'Entradas e referências',kind:'FONTES',rows:[['Statistics Canada','Censo 2021','Comunidade · moradia'],['Job Bank','2023–2024','NOC 21232 · salário']],caption:'Os períodos de referência permanecem separados.'},
 {title:'Uma dimensão conecta três fatos',kind:'MODELO ORACLE',rows:[['dim_provincia','Dimensão','Geografia conformada'],['fato_salario','Fato','Jurisdição · ocupação · período'],['fato_imigracao','Fato','Província · origem · chegada · censo'],['fato_habitacao','Fato','Província · posse · indicador · censo']],caption:'Modelo dimensional e DDL documentados no repositório de pesquisa.'},
 {title:'Critérios reproduzíveis',kind:'ANÁLISE',rows:[['Rankings','Ordenação','Conforme o indicador'],['Cruzamentos','Cortes de referência','Explicitados por consulta'],['Equilíbrio','Min–max · pesos iguais','Nove províncias completas']],caption:'A cobertura define quais jurisdições entram em cada cálculo.'},
 {title:'Resultado com contexto',kind:'SAÍDA',rows:[['title','Pergunta','O que investigamos'],['answer','Resposta','Conclusão direta'],['evidence','Evidência','Gráfico ou tabela'],['note / source','Contexto','Método, fonte e período']],caption:'Campos das consultas usados na apresentação.'},
]
const traces=[
 {input:['Censo 2021','Job Bank 2023–2024'],rule:['Selecionar os três indicadores','Registrar a referência de cada fonte'],output:['Salário · CAD/h','Comunidade · pessoas','Moradia · %']},
 {input:['Recortes de cada fonte','Unidades e cobertura'],rule:['Alinhar por jurisdição','Preservar salário ausente'],output:['Indicadores comparáveis por lugar','Ausência identificada: Sem dado']},
 {input:['Indicadores disponíveis','Uma pergunta analítica'],rule:['Aplicar ordenação ou cortes','Respeitar a cobertura do recorte'],output:['Ranking, cruzamento ou índice','Critérios que podem ser explicados']},
 {input:['Resultado da consulta','Critério e referência'],rule:['Destacar a resposta','Mostrar evidência e limitações'],output:['Pergunta + resposta','Evidência + método + fonte']},
]
function TechnicalVisual({step}:{step:number}){
 const item=technical[step]
 return <div className="technical-visual"><header><span><Database size={14}/>{item.kind}</span><span className="tech-window-dots" aria-hidden="true"><i/><i/><i/></span></header><h3>{item.title}</h3><div className="tech-table-wrap"><table><thead><tr><th>{step===0?'Origem':step===1?'Objeto':step===2?'Consulta':'Campo'}</th><th>{step===0?'Referência':step===1?'Papel':'Regra'}</th><th>{step===1?'Recorte':'Contexto'}</th></tr></thead><tbody>{item.rows.map(row=><tr key={row[0]}>{row.map((cell,index)=>index===0?<th scope="row" key={index}>{cell}</th>:<td key={index}>{cell}</td>)}</tr>)}</tbody></table></div>{step===1&&<div className="tech-rule"><code>NULL salarial</code><ArrowRight size={14}/><b>Sem dado</b></div>}{step===2&&<div className="tech-rule"><code>filtro → cálculo → comparação</code></div>}<p className="tech-caption">{item.caption}</p></div>
}
function TraceVisual({step}:{step:number}){
 const item=traces[step]
 return <div className="trace-visual"><div className="trace-label">Rastreabilidade da etapa {number(step+1)}</div><div className="trace-columns">{[{title:'Entrada',items:item.input,icon:FileSearch},{title:'Regra',items:item.rule,icon:Layers3},{title:'Saída',items:item.output,icon:Check}].map(({title,items,icon:Icon},index)=><article key={title}><header><span>{number(index+1)}</span><Icon size={22}/></header><h3>{title}</h3><ul>{items.map(text=><li key={text}>{text}</li>)}</ul>{index<2&&<ArrowRight className="trace-arrow" size={18} aria-hidden="true"/>}</article>)}</div><p className="trace-caption">Cada saída mantém o contexto necessário para explicar o resultado.</p></div>
}
function MethodVisual({step}:{step:number}) {
 return <div className={`process-visual process-visual-${step}`}>
  {step===0&&<div className="visual-source-flow"><div className="visual-source-stack"><article className="visual-source-card"><span className="source-document"><Users size={22}/></span><div><b>Statistics Canada</b><small>Censo 2021</small></div><div className="source-tags"><span>Comunidade</span><span>Moradia</span></div></article><article className="visual-source-card"><span className="source-document"><Coins size={22}/></span><div><b>Job Bank</b><small>NOC 21232 · 2023–2024</small></div><div className="source-tags"><span>Salário</span></div></article></div><div className="visual-flow-arrow" aria-hidden="true"><ArrowRight size={26}/></div><div className="visual-indicators">{[{icon:Coins,label:'Salário',unit:'CAD/h'},{icon:Users,label:'Comunidade',unit:'pessoas'},{icon:House,label:'Moradia',unit:'%'}].map(({icon:Icon,label,unit})=><div key={label}><Icon size={21}/><span>{label}</span><b>{unit}</b></div>)}</div></div>}
  {step===1&&<div className="visual-warehouse"><div className="warehouse-input"><span>Salário</span><span>Comunidade</span><span>Moradia</span></div><ArrowRight className="warehouse-arrow" size={25}/><div className="warehouse-building"><div className="warehouse-roof"><Database size={35}/></div><strong>Data Warehouse</strong><span>Províncias e territórios</span><div className="warehouse-drawers"><i/><i/><i/></div></div><div className="warehouse-output"><span><Check size={14}/> Mesmo recorte geográfico</span><span><Check size={14}/> Unidades explícitas</span><span><Check size={14}/> “Sem dado” preservado</span></div></div>}
  {step===2&&<div className="visual-analysis"><div className="analysis-input"><Database size={29}/><b>Data Warehouse</b><span>10 perguntas</span></div><div className="analysis-branches" aria-hidden="true"/><div className="analysis-types">{[{icon:BarChart3,title:'Rankings',text:'Ordenar os indicadores'},{icon:ScatterChart,title:'Cruzamentos',text:'Comparar dois critérios'},{icon:Scale,title:'Equilíbrio',text:'Combinar três indicadores'}].map(({icon:Icon,title,text})=><article key={title}><Icon size={32}/><b>{title}</b><small>{text}</small></article>)}</div></div>}
  {step===3&&<div className="visual-result"><div className="result-mini-slide"><header><span>CONSULTA</span><i/><i/></header><div className="result-question"><span>01</span><b>Pergunta da pesquisa</b></div><div className="result-answer"><Check size={18}/><b>Resposta direta</b></div><div className="result-evidence"><BarChart3 size={50}/><div><b>Gráfico ou tabela</b><span>Valores + unidades</span></div></div><footer>Método · Fonte · Período</footer></div><div className="result-label"><Presentation size={25}/><p>Dados que podem<br/><strong>ser explicados.</strong></p></div></div>}
  <span className="visual-caption">Esquema do processo de pesquisa</span>
 </div>
}
export function MethodPreview(){
 const combined=location.hash==='#metodo'
 const [design,setDesign]=useState(/^#metodo-([abc])$/.exec(location.hash)?.[1]??'a')
 const [step,setStep]=useState(0)
 const [full,setFull]=useState(false)
 const [status,setStatus]=useState('')
 const stage=useRef<HTMLElement>(null)
 const reduce=useReducedMotion()

 function choose(id:string){setDesign(id);history.replaceState(null,'',`#metodo-${id}`)}
 useEffect(()=>{
  const change=()=>{const id=/^#metodo-([abc])$/.exec(location.hash)?.[1];if(id)setDesign(id);else if(location.hash==='#metodo')setDesign('a')}
  const fullscreen=()=>setFull(document.fullscreenElement===stage.current)
  window.addEventListener('hashchange',change);document.addEventListener('fullscreenchange',fullscreen)
  return()=>{window.removeEventListener('hashchange',change);document.removeEventListener('fullscreenchange',fullscreen)}
 },[])
 useEffect(()=>{
  const advance=(event:Event)=>{
   const next=step+Number((event as CustomEvent<number>).detail)
   if(next>3)location.hash='consulta-1'
   else if(next<0)location.hash='perguntas'
   else setStep(next)
  }
  window.addEventListener('guia-method-step',advance)
  return()=>window.removeEventListener('guia-method-step',advance)
 },[step])
 useEffect(()=>{
  const key=(event:KeyboardEvent)=>{
   if(event.altKey||event.ctrlKey||event.metaKey||event.shiftKey||event.target instanceof HTMLElement&&event.target.closest('input,select,textarea'))return
   if(event.key==='ArrowLeft'||event.key==='ArrowRight'){
    event.preventDefault();setStep(value=>Math.max(0,Math.min(3,value+(event.key==='ArrowRight'?1:-1))))
   }
  }
  window.addEventListener('keydown',key);return()=>window.removeEventListener('keydown',key)
 },[])
 async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await stage.current?.requestFullscreen()}catch{setStatus('A tela cheia está indisponível neste navegador.')}}
 return <div className={`method-preview${combined?' method-combined':''}`}>
  {!combined&&<header className="method-review"><div><small>Tela 03 · Variações da A</small><strong>Como fizemos a pesquisa</strong></div><div className="method-variants" role="group" aria-label="Variações da proposta A">{designs.map(item=><button type="button" key={item.id} aria-pressed={design===item.id} onClick={()=>choose(item.id)}><b>{item.code}</b>{item.name}</button>)}</div><a href="#metodo">Ver combinação A1 + A2 <ArrowRight size={14}/></a></header>}
  <main className={`method-stage method-a method-flavor-${design}`} ref={stage} aria-labelledby="method-title">
   <header className="method-top"><a className="method-brand" href="#abertura"><Flag/> Guia Canadá<span>Um olhar orientado por dados</span></a><span>IFAL · TABD 2026.2</span></header>
   <div className="method-heading"><div><div className="method-kicker">Nosso processo</div><h1 id="method-title">Como chegamos<br/><em>às respostas?</em></h1></div><p>Das fontes oficiais às dez consultas:<br/>um caminho que pode ser explicado.</p></div>
   <div className="method-workspace">
    <nav className="method-steps" aria-label="Etapas da pesquisa" style={{'--active-step':step,'--active-column':step%2,'--active-row':Math.floor(step/2)} as CSSProperties}><span className="method-tab-slider" aria-hidden="true"/>{steps.map((item,index)=>{const StepIcon=item.icon;return <button key={item.title} type="button" aria-pressed={step===index} onClick={()=>setStep(index)} className={step===index?'is-current':''}><span className="method-step-number">{number(index+1)}</span><StepIcon size={24}/><span className="method-step-copy"><b>{item.title}</b><small>{item.label}</small></span><ArrowRight className="method-connector" size={16}/></button>})}</nav>
    <div className="method-carousel">
     <div className="method-rail">
      {steps.map((panel,panelIndex)=>{const current=panel,Icon=panel.icon;return <motion.section initial={false} animate={{opacity:step===panelIndex?1:0}} transition={{type:'tween',duration:reduce?0:.2}} key={panel.title} className="method-detail" aria-labelledby={`method-detail-title-${panelIndex}`} aria-hidden={step!==panelIndex} inert={step!==panelIndex}>
     {combined?<><div className="combined-step-heading"><div><span className="method-detail-label"><Icon size={16}/> Etapa {number(panelIndex+1)} de 04</span><h2 id={`method-detail-title-${panelIndex}`} aria-live="polite" aria-atomic="true">{current.summary}</h2></div><details className="method-more combined-explanation"><summary>Entenda esta etapa</summary><p>{current.detail}</p>{current.items.map(([title,body])=><div key={title}><b>{title}</b><p>{body}</p></div>)}</details></div><div className="combined-visual"><span className="combined-panel-label">O caminho dos dados</span><MethodVisual step={panelIndex}/></div><div className="combined-technical"><span className="combined-panel-label">A lógica por trás</span><TechnicalVisual step={panelIndex}/></div></>:<>{design==='b'?<TechnicalVisual step={panelIndex}/>:design==='c'?<TraceVisual step={panelIndex}/>:<MethodVisual step={panelIndex}/>}<div className="method-detail-intro"><span className="method-detail-label"><Icon size={16}/> Etapa {number(panelIndex+1)} de 04</span><h2 id={`method-detail-title-${panelIndex}`} aria-live="polite" aria-atomic="true">{current.summary}</h2><p>{current.detail}</p><details className="method-more"><summary>Detalhes desta etapa</summary><div className="method-detail-items">{current.items.map(([title,body])=><article key={title}><span className="method-item-mark" aria-hidden="true"/><h3>{title}</h3><p>{body}</p></article>)}</div></details></div></>}
      </motion.section>})}
     </div>
    </div>
   </div>
   <aside className="method-caveat"><span>Antes de comparar</span><div><p>Os períodos das fontes são diferentes. A análise é descritiva; valores ausentes permanecem como <b>Sem dado</b>.</p><small>{sources.census} <i/> {sources.wages}</small></div></aside>
   <footer className="method-footer"><a href="#perguntas"><ArrowLeft size={15}/> As perguntas</a><div className="method-step-controls"><button type="button" disabled={step===0} aria-label="Etapa anterior" onClick={()=>setStep(step-1)}><ArrowLeft size={16}/></button><span>{number(step+1)} / 04</span><button type="button" disabled={step===3} aria-label="Próxima etapa" onClick={()=>setStep(step+1)}><ArrowRight size={16}/></button></div><span className="method-page-number">MÉTODO <b>03</b> / 14</span></footer>
   {document.fullscreenEnabled&&<button type="button" className="method-fullscreen" onClick={fullscreen} aria-label={full?'Sair da tela cheia':'Tela cheia'}>{full?<Minimize size={17}/>:<Maximize size={17}/>}</button>}
   {status&&<p className="method-status" role="status">{status}</p>}
  </main>
  {!combined&&<footer className="method-caption"><div><b>{designs.find(item=>item.id===design)?.code} — {designs.find(item=>item.id===design)?.name}</b><p>{designs.find(item=>item.id===design)?.description}</p></div><span>Clique nas etapas ou use ← →</span></footer>}
 </div>
}







