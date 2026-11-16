import { useEffect, useRef, useState } from 'react'
import { motion, useReducedMotion, type Transition } from 'motion/react'
import { ArrowLeft, ChevronDown, ChevronUp, Coins, House, Maximize, Minimize, Users } from 'lucide-react'
import { Flag } from './components'
import { CanadaMap } from './CanadaMap'
import { queries } from './data'
import './questions.css'
import './question-variants.css'

const directions=[
 {id:'a',name:'Foco vermelho',description:'Fundo vermelho canadense e pergunta em cartão creme.'},
 {id:'b',name:'Editorial claro',description:'Fundo creme e pergunta em destaque vermelho.'},
 {id:'c',name:'Cartões em cena',description:'Vinho profundo, cartões individuais e numeração em grande escala.'},
]
const animations=[{id:'wheel',name:'Relógio 3D'},{id:'glide',name:'Deslize suave'},{id:'bounce',name:'Cartões com bounce'}] as const
const defaults:Record<string,string>={a:'wheel',b:'glide',c:'bounce'}
const two=(n:number)=>String(n).padStart(2,'0')
export function QuestionsPreview(){
 const comparing=/^#perguntas-[abc]$/.test(location.hash)
 const [variant,setVariant]=useState(/^#perguntas-([abc])$/.exec(location.hash)?.[1]??'a')
 const [animation,setAnimation]=useState(defaults[/^#perguntas-([abc])$/.exec(location.hash)?.[1]??'a'])
 const [selected,setSelected]=useState(0)
 const [full,setFull]=useState(false)
 const [status,setStatus]=useState('')
 const stage=useRef<HTMLElement>(null)
 const wheel=useRef<HTMLDivElement>(null)
 const selectedRef=useRef(0)
 const reduced=useReducedMotion()
 const refined=true
 const rowHeight=refined?136:112
 const active=directions.find(item=>item.id===variant)??directions[0]
 function select(next:number){const value=Math.max(0,Math.min(queries.length-1,next));selectedRef.current=value;setSelected(value)}
 function choose(id:string){setVariant(id);setAnimation(defaults[id]);history.replaceState(null,'',`#perguntas-${id}`)}
 useEffect(()=>{
  const hash=()=>{const value=/^#perguntas-([abc])$/.exec(location.hash)?.[1];if(value){setVariant(value);setAnimation(defaults[value])}else if(location.hash==='#perguntas'){setVariant('a');setAnimation('wheel')}}
  const fullscreen=()=>setFull(document.fullscreenElement===stage.current)
  window.addEventListener('hashchange',hash);document.addEventListener('fullscreenchange',fullscreen)
  return()=>{window.removeEventListener('hashchange',hash);document.removeEventListener('fullscreenchange',fullscreen)}
 },[])
 useEffect(()=>{
  let accumulated=0,last=0
  const onWheel=(event:WheelEvent)=>{
   if(Math.abs(event.deltaX)>Math.abs(event.deltaY)||event.ctrlKey)return
   event.preventDefault()
   const now=performance.now()
   if(now-last<260)return
   accumulated+=event.deltaY*(event.deltaMode===1?16:event.deltaMode===2?200:1)
   if(Math.abs(accumulated)<32)return
   select(selectedRef.current+Math.sign(accumulated));accumulated=0;last=now
  }
  const el=wheel.current;el?.addEventListener('wheel',onWheel,{passive:false})
  return()=>el?.removeEventListener('wheel',onWheel)
 },[])
 useEffect(()=>{
  const key=(event:KeyboardEvent)=>{
   if(event.altKey||event.ctrlKey||event.metaKey||event.shiftKey||event.target instanceof HTMLElement&&event.target.closest('input,select,textarea'))return
   if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){
    event.preventDefault();select(event.key==='Home'?0:event.key==='End'?queries.length-1:selectedRef.current+(event.key==='ArrowDown'?1:-1))
   }
  }
  window.addEventListener('keydown',key);return()=>window.removeEventListener('keydown',key)
 },[])
 async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await stage.current?.requestFullscreen()}catch{setStatus('A tela cheia está indisponível neste navegador.')}}
 return <div className={`questions-preview questions-refined questions-lab lab-${variant}${comparing?'':' questions-accepted'}`}>
  {comparing&&<header className="questions-review"><div><small>Tela 02 · Em criação</small><strong>As perguntas da pesquisa</strong></div><div className="questions-variants" role="group" aria-label="Variantes da lista de perguntas">{directions.map(item=><button type="button" key={item.id} aria-pressed={variant===item.id} onClick={()=>choose(item.id)}><b>{item.id.toUpperCase()}</b>{item.name}</button>)}</div><a href="#abertura"><ArrowLeft size={14}/> Abertura aprovada</a></header>}
  {comparing&&<div className="animation-review"><span>Movimento</span><div role="group" aria-label="Estilo da animação">{animations.map(item=><button type="button" key={item.id} aria-pressed={animation===item.id} onClick={()=>setAnimation(item.id)}>{item.name}</button>)}</div><p>Escolha o visual acima e teste qualquer movimento.</p></div>}<main className={`questions-stage questions-${variant} motion-${animation}`} ref={stage} aria-labelledby="questions-title">
   <div className="questions-backdrop" aria-hidden="true"/>
   {refined&&<div className="questions-canada-motif" aria-hidden="true"><CanadaMap compact neutral/></div>}
   <header className="questions-top"><a className="opening-brand" href="#abertura"><Flag/> Guia Canadá<span>Um olhar orientado por dados</span></a><span>IFAL · TABD 2026.2</span></header>
   <div className="questions-body">
    <div className="questions-intro"><span className="questions-kicker">O que queremos descobrir</span><h1 id="questions-title">Dez perguntas.<br/><em>{refined?<>Três<br/>perspectivas.</>:<>Um ponto<br/>de partida.</>}</em></h1><p>Para entender as diferenças entre os lugares, começamos pelas perguntas certas.</p><div className="questions-topics"><span><Coins size={17}/><b>Salário</b><small>Oportunidades de trabalho</small></span><span><Users size={17}/><b>Comunidade</b><small>Presença brasileira</small></span><span><House size={17}/><b>Moradia</b><small>Comprometimento da renda</small></span></div>{variant==='c'&&<motion.div key={selected} className="stage-number" aria-hidden="true" initial={{opacity:0,y:reduced?0:15}} animate={{opacity:1,y:0}} transition={{duration:reduced?0:.22}}>{two(selected+1)}<small>/ 10</small></motion.div>}</div>
    <div className="questions-selector"><div className="selector-header"><span>{refined?'Nossa investigação':'Perguntas da pesquisa'}</span><span aria-hidden="true">{two(selected+1)} / 10</span></div>
     <div ref={wheel} className="question-wheel" role="region" aria-label="Seletor de perguntas. Role, arraste ou use as setas para cima e para baixo." tabIndex={0}>
      <div className="wheel-focus" style={{height:rowHeight}} aria-hidden="true"/>
      <motion.div className="wheel-drag" drag="y" dragConstraints={{top:0,bottom:0}} dragElastic={reduced?0:.12} onDragEnd={(_,info)=>{if(Math.abs(info.offset.y)>24||Math.abs(info.velocity.y)>180)select(selectedRef.current+(info.offset.y<0?1:-1))}}>
       {queries.map((query,index)=>{const distance=index-selected;return <motion.button key={query.title} type="button" className={`wheel-question${distance===0?' is-selected':''}`} tabIndex={-1} aria-current={distance===0?'true':undefined} aria-label={`Pergunta ${index+1}: ${query.title}`} aria-hidden={Math.abs(distance)>2?true:undefined} style={{pointerEvents:Math.abs(distance)>2?'none':undefined,height:rowHeight,marginTop:-rowHeight/2}} initial={false} animate={{y:distance*rowHeight,x:reduced||animation!=='bounce'?0:distance===0?0:Math.min(2,Math.abs(distance))*24,scale:animation==='glide'?1:distance===0?1:Math.abs(distance)===1?.91:.82,opacity:Math.abs(distance)>2?0:distance===0?1:Math.abs(distance)===1?.48:.18,rotateX:reduced||animation!=='wheel'?0:distance*-20}} transition={(reduced?{duration:0}:animation==='glide'?{type:'tween',duration:.3,ease:[.22,1,.36,1]}:animation==='bounce'?{type:'spring',stiffness:300,damping:17,mass:.8}:{type:'spring',stiffness:250,damping:24,mass:.85}) as Transition} onFocus={()=>wheel.current?.focus({preventScroll:true})} onClick={()=>select(index)}><span className="wheel-number">{two(index+1)}</span><span>{query.title}</span></motion.button>})}
      </motion.div>
     </div>
     <div className="selector-controls"><span>{refined?<>Role para explorar <i/> ou use <kbd>↑</kbd> <kbd>↓</kbd></>:'Role ou arraste para explorar'}</span><div><button type="button" aria-label="Pergunta anterior" disabled={selected===0} onClick={()=>select(selected-1)}><ChevronUp size={19}/></button><button type="button" aria-label="Próxima pergunta" disabled={selected===queries.length-1} onClick={()=>select(selected+1)}><ChevronDown size={19}/></button></div></div>
     <p className="selected-question-announcement sr-only" aria-live="polite" aria-atomic="true">Pergunta {selected+1} de 10: {queries[selected].title}</p>
    </div>
   </div>
   <footer className="questions-footer"><a href="#abertura"><ArrowLeft size={16}/> Por que fizemos este projeto?</a><div className="question-dots" role="group" aria-label="Ir para uma pergunta">{queries.map((query,index)=><button type="button" key={query.title} aria-label={`Pergunta ${index+1}: ${query.title}`} aria-pressed={selected===index} onClick={()=>select(index)}><span>{refined?two(index+1):null}</span></button>)}</div>{!comparing&&<a className="questions-method-link" href="#metodo">Como fizemos a pesquisa <ChevronDown size={16}/></a>}<div className="questions-slide-count"><span>PERGUNTAS</span><b>02</b> / 14</div></footer>
   {document.fullscreenEnabled&&<button className="questions-fullscreen" type="button" aria-label={full?'Sair da tela cheia':'Tela cheia'} onClick={fullscreen}>{full?<Minimize size={17}/>:<Maximize size={17}/>}</button>}
   {status&&<p className="questions-status" role="status">{status}</p>}
  </main>
  {comparing&&<footer className="questions-caption"><div><b>{active.id.toUpperCase()} — {active.name}</b><p>{active.description} Movimento: {animations.find(item=>item.id===animation)?.name}.</p></div><span>↑ ↓ selecionam perguntas · Home / End vão ao início / fim</span></footer>}
 </div>
}







