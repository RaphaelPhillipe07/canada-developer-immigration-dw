import { useId, useState, type ComponentProps, type ReactNode } from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { AnimatePresence, motion, useReducedMotion } from 'motion/react'
import { ChevronDown } from 'lucide-react'

// shadcn/ui Button with the site's theme and size variants.
const buttonVariants = cva('action', {
  variants: { variant: { default: 'action-primary', outline: 'action-outline', ghost: 'action-ghost' } },
  defaultVariants: { variant: 'default' },
})

export function Button({className, variant, asChild, ...props}: ComponentProps<'button'> & VariantProps<typeof buttonVariants> & {asChild?:boolean}) {
  const Element = asChild ? Slot : 'button'
  return <Element {...props} className={twMerge(clsx(buttonVariants({variant}), className))} />
}

// Adapted from beUI Animated Collapsible (MIT). Attribution in THIRD_PARTY_NOTICES.
export function Collapsible({label, children}: {label:string; children:ReactNode}) {
  const [open, setOpen] = useState(false)
  const reduce = useReducedMotion()
  const id = useId()
  return <div className="disclosure">
    <motion.button type="button" id={`${id}-trigger`} aria-expanded={open} aria-controls={id} onClick={() => setOpen(!open)}>
      {label}<motion.span animate={{rotate:open ? 180 : 0}} transition={{duration:reduce ? 0 : .2}}><ChevronDown size={18}/></motion.span>
    </motion.button>
    <div id={id} role="region" aria-labelledby={`${id}-trigger`} inert={!open}>
      <AnimatePresence initial={false}>
        {open && <motion.div className="disclosure-content" initial={{height:0,opacity:0}} animate={{height:'auto',opacity:1}} exit={{height:0,opacity:0}} transition={{duration:reduce ? 0 : .2}}><div>{children}</div></motion.div>}
      </AnimatePresence>
    </div>
  </div>
}

export function Flag() {
 return <span className="flag" aria-hidden="true" style={{width:40,height:20,background:'transparent',borderRadius:0,border:0}}><img src={`${import.meta.env.BASE_URL}flags/CA.svg`} alt="" width={40} height={20} style={{display:'block',width:'100%',height:'100%',objectFit:'contain',filter:'none'}}/></span>
}
