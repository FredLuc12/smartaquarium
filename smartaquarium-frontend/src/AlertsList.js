import { useEffect, useState } from "react";
import { getActiveAlerts } from "./api/alertes";

export function AlertsList() {
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getActiveAlerts().then(({ data, error }) => {
      if (error) setError("Erreur alertes");
      else setAlerts(data || []);
    });
  }, []);

  if (error) return <p>{error}</p>;
  if (alerts.length === 0) return <p>Aucune alerte.</p>;

  return (
    <ul>
      {alerts.map((a) => (
        <li key={a.id}>{a.message}</li>
      ))}
    </ul>
  );
}