import { useEffect, useState } from 'react'
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { AnalyticalSlide } from './AnalyticalSlide'
import { MethodPreview } from './MethodPreview'
import { Presentation } from './Presentation'
import { PresentationControls } from './PresentationControls'

const census='Statistics Canada · Censo 2021'
const wages='Job Bank · NOC 21232 · 2023–2024'
// Approved classroom content is fixed here so accidental edits to the source
// cannot make these checks pass by changing the expected copy as well.
const approved=[
  ['Onde estão os maiores salários medianos?','British Columbia lidera com CAD 52,40/h.',wages],
  ['Onde moram os imigrantes brasileiros e quando chegaram?','Ontario reúne 23.120 imigrantes nascidos no Brasil. O maior grupo na província chegou entre 2011 e 2021.',census],
  ['Onde a moradia pesa mais na renda dos inquilinos?','Ontario (38,4%) e British Columbia (37,8%) têm os maiores percentuais.',census],
  ['Onde salário alto e comunidade brasileira numerosa coincidem?','Quebec, Ontario, Alberta e British Columbia atendem aos dois critérios.',`${wages} · ${census}`],
  ['Como as chegadas entre 2011 e 2021 se distribuem por salário?','93,3% das chegadas ocorreram nas províncias com salário mediano de pelo menos CAD 45,67/h.',`${wages} · ${census}`],
  ['Onde há salário alto e menor comprometimento com moradia?','New Brunswick, Quebec e Saskatchewan atendem aos dois critérios.',`${wages} · ${census}`],
  ['Onde comunidade numerosa e moradia menos acessível coincidem?','Ontario, Manitoba, Alberta e British Columbia atingem as duas medianas de referência.',census],
  ['Como se comparam os grupos com maior e menor presença brasileira?','O grupo das cinco maiores comunidades tem medianas mais altas em salário e inacessibilidade habitacional.',`${wages} · ${census}`],
  ['Quais províncias equilibram os três indicadores?','Quebec lidera com 61,1/100, seguido de Ontario com 54,2/100.',`${wages} · ${census}`],
  ['Quais jurisdições não têm salário provincial utilizável?','Prince Edward Island, Yukon, Northwest Territories e Nunavut.',`${wages} · ${census}`],
] as const

function RevealHarness({index}:{index:number}){
  const [revealed,setRevealed]=useState(false)
  return <AnalyticalSlide index={index} revealed={revealed} onReveal={()=>setRevealed(true)}/>
}
function HashPresentation(){
  const [page,setPage]=useState(()=>location.hash.slice(1)||'abertura')
  useEffect(()=>{const change=()=>setPage(location.hash.slice(1));window.addEventListener('hashchange',change);return()=>window.removeEventListener('hashchange',change)},[])
  return <Presentation page={page}/>
}
function expectActiveMethod(container:HTMLElement,index:number,nodes:Element[]){
  const panels=Array.from(container.querySelectorAll('.method-detail'))
  expect(panels).toHaveLength(4)
  panels.forEach((panel,panelIndex)=>{
    expect(panel).toBe(nodes[panelIndex])
    expect(panel.getAttribute('aria-hidden')).toBe(String(panelIndex!==index))
    expect(panel.hasAttribute('inert')).toBe(panelIndex!==index)
  })
}

beforeEach(()=>{history.replaceState(null,'','#abertura')})

describe('Uma pergunta e uma resposta por consulta',()=>{
  it.each(approved.map((entry,index)=>({index,title:entry[0],answer:entry[1],source:entry[2]})))('consulta $index preserva a pergunta, resposta e referência aprovadas',async({index,title,answer,source})=>{
    const user=userEvent.setup()
    const {container}=render(<RevealHarness index={index}/>)
    expect(screen.getByRole('heading',{level:1,name:title})).toBeTruthy()
    expect(screen.queryByText(answer,{exact:true})).toBeNull()
    expect(container.querySelector('.analytical-source')?.textContent).toContain(source)
    await user.click(screen.getByRole('button',{name:'Ver resposta'}))
    expect(screen.getByText(answer,{exact:true})).toBeTruthy()
    expect(screen.getAllByRole('heading',{name:'Resposta'})).toHaveLength(1)
    expect(document.activeElement).toBe(screen.getByRole('heading',{name:'Resposta'}))
    expect(screen.getByRole('heading',{name:'Como chegamos a esse resultado'})).toBeTruthy()
    expect(screen.queryByRole('button',{name:'Ver resposta'})).toBeNull()
    expect(container.querySelector('.analytical-source')?.textContent).toContain(source)
  })

  it('mostra as quatro ausências salariais com os indicadores censitários, sem convertê-las em zero',()=>{
    render(<AnalyticalSlide index={9} revealed onReveal={()=>{}}/>)
    const table=screen.getByRole('table')
    expect(within(table).getAllByRole('row')).toHaveLength(5)
    expect(within(table).getAllByText('Sem dado',{exact:true})).toHaveLength(4)
    for(const [place,community,housing] of [['Prince Edward Island','85','30,2%'],['Yukon','0','24,9%'],['Northwest Territories','10','15,6%'],['Nunavut','10','5,2%']]){
      const row=within(table).getByRole('rowheader',{name:place}).closest('tr')!
      expect(within(row).getByRole('cell',{name:'Sem dado'})).toBeTruthy()
      expect(within(row).getByRole('cell',{name:community})).toBeTruthy()
      expect(within(row).getByRole('cell',{name:housing})).toBeTruthy()
    }
  })
})

describe('Controles usados durante a apresentação',()=>{
  it('a primeira seta revela a resposta e a segunda avança; repetições de tecla não pulam slides',()=>{
    const onNext=vi.fn(),onPrevious=vi.fn(),onReveal=vi.fn()
    const props={page:'consulta-1',onNext,onPrevious,onReveal}
    const {rerender}=render(<PresentationControls {...props} revealed={false}/>)
    fireEvent.keyDown(window,{key:'ArrowRight'})
    expect(onReveal).toHaveBeenCalledTimes(1)
    expect(onNext).not.toHaveBeenCalled()
    rerender(<PresentationControls {...props} revealed/>)
    fireEvent.keyDown(window,{key:'ArrowRight'})
    expect(onNext).toHaveBeenCalledTimes(1)
    fireEvent.keyDown(window,{key:'ArrowRight',repeat:true})
    expect(onNext).toHaveBeenCalledTimes(1)
    fireEvent.keyDown(window,{key:'ArrowLeft'})
    expect(onPrevious).toHaveBeenCalledTimes(1)
  })

  it('oferece acesso direto aos 14 slides e identifica o atual',async()=>{
    const user=userEvent.setup()
    render(<PresentationControls page="consulta-4" revealed onNext={()=>{}} onPrevious={()=>{}}/>)
    await user.click(screen.getByRole('button',{name:'Selecionar slide. Slide 7 de 14'}))
    const dialog=screen.getByRole('dialog',{name:'Escolha um slide'})
    const links=within(dialog).getAllByRole('link')
    expect(links.map(link=>link.getAttribute('href'))).toEqual(['#abertura','#perguntas','#metodo',...Array.from({length:10},(_,index)=>`#consulta-${index+1}`),'#conclusoes'])
    expect(links.filter(link=>link.getAttribute('aria-current')==='page')).toHaveLength(1)
    expect(links.find(link=>link.getAttribute('aria-current')==='page')?.getAttribute('href')).toBe('#consulta-4')
    await user.keyboard('{Escape}')
    await waitFor(()=>expect(screen.queryByRole('dialog')).toBeNull())
  })

  it('abre notas com N, protege o slide contra setas no painel e restaura o foco ao fechar',async()=>{
    const user=userEvent.setup(),onNext=vi.fn()
    render(<PresentationControls page="consulta-5" revealed onNext={onNext} onPrevious={()=>{}}/>)
    const notesButton=screen.getByRole('button',{name:'Notas do apresentador. Atalho N'})
    notesButton.focus()
    await user.keyboard('n')
    const dialog=screen.getByRole('dialog',{name:'Notas do apresentador'})
    expect(within(dialog).getByRole('heading',{name:'Percurso sugerido'})).toBeTruthy()
    expect(within(dialog).getByRole('heading',{name:'Cuidados na interpretação'})).toBeTruthy()
    expect(dialog.contains(document.activeElement)).toBe(true)
    await user.keyboard('{ArrowRight}')
    expect(onNext).not.toHaveBeenCalled()
    await user.keyboard('{Escape}')
    await waitFor(()=>expect(screen.queryByRole('dialog')).toBeNull())
    expect(document.activeElement).toBe(notesButton)
    await user.keyboard('n')
    expect(screen.getByRole('dialog',{name:'Notas do apresentador'})).toBeTruthy()
    await user.keyboard('n')
    await waitFor(()=>expect(screen.queryByRole('dialog')).toBeNull())
  })

  it('usa a API fullscreen suportada e mantém um aviso quando o navegador a recusa',async()=>{
    const user=userEvent.setup()
    render(<PresentationControls page="consulta-1" revealed onNext={()=>{}} onPrevious={()=>{}}/>)
    await user.keyboard('f')
    expect(document.documentElement.requestFullscreen).toHaveBeenCalledTimes(1)
    expect(screen.getByRole('button',{name:'Sair da tela cheia. Atalho F'})).toBeTruthy()
    await user.keyboard('f')
    expect(document.exitFullscreen).toHaveBeenCalledTimes(1)
    vi.mocked(document.documentElement.requestFullscreen).mockRejectedValueOnce(new Error('denied'))
    await user.keyboard('f')
    expect(screen.getByRole('status').textContent).toContain('Não foi possível ativar a tela cheia')
  })
})

describe('Fluxos integrados da apresentação',()=>{
  it('navega entre consultas e preserva uma resposta já revelada ao voltar',async()=>{
    const user=userEvent.setup()
    history.replaceState(null,'','#consulta-1')
    render(<HashPresentation/>)
    await user.keyboard('{ArrowRight}')
    expect(location.hash).toBe('#consulta-1')
    expect(screen.getByText(approved[0][1],{exact:true})).toBeTruthy()
    await user.keyboard('{ArrowRight}')
    await waitFor(()=>expect(screen.getByRole('heading',{level:1,name:approved[1][0]})).toBeTruthy())
    expect(location.hash).toBe('#consulta-2')
    expect(screen.queryByText(approved[1][1],{exact:true})).toBeNull()
    await user.keyboard('{ArrowLeft}')
    await waitFor(()=>expect(screen.getByRole('heading',{level:1,name:approved[0][0]})).toBeTruthy())
    expect(screen.getByText(approved[0][1],{exact:true})).toBeTruthy()
  })

  it('mantém os quatro painéis do método montados e torna apenas a fase atual acessível',()=>{
    history.replaceState(null,'','#metodo')
    const {container}=render(<MethodPreview/>)
    const nodes=Array.from(container.querySelectorAll('.method-detail'))
    expectActiveMethod(container,0,nodes)
    for(let index=1;index<4;index++){
      act(()=>window.dispatchEvent(new CustomEvent('guia-method-step',{detail:1})))
      expectActiveMethod(container,index,nodes)
    }
    act(()=>window.dispatchEvent(new CustomEvent('guia-method-step',{detail:-1})))
    expectActiveMethod(container,2,nodes)
  })

  it('avança pelas quatro fases do método antes de entrar na primeira consulta',async()=>{
    const user=userEvent.setup()
    history.replaceState(null,'','#metodo')
    const {container}=render(<HashPresentation/>)
    const nodes=Array.from(container.querySelectorAll('.method-detail'))
    for(let index=1;index<4;index++){
      await user.keyboard('{ArrowRight}')
      expect(location.hash).toBe('#metodo')
      expectActiveMethod(container,index,nodes)
    }
    await user.keyboard('{ArrowRight}')
    await waitFor(()=>expect(location.hash).toBe('#consulta-1'))
    await waitFor(()=>expect(screen.getByRole('heading',{level:1,name:approved[0][0]})).toBeTruthy())
  })
})

