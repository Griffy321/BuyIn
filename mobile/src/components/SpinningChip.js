import { useRef, useState } from 'react';
import { Animated, Easing, Platform, Pressable, StyleSheet, Text } from 'react-native';
import { chipOrder, colors } from '../theme';
import Chip from './Chip';

const useNativeDriver = Platform.OS !== 'web';
const MAX_QUEUED_SPINS = 2;

// Tap to spin the chip like a flipped coin. The colour changes when the chip is edge-on,
// which is the moment nobody can see the swap.
export default function SpinningChip({ label, size = 60, startColor = colors.blue }) {
  const [index, setIndex] = useState(chipOrder.indexOf(startColor));
  const angle = useRef(new Animated.Value(0)).current;
  const isSpinning = useRef(false);
  const queuedSpins = useRef(0);

  const rotateY = angle.interpolate({
    inputRange: [0, 450],
    outputRange: ['0deg', '450deg'],
  });

  function spin() {
    isSpinning.current = true;

    // One and a quarter turns, which leaves the chip edge-on.
    Animated.timing(angle, {
      toValue: 450,
      duration: 380,
      easing: Easing.in(Easing.quad),
      useNativeDriver,
    }).start(({ finished }) => {
      if (!finished) return;
      setIndex((current) => (current + 1) % chipOrder.length);

      // 270 degrees is edge-on too, so this last quarter turn shows the new colour face-on
      // and the letter is never left mirrored.
      angle.setValue(270);
      Animated.timing(angle, {
        toValue: 360,
        duration: 220,
        easing: Easing.out(Easing.cubic),
        useNativeDriver,
      }).start(({ finished: settled }) => {
        if (!settled) return;
        angle.setValue(0);
        if (queuedSpins.current > 0) {
          queuedSpins.current -= 1;
          spin();
        } else {
          isSpinning.current = false;
        }
      });
    });
  }

  function handlePress() {
    if (isSpinning.current) {
      queuedSpins.current = Math.min(queuedSpins.current + 1, MAX_QUEUED_SPINS);
    } else {
      spin();
    }
  }

  const color = chipOrder[index];
  const letterColor = color === colors.white ? colors.black : colors.white;

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel="Spin your chip to change its colour"
      hitSlop={8}
      onPress={handlePress}
    >
      <Animated.View style={{ transform: [{ perspective: 400 }, { rotateY }] }}>
        <Chip color={color} size={size}>
          <Text style={[styles.letter, { color: letterColor }]}>{label}</Text>
        </Chip>
      </Animated.View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  letter: { fontSize: 20, fontWeight: '800' },
});
