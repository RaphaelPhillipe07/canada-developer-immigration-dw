import { useEffect, useRef, useState, type ElementType } from 'react'
import { createRoot } from 'react-dom/client'
import { motion, useReducedMotion } from 'motion/react'
import { ArrowLeft, ArrowRight, BarChart3, BookOpen, ChevronLeft, ChevronRight, Coins, Compass, ExternalLink, House, Layers3, MapPin, Maximize, Menu, Minimize, Presentation, Scale, Users, X } from 'lucide-react'
import { Button, Collapsible, Flag } from './components'
import { BarPanel, DataTable, GroupPanel, PeriodPanel, ScatterPanel } from './charts'
import { CanadaMap, ProvinceFlag, ProvinceSilhouette } from './CanadaMap'
import { format, metricKeys, metrics, priorityLabels, queries, rank, regions, regionsByCode, sources, tips, type Metric, type Priority, type Region } from './data'
import './styles.css'
import { OpeningPreview } from './OpeningPreview'
import { QuestionsPreview } from './QuestionsPreview'
import { MethodPreview } from './MethodPreview'
import { Presentation as SchoolPresentation } from './Presentation'
import { presentationPages } from './presentation-model'
import canadaPhoto from './assets/canada-rockies.jpg'
import { PresenterWindow } from './PresenterWindow'

const icons: Record<Priority,ElementType> = {salary:Coins,community:Users,housing:House,score:Scale}
const guideOptions: Priority[] = ['salary','community','housing','score']
const heroPhoto = canadaPhoto
const censusUrl = 'https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/dt-td/index-eng.cfm'
const wagesUrl = 'https://www.jobbank.gc.ca/trend-analysis/search-wages'

function Header({page}: {page:string}) {
  const [menuOpen,setMenuOpen] = useState(false)
  const navigation = [
    {href:'#por-que',label:'O projeto',active:['por-que','dados'].includes(page)},
    {href:'#explorar',label:'Explorar',active:['explorar','comparar'].includes(page)},
    {href:'#consulta-1',label:'Consultas',active:page.startsWith('consulta-')},
  ]
  const links = navigation.map(item=><a href={item.href} key={item.href} aria-current={item.active ? 'true' : undefined} onClick={()=>setMenuOpen(false)}>{item.label}</a>)
  return <header className="site-header"><div className="shell header-inner">
    <div className="header-primary"><a className="wordmark" href="#inicio" onClick={()=>setMenuOpen(false)}><Flag/><span>Guia Canadá</span></a>
    <nav aria-label="Navegação principal" className="header-nav">{links}</nav></div>
    <div className="header-tools"><a className="utility-link" href="#fontes">Fontes</a><Button asChild><a href="#por-que" onClick={()=>setMenuOpen(false)}>Começar</a></Button>
    <Button variant="ghost" className="mobile-toggle" type="button" aria-label={menuOpen?'Fechar menu':'Abrir menu'} aria-expanded={menuOpen} aria-controls="mobile-nav" onClick={()=>setMenuOpen(!menuOpen)}>{menuOpen?<X/>:<Menu/>}</Button></div>
  </div><nav id="mobile-nav" className="shell mobile-nav" aria-label="Navegação móvel" hidden={!menuOpen}>{links}<a href="#fontes" onClick={()=>setMenuOpen(false)}>Fontes</a></nav></header>
}

function Hero() {
  const [photoMissing,setPhotoMissing] = useState(false)
  return <section className="hero" id="inicio" aria-labelledby="hero-title">
    <div className="hero-copy">
      <div className="eyebrow"><MapPin size={15}/> Canadá para desenvolvedores</div>
      <h1 id="hero-title">Qual província <span>combina com você?</span></h1>
      <p>Explore dados de salários, comunidade brasileira e moradia nas províncias e territórios do Canadá.</p>
      <div className="hero-actions">
        <Button asChild><a href="#por-que">Conheça o projeto <ArrowRight/></a></Button>
      </div>
      <div className="hero-scope"><span><strong>13</strong> jurisdições</span><span><strong>3</strong> indicadores</span><span><strong>10</strong> consultas</span></div>
    </div>
    <figure className="hero-photo">
      {photoMissing ? <div className="photo-fallback" aria-hidden="true"><Flag/><span>Canadá</span></div> : <img src={heroPhoto} alt="Lago azul cercado por montanhas nas Rochosas canadenses" onError={()=>setPhotoMissing(true)} width={1300} height={860}/>}
      <div className="photo-location"><MapPin size={15}/> Um país. Muitas possibilidades.</div>
      <div className="photo-fact"><ProvinceFlag code="BC"/><div><small>Maior salário mediano</small><strong>CAD 52,40<span>/h</span></strong><small>British Columbia · 2023–2024</small></div></div>
      {!photoMissing && <figcaption><a href="https://unsplash.com/photos/JhDHKezS6O8" rel="noreferrer" target="_blank">Kowshik Roy Sagor · Unsplash</a></figcaption>}
    </figure>
  </section>
}

function MetricList({region}: {region:Region}) {
  return <dl className="metric-list">{metricKeys.map(key=>{const Icon=icons[key];return <div key={key}>
    <dt><Icon size={16}/>{metrics[key].label}</dt><dd>{format(key,region[key])}</dd>
  </div>})}</dl>
}

function Explorer({onCompare}: {onCompare:(code:string)=>void}) {
  const [priority,setPriority] = useState<Priority>('salary')
  const [selected,setSelected] = useState('BC')
  const ordered = rank(priority)
  const active = regionsByCode[selected]
  const ranked = priority==='housing' ? ordered.filter(region=>!['NT','YT','NU'].includes(region.code)) : ordered
  function selectPriority(next:Priority) {
    setPriority(next)
    setSelected(rank(next).find(region=>next!=='housing' || !['NT','YT','NU'].includes(region.code))?.code ?? 'BC')
  }
  return <section className="section" id="explorar" aria-labelledby="explorer-title">
    <div className="section-heading"><div><div className="eyebrow"><Compass size={16}/> Explorador</div><h2 id="explorer-title">O que mais importa para você?</h2></div></div>
    <div className="priority-picker" role="group" aria-label="Prioridade">{guideOptions.map(key=>{const Icon=icons[key];return <button type="button" key={key} aria-pressed={priority===key} onClick={()=>selectPriority(key)}><Icon size={21}/>{priorityLabels[key]}</button>})}</div>
    <div className="explorer-grid">
      <div className="panel map-panel"><header className="panel-head"><div><div className="eyebrow">De costa a costa</div><h3>Um olhar sobre o Canadá</h3><p>Selecione uma província ou território.</p></div><Compass size={24}/></header>
        <CanadaMap metric={priority} selected={selected} onSelect={setSelected}/>
      </div>
      <div className="explorer-sidebar"><div className="panel chosen"><label className="jurisdiction-label" htmlFor="explorer-jurisdiction">Selecionar jurisdição</label><select id="explorer-jurisdiction" className="jurisdiction-select" value={selected} onChange={event=>setSelected(event.target.value)}>{regions.map(region=><option key={region.code} value={region.code}>{region.name}</option>)}</select><div aria-live="polite"><div className="chosen-header"><ProvinceFlag key={active.code} code={active.code}/><div><small>Conheça a jurisdição</small><h3>{active.name}</h3></div><span className="province-code">{active.code}</span></div><MetricList region={active}/></div><Button asChild variant="outline"><a href="#comparar" onClick={()=>onCompare(active.code)}>Comparar {active.code} <ArrowRight/></a></Button></div>
      <div className="panel rank-panel"><header className="panel-head"><div><h3>{priority==='housing' ? 'Menor comprometimento' : `Destaques por ${priorityLabels[priority].toLowerCase()}`}</h3><p>{priority==='housing' ? 'Menor percentual entre as dez províncias.' : priority==='score' ? 'Índice com pesos iguais entre os três indicadores.' : metrics[priority].title}</p></div><BarChart3 size={22}/></header>
        <ol className="ranking">{ranked.slice(0,5).map((row,i)=><li key={row.code}><button type="button" aria-pressed={selected===row.code} onClick={()=>setSelected(row.code)}><span className="rank-number">{ranked.findIndex(region=>region[priority]===row[priority])+1}</span><span>{row.name}</span><strong>{format(priority,row[priority])}</strong>{i===0 && <span className="sr-only">Primeiro resultado</span>}</button></li>)}</ol>
        <p className="micro">{priority==='salary' ? sources.wages : priority==='score' ? 'Censo 2021 e Job Bank, 2023–2024.' : sources.census}</p>
      </div></div>
    </div>
  </section>
}

function ProvinceSelect({id,code,onChange,exclude}: {id:string;code:string;onChange:(code:string)=>void;exclude:string}) {
  return <article className={`panel province province-${id==='province-a'?'a':'b'}`}><div className="province-heading"><ProvinceFlag code={code}/><span>Jurisdição {id==='province-a'?'01':'02'}</span><ProvinceSilhouette code={code}/></div><label className="sr-only" htmlFor={id}>Jurisdição {id==='province-a'?'1':'2'}</label><select id={id} value={code} onChange={event=>onChange(event.target.value)}>{regions.map(region=><option key={region.code} value={region.code} disabled={region.code===exclude}>{region.name}</option>)}</select><div aria-live="polite"><MetricList region={regionsByCode[code]}/><div className="province-bars" aria-hidden="true">{metricKeys.map(metric=><div key={metric}><span>{metrics[metric].label}</span><div><i style={{width:`${(regionsByCode[code][metric] ?? 0)/metrics[metric].scale*100}%`}}/></div></div>)}</div></div></article>
}

const chapters = [
  {id:'por-que',label:'Por que fizemos este projeto?',next:'dados',nextLabel:'Entender os dados'},
  {id:'dados',label:'De onde vêm os dados',next:'explorar',nextLabel:'Explorar o Canadá'},
  {id:'explorar',label:'Explorar o Canadá',next:'comparar',nextLabel:'Comparar jurisdições'},
  {id:'comparar',label:'Comparar jurisdições',next:'consulta-1',nextLabel:'Ver as 10 consultas'},
  {id:'fontes',label:'Fontes e metodologia',next:'inicio',nextLabel:'Voltar ao início'},
]

function ChapterNavigation({index}: {index:number}) {
  const chapter=chapters[index]
  const back=index===chapters.length-1 ? 'consulta-10' : chapters[index-1]?.id ?? 'inicio'
  return <nav className="chapter-nav" aria-label="Navegação entre seções">
    <Button asChild variant="outline"><a href={`#${back}`}><ArrowLeft/>{index===0?'Início':'Voltar'}</a></Button>
    <Button asChild><a href={`#${chapter.next}`}>{chapter.nextLabel}<ArrowRight/></a></Button>
  </nav>
}

function Why() {
  return <section className="chapter-intro" aria-labelledby="why-title">
    <div className="eyebrow"><Compass size={16}/> O projeto</div>
    <h1 id="why-title">Por que fizemos este projeto?</h1>
    <p>Para ajudar desenvolvedores brasileiros a entender o que muda de uma província canadense para outra antes de escolher onde pesquisar oportunidades.</p>
    <div className="chapter-cards">
      <article className="panel"><Coins/><h2>Salário</h2><p>Onde a remuneração mediana é mais alta?</p></article>
      <article className="panel"><Users/><h2>Comunidade</h2><p>Onde vivem as maiores comunidades nascidas no Brasil?</p></article>
      <article className="panel"><House/><h2>Moradia</h2><p>Onde a moradia pesa mais na renda de quem aluga?</p></article>
    </div>
    <p className="chapter-summary">O projeto TABD reuniu esses três indicadores em um Data Warehouse e formulou dez consultas para investigar como eles se combinam.</p>
  </section>
}

function DataChapter() {
  return <section className="chapter-intro" aria-labelledby="data-title">
    <div className="eyebrow"><Layers3 size={16}/> Os dados</div>
    <h1 id="data-title">De onde vêm os dados?</h1>
    <p>Reunimos as fontes por província e território para observar os três indicadores na mesma escala geográfica.</p>
    <div className="chapter-cards">
      <article className="panel"><Coins/><h2>Salário por hora</h2><p>Mediana do grupo NOC 21232, em dólares canadenses por hora. Há dados provinciais para nove jurisdições.</p><small>{sources.wages}</small></article>
      <article className="panel"><Users/><h2>Comunidade brasileira</h2><p>Número de imigrantes nascidos no Brasil por jurisdição e por período de chegada.</p><small>{sources.census}</small></article>
      <article className="panel"><House/><h2>Moradia inacessível</h2><p>Percentual de inquilinos que gastam pelo menos 30% da renda com moradia no universo da tabela.</p><small>{sources.census}</small></article>
    </div>
    <p className="chapter-summary">Os períodos das fontes são diferentes. Os resultados descrevem o que aparece nos dados, e valores indisponíveis aparecem como “Sem dado”.</p>
  </section>
}

function Story({page}: {page:string}) {
  const [left,setLeft] = useState('BC')
  const [right,setRight] = useState('QC')
  function compare(code:string) {
    setLeft(code)
    if (code===right) setRight(left)
  }
  const index=chapters.findIndex(chapter=>chapter.id===page)
  return <main className="shell story" id="conteudo" tabIndex={-1} hidden={index<0}>
    {index>=0 && <p className="chapter-progress" aria-live="polite">{index===chapters.length-1 ? 'Depois das consultas' : `Etapa ${index+1} de 4`} <span>·</span> {chapters[index].label}</p>}
    {page==='por-que' && <Why/>}
    {page==='dados' && <DataChapter/>}
    <div hidden={page!=='explorar'}><Explorer onCompare={compare}/></div>
    {page==='comparar' && <section className="section" id="comparar" aria-labelledby="compare-title">
      <div className="section-heading"><div><div className="eyebrow"><Layers3 size={16}/> Comparação</div><h2 id="compare-title">Duas jurisdições, lado a lado.</h2></div><p>Selecione dois lugares e compare os indicadores na mesma ordem.</p></div>
      <div className="compare-grid"><ProvinceSelect id="province-a" code={left} onChange={setLeft} exclude={right}/><ProvinceSelect id="province-b" code={right} onChange={setRight} exclude={left}/></div>
      <p className="micro compare-note">Moradia indica o percentual de inquilinos que gastam pelo menos 30% da renda com habitação. Menor percentual indica menor comprometimento no recorte da tabela.</p>
    </section>}
    {page==='fontes' && <section className="section resources" id="fontes" aria-labelledby="resources-title">
      <div className="section-heading"><div><div className="eyebrow"><BookOpen size={16}/> Pesquisa</div><h2 id="resources-title">Fontes e metodologia</h2></div></div>
      <div className="resource-grid">
        <article className="panel source-panel"><h3>Fontes e metodologia</h3><p>O projeto TABD cruza remuneração, imigração e moradia por jurisdição. Os períodos das fontes são diferentes e a análise é descritiva.</p><ul><li><a href={censusUrl} target="_blank" rel="noreferrer">Statistics Canada · Censo 2021 <ExternalLink size={14}/></a></li><li><a href={wagesUrl} target="_blank" rel="noreferrer">Job Bank · salários de 2023–2024 <ExternalLink size={14}/></a></li></ul><Collapsible label="Como o ranking de equilíbrio funciona"><p>O índice usa normalização min–max nas nove províncias com os três indicadores, pesos iguais e pontuação maior para menor comprometimento com moradia. As outras quatro jurisdições aparecem nos recortes censitários.</p></Collapsible></article>
        <article className="panel tips"><h3>10 dicas para usar o guia</h3>{tips.map(([label,body])=><Collapsible key={label} label={label}><p>{body}</p></Collapsible>)}</article>
      </div>
    </section>}
    {index>=0 && <ChapterNavigation index={index}/>}
  </main>
}

function QueryChart({index}: {index:number}) {
  const query=queries[index]
  if (query.chart==='coverage') return <DataTable headers={['Jurisdição','Salário · CAD/h','Brasileiros · pessoas','Moradia · %']} rows={regions.filter(region=>region.salary===null).map(region=>[region.name,'Sem dado',format('community',region.community),format('housing',region.housing)])}/>
  if (query.chart==='groups') return <GroupPanel/>
  if (query.chart==='scatter' && query.xy) return <ScatterPanel xy={query.xy} highlight={query.highlight} presentation/>
  if (query.chart==='periods') return <PeriodPanel/>
  const metric=query.chart==='scatter' ? 'salary' : query.chart
  const ranked=rank(metric)
  return <BarPanel metric={metric} items={metric==='housing' ? [...ranked].reverse() : ranked} presentation/>
}

function Deck({index}: {index:number}) {
  const query=queries[index]
  const stage=useRef<HTMLElement>(null)
  const [full,setFull]=useState(false)
  const [fullscreenError,setFullscreenError]=useState(false)
  const current=String(index+1).padStart(2,'0')
  const total=String(queries.length).padStart(2,'0')
  const reduced=useReducedMotion()
  useEffect(()=>{
    const changed=()=>setFull(document.fullscreenElement===stage.current)
    document.addEventListener('fullscreenchange',changed)
    return ()=>document.removeEventListener('fullscreenchange',changed)
  },[])
  async function toggleFullscreen() {
    setFullscreenError(false)
    try {
      if (document.fullscreenElement===stage.current) await document.exitFullscreen()
      else await stage.current?.requestFullscreen()
    } catch { setFullscreenError(true) }
  }
  useEffect(()=>{
    function keydown(event:KeyboardEvent) {
      if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || (event.target instanceof HTMLElement && event.target.closest('select,input,textarea,[contenteditable],.table-scroll'))) return
      const delta=event.key==='ArrowLeft' ? -1 : event.key==='ArrowRight' ? 1 : 0
      const next=index+delta
      if (!delta || next<0 || next>=queries.length) return
      event.preventDefault()
      location.hash=`consulta-${next+1}`
    }
    window.addEventListener('keydown',keydown)
    return ()=>window.removeEventListener('keydown',keydown)
  },[index])
  return <main className="deck" id="apresentacao" ref={stage} tabIndex={-1}><div className="shell deck-inner">
    <div className="deck-top"><div className="eyebrow"><Presentation size={17}/> Consultas analíticas · TABD</div>
      {document.fullscreenEnabled && <Button type="button" variant="outline" onClick={toggleFullscreen}>{full?<Minimize/>:<Maximize/>}{full?'Sair da tela cheia':'Tela cheia'}</Button>}
    </div>
    {fullscreenError && <p role="status" className="micro">A tela cheia está indisponível neste navegador.</p>}
    <div className="deck-progress" aria-hidden="true"><motion.span animate={{width:`${(index+1)/queries.length*100}%`}} transition={{duration:reduced?0:.25}}/></div>
    <motion.article key={index} initial={{opacity:0,y:reduced?0:10}} animate={{opacity:1,y:0}} transition={{duration:reduced?0:.22}} className={`panel slide slide-${query.chart}`} aria-labelledby="query-title">
      <header className="slide-question"><span className="slide-count" aria-live="polite">Consulta {current} de {total}</span><h1 id="query-title">{query.title}</h1></header>
      <section className="slide-answer" aria-labelledby="slide-answer-label"><h2 className="eyebrow" id="slide-answer-label">Resposta</h2><p className="answer-text">{query.answer}</p></section>
      <div className="slide-content">
        <section className="slide-visual" aria-labelledby="slide-evidence-label"><div className="eyebrow">Evidência nos dados</div><h2 id="slide-evidence-label">{query.evidence}</h2><QueryChart index={index}/></section>
        <aside className="slide-reading" aria-labelledby="slide-reading-label"><span className="reading-icon" aria-hidden="true"><BookOpen size={22}/></span><h2 id="slide-reading-label">Como interpretar</h2><p className="answer-note">{query.note}</p><div className="slide-reference"><h3>Fonte e referência</h3><p>{query.source}</p></div></aside>
      </div>
      <footer className="slide-source"><strong>Fonte e período de referência</strong><p>{query.source}</p></footer>
    </motion.article>
    <nav className="deck-nav" aria-label="Controles da apresentação">
      <Button asChild variant="outline"><a href={index>0 ? `#consulta-${index}` : '#comparar'}><ChevronLeft/>{index>0?'Anterior':'Comparação'}</a></Button>
      <div role="group" aria-label="Ir para uma consulta" className="slide-numbers">{queries.map((item,i)=><a key={item.title} href={`#consulta-${i+1}`} aria-label={`Consulta ${i+1}: ${item.title}`} aria-current={i===index ? 'step' : undefined}>{i+1}</a>)}</div>
      {index<queries.length-1 ? <Button asChild><a href={`#consulta-${index+2}`}>Próxima <ChevronRight/></a></Button> : <Button asChild><a href="#fontes">Fontes <ArrowRight/></a></Button>}
    </nav>
    <p className="keyboard-hint"><span>←</span><span>→</span> para navegar entre as consultas</p>
  </div></main>
}

function activeQuery(hash:string) {
  const match=/^#consulta-(\d+)$/.exec(hash)
  const index=match ? Number(match[1])-1 : -1
  return index>=0 && index<queries.length ? index : -1
}

function App() {
  const [hash,setHash]=useState(location.hash)
  const query=activeQuery(hash)
  const route=hash.slice(1)
  const page=query>=0 || chapters.some(chapter=>chapter.id===route) ? route : 'inicio'
  const isHome=page==='inicio'
  useEffect(()=>{
    const change=()=>setHash(location.hash)
    window.addEventListener('hashchange',change)
    return ()=>window.removeEventListener('hashchange',change)
  },[])
  useEffect(()=>{
    if (hash) window.scrollTo({top:0,behavior:'instant'})
  },[hash])
  const mainId=query>=0?'apresentacao':isHome?'principal':'conteudo'
  if (new URLSearchParams(location.search).get('apresentador')==='1') return <PresenterWindow/>
  const presentationPage=!hash?'abertura':route
  if (presentationPages.some(item=>item.id===presentationPage)) return <SchoolPresentation page={presentationPage}/>
  if (/^#abertura-[abc]$/.test(hash)) return <OpeningPreview/>
  if (/^#perguntas-[abc]$/.test(hash)) return <QuestionsPreview/>
  if (/^#metodo-[abc]$/.test(hash)) return <MethodPreview/>
  return <div className={`site-shell${query>=0?' is-deck':''}`}><a className="skip-link" href={`#${mainId}`} onClick={event=>{event.preventDefault();document.getElementById(mainId)?.focus()}}>Ir para o conteúdo</a>
    <Header key={page} page={page}/>
    {isHome && <main className="shell landing" id="principal" tabIndex={-1}><Hero/></main>}
    <Story page={page}/>
    {query>=0 && <Deck index={query}/>}
    <footer className="site-footer"><div className="shell footer-inner"><a className="wordmark" href="#inicio"><Flag/> Guia Canadá</a><p>TABD 2026.2 · IFAL · Eliezir Moreira e Raphael Phillipe</p><a className="utility-link" href="#fontes">Fontes</a></div></footer>
  </div>
}

createRoot(document.getElementById('root')!).render(<App/>)
