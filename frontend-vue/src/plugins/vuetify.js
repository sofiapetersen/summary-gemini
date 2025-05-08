// src/plugins/vuetify.js

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          background: '#f5f5f5',
          surface: '#ffffff',
          primary: '#1976d2',
          secondary: '#03dac6',
          error: '#ff5252',
        },
      },
      dark: {
        dark: true,
        colors: {
          background: '#121212',
          surface: '#1e1e1e',
          primary: '#90caf9',
          secondary: '#03dac6',
          error: '#ef9a9a',
          'field-text': '#90caf9',
        },
      },
    },
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
})
