module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
    "postcss-simple-vars": {},
    "postcss-nested": {}
  },
   content: ["./**/*.html", "./**/*.js"],
  safelist: [
    { pattern: /(hover:)?bg-(red|green)-(100|200|300|400|500|600|700|800|900)\/(5|10|20|30|40|50|60|70|80|90)/ },
    { pattern: /border-(red|green)-(100|200|300|400|500|600|700|800|900)\/(5|10|20|30|40|50|60|70|80|90)/ },
    { pattern: /text-(red|green)-(100|200|300|400|500|600|700|800|900)\/(5|10|20|30|40|50|60|70|80|90)/ },
  ],
}
