/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './theme/templates/**/*.html',
    './theme/static_src/**/*.{js,css}',
    './**/*.py', // Add any other paths where you use Tailwind classes
  ],
  theme: {
    extend: {
      animation: {
        'fade-in-up': 'fadeInUp 0.5s ease-out forwards',
        'fade-in-right': 'fadeInRight 0.5s ease-out forwards',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: 0, transform: 'translateY(20px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        fadeInRight: {
          '0%': { opacity: 0, transform: 'translateX(20px)' },
          '100%': { opacity: 1, transform: 'translateX(0)' },
        },
      },
      transitionDelay: {
        '0': '0ms',
        '100': '100ms',
        '200': '200ms',
        '300': '300ms',
        '400': '400ms',
        '500': '500ms',
      }
    },
  },
  plugins: [],
} 