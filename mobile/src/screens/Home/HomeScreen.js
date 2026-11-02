import { useState } from 'react';
import { Alert, Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import Chip from '../../components/Chip';
import { colors, radius, spacing } from '../../theme';

// Shown when this phone already has a player saved.
// For now it only knows the player's ID; once GET /players/{id} exists it can show their name.
export default function HomeScreen({ playerId, onForget }) {
  const [forgetting, setForgetting] = useState(false);

  function confirmForget() {
    Alert.alert(
      'Forget this player?',
      'The app will act like a fresh install and ask you to create a new player. The player stays in the database.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Forget me',
          style: 'destructive',
          onPress: async () => {
            setForgetting(true);
            try {
              await onForget();
            } catch {
              setForgetting(false);
              Alert.alert("Couldn't forget the player", 'Something went wrong clearing saved data.');
            }
          },
        },
      ],
    );
  }

  return (
    <SafeAreaView style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Chip color={colors.blue} size={40} />
          <View style={styles.headerText}>
            <Text style={styles.title}>Welcome back!</Text>
            <Text style={styles.subtitle}>This phone remembers you</Text>
          </View>
        </View>

        <View style={styles.card}>
          <Text style={styles.label}>Your player ID</Text>
          <Text style={styles.playerId} selectable>
            {playerId}
          </Text>
        </View>

        {/* Dev tool: lets you test the new-player flow without reinstalling. */}
        <Pressable
          accessibilityRole="button"
          onPress={confirmForget}
          disabled={forgetting}
          style={({ pressed }) => [styles.forgetButton, (pressed || forgetting) && styles.pressed]}
        >
          <Text style={styles.forgetText}>Forget me</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.md, gap: spacing.md },
  header: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  headerText: { flex: 1 },
  title: { color: colors.black, fontSize: 24, fontWeight: '800' },
  subtitle: { color: colors.muted, fontSize: 14, marginTop: 2 },
  card: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.lg,
    padding: spacing.md,
    gap: spacing.sm,
  },
  label: { color: colors.muted, fontSize: 14, fontWeight: '600' },
  playerId: {
    color: colors.black,
    fontSize: 16,
    fontWeight: '700',
    fontFamily: Platform.select({ android: 'monospace', ios: 'Menlo' }),
  },
  forgetButton: {
    alignSelf: 'center',
    borderColor: colors.red,
    borderWidth: 2,
    borderRadius: radius.md,
    paddingVertical: 10,
    paddingHorizontal: spacing.lg,
  },
  pressed: { opacity: 0.6 },
  forgetText: { color: colors.red, fontSize: 15, fontWeight: '800' },
});
