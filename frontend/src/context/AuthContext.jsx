import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

const AuthContext = createContext(null);

export const DEFAULT_USER = {
  uid: 'usr-siva-01',
  displayName: 'Sivasubramanian (Director B01)',
  email: 'siva@thiraikuzhu.ai',
  role: 'admin',
  crewPersonaId: 'B01',
  crewPersonaTitle: 'Principal Director',
  department: 'Directing',
  avatarInitials: 'B01'
};

export const CREW_QUICK_LOGINS = [
  { id: 'B01', title: 'Director', dept: 'Directing', theme: 'director-noir', icon: '🎬', band: 'B' },
  { id: 'C04', title: 'Line Producer', dept: 'Producing', theme: 'legal-navy', icon: '💼', band: 'C' },
  { id: 'H01', title: 'Fight Master', dept: 'Action', theme: 'stunt-hazard', icon: '⚔️', band: 'H' },
  { id: 'E01', title: 'Cinematographer', dept: 'Camera', theme: 'camera-tungsten', icon: '🎥', band: 'E' },
  { id: 'E11', title: 'DIT (Data Integrity)', dept: 'Camera', theme: 'camera-tungsten', icon: '💾', band: 'E' },
  { id: 'K01', title: 'VFX Supervisor', dept: 'VFX', theme: 'vfx-cyber', icon: '✨', band: 'K' },
  { id: 'G01', title: 'Music Director', dept: 'Sound', theme: 'sound-emerald', icon: '🎵', band: 'G' },
  { id: 'L08', title: 'OTT Content Lead', dept: 'Distribution', theme: 'legal-navy', icon: '📡', band: 'L' },
  { id: 'P01', title: 'Studio Reliability Eng', dept: 'Platform', theme: 'director-noir', icon: '🛡️', band: 'P' }
];

export function AuthProvider({ children }) {
  const [user, setUser] = useState(DEFAULT_USER);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  const loginWithPersona = useCallback((personaId, personaTitle, department, _theme) => {
    setUser({
      uid: `usr-persona-${personaId.toLowerCase()}`,
      displayName: `${personaTitle} (${personaId})`,
      email: `${personaId.toLowerCase()}@crew.thiraikuzhu.ai`,
      role: 'CREW',
      crewPersonaId: personaId,
      crewPersonaTitle: personaTitle,
      department: department || 'Directing',
      avatarInitials: personaId.slice(0, 3)
    });
    setIsAuthModalOpen(false);
  }, []);

  const loginAsCrewPersona = useCallback((personaObj) => {
    if (!personaObj) return;
    loginWithPersona(
      personaObj.id,
      personaObj.title || personaObj.name || personaObj.id,
      personaObj.band || personaObj.dept || 'Crew'
    );
  }, [loginWithPersona]);

  const switchRole = useCallback((newRole) => {
    setUser((prev) => ({
      ...prev,
      role: newRole,
      displayName: newRole.toLowerCase() === 'admin' ? 'Studio Head (Admin)' : (prev?.crewPersonaTitle || 'Crew')
    }));
    setIsAuthModalOpen(false);
  }, []);

  const logout = useCallback(() => {
    setUser({
      uid: 'usr-guest',
      displayName: 'Studio Guest (Observer)',
      email: 'guest@thiraikuzhu.ai',
      role: 'GUEST',
      crewPersonaId: null,
      crewPersonaTitle: 'Guest Observer',
      department: 'Guest',
      avatarInitials: 'GU'
    });
  }, []);

  const openAuthModal = useCallback(() => setIsAuthModalOpen(true), []);
  const closeAuthModal = useCallback(() => setIsAuthModalOpen(false), []);

  const currentPersona = useMemo(() => {
    if (!user || !user.crewPersonaId) return null;
    return {
      id: user.crewPersonaId,
      title: user.crewPersonaTitle || user.displayName,
      band: user.crewPersonaId.startsWith('COMP') ? 'COMP' :
            user.crewPersonaId.startsWith('ANTG') ? 'ANTG' :
            user.crewPersonaId[0]
    };
  }, [user]);

  const contextValue = useMemo(() => ({
    user,
    currentUser: user,
    setUser,
    userRole: user?.role || 'GUEST',
    currentPersona,
    isAuthModalOpen,
    setIsAuthModalOpen,
    openAuthModal,
    closeAuthModal,
    loginWithPersona,
    loginAsCrewPersona,
    switchRole,
    logout
  }), [user, currentPersona, isAuthModalOpen, openAuthModal, closeAuthModal, loginWithPersona, loginAsCrewPersona, switchRole, logout]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
