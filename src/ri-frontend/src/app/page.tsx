import Search from "@/ui/search";
import PublicacionesResults from "@/ui/pub-results";
import { fetchResultsPages } from "@/lib/api";
import Pagination from "@/ui/pagination";
import SearchFilters from "@/ui/filters";

export default async function Page({
  searchParams,
}: {
  searchParams?: {
    query?: string;
    page?: string;
    order?: string;
  };
}) {
  const query = searchParams?.query || '';
  const currentPage = Number(searchParams?.page) || 1;
  const order = query ? searchParams?.order || 'Date.DESC' : searchParams?.order || '';

  const totalPages = await fetchResultsPages(query);

  return (
    <main className="flex flex-col items-center pb-8">
      <div className="w-full h-40 bg-slate-400"></div>
      <Search placeholder="Buscar publicación" />
      <SearchFilters />
      <PublicacionesResults order={order} query={query} currentPage={currentPage} />
      <Pagination totalPages={totalPages} />
    </main>
  );
}