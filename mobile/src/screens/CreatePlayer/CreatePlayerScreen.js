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
import { ApiError } from '../../api/client';
import { createPlayer } from '../../api/players';
import Card from '../../components/Card';
import Chip from '../../components/Chip';
import { savePlayerId } from '../../storage/playerStorage';
import { colors, radius, spacing } from '../../theme';

// Sends POST /players to the Python server, saves the playerId it sends back on this phone,
// then hands App the new player (via onCreated) so it can move on to the Home screen.
// The names come from what was typed, so there's no need to ask the server for them again.
export default function CreatePlayerScreen({ onCreated }) {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleCreate() {
    if (loading) return; // stops a double-tap from creating two players
    setLoading(true);
    setError(null);
    const trimmedFirstName = firstName.trim();
    const trimmedLastName = lastName.trim();
    try {
      const { playerId } = await createPlayer(trimmedFirstName, trimmedLastName);
      await savePlayerId(playerId);
      onCreated({ playerId, firstName: trimmedFirstName, lastName: trimmedLastName });
    } catch (createError) {
      // An ApiError means the server answered but said no; anything else means it never answered.
      setError({ message: createError.message, serverAnswered: createError instanceof ApiError });
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
              <Text style={styles.subtitle}>Tell us who's at the table</Text>
            </View>
          </View>

          <Card style={styles.form}>
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
          </Card>

          {error && (
            <Card style={styles.errorCard}>
              <Text style={styles.errorTitle}>Something went wrong</Text>
              <Text style={styles.errorText}>{error.message}</Text>
              {!error.serverAnswered && (
                <Text style={styles.hint}>
                  Check the server is running on the PC, listening on 0.0.0.0, and that the
                  phone is on the same Wi-Fi.
                </Text>
              )}
            </Card>
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
  subtitle: { color: colors.muted, fontSize: 14, marginTop: 2 },
  form: { gap: spacing.sm },
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
  errorCard: { borderColor: colors.red, borderWidth: 2, gap: spacing.sm },
  errorTitle: { color: colors.red, fontSize: 16, fontWeight: '800' },
  errorText: { color: colors.black, fontSize: 14 },
  hint: { color: colors.muted, fontSize: 13 },
});
