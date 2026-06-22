import { Platform } from "react-native";

export interface GhostEyeMobileSession {
  deviceId: string;
  sessionId: string;
  teamId?: string | null;
  startedAt: string;
}

const DEVICE_ID = `ghosteye-${Platform.OS}-${randomToken()}`;

let currentSession: GhostEyeMobileSession | null = null;

export function getOrCreateSession(teamId?: string | null): GhostEyeMobileSession {
  if (!currentSession) {
    currentSession = createSession(teamId);
  } else if (typeof teamId !== "undefined") {
    currentSession = { ...currentSession, teamId };
  }
  return currentSession;
}

export function rotateSession(teamId?: string | null): GhostEyeMobileSession {
  currentSession = createSession(teamId);
  return currentSession;
}

function createSession(teamId?: string | null): GhostEyeMobileSession {
  const timestamp = new Date().toISOString();
  return {
    deviceId: DEVICE_ID,
    sessionId: `mobile-${Date.now().toString(36)}-${randomToken()}`,
    teamId,
    startedAt: timestamp,
  };
}

function randomToken(): string {
  return Math.random().toString(36).slice(2, 10);
}
