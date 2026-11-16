import { queries } from './data'

export const presentationPages = [
 {id:'abertura',title:'Por que fizemos este projeto?'},
 {id:'perguntas',title:'As dez perguntas da pesquisa'},
 {id:'metodo',title:'Como fizemos a pesquisa'},
 ...queries.map((query,index)=>({id:`consulta-${index+1}`,title:`Consulta ${String(index+1).padStart(2,'0')} · ${query.title}`})),
 {id:'conclusoes',title:'O que aprendemos e quais são os limites'},
]
export function pageIndex(page:string){return presentationPages.findIndex(item=>item.id===page)}
export function navigatePresentation(page:string){location.hash=page}
