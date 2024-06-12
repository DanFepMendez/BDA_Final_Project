"use client";

import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import { useSearchParams, usePathname, useRouter } from "next/navigation";

export default function Search({ placeholder }: { placeholder: string }) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  function handleSearch(term: string) {
    const params = new URLSearchParams(searchParams);
    params.set("page", "1");

    if (term) {
      params.set("query", term);
      // if (!params.get('order'))
      params.set('order', 'Sim.DESC')
  } else {
      params.delete("query");
      params.delete('order')
    }

    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="w-full md:max-w-7xl -translate-y-1/2 px-4 xl:p-0">
      <div className="relative flex flex-1 flex-shrink-0 shadow-md">
        <label htmlFor="search" className="sr-only">
          Search
        </label>
        <input
          className="peer block w-full rounded-md border border-gray-200 py-[15px] pl-14 text-lg outline-2 placeholder:text-gray-500"
          placeholder={placeholder}
          onKeyDown={(e) => {
            if (e.key == "Enter") {
              handleSearch(e.currentTarget.value);
            }
          }}
          defaultValue={searchParams.get("query")?.toString()}
        />
        <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-[30px] w-[30px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
      </div>
    </div>
  );
}
