import { useEffect, useState } from "react";
import { getCapteurs } from "./api/capteurs";

export default function CapteursList() {
  const [capteurs, setCapteurs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getCapteurs().then(({ data, error }) => {
      if (error) setError("Erreur capteurs");
      else setCapteurs(data || []);
    });
  }, []);

  useEffect(() => {
    getCapteurs()
      .then(setCapteurs)
      .catch((e) => {
        console.error(e);
        setError("Erreur de chargement");
      });
  }, []);

  if (error) return <p>{error}</p>;

  return (
    <pre>{JSON.stringify(capteurs, null, 2)}</pre>
  );
}
