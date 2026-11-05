import { request } from './client';

// One function per player endpoint. Keep these in step with the request/response shapes in src/main.py.

// POST /players  { firstName, lastName }  →  { playerId }
export function createPlayer(firstName, lastName) {
  return request('/players', {
    method: 'POST',
    body: JSON.stringify({ firstName, lastName }),
  });
}
