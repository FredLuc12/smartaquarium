import { useEffect, useState } from "react";
import { getLastMeasure } from "./api/mesures";

export function CapteurCard({ capteur }) {
  const [last, setLast] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getLastMeasure(capteur.id).then(({ data, error }) => {
      if (error) setError("Erreur mesure");
      else setLast(data);
    });
  }, [capteur.id]);

  if (error) return <p>{error}</p>;

  return (
    <div>
      <h3>{capteur.nom}</h3>
      {last ? (
        <p>{last.valeur} {capteur.unite}</p>
      ) : (
        <p>Aucune mesure</p>
      )}
    </div>
  );
}
