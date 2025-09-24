module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
    "postcss-simple-vars": {},
    "postcss-nested": {}
  },
   content: ["./main/**/*.{html,js,jsx,ts,tsx}",   // todos los archivos dentro de main
    "./main/global/**/*.{html,js}",       // modales, alerts, globals.js
    "./main/src/**/*.{html,js,jsx,ts,tsx,php}", // vistas principales, estilos, php templates
    "./main/log/src/**/*.{html,js,css}",  // recursos dentro de log/src
    "./templates/**/*.{html,js}",         // si tienes plantillas Django/HTML
    "./**/*.html"         ],
  safelist: [
    { pattern: /(hover:)?bg-(red|green)-(100|200|300|400|500|600|700|800|900)\/(5|10|20|30|40|50|60|70|80|90)/ },
    { pattern: /border-(red|green)-(100|200|300|400|500|600|700|800|900)\/(5|10|20|30|40|50|60|70|80|90)/ },
    { pattern: /text-(red|green)-(100|200|300|400|500|600|700|800|900)\/(5|10|20|30|40|50|60|70|80|90)/ },
  ],
}
