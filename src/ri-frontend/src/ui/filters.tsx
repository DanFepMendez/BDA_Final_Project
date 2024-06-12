'use client';

import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/outline";
import clsx from "clsx";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

export default function SearchFilters () {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  const params = new URLSearchParams(searchParams);
  const order = params.get('order')

  function sort(sortOrder: string) {
    params.set('order', sortOrder)

    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="w-full px-4 flex max-w-7xl">
      <div className="flex rounded-md border-2">
        <OrderButton onclick={sort} name="Fecha" isActive={order ? order.split('.')[0] == 'Date' : true} direction={order?.split('.')[1]} />
        <OrderButton onclick={sort} name="Similitud" isActive={order ? order.split('.')[0] == 'Sim' : false} direction={order?.split('.')[1]} last={true} hidden={!params.get('query')} />
      </div>
    </div>
  );
}

function OrderButton ({
  name,
  isActive,
  direction,
  last,
  hidden,
  onclick
}:{
  name: string,
  isActive: boolean,
  direction?: string
  last?: boolean,
  hidden?: boolean,
  onclick: Function
}){
  const className = clsx("flex items-center p-2 text-sm", {
    'bg-gray-100 text-blue-400 font-bold': isActive,
    'border-r-2': !last,
    'hidden': hidden
  }); 

  const Arrow = () => {
    if (direction == 'ASC' && isActive)
      return (<ChevronUpIcon className="w-4 h-4 ml-1 mt-0.5" />)
    else
      return (<ChevronDownIcon className="w-4 h-4 ml-1 mt-0.5" />)
  }

  return (
    <button onClick={(e) => {
      if (name === 'Fecha')
        onclick('Date.'+ (direction == 'ASC' ? 'DESC' : 'ASC'))        
      else if (name === 'Similitud') {
        onclick('Sim.'+ (direction == 'ASC' ? 'DESC' : 'ASC'))        
      }
    }} className={className}>
      {name} <Arrow />
    </button>
  );
}