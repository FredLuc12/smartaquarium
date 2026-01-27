import { api } from "./client";

export async function getCapteurs() {
  const res = await api.get("/api/capteurs");
  return res.data;
}
