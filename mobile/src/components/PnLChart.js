import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Svg, { Circle, Line, Path, Text as SvgText } from 'react-native-svg';
import { formatPnL, formatPounds } from '../format';
import { colors, pnlColor, radius, spacing } from '../theme';

const PLOT_HEIGHT = 170;
const PLOT_TOP = 8;
const PLOT_LEFT = 44;
const PLOT_RIGHT = 10;
const AXIS_HEIGHT = 40;
const CHART_HEIGHT = PLOT_TOP + PLOT_HEIGHT + AXIS_HEIGHT;

// Picks a round gap between y-axis labels, such as £20 or £50.
function roundStep(range) {
  const rough = Math.max(range, 1) / 5;
  const scale = 10 ** Math.floor(Math.log10(rough));
  const multiple = [1, 2, 2.5, 5, 10].find((m) => m * scale >= rough);
  return multiple * scale;
}

function xTicks(count) {
  const step = count > 50 ? 20 : count > 20 ? 5 : count > 8 ? 2 : 1;
  const ticks = [1];
  for (let game = step; game <= count; game += step) {
    if (game > 1) ticks.push(game);
  }
  return ticks;
}

// Splits the line into stretches that are entirely above or entirely below £0. Where it
// crosses, both stretches end at the exact crossing point, so the colour changes on the £0 line.
function splitAtZero(totals, xFor, yFor) {
  const stretches = [];
  let current = null;

  totals.forEach((total, index) => {
    const sign = Math.sign(total);
    const point = [xFor(index), yFor(total)];

    if (current === null) {
      current = { sign, points: [point] };
      stretches.push(current);
      return;
    }

    if (current.sign === 0) {
      // Everything so far sits exactly on £0, so this stretch takes the first real direction.
      current.sign = sign;
    } else if (sign !== 0 && sign !== current.sign) {
      const previous = totals[index - 1];
      const crossing = index - 1 + previous / (previous - total);
      const crossingPoint = [xFor(crossing), yFor(0)];
      current.points.push(crossingPoint);
      current = { sign, points: [crossingPoint] };
      stretches.push(current);
    }
    current.points.push(point);
  });

  return stretches;
}

// A line of your running total after each game, green above £0 and red below. Touching the chart shows the total
// after any game in the top right corner, and letting go returns to your current total.
// With no games yet there's nothing to draw, so it shows £0.00 and a short note instead.
export default function PnLChart({ totals }) {
  if (totals.length === 0) {
    return (
      <View>
        <View style={styles.header}>
          <Text style={styles.label}>Lifetime P&L</Text>
          <Text style={[styles.value, { color: pnlColor(0) }]}>{formatPnL(0)}</Text>
        </View>
        <View style={styles.empty}>
          <Text style={styles.emptyText}>Your chart starts after your first game.</Text>
        </View>
      </View>
    );
  }

  return <FilledChart totals={totals} />;
}

function FilledChart({ totals }) {
  const [width, setWidth] = useState(0);
  const [selected, setSelected] = useState(null);

  const count = totals.length;
  const latest = totals[count - 1];
  const shownIndex = selected ?? count - 1;
  const shownValue = selected === null ? latest : totals[selected];

  // The axis always includes £0, so it's clear when you're up or down overall.
  const step = roundStep(Math.max(0, ...totals) - Math.min(0, ...totals));
  const yMin = Math.floor(Math.min(0, ...totals) / step) * step;
  const yMax = Math.max(Math.ceil(Math.max(0, ...totals) / step) * step, yMin + step);
  const yTicks = [];
  for (let value = yMin; value <= yMax; value += step) yTicks.push(value);

  const plotWidth = Math.max(width - PLOT_LEFT - PLOT_RIGHT, 1);
  const xFor = (index) => PLOT_LEFT + (index / Math.max(count - 1, 1)) * plotWidth;
  const yFor = (value) => PLOT_TOP + ((yMax - value) / (yMax - yMin)) * PLOT_HEIGHT;

  const stretches = splitAtZero(totals, xFor, yFor);

  function selectAt(x) {
    const index = Math.round(((x - PLOT_LEFT) / plotWidth) * (count - 1));
    setSelected(Math.min(Math.max(index, 0), count - 1));
  }

  return (
    <View>
      <View style={styles.header}>
        <Text style={styles.label}>
          {selected === null ? 'Lifetime P&L' : `After game ${selected + 1}`}
        </Text>
        <Text style={[styles.value, { color: pnlColor(shownValue) }]}>{formatPnL(shownValue)}</Text>
      </View>

      <View
        style={styles.chart}
        onLayout={(event) => setWidth(event.nativeEvent.layout.width)}
        accessibilityRole="image"
        accessibilityLabel={`Running profit and loss over ${count} games, currently ${formatPnL(latest)}`}
      >
        {width > 0 ? (
          <Svg width={width} height={CHART_HEIGHT}>
            {yTicks.map((value) => (
              <Line
                key={`grid-${value}`}
                x1={PLOT_LEFT}
                x2={width - PLOT_RIGHT}
                y1={yFor(value)}
                y2={yFor(value)}
                stroke={value === 0 ? colors.inactive : colors.border}
                strokeWidth={1}
              />
            ))}
            {yTicks.map((value) => (
              <SvgText
                key={`y-${value}`}
                x={PLOT_LEFT - 6}
                y={yFor(value) + 4}
                fontFamily="sans-serif"
                fontSize={11}
                fill={colors.muted}
                textAnchor="end"
              >
                {formatPounds(value)}
              </SvgText>
            ))}
            {xTicks(count).map((game) => (
              <SvgText
                key={`x-${game}`}
                x={xFor(game - 1)}
                y={PLOT_TOP + PLOT_HEIGHT + 16}
                fontFamily="sans-serif"
                fontSize={11}
                fill={colors.muted}
                textAnchor="middle"
              >
                {game}
              </SvgText>
            ))}
            <SvgText
              x={PLOT_LEFT + plotWidth / 2}
              y={PLOT_TOP + PLOT_HEIGHT + 34}
              fontFamily="sans-serif"
              fontSize={12}
              fontWeight="600"
              fill={colors.muted}
              textAnchor="middle"
            >
              Games
            </SvgText>

            {selected !== null ? (
              <Line
                x1={xFor(selected)}
                x2={xFor(selected)}
                y1={PLOT_TOP}
                y2={PLOT_TOP + PLOT_HEIGHT}
                stroke={colors.inactive}
                strokeWidth={1}
              />
            ) : null}

            {stretches.map((stretch, index) => (
              <Path
                key={`line-${index}`}
                d={stretch.points
                  .map(([x, y], pointIndex) => `${pointIndex === 0 ? 'M' : 'L'}${x} ${y}`)
                  .join(' ')}
                fill="none"
                stroke={pnlColor(stretch.sign)}
                strokeWidth={2}
                strokeLinejoin="round"
                strokeLinecap="round"
              />
            ))}
            <Circle
              cx={xFor(shownIndex)}
              cy={yFor(shownValue)}
              r={5}
              fill={pnlColor(shownValue)}
              stroke={colors.white}
              strokeWidth={2}
            />
          </Svg>
        ) : null}

        <View
          style={styles.touchLayer}
          onStartShouldSetResponder={() => true}
          onMoveShouldSetResponder={() => true}
          onResponderTerminationRequest={() => false}
          onResponderGrant={(event) => selectAt(event.nativeEvent.locationX)}
          onResponderMove={(event) => selectAt(event.nativeEvent.locationX)}
          onResponderRelease={() => setSelected(null)}
          onResponderTerminate={() => setSelected(null)}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  label: { color: colors.muted, fontSize: 15, fontWeight: '600', paddingTop: spacing.xs },
  value: { fontSize: 30, fontWeight: '800' },
  chart: { height: CHART_HEIGHT },
  empty: {
    height: 120,
    alignItems: 'center',
    justifyContent: 'center',
    borderColor: colors.border,
    borderWidth: 1,
    borderStyle: 'dashed',
    borderRadius: radius.md,
  },
  emptyText: { color: colors.muted, fontSize: 14, fontWeight: '600' },
  touchLayer: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
  },
});
