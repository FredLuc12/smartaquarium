import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export async function safeRequest(promise) {
  try {
    const res = await promise;
    return { data: res.data, error: null };
  } catch (err) {
    console.error(err);
    return { data: null, error: err };
  }
}
