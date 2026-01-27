// src/api/actionneurs.js
import { api, safeRequest } from "./client";

export async function toggleActionneur(id, newEtat) {
  // selon la spec de ton collègue : PUT /api/actionneurs/{id}
  return safeRequest(
    api.put(`/api/actionneurs/${id}`, { etat: newEtat })
  );
}
