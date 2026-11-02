import { API_URL } from '../config';

// Shared by every API call: sends JSON, reads JSON back, and turns failures into readable errors.
// Gives up after a few seconds instead of hanging forever when the server can't be reached.
export async function request(path, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);

  try {
    const res = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
      signal: controller.signal,
    });
    if (!res.ok) {
      throw new Error(`Server replied with ${res.status}`);
    }
    return await res.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error(`Couldn't reach the server at ${API_URL}`);
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}
