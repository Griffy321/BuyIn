import { API_URL } from '../config';

// Thrown when the server answers with an error. `status` lets screens react to specific replies,
// e.g. App treats a 404 from GET /players/{id} as "this player no longer exists".
export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

// Shared by every API call: sends JSON, reads JSON back, and turns failures into readable errors.
// Gives up after a few seconds instead of hanging forever when the server can't be reached.
export async function request(path, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);

  try {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new ApiError(response.status, await readErrorMessage(response));
    }
    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error(`Couldn't reach the server at ${API_URL}`);
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

// The server's problem() responses carry a human-readable "detail", e.g.
// "Please provide both first and last name". Falls back to the status code if there isn't one.
async function readErrorMessage(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === 'string') return body.detail;
  } catch {
    // Not JSON, so there's no detail to show.
  }
  return `Server replied with ${response.status}`;
}
