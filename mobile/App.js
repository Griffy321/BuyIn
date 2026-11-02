import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import CreatePlayerScreen from './src/screens/CreatePlayer/CreatePlayerScreen';
import HomeScreen from './src/screens/Home/HomeScreen';
import { forgetPlayerId, getPlayerId } from './src/storage/playerStorage';
import { colors, spacing } from './src/theme';

// On launch, checks whether this phone already has a player saved:
//   saved     → Home
//   not saved → Create player
//
// TODO once GET /players/{id} exists: look the saved ID up on the server here,
// and forget it if the server replies 404 (e.g. after the database was reset).
export default function App() {
  const [status, setStatus] = useState('loading'); // 'loading' | 'ready' | 'error'
  const [playerId, setPlayerId] = useState(null);

  useEffect(() => {
    getPlayerId()
      .then((savedId) => {
        setPlayerId(savedId);
        setStatus('ready');
      })
      .catch(() => setStatus('error'));
  }, []);

  async function handleForget() {
    await forgetPlayerId();
    setPlayerId(null);
  }

  let screen;
  if (status === 'loading') {
    screen = (
      <View style={styles.centered}>
        <ActivityIndicator color={colors.green} size="large" />
      </View>
    );
  } else if (status === 'error') {
    screen = (
      <View style={styles.centered}>
        <Text style={styles.errorText}>Couldn't read saved data on this phone.</Text>
      </View>
    );
  } else if (playerId) {
    screen = <HomeScreen playerId={playerId} onForget={handleForget} />;
  } else {
    screen = <CreatePlayerScreen onCreated={setPlayerId} />;
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
    padding: spacing.lg,
    backgroundColor: colors.background,
  },
  errorText: { color: colors.red, fontSize: 16, fontWeight: '700', textAlign: 'center' },
});
