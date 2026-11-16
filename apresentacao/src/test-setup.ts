import { afterEach, vi } from 'vitest'
import { cleanup } from '@testing-library/react'

Object.defineProperty(window,'matchMedia',{configurable:true,writable:true,value:vi.fn((query:string)=>({matches:query.includes('prefers-reduced-motion'),media:query,onchange:null,addListener:vi.fn(),removeListener:vi.fn(),addEventListener:vi.fn(),removeEventListener:vi.fn(),dispatchEvent:()=>true}))})
Object.defineProperty(window,'scrollTo',{configurable:true,writable:true,value:vi.fn()})

const measure=function(this:HTMLElement){
  const measuringText=this.tagName==='SPAN' || this.tagName==='TEXT'
  return new DOMRect(0,0,measuringText ? Math.max(1,(this.textContent?.length??0)*7) : 900,measuringText ? 18 : 400)
}
Object.defineProperty(HTMLElement.prototype,'getBoundingClientRect',{configurable:true,value:measure})
Object.defineProperty(HTMLElement.prototype,'getClientRects',{configurable:true,value:function(this:HTMLElement){return [this.getBoundingClientRect()]}})
class TestResizeObserver implements ResizeObserver {
  constructor(private callback:ResizeObserverCallback){}
  observe(target:Element){this.callback([{target,contentRect:target.getBoundingClientRect()} as ResizeObserverEntry],this)}
  unobserve(){}
  disconnect(){}
}
vi.stubGlobal('ResizeObserver',TestResizeObserver)
Object.defineProperty(document,'fullscreenEnabled',{configurable:true,value:true})
Object.defineProperty(document,'fullscreenElement',{configurable:true,writable:true,value:null})
Object.defineProperty(document.documentElement,'requestFullscreen',{configurable:true,writable:true,value:vi.fn(async()=>{Object.defineProperty(document,'fullscreenElement',{configurable:true,writable:true,value:document.documentElement});document.dispatchEvent(new Event('fullscreenchange'))})})
Object.defineProperty(document,'exitFullscreen',{configurable:true,writable:true,value:vi.fn(async()=>{Object.defineProperty(document,'fullscreenElement',{configurable:true,writable:true,value:null});document.dispatchEvent(new Event('fullscreenchange'))})})

afterEach(()=>{cleanup();Object.defineProperty(document,'fullscreenElement',{configurable:true,writable:true,value:null})})
