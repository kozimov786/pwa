/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        base: {
          950: "#05060a",
          900: "#0b0e17",
          800: "#121627",
          700: "#1b2036",
        },
        neon: {
          cyan: "#22d3ee",
          violet: "#a78bfa",
          pink: "#f472b6",
        },
      },
      boxShadow: {
        glow: "0 0 24px rgba(34, 211, 238, 0.35)",
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};
