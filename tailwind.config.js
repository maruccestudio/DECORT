/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './src/**/*.css'],
  theme: {
    extend: {
      colors: {
        terracotta: {
          50:  '#fdf6f1',
          100: '#f9e8da',
          200: '#f2ccb0',
          300: '#e5a97d',
          400: '#d48a55',
          500: '#A0633B',
          600: '#8b5332',
          700: '#73422a',
          800: '#5e3624',
          900: '#4d2d1f',
        },
        arena: {
          50:  '#FEFCF9',
          100: '#FAF7F2',
          200: '#F5F0E8',
          300: '#EBE3D6',
          400: '#E0D5C0',
          500: '#D4C5A9',
          600: '#B8A88B',
          700: '#9A8B6E',
          800: '#7D7057',
          900: '#5F5541',
        },
        oliva: {
          50:  '#f7f7ef',
          100: '#eeeedd',
          200: '#ddddb8',
          300: '#c4c48a',
          400: '#a8a85e',
          500: '#8B8B3D',
          600: '#6f6f31',
          700: '#555528',
          800: '#454521',
          900: '#3a3a1d',
        },
      },
      fontFamily: {
        'display': ['"Cormorant Garamond"', 'Georgia', 'serif'],
        'body':    ['"Inter"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
