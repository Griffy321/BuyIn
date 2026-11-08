import { StatusBar } from 'expo-status-bar';
import { useCallback, useEffect, useState } from 'react';
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ApiError } from './src/api/client';
import { getPlayer } from './src/api/players';
import CreatePlayerScreen from './src/screens/CreatePlayer/CreatePlayerScreen';
import HomeScreen from './src/screens/Home/HomeScreen';
import { forgetPlayerId, getPlayerId } from './src/storage/playerStorage';
import { colors, radius, spacing } from './src/theme';

// On launch, works out who's using this phone:
//   no saved ID                          → Create player (first time)
//   saved ID, server knows it            → Home (returning player)
//   saved ID, server says 404            → forget the ID, then Create player
//                                          (e.g. the database was reset)
//   saved ID, server can't be reached    → offline screen with Retry. The ID is kept,
//                                          because the player probably still exists.
export default function App() {
  // 'loading' | 'ready' | 'offline' | 'storageError'
  const [status, setStatus] = useState('loading');
  const [player, setPlayer] = useState(null);
  const [isNewPlayer, setIsNewPlayer] = useState(false);
  const [offlineMessage, setOfflineMessage] = useState('');

  const loadSavedPlayer = useCallback(async () => {
    setStatus('loading');

    let savedId;
    try {
      savedId = await getPlayerId();
    } catch {
      setStatus('storageError');
      return;
    }

    if (!savedId) {
      setPlayer(null);
      setStatus('ready');
      return;
    }

    try {
      const savedPlayer = await getPlayer(savedId);
      setPlayer(savedPlayer);
      setIsNewPlayer(false);
      setStatus('ready');
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        await forgetPlayerId();
        setPlayer(null);
        setStatus('ready');
      } else {
        setOfflineMessage(error.message);
        setStatus('offline');
      }
    }
  }, []);

  useEffect(() => {
    loadSavedPlayer();
  }, [loadSavedPlayer]);

  function handleCreated(newPlayer) {
    setPlayer(newPlayer);
    setIsNewPlayer(true);
  }

  async function handleForget() {
    await forgetPlayerId();
    setPlayer(null);
  }

  let screen;
  if (status === 'loading') {
    screen = (
      <View style={styles.centered}>
        <ActivityIndicator color={colors.green} size="large" />
      </View>
    );
  } else if (status === 'storageError') {
    screen = (
      <View style={styles.centered}>
        <Text style={styles.errorTitle}>Couldn't read saved data on this phone.</Text>
      </View>
    );
  } else if (status === 'offline') {
    screen = (
      <View style={styles.centered}>
        <Text style={styles.errorTitle}>Can't reach BuyIn right now</Text>
        <Text style={styles.errorText}>{offlineMessage}</Text>
        <Text style={styles.hint}>
          Check the server is running on the PC and the phone is on the same Wi-Fi.
        </Text>
        <Pressable
          accessibilityRole="button"
          onPress={loadSavedPlayer}
          style={({ pressed }) => [styles.retryButton, pressed && styles.pressed]}
        >
          <Text style={styles.retryText}>Try again</Text>
        </Pressable>
      </View>
    );
  } else if (player) {
    screen = <HomeScreen player={player} isNewPlayer={isNewPlayer} onForget={handleForget} />;
  } else {
    screen = <CreatePlayerScreen onCreated={handleCreated} />;
  }

  return (
    <SafeAreaProvider>
      <StatusBar style="dark" />
      {screen}
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    padding: spacing.lg,
    backgroundColor: colors.background,
  },
  errorTitle: { color: colors.red, fontSize: 18, fontWeight: '800', textAlign: 'center' },
  errorText: { color: colors.black, fontSize: 14, textAlign: 'center' },
  hint: { color: colors.muted, fontSize: 13, textAlign: 'center' },
  retryButton: {
    marginTop: spacing.md,
    backgroundColor: colors.green,
    borderRadius: radius.md,
    paddingVertical: 12,
    paddingHorizontal: spacing.xl,
  },
  pressed: { opacity: 0.7 },
  retryText: { color: colors.white, fontSize: 16, fontWeight: '800' },
});
