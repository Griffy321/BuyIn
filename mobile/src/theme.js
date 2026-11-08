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
};

// The order chips appear in the home screen's row, and the order the spinning chip cycles through.
export const chipOrder = [colors.white, colors.red, colors.green, colors.blue, colors.black];

// Green for up and red for down, used anywhere a profit or loss is shown.
export function pnlColor(amount) {
  return amount > 0 ? colors.green : amount < 0 ? colors.red : colors.black;
}

export const spacing = { xs: 4, sm: 8, md: 16, lg: 24, xl: 32 };
export const radius = { md: 14, lg: 22 };
