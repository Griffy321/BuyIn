import { StyleSheet, Text } from 'react-native';
import { colors, spacing } from '../theme';
import Card from './Card';

// How many games you've played.
export default function GamesPlayedCard({ count }) {
  return (
    <Card style={styles.card}>
      <Text style={styles.label}>Games played</Text>
      <Text style={styles.count}>{count}</Text>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: { paddingHorizontal: spacing.lg },
  label: { color: colors.muted, fontSize: 15, fontWeight: '600' },
  count: { color: colors.black, fontSize: 34, fontWeight: '800', marginTop: spacing.xs },
});
