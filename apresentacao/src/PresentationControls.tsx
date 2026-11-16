import { useCallback, useEffect, useId, useRef, useState } from 'react'
import { AnimatePresence, motion, useReducedMotion } from 'motion/react'
import { ArrowLeft, ArrowRight, BookOpen, Check, ChevronDown, Eye, Grid2X2, Maximize, Minimize, MonitorUp, X } from 'lucide-react'
import { presentationPages } from './presentation-model'
import { presenterNotes } from './presenter-notes'
import './presentation-controls.css'

type PresentationControlsProps = {
  page:string
  revealed?:boolean
  onNext:()=>void
  onPrevious:()=>void
  onReveal?:()=>void
}
type Overlay='slides'|'notes'|null
const two=(value:number)=>String(value).padStart(2,'0')
const focusable='a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])'

/** Presentation-level controls take precedence over the individual screen shortcuts. */
export function PresentationControls({page,revealed,onNext,onPrevious,onReveal}:PresentationControlsProps) {
  const [overlay,setOverlay]=useState<Overlay>(null)
  const [full,setFull]=useState(Boolean(document.fullscreenElement))
  const [status,setStatus]=useState('')
  const dialog=useRef<HTMLDivElement>(null)
  const trigger=useRef<HTMLElement|null>(null)
  const reduced=useReducedMotion()
  const titleId=useId()
  const descriptionId=useId()
  const current=Math.max(0,presentationPages.findIndex(item=>item.id===page))
  const needsReveal=page.startsWith('consulta-')&&revealed===false
  const note=presenterNotes[page]
  const close=useCallback(()=>setOverlay(null),[])
  const openPresenter=()=>{
    const url=new URL(location.href)
    url.searchParams.set('apresentador','1')
    url.hash=page
    const popup=window.open(url.toString(),'guia-canada-apresentador','popup,width=580,height=880')
    if(!popup)setStatus('O navegador bloqueou a nova janela. Use N para consultar as notas aqui.')
  }
  const advance=useCallback(()=>{
    if(needsReveal&&onReveal)onReveal()
    else onNext()
  },[needsReveal,onReveal,onNext])

  const toggleFullscreen=useCallback(async()=>{
    setStatus('')
    try {
      if(document.fullscreenElement)await document.exitFullscreen()
      else await document.documentElement.requestFullscreen()
    } catch {setStatus('Não foi possível ativar a tela cheia neste navegador.')}
  },[])

  useEffect(()=>{
    const change=()=>setFull(Boolean(document.fullscreenElement))
    document.addEventListener('fullscreenchange',change)
    return()=>document.removeEventListener('fullscreenchange',change)
  },[])
  useEffect(()=>{setOverlay(null);setStatus('')},[page])
  useEffect(()=>{
    if(!overlay)return
    const previousOverflow=document.body.style.overflow
    document.body.style.overflow='hidden'
    trigger.current=document.activeElement instanceof HTMLElement?document.activeElement:null
    const first=dialog.current?.querySelector<HTMLElement>(focusable)
    first?.focus({preventScroll:true})
    return()=>{document.body.style.overflow=previousOverflow;if(trigger.current?.isConnected)trigger.current.focus({preventScroll:true})}
  },[overlay])

  useEffect(()=>{
    function keydown(event:KeyboardEvent) {
      if(event.defaultPrevented||event.altKey||event.ctrlKey||event.metaKey||event.shiftKey&&event.key!=='Tab')return
      const target=event.target instanceof HTMLElement?event.target:null
      const key=event.key.toLowerCase()
      if(overlay) {
        if(event.key==='Escape') {event.preventDefault();event.stopImmediatePropagation();close();return}
        if(event.key==='Tab') {
          const elements=Array.from(dialog.current?.querySelectorAll<HTMLElement>(focusable)??[]).filter(element=>element.getClientRects().length>0)
          const first=elements[0],last=elements.at(-1)
          if(!first){event.preventDefault();dialog.current?.focus();return}
          if(event.shiftKey&&(document.activeElement===first||!dialog.current?.contains(document.activeElement))){event.preventDefault();last?.focus()}
          else if(!event.shiftKey&&(document.activeElement===last||!dialog.current?.contains(document.activeElement))){event.preventDefault();first.focus()}
          event.stopImmediatePropagation();return
        }
        if(key==='n'&&overlay==='notes'&&!target?.closest('input,textarea,select,[contenteditable]')){event.preventDefault();event.stopImmediatePropagation();close();return}
        // Preserve native scrolling and link/button operation inside the modal, while
        // preventing older screen-level listeners from moving the underlying slide.
        if(['ArrowRight','ArrowLeft','ArrowDown','ArrowUp','PageDown','PageUp',' ','Home','End'].includes(event.key))event.stopImmediatePropagation()
        return
      }
      if(target?.closest('input,textarea,select,[contenteditable]:not([contenteditable="false"]),.table-scroll,[role="dialog"]'))return
      if(event.key==='Tab')return
      const next=['ArrowRight','PageDown',' '].includes(event.key)
      const previous=['ArrowLeft','PageUp'].includes(event.key)
      if(event.key===' '&&target?.closest('button,a,summary'))return
      if(next||previous) {
        event.preventDefault();event.stopImmediatePropagation()
        if(!event.repeat){if(next)advance();else onPrevious()}
      } else if(key==='n'&&note) {
        event.preventDefault();event.stopImmediatePropagation();if(!event.repeat)setOverlay('notes')
      } else if(key==='f'&&document.fullscreenEnabled) {
        event.preventDefault();event.stopImmediatePropagation();if(!event.repeat)void toggleFullscreen()
      }
    }
    window.addEventListener('keydown',keydown,{capture:true})
    return()=>window.removeEventListener('keydown',keydown,{capture:true})
  },[advance,onPrevious,overlay,note,toggleFullscreen,close])

  return <>
    <div className="presenter-toolbar-wrap">
      <div className="presenter-toolbar" role="toolbar" aria-label="Controles da apresentação">
        <button className="presenter-button presenter-prev" type="button" onClick={onPrevious} disabled={current===0} aria-label="Slide anterior"><ArrowLeft size={18}/><span>Anterior</span></button>
        <button className={`presenter-slide-picker ${overlay==='slides'?'is-open':''}`} type="button" onClick={()=>setOverlay(overlay==='slides'?null:'slides')} aria-haspopup="dialog" aria-expanded={overlay==='slides'} aria-label={`Selecionar slide. Slide ${current+1} de ${presentationPages.length}`}><Grid2X2 size={17}/><span><b>{two(current+1)}</b><i>/</i>{two(presentationPages.length)}</span><ChevronDown size={15}/></button>
        <button className="presenter-button presenter-next" type="button" onClick={advance}>{needsReveal?<Eye size={18}/>:null}<span>{needsReveal?'Ver resposta':'Próxima'}</span><ArrowRight size={18}/></button>
        <span className="presenter-divider" aria-hidden="true"/>
        <button className="presenter-tool" type="button" aria-label="Notas do apresentador. Atalho N" title="Notas do apresentador · N" aria-haspopup="dialog" aria-expanded={overlay==='notes'} onClick={()=>setOverlay(overlay==='notes'?null:'notes')} disabled={!note}><BookOpen size={19}/></button>
        <button className="presenter-tool presenter-window-launch" type="button" aria-label="Abrir janela do apresentador" title="Roteiro em uma janela separada" onClick={openPresenter}><MonitorUp size={19}/></button>
        {document.fullscreenEnabled&&<button className="presenter-tool" type="button" aria-label={full?'Sair da tela cheia. Atalho F':'Tela cheia. Atalho F'} title={full?'Sair da tela cheia · F':'Tela cheia · F'} onClick={()=>void toggleFullscreen()}>{full?<Minimize size={19}/>:<Maximize size={19}/>}</button>}
      </div>
      <p className="presenter-shortcuts" aria-hidden="true"><span><kbd>←</kbd><kbd>→</kbd> navegar</span><span><kbd>N</kbd> notas</span><span><kbd>F</kbd> tela cheia</span></p>
      {status&&<p className="presenter-status" role="status">{status}</p>}
    </div>
    <AnimatePresence>
      {overlay&&<motion.div key="presenter-overlay" className={`presenter-overlay presenter-overlay-${overlay}`} initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} transition={{duration:reduced?0:.16}}>
        <div className="presenter-backdrop" onClick={close} aria-hidden="true"/>
        <div className={`presenter-dialog presenter-${overlay}`} ref={dialog} role="dialog" aria-modal="true" aria-labelledby={titleId} aria-describedby={descriptionId} tabIndex={-1}>
          <header className="presenter-dialog-header"><div><span className="presenter-dialog-kicker">Guia Canadá · Apresentação</span><h2 id={titleId}>{overlay==='slides'?'Escolha um slide':'Notas do apresentador'}</h2></div><button type="button" className="presenter-close" onClick={close} aria-label="Fechar painel"><X size={21}/></button></header>
          {overlay==='slides'?<>
            <p className="presenter-dialog-description" id={descriptionId}>{presentationPages.length} slides, da pergunta à conclusão. Selecione para ir diretamente.</p>
            <nav className="presenter-slide-list" aria-label="Slides da apresentação">{presentationPages.map((item,index)=><a key={item.id} href={`#${item.id}`} aria-current={item.id===page?'page':undefined} onClick={close}><span className="presenter-slide-index">{two(index+1)}</span><span>{item.title}</span>{item.id===page?<Check size={18} aria-hidden="true"/>:<ArrowRight size={16} aria-hidden="true"/>}</a>)}</nav>
          </>:<>
            <p className="presenter-dialog-description" id={descriptionId}>Roteiro de fala do slide {two(current+1)}. Feche este painel antes de projetar o conteúdo para a turma.</p>
            {note&&<div className="presenter-note-content"><p className="presenter-note-count">SLIDE {two(current+1)} DE {two(presentationPages.length)}</p><h3>{note.heading}</h3><section className="presenter-note-intro"><h4>Abertura da fala</h4><p>{note.intro}</p></section><section><h4>Percurso sugerido</h4><ol>{note.steps.map((step,index)=><li key={index}>{step}</li>)}</ol></section><section className="presenter-note-caveats"><h4>Cuidados na interpretação</h4><ul>{note.caveats.map((caveat,index)=><li key={index}>{caveat}</li>)}</ul></section><section className="presenter-note-handoff"><h4>Transição para o próximo slide</h4><p>{note.handoff}</p></section></div>}
          </>}
          <footer className="presenter-dialog-footer"><span><kbd>Esc</kbd> fechar</span>{overlay==='notes'&&<><a href={`${import.meta.env.BASE_URL}roteiro-apresentador.md`} download>Baixar roteiro</a><span><kbd>N</kbd> alternar notas</span></>}</footer>
        </div>
      </motion.div>}
    </AnimatePresence>
  </>
}

