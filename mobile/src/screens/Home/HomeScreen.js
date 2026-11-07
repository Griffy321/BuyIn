import { useState } from 'react';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import Card from '../../components/Card';
import Chip from '../../components/Chip';
import GamesPlayedCard from '../../components/GamesPlayedCard';
import PnLChart from '../../components/PnLChart';
import SpinningChip from '../../components/SpinningChip';
import { chipOrder, colors, radius, spacing } from '../../theme';

// The player's home: greeting, lifetime P&L chart, games played.
//
// `player` is { playerId, firstName, lastName } from GET /players/{id} (or from the create screen).
// `isNewPlayer` is true straight after creating a player, so the greeting can say welcome
// instead of welcome back.
//
// TODO once the server can return a player's games: pass the real list in here. Until then
// every player has no games, so the chart shows its empty state and the count is 0.
export default function HomeScreen({ player, isNewPlayer, onForget }) {
  const [forgetting, setForgetting] = useState(false);
  const games = [];
  const runningTotals = toRunningTotals(games);

  const firstName = player.firstName || 'there';
  const initial = player.firstName ? player.firstName[0].toUpperCase() : '?';

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
      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <SpinningChip label={initial} />
          <View style={styles.headerText}>
            <Text style={styles.greeting} numberOfLines={1}>
              {isNewPlayer ? `Welcome, ${firstName}!` : `Hey ${firstName}!`}
            </Text>
            <Text style={styles.subtitle}>
              {isNewPlayer ? "You're all set. Pull up a chair" : 'Good to see you back at the table'}
            </Text>
          </View>
        </View>

        <Card>
          <PnLChart totals={runningTotals} />
        </Card>

        <GamesPlayedCard count={games.length} />

        <View style={styles.chipRow}>
          {chipOrder.map((color) => (
            <Chip key={color} color={color} size={44} />
          ))}
        </View>

        {/* Dev tool: lets you test the new-player flow without reinstalling. */}
        <Pressable
          accessibilityRole="button"
          onPress={confirmForget}
          disabled={forgetting}
          style={({ pressed }) => [styles.forgetButton, (pressed || forgetting) && styles.pressed]}
        >
          <Text style={styles.forgetText}>Forget me (dev)</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

// Your total after each game, oldest first, which is what the chart draws.
function toRunningTotals(games) {
  let total = 0;
  return games.map((game) => (total += game.profit));
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.background },
  content: {
    flexGrow: 1,
    paddingHorizontal: spacing.md,
    paddingBottom: spacing.md,
    gap: spacing.md,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    paddingVertical: spacing.md,
  },
  headerText: { flex: 1 },
  greeting: { color: colors.black, fontSize: 26, fontWeight: '800' },
  subtitle: { color: colors.muted, fontSize: 14, marginTop: 2 },
  chipRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: spacing.sm,
    marginTop: 'auto',
    paddingTop: spacing.md,
  },
  forgetButton: {
    alignSelf: 'center',
    borderColor: colors.red,
    borderWidth: 1,
    borderRadius: radius.md,
    paddingVertical: 6,
    paddingHorizontal: spacing.md,
  },
  pressed: { opacity: 0.6 },
  forgetText: { color: colors.red, fontSize: 13, fontWeight: '700' },
});
