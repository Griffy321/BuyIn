import { request } from './client';

// One function per player endpoint. Keep these in step with the request/response shapes in
// src/buyin/api/players.py.

// POST /players  { firstName, lastName }  →  { playerId }
export function createPlayer(firstName, lastName) {
  return request('/players', {
    method: 'POST',
    body: JSON.stringify({ firstName, lastName }),
  });
}

// GET /players/{playerId}  →  { playerId, firstName, lastName }
// Throws an ApiError with status 404 if there's no player with that ID.
export function getPlayer(playerId) {
  return request(`/players/${encodeURIComponent(playerId)}`);
}
