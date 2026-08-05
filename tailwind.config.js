const plugin = require('tailwindcss/plugin')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './src/**/*.css', './public/js/**/*.js'],
  theme: {
    extend: {
      colors: {
        terracotta: {
          50:  '#f8f2f0',
          100: '#edded9',
          200: '#d9b8ad',
          300: '#c08b78',
          400: '#ad674f',
          500: '#A05034',
          600: '#8b462d',
          700: '#733a25',
          800: '#5e2f1f',
          900: '#4d2619',
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
          50:  '#f5f6f2',
          100: '#e5e6dd',
          200: '#c7cab7',
          300: '#a3a789',
          400: '#868d65',
          500: '#747B4D',
          600: '#656b43',
          700: '#535837',
          800: '#44482d',
          900: '#383b25',
        },
      },
      fontFamily: {
        'display': ['"Cormorant Garamond"', 'Georgia', 'serif'],
        'body':    ['"Inter"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [
    plugin(function ({ addVariant }) {
      addVariant('hover', '@media (hover: hover) and (pointer: fine) { &:hover }')
      addVariant('group-hover', '@media (hover: hover) and (pointer: fine) { :merge(.group):hover & }')
    }),
  ],
}
