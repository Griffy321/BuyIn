// Where the Python server is running. The phone can't use "localhost" (that means the phone itself),
// so this is the PC's address on the Wi-Fi.
//
// dev.ps1 (in the repo root) looks up the PC's current IP and passes it in as EXPO_PUBLIC_API_URL,
// so you normally don't need to touch this. The address below is only a fallback for when the app
// is started some other way, e.g. a plain `npx expo start`.
export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://192.168.40.248:5000';
