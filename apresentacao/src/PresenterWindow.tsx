import { useEffect, useRef, useState } from 'react'
import { ArrowLeft, ArrowRight, Eye, Presentation } from 'lucide-react'
import { queries } from './data'
import { presenterNotes } from './presenter-notes'
import './presenter-window.css'

const pages = ['abertura','perguntas','metodo',...queries.map((_,index)=>`consulta-${index+1}`),'conclusoes']
const channelName = 'guia-canada-live'
type LiveState = { type:'state'; page:string; revealed:boolean }
type PresenterMessage = {type:'request-state'} | {type:'action';action:'next'|'previous'|'reveal'} | {type:'navigate';page:string}

/** Same-origin companion: notes never render in the audience presentation. */
export function PresenterWindow() {
  const [page,setPage] = useState('abertura')
  const [revealed,setRevealed] = useState(false)
  const [connected,setConnected] = useState(false)
  const [supported,setSupported] = useState(true)
  const channel = useRef<BroadcastChannel|null>(null)
  const note = presenterNotes[page] ?? presenterNotes.abertura
  const slideIndex = pages.indexOf(page)
  const queryIndex = /^consulta-(\d+)$/.exec(page)
  const query = queryIndex ? queries[Number(queryIndex[1])-1] : undefined

  useEffect(()=>{
    document.title='Apresentador · Guia Canadá'
    if (typeof BroadcastChannel==='undefined') { setSupported(false); return }
    let live:BroadcastChannel
    try { live=new BroadcastChannel(channelName) } catch { setSupported(false); return }
    channel.current=live
    live.onmessage=(event:MessageEvent<unknown>)=>{
      const data=event.data as Partial<LiveState>|null
      if (!data || data.type!=='state' || typeof data.page!=='string' || !pages.includes(data.page) || typeof data.revealed!=='boolean') return
      setPage(data.page);setRevealed(data.revealed);setConnected(true)
    }
    live.postMessage({type:'request-state'} satisfies PresenterMessage)
    const requestState=()=>live.postMessage({type:'request-state'} satisfies PresenterMessage)
    window.addEventListener('focus',requestState)
    return()=>{window.removeEventListener('focus',requestState);live.close();channel.current=null}
  },[])

  function send(message:PresenterMessage) {
    if (!channel.current) return
    try { channel.current.postMessage(message) } catch { setConnected(false) }
  }
  function navigate(nextPage:string) {
    if (!pages.includes(nextPage)) return
    setPage(nextPage);setRevealed(false)
    send({type:'navigate',page:nextPage})
  }
  function next() {
    if (!channel.current || !connected) {
      if(query && !revealed) setRevealed(true)
      else navigate(pages[Math.min(pages.length-1,slideIndex+1)])
      return
    }
    send({type:'action',action:'next'})
  }
  function previous() {
    if (!channel.current || !connected) { navigate(pages[Math.max(0,slideIndex-1)]); return }
    send({type:'action',action:'previous'})
  }
  const nextLabel=query && !revealed ? 'Ver resposta' : 'Próxima'
  return <main className="presenter-window">
    <header className="presenter-window-header"><div className="presenter-identity"><Presentation size={24} aria-hidden="true"/><div><span>Guia Canadá · IFAL TABD 2026.2</span><h1>Janela do apresentador</h1></div></div><p className={`presenter-connection${connected?' is-connected':''}`} role="status"><span aria-hidden="true"/>{!supported?'Leitura local das notas':connected?'Sincronizada com a apresentação':'Aguardando a apresentação'}</p></header>
    <p className="presenter-instruction">Mantenha esta janela na sua tela e projete somente a janela da apresentação.</p>
    {!supported && <p className="presenter-notice">Este navegador não oferece comunicação entre janelas. Você pode consultar todas as notas pelo seletor; use os controles da janela principal para apresentar.</p>}
    {supported && !connected && <p className="presenter-notice">Abra e mantenha a apresentação principal nesta mesma origem e navegador. As notas continuam disponíveis enquanto aguardamos a conexão.</p>}
    <div className="presenter-workspace">
      <aside className="presenter-sidebar" aria-label="Controles do apresentador"><label htmlFor="presenter-slide">Ir para uma tela</label><select id="presenter-slide" value={page} onChange={event=>navigate(event.target.value)}>{pages.map((item,index)=><option key={item} value={item}>{String(index+1).padStart(2,'0')} · {presenterNotes[item].heading}</option>)}</select><div className="presenter-position">Tela <strong>{String(slideIndex+1).padStart(2,'0')}</strong> de 14</div><h2>{note.heading}</h2>
        {query && <section className="presenter-answer-reference" aria-labelledby="presenter-answer-label"><h3 id="presenter-answer-label"><Eye size={16} aria-hidden="true"/>Resposta para consulta</h3><p>{query.answer}</p><small>{revealed?'Resposta revelada na apresentação.':'Resposta ainda não revelada na apresentação.'}</small></section>}
        <nav className="presenter-window-controls" aria-label="Controlar a apresentação"><button type="button" onClick={previous} disabled={slideIndex===0}><ArrowLeft size={17} aria-hidden="true"/>Anterior</button><button className="presenter-next" type="button" onClick={next} disabled={slideIndex===pages.length-1}>{nextLabel}<ArrowRight size={17} aria-hidden="true"/></button></nav>
        {query && !revealed && connected && <button className="presenter-reveal-only" type="button" onClick={()=>send({type:'action',action:'reveal'})}>Revelar sem avançar</button>}
        <p className="presenter-control-hint">{supported && connected?'Os controles mudam a janela principal.':'Os controles percorrem as notas localmente até a conexão.'}</p>
      </aside>
      <article className="presenter-notes-content" aria-labelledby="presenter-notes-title"><header><span>Roteiro de fala</span><h2 id="presenter-notes-title">O que apresentar nesta tela</h2></header><section className="presenter-intro"><h3>Comece por aqui</h3><p>{note.intro}</p></section><section><h3>Como explicar o processo</h3><ol className="presenter-steps">{note.steps.map((step,index)=><li key={step}><span aria-hidden="true">{String(index+1).padStart(2,'0')}</span><p>{step}</p></li>)}</ol></section><section className="presenter-caveats"><h3>Cuidados e limites</h3><ul>{note.caveats.map(caveat=><li key={caveat}>{caveat}</li>)}</ul></section><section className="presenter-handoff"><h3>Transição de fala</h3><p>{note.handoff}</p></section></article>
    </div>
  </main>
}
