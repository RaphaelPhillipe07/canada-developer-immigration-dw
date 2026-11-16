import { useEffect, useState } from 'react'
import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, expect, it, vi } from 'vitest'
import { Presentation } from './Presentation'
import { PresenterWindow } from './PresenterWindow'

class LocalChannel {
 static peers=new Set<LocalChannel>()
 onmessage:((event:MessageEvent)=>void)|null=null
 constructor(public name:string){LocalChannel.peers.add(this)}
 postMessage(data:unknown){for(const peer of LocalChannel.peers)if(peer!==this&&peer.name===this.name)queueMicrotask(()=>{if(LocalChannel.peers.has(peer))peer.onmessage?.({data} as MessageEvent)})}
 close(){LocalChannel.peers.delete(this)}
}
const original=globalThis.BroadcastChannel
afterEach(()=>{vi.stubGlobal('BroadcastChannel',original);LocalChannel.peers.clear()})
function LivePresentation(){
 const [page,setPage]=useState(location.hash.slice(1))
 useEffect(()=>{const change=()=>setPage(location.hash.slice(1));window.addEventListener('hashchange',change);return()=>window.removeEventListener('hashchange',change)},[])
 return <><Presentation page={page}/><PresenterWindow/></>
}
it('sincroniza o roteiro separado, revela sem avançar e navega pela janela do apresentador',async()=>{
 vi.stubGlobal('BroadcastChannel',LocalChannel)
 history.replaceState(null,'','#consulta-1')
 const user=userEvent.setup()
 const {container}=render(<LivePresentation/>)
 const companion=container.querySelector('.presenter-window') as HTMLElement
 await waitFor(()=>expect(within(companion).getByRole('status').textContent).toContain('Sincronizada'))
 expect(within(companion).getByText('Resposta ainda não revelada na apresentação.')).toBeTruthy()
 await user.click(within(companion).getByRole('button',{name:'Ver resposta'}))
 await waitFor(()=>expect(container.querySelector('.analytical-answer')).toBeTruthy())
 expect(location.hash).toBe('#consulta-1')
 await waitFor(()=>expect(within(companion).getByText('Resposta revelada na apresentação.')).toBeTruthy())
 await user.selectOptions(within(companion).getByRole('combobox'),'consulta-10')
 await waitFor(()=>expect(location.hash).toBe('#consulta-10'))
 await waitFor(()=>expect(container.querySelector('.analytical-coverage')).toBeTruthy())
 expect(within(companion).getByRole('heading',{name:'O que apresentar nesta tela'})).toBeTruthy()
})
