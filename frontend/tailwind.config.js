/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        serif: ["Georgia", "Cambria", "serif"],
      },
      colors: {
        canvas: {
          light: "#faf8f4",
          dark: "#1a1816",
        },
        ink: {
          light: "#1f1c1a",
          dark: "#ece7e1",
        },
        accent: {
          DEFAULT: "#a8492e",
          light: "#c25a3c",
          dark: "#d17654",
        },
      },
    },
  },
  plugins: [],
}