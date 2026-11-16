import fs from 'node:fs'
import ts from 'typescript'

function moduleFromFile(path, requireLocal=()=>{throw new Error('Unexpected dependency')}) {
 const source=fs.readFileSync(path,'utf8')
 const code=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText
 const exports={}
 new Function('exports','require',code)(exports,requireLocal)
 return exports
}
const data=moduleFromFile('src/data.ts')
const {presenterNotes}=moduleFromFile('src/presenter-notes.ts',name=>{if(name==='./data')return data;throw new Error(`Unexpected dependency: ${name}`)})
const lines=['# Guia Canadá — roteiro do apresentador','','IFAL · TABD 2026.2 · Eliezir Moreira e Raphael Phillipe','','Use este roteiro na janela do apresentador; o conteúdo destinado à turma está nos slides.','','Atalhos: ← / → navegam; → revela a resposta antes de avançar; N abre notas; F alterna tela cheia.','','## Procedência e limites','','Os dados e textos das consultas estão em src/data.ts. O processo documentado de extração e integração foi conferido no README do repositório de pesquisa. Não presumimos tabelas físicas nem SQL que não estejam documentados.','']
let index=0
for(const [page,note] of Object.entries(presenterNotes)) {
 lines.push(`## ${String(++index).padStart(2,'0')} — ${note.heading}`,'',`Slide: #${page}`,'',note.intro,'','### Percurso de fala','',...note.steps.map(item=>`- ${item}`),'','### Cuidados','',...note.caveats.map(item=>`- ${item}`),'','### Transição','',note.handoff,'')
}
fs.mkdirSync('public',{recursive:true})
fs.writeFileSync('public/roteiro-apresentador.md',lines.join(String.fromCharCode(10)))
console.log(`Roteiro exportado: ${index} slides.`)
