import { useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { createPlayer } from '../../api/players';
import Chip from '../../components/Chip';
import { API_URL } from '../../config';
import { savePlayerId } from '../../storage/playerStorage';
import { colors, radius, spacing } from '../../theme';

// Sends POST /players to the Python server, saves the playerId it sends back on this phone,
// then tells App (via onCreated) so it can move on to the Home screen.
export default function CreatePlayerScreen({ onCreated }) {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleCreate() {
    if (loading) return; // stops a double-tap from creating two players
    setLoading(true);
    setError(null);
    try {
      const { playerId } = await createPlayer(firstName.trim(), lastName.trim());
      await savePlayerId(playerId);
      onCreated(playerId);
    } catch (e) {
      setError(e.message);
      setLoading(false);
    }
    // No setLoading(false) on success: this screen is replaced by Home straight away.
  }

  return (
    <SafeAreaView style={styles.screen}>
      <KeyboardAvoidingView
        style={styles.screen}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
          <View style={styles.header}>
            <Chip color={colors.green} size={40} />
            <View style={styles.headerText}>
              <Text style={styles.title}>Create player</Text>
              <Text style={styles.subtitle} numberOfLines={1}>
                POST {API_URL}/players
              </Text>
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.label}>First name</Text>
            <TextInput
              style={styles.input}
              value={firstName}
              onChangeText={setFirstName}
              placeholder="James"
              placeholderTextColor={colors.inactive}
              autoCapitalize="words"
              returnKeyType="next"
            />
            <Text style={styles.label}>Last name</Text>
            <TextInput
              style={styles.input}
              value={lastName}
              onChangeText={setLastName}
              placeholder="G"
              placeholderTextColor={colors.inactive}
              autoCapitalize="words"
              returnKeyType="done"
              onSubmitEditing={handleCreate}
            />

            <Pressable
              accessibilityRole="button"
              onPress={handleCreate}
              disabled={loading}
              style={({ pressed }) => [styles.button, (pressed || loading) && styles.pressed]}
            >
              {loading ? (
                <ActivityIndicator color={colors.white} />
              ) : (
                <Text style={styles.buttonText}>Create player</Text>
              )}
            </Pressable>
          </View>

          {error && (
            <View style={[styles.card, styles.errorCard]}>
              <Text style={styles.errorTitle}>Something went wrong</Text>
              <Text style={styles.errorText}>{error}</Text>
              <Text style={styles.hint}>
                Check the server is running on the PC, listening on 0.0.0.0, and that the
                phone is on the same Wi-Fi.
              </Text>
            </View>
          )}
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.md, gap: spacing.md },
  header: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  headerText: { flex: 1 },
  title: { color: colors.black, fontSize: 24, fontWeight: '800' },
  subtitle: { color: colors.muted, fontSize: 12, marginTop: 2 },
  card: {
    backgroundColor: colors.white,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.lg,
    padding: spacing.md,
    gap: spacing.sm,
  },
  label: { color: colors.muted, fontSize: 14, fontWeight: '600' },
  input: {
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.md,
    paddingHorizontal: spacing.md,
    paddingVertical: 10,
    fontSize: 16,
    color: colors.black,
    marginBottom: spacing.xs,
  },
  button: {
    backgroundColor: colors.green,
    borderRadius: radius.md,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: spacing.xs,
  },
  pressed: { opacity: 0.7 },
  buttonText: { color: colors.white, fontSize: 16, fontWeight: '800' },
  errorCard: { borderColor: colors.red, borderWidth: 2 },
  errorTitle: { color: colors.red, fontSize: 16, fontWeight: '800' },
  errorText: { color: colors.black, fontSize: 14 },
  hint: { color: colors.muted, fontSize: 13 },
});
