import { Component, type ReactNode } from 'react'
import { useEffect, useState } from 'react'
import { useReducedMotion } from 'motion/react'
import { Bar, BarChart, CartesianGrid, Cell, LabelList, ReferenceLine, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from 'recharts'
import { format, metrics, periods, rank, regions, type Metric, type Priority, type Region } from './data'
import './charts.css'

const palette = { red:'#a72f3d', redSoft:'#dba39d', green:'#315b4c', ink:'#423d36', muted:'#776d62', grid:'#e7dfd2', cream:'#fbf8f1' }
const periodColors = ['#d8d2c7','#b3bba8','#7b9481','#3f6a59','#a72f3d']
const num = (value:number) => value.toLocaleString('pt-BR')
const compact = (value:number) => value>=1000 ? `${(value/1000).toLocaleString('pt-BR',{maximumFractionDigits:1})} mil` : num(value)

function useCompactCharts(query='(max-width:600px)') {
  const [compactLayout,setCompactLayout] = useState(()=>typeof window!=='undefined' && window.matchMedia(query).matches)
  useEffect(()=>{
    const media=window.matchMedia(query)
    const change=()=>setCompactLayout(media.matches)
    media.addEventListener('change',change)
    return ()=>media.removeEventListener('change',change)
  },[query])
  return compactLayout
}

class ChartBoundary extends Component<{children:ReactNode;fallback:ReactNode},{failed:boolean}> {
  state = {failed:false}
  static getDerivedStateFromError() { return {failed:true} }
  render() { return this.state.failed ? <div className="chart-error"><p>Valores disponíveis em tabela.</p>{this.props.fallback}</div> : this.props.children }
}

export function DataTable({headers,rows}: {headers:string[];rows:(number|string)[][]}) {
  return <div className="table-scroll" tabIndex={0} role="region" aria-label="Tabela de dados"><table><thead><tr>{headers.map(header=><th key={header} scope="col">{header}</th>)}</tr></thead><tbody>{rows.map((row,rowIndex)=><tr key={`${row[0]}-${rowIndex}`} className={String(row[0]).startsWith('●') ? 'data-highlight' : undefined}><th scope="row">{row[0]}</th>{row.slice(1).map((cell,index)=><td key={index}><span className={cell==='Sem dado' ? 'no-data-value' : undefined}>{cell}</span></td>)}</tr>)}</tbody></table></div>
}

function Evidence({label,children,table,summary='Ver todos os valores'}: {label:string;children:ReactNode;table:ReactNode;summary?:string}) {
  return <div className="evidence-chart" role="group" aria-label={label}><ChartBoundary key={label} fallback={table}>{children}</ChartBoundary><details className="chart-values"><summary>{summary}</summary>{table}</details></div>
}

function ValueLabel({x=0,y=0,width=0,height=0,value,metric,size=15}: {x?:number|string;y?:number|string;width?:number|string;height?:number|string;value?:unknown;metric:Priority;size?:number}) {
  return <text x={Number(x)+Number(width)+9} y={Number(y)+Number(height)/2} dominantBaseline="central" fill={palette.ink} fontSize={size} fontWeight={700}>{format(metric,typeof value==='number' ? value : Number(value))}</text>
}

export function BarPanel({metric, items, presentation=false}: {metric:Priority;items:Region[];presentation?:boolean}) {
  const reduce = useReducedMotion()
  const compactLayout = useCompactCharts()
  const shortScreen = useCompactCharts('(min-width:850px) and (max-height:800px)')
  const title = metric==='score' ? 'Pontuação de equilíbrio' : metrics[metric].title
  const unit = metric==='score' ? 'pontos · escala 0–100' : metrics[metric].unit
  const max = metric==='score' ? 100 : metrics[metric].scale
  const data = items.map(region=>({...region,value:region[metric]}))
  const table = <DataTable headers={['Jurisdição',`${title} · ${unit}`]} rows={items.map(region=>[region.name,format(metric,region[metric])])}/>
  const height = Math.max(presentation ? shortScreen ? 230 : 260 : 190,items.length*(presentation ? shortScreen ? 21 : 25 : 28)+35)
  return <Evidence label={`${title} por jurisdição`} table={table}>
    <div className={`chart-surface bar-chart${presentation ? ' is-presentation' : ''}`} style={{height}}>
      <ResponsiveContainer width="100%" height="100%" minWidth={0} debounce={50}>
        <BarChart layout="vertical" data={data} margin={{top:5,right:compactLayout ? 107 : 127,left:0,bottom:0}} barCategoryGap="28%" accessibilityLayer>
          <CartesianGrid stroke={palette.grid} strokeDasharray="3 5" horizontal={false}/>
          <XAxis type="number" domain={[0,max]} tick={{fontSize:presentation ? 14 : 13,fill:palette.muted}} tickLine={false} axisLine={false} tickFormatter={value=>num(Number(value))} tickCount={compactLayout ? 3 : 5}/>
          <YAxis type="category" dataKey={presentation && !compactLayout ? 'name' : 'code'} width={presentation && !compactLayout ? 205 : 34} tick={{fontSize:presentation && !compactLayout ? 14 : 13,fill:palette.ink,fontWeight:600}} tickLine={false} axisLine={false} interval={0}/>
          <Tooltip cursor={{fill:'#f0e7dc'}} contentStyle={{border:'1px solid #e0d4c7',borderRadius:12,background:palette.cream,fontSize:13}} formatter={value=>[format(metric,Number(value)),title]} labelFormatter={(_,payload)=>payload?.[0]?.payload?.name ?? ''}/>
          <Bar dataKey="value" radius={[0,5,5,0]} maxBarSize={22} isAnimationActive={!reduce} animationDuration={500} animationBegin={30}>
            {data.map((row,index)=><Cell key={row.code} fill={index===0 ? palette.red : index<3 ? palette.green : '#98aa99'}/>)}
            <LabelList dataKey="value" content={<ValueLabel metric={metric} size={compactLayout ? 13 : 15}/>}/>
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
    <div className="chart-axis-caption">{unit}</div>
  </Evidence>
}

export function PeriodPanel() {
  const reduce = useReducedMotion()
  const compactLayout = useCompactCharts()
  const groups = rank('community')
  const top = groups.slice(0,5).map(region=>({name:region.name,code:region.code,...Object.fromEntries(region.periods.map((value,index)=>[`p${index}`,value]))}))
  const table = <DataTable headers={['Jurisdição',...periods.map(period=>`${period} · pessoas`)]} rows={groups.map(region=>[region.name,...region.periods.map(value=>num(value))])}/>
  return <Evidence label="Imigrantes nascidos no Brasil por período de chegada" table={table} summary="Ver as 13 jurisdições por período">
    <div className="chart-context">Cinco maiores comunidades <span>· pessoas por período de chegada</span></div>
    <div className="chart-surface period-chart" style={{height:240}}>
      <ResponsiveContainer width="100%" height="100%" minWidth={0} debounce={50}>
        <BarChart layout="vertical" data={top} margin={{top:5,right:16,left:0,bottom:0}} accessibilityLayer barCategoryGap="30%">
          <CartesianGrid stroke={palette.grid} strokeDasharray="3 5" horizontal={false}/>
          <XAxis type="number" tick={{fontSize:14,fill:palette.muted}} tickLine={false} axisLine={false} tickFormatter={value=>compact(Number(value))} tickCount={compactLayout ? 3 : 5}/>
          <YAxis type="category" dataKey={compactLayout ? 'code' : 'name'} width={compactLayout ? 36 : 128} tick={{fontSize:compactLayout ? 13 : 14,fill:palette.ink,fontWeight:600}} tickLine={false} axisLine={false} interval={0}/>
          <Tooltip cursor={{fill:'#f0e7dc'}} contentStyle={{border:'1px solid #e0d4c7',borderRadius:12,background:palette.cream,fontSize:13}} formatter={(value,name)=>[`${num(Number(value))} pessoas`,periods[Number(String(name).replace('p',''))] ?? name]}/>
          {periods.map((period,index)=><Bar key={period} dataKey={`p${index}`} name={`p${index}`} stackId="arrivals" fill={periodColors[index]} radius={index===4 ? [0,4,4,0] : undefined} maxBarSize={30} isAnimationActive={!reduce} animationDuration={500}>
            {index===4 && <LabelList dataKey="p4" position="insideRight" fill="#fffaf2" fontSize={compactLayout ? 12 : 14} fontWeight={700} formatter={value=>num(Number(value))}/>}
          </Bar>)}
        </BarChart>
      </ResponsiveContainer>
    </div>
    <ul className="viz-legend period-legend">{periods.map((period,index)=><li key={period}><span style={{background:periodColors[index]}}/>{period}</li>)}</ul>
    <div className="community-totals">{groups.slice(0,3).map(region=><div key={region.code}><span>{region.name}</span><strong>{num(region.community)} <small>pessoas · total censitário</small></strong><p>{num(region.periods[4])} em 2011–2021</p></div>)}</div>
  </Evidence>
}

type Point = {x:number;y:number;code:string;name:string;highlight:boolean}
type PointShapeProps = {cx?:number;cy?:number;payload?:Point}
function ScatterPoint({cx=0,cy=0,payload}:PointShapeProps) {
  if (!payload) return <g/>
  const offsets:Record<string,[number,number]> = {NL:[10,-8],PE:[10,18],NS:[10,16],NB:[-12,-12],QC:[11,17],ON:[-11,-11],MB:[10,-12],SK:[10,-12],AB:[10,17],BC:[-11,-11]}
  const [dx,dy] = offsets[payload.code] ?? [10,-10]
  return <g><circle cx={cx} cy={cy} r={payload.highlight ? 7 : 5} fill={payload.highlight ? palette.red : '#85958b'} stroke={palette.cream} strokeWidth={2}/><text x={cx+dx} y={cy+dy} textAnchor={dx<0 ? 'end' : 'start'} fill={payload.highlight ? palette.red : palette.ink} fontSize={14} fontWeight={700} paintOrder="stroke" stroke={palette.cream} strokeWidth={4} strokeLinejoin="round">{payload.code}</text></g>
}

export function ScatterPanel({xy,highlight=[],presentation=false}: {xy:[Metric|'arrivals',Metric];highlight?:string[];presentation?:boolean}) {
  const reduce = useReducedMotion()
  const compactLayout = useCompactCharts()
  const [x,y] = xy
  const titleX = x==='arrivals' ? 'Chegadas em 2011–2021 · pessoas' : `${metrics[x].title} · ${metrics[x].unit}`
  const titleY = `${metrics[y].title} · ${metrics[y].unit}`
  const xMetric = x==='arrivals' ? 'community' : x
  const values:Point[] = regions.filter(region=>!['NU','NT','YT'].includes(region.code) && region[y]!==null).map(region=>({x:x==='arrivals' ? region.periods[4] : region[x] ?? 0,y:region[y] ?? 0,code:region.code,name:region.name,highlight:highlight.includes(region.code)}))
  const thresholdX = x==='community' ? 1122.5 : x==='housing' ? 33.3 : undefined
  const thresholdY = y==='salary' ? 45.67 : y==='housing' ? 33.3 : undefined
  const minY = y==='salary' ? 38 : 22
  const maxY = y==='salary' ? 56 : 42
  const maxX = x==='housing' ? 42 : Math.ceil(Math.max(...values.map(point=>point.x))*1.14/1000)*1000
  const table = <DataTable headers={['Jurisdição',titleX,titleY,'Critérios']} rows={values.map(value=>[value.name,format(xMetric,value.x),format(y,value.y),value.highlight ? 'Atende' : '—'])}/>
  return <Evidence label={`${titleX} × ${titleY}`} table={table} summary="Ver valores e nomes completos">
    <div className="chart-axis-top">{titleY}</div>
    <div className="chart-surface scatter-chart" style={{height:presentation ? 267 : 275}}>
      <ResponsiveContainer width="100%" height="100%" minWidth={0} debounce={50}>
        <ScatterChart margin={{top:18,right:28,left:0,bottom:5}} accessibilityLayer>
          <CartesianGrid stroke={palette.grid} strokeDasharray="3 5"/>
          <XAxis type="number" dataKey="x" domain={[0,maxX]} tick={{fontSize:presentation ? 14 : 13,fill:palette.muted}} tickLine={false} axisLine={false} tickFormatter={value=>x==='housing' ? `${num(Number(value))}%` : compact(Number(value))} tickCount={compactLayout ? 3 : 5}/>
          <YAxis type="number" dataKey="y" domain={[minY,maxY]} width={48} tick={{fontSize:presentation ? 14 : 13,fill:palette.muted}} tickLine={false} axisLine={false} tickFormatter={value=>y==='housing' ? `${num(Number(value))}%` : num(Number(value))} tickCount={5}/>
          {thresholdX!==undefined && <ReferenceLine x={thresholdX} stroke={palette.green} strokeDasharray="5 5" strokeOpacity={.6}/>}
          {thresholdY!==undefined && <ReferenceLine y={thresholdY} stroke={palette.green} strokeDasharray="5 5" strokeOpacity={.6}/>}
          <Tooltip cursor={{strokeDasharray:'3 3'}} content={({active,payload})=>{const point=payload?.[0]?.payload as Point|undefined;return active && point ? <div className="viz-tooltip"><strong>{point.name}</strong><span>{format(xMetric,point.x)}</span><span>{format(y,point.y)}</span></div> : null}}/>
          <Scatter data={values} shape={<ScatterPoint/>} isAnimationActive={!reduce} animationDuration={450}/>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
    <div className="chart-axis-caption">{titleX}</div>
    <ul className="viz-legend scatter-legend"><li><span style={{background:palette.red}}/>Atende aos critérios</li><li><span style={{background:'#85958b'}}/>Demais províncias</li><li><span className="legend-line"/>Cortes de referência</li></ul>
    <div className="highlight-provinces">{values.filter(value=>value.highlight).map(value=><span key={value.code}><b>{value.code}</b><span className="highlight-province-data"><strong>{value.name}</strong><small>{format(xMetric,value.x)}{xMetric==='community' ? ' pessoas' : ''} · {format(y,value.y)}</small></span></span>)}</div>
  </Evidence>
}

export function GroupPanel() {
  const reduce=useReducedMotion()
  const compactLayout=useCompactCharts()
  const groups=[
    {name:'Maiores',fullName:'Cinco maiores comunidades',salary:48.08,housing:34,coverage:'5 de 5'},
    {name:'Menores',fullName:'Cinco menores comunidades',salary:44.71,housing:32.5,coverage:'4 de 5'},
  ]
  const table=<DataTable headers={['Grupo','Salário mediano · CAD/h','Cobertura salarial','Moradia · %']} rows={groups.map(group=>[group.fullName,format('salary',group.salary),group.coverage,format('housing',group.housing)])}/>
  return <Evidence label="Medianas por grupo de presença brasileira" table={table}>
    <ul className="viz-legend group-legend"><li><span style={{background:palette.red}}/>Cinco maiores comunidades</li><li><span style={{background:palette.green}}/>Cinco menores comunidades</li></ul>
    <div className="group-comparisons">{(['salary','housing'] as const).map(metric=><section className="group-comparison" key={metric}><h3>{metric==='salary' ? 'Salário mediano' : 'Inacessibilidade habitacional'}</h3><p>{metric==='salary' ? 'CAD por hora' : 'Percentual de inquilinos'}</p><div className="chart-surface" style={{height:145}}><ResponsiveContainer width="100%" height="100%" minWidth={0}><BarChart data={groups} layout="vertical" margin={{top:12,right:compactLayout ? 105 : 100,left:0,bottom:0}} barCategoryGap="35%" accessibilityLayer><CartesianGrid stroke={palette.grid} strokeDasharray="3 5" horizontal={false}/><XAxis type="number" domain={[0,metric==='salary' ? 60 : 50]} tick={{fontSize:14,fill:palette.muted}} axisLine={false} tickLine={false} tickCount={4}/><YAxis dataKey="name" type="category" width={60} tick={{fontSize:14,fill:palette.ink,fontWeight:600}} axisLine={false} tickLine={false}/><Bar dataKey={metric} maxBarSize={24} radius={[0,5,5,0]} isAnimationActive={!reduce} animationDuration={450}>{groups.map((group,index)=><Cell key={group.name} fill={index===0 ? palette.red : palette.green}/>)}<LabelList dataKey={metric} content={<ValueLabel metric={metric} size={compactLayout ? 13 : 15}/>}/></Bar></BarChart></ResponsiveContainer></div></section>)}</div>
    <div className="group-coverage"><span><strong>5 de 5</strong> províncias com salário · maiores comunidades</span><span><strong>4 de 5</strong> províncias com salário · menores comunidades</span></div>
  </Evidence>
}
