// api/alertes.js
import { api } from "./client";

export async function getActiveAlerts() {
  const res = await api.get("/api/alertes/active");
  return res.data;
}