import * as SecureStore from 'expo-secure-store';

// Remembers who the player is between app launches, using the phone's encrypted storage
// (the Android Keystore). Screens use these functions rather than SecureStore directly, so when
// the player ID is swapped for a secret token later, only this file needs to change.
//
// Stored values are wiped if the app is uninstalled.

const PLAYER_ID_KEY = 'playerId';

// The saved player ID, or null if this phone hasn't created a player yet.
export function getPlayerId() {
  return SecureStore.getItemAsync(PLAYER_ID_KEY);
}

export function savePlayerId(playerId) {
  return SecureStore.setItemAsync(PLAYER_ID_KEY, playerId);
}

// Makes the app treat this phone as a brand-new player again.
export function forgetPlayerId() {
  return SecureStore.deleteItemAsync(PLAYER_ID_KEY);
}
