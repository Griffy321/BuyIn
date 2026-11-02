import { request } from './client';

// One function per player endpoint. Keep these in step with the records in src/Program.cs.

// POST /players  { firstName, lastName }  →  { playerId }
export function createPlayer(firstName, lastName) {
  return request('/players', {
    method: 'POST',
    body: JSON.stringify({ firstName, lastName }),
  });
}
