import { useState } from "react";
import { toggleActionneur } from "./api/actionneurs";

export function ActionneurToggle({ actionneur }) {
  const [etat, setEtat] = useState(actionneur.etat);
  const [loading, setLoading] = useState(false);

  async function handleClick() {
    setLoading(true);
    const { data, error } = await toggleActionneur(actionneur.id, !etat);
    setLoading(false);
    if (!error) setEtat(!etat);
  }

  return (
    <button onClick={handleClick} disabled={loading}>
      {etat ? "ON" : "OFF"}
    </button>
  );
}
