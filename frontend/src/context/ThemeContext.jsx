import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const ThemeContext = createContext(null);

export const CINEMA_THEMES = [
  { id: 'director-noir', name: 'Director Noir', accent: '#e50914', desc: 'Deep Obsidian & Crimson Gold' },
  { id: 'camera-tungsten', name: 'Camera Tungsten', accent: '#f59e0b', desc: 'Warm 3200K Tungsten & Amber' },
  { id: 'stunt-hazard', name: 'Stunt Hazard', accent: '#f97316', desc: 'High-Voltage Carbon & Hazard Orange' },
  { id: 'vfx-cyber', name: 'VFX Cyberpunk', accent: '#8b5cf6', desc: 'Electric Violet & Holographic Cyan' },
  { id: 'sound-emerald', name: 'Sound Emerald', accent: '#10b981', desc: 'Deep Forest & Sonic Waveform Emerald' },
  { id: 'legal-navy', name: 'Studio Legal Navy', accent: '#3b82f6', desc: 'Imperial Navy & Platinum Slate' }
];

export const CINEMA_PALETTES = {
  'director-noir': { name: 'Director Noir', accent: '#e50914', description: 'Deep Obsidian & Crimson Gold' },
  'camera-tungsten': { name: 'Camera Tungsten', accent: '#f59e0b', description: 'Warm 3200K Tungsten & Amber' },
  'stunt-hazard': { name: 'Stunt Hazard', accent: '#f97316', description: 'High-Voltage Carbon & Hazard Orange' },
  'vfx-cyber': { name: 'VFX Cyberpunk', accent: '#8b5cf6', description: 'Electric Violet & Holographic Cyan' },
  'sound-emerald': { name: 'Sound Emerald', accent: '#10b981', description: 'Deep Forest & Sonic Waveform Emerald' },
  'legal-navy': { name: 'Studio Legal Navy', accent: '#3b82f6', description: 'Imperial Navy & Platinum Slate' }
};

export function ThemeProvider({ children }) {
  const [mode, setMode] = useState('dark');
  const [cinemaTheme, setCinemaTheme] = useState('director-noir');

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute('data-theme', mode);
    root.setAttribute('data-cinema-theme', cinemaTheme);
  }, [mode, cinemaTheme]);

  const toggleMode = useCallback(() => {
    setMode((prev) => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const changeCinemaTheme = useCallback((themeId) => {
    setCinemaTheme(themeId);
  }, []);

  return (
    <ThemeContext.Provider
      value={{
        mode,
        cinemaTheme,
        toggleMode,
        setCinemaTheme: changeCinemaTheme,
        changeCinemaTheme,
        themes: CINEMA_THEMES,
        CINEMA_PALETTES
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}


export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
