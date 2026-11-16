import { useEffect, useRef, useState } from 'react'
import { AnimatePresence, motion, useReducedMotion } from 'motion/react'
import { ArrowDown, ArrowLeft, ArrowRight, Coins, House, Maximize, Minimize, Users } from 'lucide-react'
import { CanadaMap } from './CanadaMap'
import { Flag } from './components'
import './opening.css'

const variants = [
 {id:'a',name:'Atlas editorial',description:'Creme, mapa e tipografia. Uma abertura clara, com identidade de pesquisa.'},
 {id:'b',name:'Expedição',description:'Paisagem em tela cheia, contraste e entrada cinematográfica.'},
 {id:'c',name:'Manifesto',description:'Vermelho canadense, composição tipográfica e perguntas em destaque.'},
] as const
const pillars = [
 {icon:Coins,title:'Salário',question:'Onde a remuneração é mais alta?',number:'01'},
 {icon:Users,title:'Comunidade',question:'Onde vivem os brasileiros?',number:'02'},
 {icon:House,title:'Moradia',question:'Onde a renda é mais comprometida?',number:'03'},
]

export function OpeningPreview() {
 const comparing = /^#abertura-[abc]$/.test(location.hash)
 const initial = /^#abertura-([abc])$/.exec(location.hash)?.[1] ?? 'b'
 const [variant,setVariant] = useState(initial)
 const [full,setFull] = useState(false)
 const [status,setStatus] = useState('')
 const stage=useRef<HTMLElement>(null)
 const reduced=useReducedMotion()
 const active=variants.find(item=>item.id===variant) ?? variants[0]
 function choose(id:string) {setVariant(id);history.replaceState(null,'',`#abertura-${id}`)}
 useEffect(()=>{
  const changed=()=>setFull(document.fullscreenElement===stage.current)
  const hash=()=>{const id=/^#abertura-([abc])$/.exec(location.hash)?.[1];if(id)setVariant(id);else if(location.hash==='#abertura'||!location.hash)setVariant('b')}
  document.addEventListener('fullscreenchange',changed);window.addEventListener('hashchange',hash)
  return()=>{document.removeEventListener('fullscreenchange',changed);window.removeEventListener('hashchange',hash)}
 },[])
 useEffect(()=>{
  const onKey=(event:KeyboardEvent)=>{
   if(!comparing){if(event.key==='ArrowRight'&&!event.altKey&&!event.ctrlKey&&!event.metaKey){event.preventDefault();location.hash='perguntas'}return}
   if(event.altKey||event.metaKey||event.ctrlKey||event.shiftKey||event.target instanceof HTMLElement&&event.target.closest('input,select,textarea'))return
   const step=event.key==='ArrowRight'?1:event.key==='ArrowLeft'?-1:0
   if(step){event.preventDefault();choose(variants[(variants.findIndex(item=>item.id===variant)+step+3)%3].id)}
  }
  window.addEventListener('keydown',onKey);return()=>window.removeEventListener('keydown',onKey)
 },[variant,comparing])
 async function toggle(){try{if(document.fullscreenElement)await document.exitFullscreen();else await stage.current?.requestFullscreen();setStatus('')}catch{setStatus('Não foi possível abrir a tela cheia neste navegador.')}}
 return <div className={`opening-preview${comparing?'':' opening-approved'}`}>
  {comparing&&<header className="preview-toolbar"><div><span className="preview-badge">Direção escolhida: B</span><strong>Abertura da apresentação</strong></div><div className="variant-tabs" role="group" aria-label="Variantes da abertura">{variants.map(item=><button key={item.id} type="button" aria-pressed={variant===item.id} onClick={()=>choose(item.id)}><b>{item.id.toUpperCase()}</b><span>{item.name}</span></button>)}</div><a href="#abertura" className="previous-deck"><ArrowLeft size={14}/> Abertura aprovada</a></header>}
  <main ref={stage} className={`opening-stage opening-${variant}`} aria-label={`Variante ${variant.toUpperCase()}: ${active.name}`}>
   <AnimatePresence mode="wait" initial={false}><motion.section className="opening-slide" key={variant} initial={{opacity:0,y:reduced?0:18}} animate={{opacity:1,y:0}} exit={{opacity:0,y:reduced?0:-8}} transition={{type:'spring',stiffness:210,damping:25,duration:reduced?0:undefined}}>
    {variant==='b'&&<div className="opening-landscape" aria-hidden="true"/>}
    <div className="opening-top"><a className="opening-brand" href="#abertura"><Flag/> Guia Canadá<span>Um olhar orientado por dados</span></a><span className="opening-course">IFAL <i/> TABD 2026.2</span></div>
    <div className="opening-body">
     <div className="opening-copy"><div className="opening-kicker"><span/> Por que fizemos este projeto?</div><h1>{variant==='c'?<>Uma decisão.<br/><em>Três perspectivas.</em></>:<>O Canadá é um país.<br/><em>As oportunidades<br/>não são iguais.</em></>}</h1><p className="opening-motivation">Criamos o Guia Canadá para ajudar desenvolvedores brasileiros a entender como salário, comunidade e moradia variam entre províncias e territórios.</p><div className="opening-research"><span>Nosso ponto de partida</span><p>Como os dados podem ajudar a comparar esses lugares?</p></div></div>
     {variant==='a'&&<div className="opening-atlas"><div className="atlas-label"><span>CANADÁ</span><span>10 províncias · 3 territórios</span></div><CanadaMap compact neutral/><div className="atlas-caption"><span className="atlas-cross">+</span><p>Um território.<br/><strong>Diferentes realidades.</strong></p><ArrowDown size={22}/></div></div>}
     {variant==='b'&&<div className="expedition-coordinate"><span>CANADÁ / AMÉRICA DO NORTE</span><div className="expedition-line"/><p>Antes de escolher um lugar,<br/><strong>entenda o que muda entre eles.</strong></p></div>}
     {variant==='c'&&<div className="manifesto-mark" aria-hidden="true"><Flag/><span>CA</span><span className="manifesto-orbit"/></div>}
    </div>
    <div className="opening-bottom"><div className="opening-pillars">{pillars.map(({icon:Icon,title,question,number},index)=><motion.div className="opening-pillar" key={title} initial={{opacity:0,y:reduced?0:14}} animate={{opacity:1,y:0}} transition={{delay:reduced?0:.1+index*.07,duration:reduced?0:.35}}><span className="pillar-number">{number}</span><Icon size={22}/><div><h2>{title}</h2><p>{question}</p></div></motion.div>)}</div><footer className="opening-footer"><div><span>Pesquisa e apresentação</span><p>Eliezir Moreira <i/> Raphael Phillipe</p></div><div className="opening-counter"><span>ABERTURA</span><b>01</b><span>/ 14</span></div></footer></div>
   </motion.section></AnimatePresence>
   {!comparing&&<a className="opening-next" href="#perguntas">As perguntas da pesquisa <ArrowRight size={17}/></a>}
   {document.fullscreenEnabled&&<button className="opening-fullscreen" type="button" onClick={toggle} aria-label={full?'Sair da tela cheia':'Ver abertura em tela cheia'}>{full?<Minimize size={18}/>:<Maximize size={18}/>}</button>}
  </main>
  {comparing&&<footer className="preview-caption"><div><b>{active.id.toUpperCase()} — {active.name}</b><p>{active.description}</p></div><span>Use ← → para comparar as variantes</span></footer>}
  {status&&<p className="preview-status" role="status">{status}</p>}
 </div>
}


