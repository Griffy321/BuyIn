import { StyleSheet, View } from 'react-native';
import { colors, radius, spacing } from '../theme';

// The white rounded box that every section of the app sits in.
// Pass `style` to add to it, e.g. a red border for an error.
export default function Card({ style, children }) {
  return <View style={[styles.card, style]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.lg,
    padding: spacing.md,
  },
});
