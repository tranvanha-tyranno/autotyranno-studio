export const font = '"Bread Be Vietnam Pro", sans-serif';
export const palette = {
  ink: '#10100e',
  white: '#fffaf0',
  quiet: '#d5cebf',
  warm: '#e2b36c',
  rust: '#e48b6d',
  green: '#a7ceb1',
  rule: 'rgba(255,250,240,.25)',
};
export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const number = (n: number, decimals = 0) => n.toLocaleString('vi-VN', {maximumFractionDigits: decimals});
export const money = (n: number) => `${number(n)} đ`;
