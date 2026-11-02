import { StyleSheet, View } from 'react-native';
import Svg, { Circle, Rect } from 'react-native-svg';
import { colors } from '../theme';

const MARK_COUNT = 6;

// A poker chip drawn from code, so it stays sharp at any size.
// Anything passed as children is centred on the chip.
export default function Chip({ color = colors.red, size = 48, children }) {
  // White marks wouldn't show on a white chip, so it gets grey marks and an outline.
  const isWhite = color === colors.white;
  const markColor = isWhite ? colors.border : colors.white;
  const ringColor = isWhite ? colors.border : colors.white;

  return (
    <View style={{ width: size, height: size }}>
      <Svg width={size} height={size} viewBox="0 0 100 100">
        <Circle
          cx="50"
          cy="50"
          r={isWhite ? 48.5 : 50}
          fill={color}
          stroke={isWhite ? colors.border : 'none'}
          strokeWidth={isWhite ? 3 : 0}
        />
        {Array.from({ length: MARK_COUNT }, (_, i) => (
          <Rect
            key={i}
            x="42"
            y="1"
            width="16"
            height="15"
            fill={markColor}
            transform={`rotate(${(360 / MARK_COUNT) * i} 50 50)`}
          />
        ))}
        <Circle cx="50" cy="50" r="31" fill={color} stroke={ringColor} strokeWidth="3" />
      </Svg>
      {children ? <View style={styles.center}>{children}</View> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  center: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
