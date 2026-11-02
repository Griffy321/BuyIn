// The five chip colours, plus the light neutrals that sit behind them.
export const colors = {
  white: '#FFFFFF',
  red: '#D93636',
  green: '#15924F',
  blue: '#2468DB',
  black: '#17191C',

  background: '#F4F6F9',
  border: '#DDE2E9',
  muted: '#5F6773',
  inactive: '#A9B0BA',

  // Only used on the pretend camera, which is dark like a real viewfinder.
  camera: '#17191C',
};

// The order chips appear in the home screen's row, and the order the spinning chip cycles through.
export const chipOrder = [colors.white, colors.red, colors.green, colors.blue, colors.black];

// Every colour a host can choose for their chips.
export const chipPalette = [
  { name: 'White', hex: colors.white },
  { name: 'Red', hex: colors.red },
  { name: 'Green', hex: colors.green },
  { name: 'Blue', hex: colors.blue },
  { name: 'Black', hex: colors.black },
  { name: 'Yellow', hex: '#E3A712' },
  { name: 'Orange', hex: '#EE7A1B' },
  { name: 'Pink', hex: '#E85A9B' },
  { name: 'Purple', hex: '#7B3FC4' },
];

export function chipName(hex) {
  return chipPalette.find((option) => option.hex === hex)?.name ?? 'Chip';
}

// Green for up and red for down, used anywhere a profit or loss is shown.
export function pnlColor(amount) {
  return amount > 0 ? colors.green : amount < 0 ? colors.red : colors.black;
}

export const spacing ={ xs: 4, sm: 8, md: 16, lg: 24, xl: 32 };
export const radius = { md: 14, lg: 22 };
