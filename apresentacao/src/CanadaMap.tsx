import { useId, useMemo, useState } from 'react'
import { geoConicConformal, geoPath } from 'd3-geo'
import type { FeatureCollection, Geometry, Feature } from 'geojson'
import { canadaGeography } from './canada-geography'
import { format, regions, regionsByCode, metrics, type Priority } from './data'
import './canada-map.css'

type GeographyProperties = {code:string; name:string; latitude:number; longitude:number}
const geography = canadaGeography as unknown as FeatureCollection<Geometry,GeographyProperties>
const projection = geoConicConformal().rotate([96,0]).center([0,60]).parallels([49,77]).fitExtent([[24,18],[682,440]],geography)
const path = geoPath(projection)
const features = geography.features.map(feature=>({feature,code:feature.properties.code,d:path(feature) ?? '',point:projection([feature.properties.longitude,feature.properties.latitude]) ?? [0,0]}))
const coral = ['#526f65','#8d9a80','#c7bd98','#e7aa8e','#f28f7b']

export type CanadaMapProps = {metric?:Priority;selected?:string;onSelect?:(code:string)=>void;compact?:boolean;highlight?:string[];neutral?:boolean}

/** Simplified geographic boundaries; all thirteen jurisdictions remain selectable. */
export function CanadaMap({metric='salary',selected,onSelect,compact=false,highlight=[],neutral=false}:CanadaMapProps) {
  const patternId=useId().replace(/:/g,'')
  const [hovered,setHovered]=useState<string|null>(null)
  const values=regions.map(region=>region[metric]).filter((value):value is number=>value!==null)
  const low=Math.min(...values),high=Math.max(...values)
  const active=hovered ?? selected
  function fill(code:string) {
    if(neutral) return '#b6c7b0'
    const value=regionsByCode[code][metric]
    if(value===null) return `url(#missing-${patternId})`
    if(highlight.length) return highlight.includes(code)?'#f39a83':'#426358'
    const intensity=metric==='housing'?(high-value)/(high-low):(value-low)/(high-low)
    return coral[Math.min(4,Math.max(0,Math.round(intensity*4)))]
  }
  return <div className={`canada-map ${compact?'canada-map-compact':''}`}>
    <svg viewBox="0 0 706 480" role={onSelect?'group':'img'} aria-label={onSelect?'Mapa das províncias e territórios do Canadá. Use Tab e Enter para selecionar.':'Mapa geográfico das treze províncias e territórios do Canadá'}>
      <defs><pattern id={`missing-${patternId}`} width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="7" height="7" fill="#39594d"/><path d="M0 0v7" stroke="#789084" strokeWidth="2"/></pattern></defs>
      <g className="map-graticule" aria-hidden="true"><path d="M70 146 Q350 80 654 174 M34 264 Q350 199 691 285 M90 380 Q350 322 620 390"/><path d="M168 47 Q121 230 181 421 M356 22 Q332 243 355 451 M550 62 Q597 230 562 425"/></g>
      {features.map(({code,d,point})=>{
        const region=regionsByCode[code]
        const isActive=active===code
        const value=region[metric]
        return <g key={code} className={`map-jurisdiction ${isActive?'is-active':''} ${selected===code?'is-selected':''}`} role={onSelect?'button':undefined} tabIndex={onSelect?0:undefined} aria-label={neutral?region.name:`${region.name}: ${format(metric,value)}`} aria-pressed={onSelect?selected===code:undefined} onClick={()=>onSelect?.(code)} onKeyDown={event=>{if(onSelect&&(event.key==='Enter'||event.key===' ')){event.preventDefault();onSelect(code)}}} onMouseEnter={()=>setHovered(code)} onMouseLeave={()=>setHovered(null)} onFocus={()=>setHovered(code)} onBlur={()=>setHovered(null)}>
          <title>{neutral?region.name:`${region.name} · ${format(metric,value)}`}</title>
          <path className="map-region" d={d} fill={fill(code)}/>
          {(!compact||['BC','AB','ON','QC'].includes(code)) && !['PE','NB','NS'].includes(code) && <text className="map-label" x={point[0]} y={point[1]+4} textAnchor="middle" aria-hidden="true">{code}</text>}
        </g>
      })}
      {!compact && <g className="map-atlantic" aria-hidden="true">{features.filter(({code})=>['PE','NB','NS'].includes(code)).map(({code,point})=>{
        const offset={NB:[40,-23],PE:[55,-5],NS:[45,20]}[code]!
        const x=point[0]+offset[0],y=point[1]+offset[1]
        return <g key={code}><path d={`M${point[0]},${point[1]} L${x-10},${y-4}`} stroke="#d9e4d4" strokeWidth="1" fill="none"/><text className="map-label map-label-external" x={x} y={y}>{code}</text></g>
      })}</g>}
      <text className="map-ocean" x="74" y="354" transform="rotate(-18 74 354)" aria-hidden="true">PACÍFICO</text><text className="map-ocean" x="620" y="335" transform="rotate(15 620 335)" aria-hidden="true">ATLÂNTICO</text>
    </svg>
    {!compact && <div className="map-legend"><div className="map-scale"><span>{format(metric,metric==='housing'?high:low)}</span><i aria-hidden="true"/><span>{format(metric,metric==='housing'?low:high)}</span></div><span className="map-missing"><i aria-hidden="true"/> Sem dado</span></div>}
    {!compact && <p className="map-unit">{metric==='score'?'Índice de equilíbrio · escala de 0 a 100':`${metrics[metric].title} · ${metrics[metric].unit}`}<span>Limites geográficos simplificados · Natural Earth</span></p>}
  </div>
}

export function ProvinceFlag({code}:{code:string}) {
  const [failed,setFailed]=useState(false)
  return failed?<span className="province-flag-fallback" aria-label={regionsByCode[code]?.name ?? code}>{code}</span>:<img className="province-flag" src={`${import.meta.env.BASE_URL}flags/${code}.svg`} alt={`Bandeira de ${regionsByCode[code]?.name ?? code}`} width="56" height="36" loading="lazy" onError={()=>setFailed(true)}/>
}

export function ProvinceSilhouette({code}:{code:string}) {
  const d=useMemo(()=>{
    const feature=geography.features.find(feature=>feature.properties.code===code)
    if(!feature)return ''
    const localProjection=geoConicConformal().rotate([96,0]).center([0,60]).parallels([49,77]).fitExtent([[8,8],[152,112]],feature as Feature)
    return geoPath(localProjection)(feature) ?? ''
  },[code])
  return <svg className="province-silhouette" viewBox="0 0 160 120" aria-hidden="true"><path d={d}/></svg>
}


