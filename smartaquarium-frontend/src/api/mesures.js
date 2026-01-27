// api/mesures.js
import { api } from "./client";

export async function getLastMeasure(capteurId) {
  const res = await api.get(`/api/mesures/capteur/${capteurId}/latest`);
  return res.data;
}