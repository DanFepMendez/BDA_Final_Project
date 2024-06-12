import { fetchPublicaciones } from "@/lib/api";
import { EgresadoRes, RegistroPublicacionRes } from "@/lib/definitions";
import { formatDateToLocal, formatEgresado } from "@/lib/utils";


export default async function PublicacionesResults({
  query,
  currentPage,
  order
}: {
  query: string;
  currentPage: number;
  order: string;
}) {
  const results = await fetchPublicaciones(query, currentPage, order);

  return (
    <div className="w-full md:max-w-6xl px-4">
      <div className="mt-6 flex flex-col">
        {results.map((result: RegistroPublicacionRes) => (
          <div
            key={result.registration_id}
            className="flex flex-col mb-4 py-8 border-b-slate-300 border-b-[1px]"
          >
            <p className="mb-1 text-lg">{result.publicacion_id.descripcion}</p>
            <p className="mb-1 text-base text-gray-500">
              {formatEgresado(result.egresado_id)}
            </p>
            <div className="flex text-sm">
              <p>{formatDateToLocal(result.date_id)}</p>
              <span className="mx-2">|</span>
              <p>
                {result.revista_id ? (
                  <p>
                    <b>revista: </b>
                    {result.revista_id.revista_nombre}
                  </p>
                ) : (
                  <p>
                    <b>institución: </b>
                    {result.institucion_id?.institucion_nombre}
                  </p>
                )}
              </p>
              {result.similitud ? (
                <>
                  <span className="mx-2">|</span>
                  <p>
                    <b>similitud: </b>
                    {result.similitud}
                  </p>
                </>
              ) : (
                <></>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
