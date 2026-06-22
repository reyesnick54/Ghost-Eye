export type CalibrationPhase =
  | "idle"
  | "empty_room_start"
  | "empty_room_sample"
  | "empty_room_complete"
  | "zone_start"
  | "zone_sample"
  | "zone_complete";

export interface CalibrationObservationState {
  phase: CalibrationPhase;
  zone_id?: string | null;
  sample_index?: number;
  sample_count?: number;
  started_at?: string;
  completed_at?: string;
  notes?: string;
}

export interface CalibrationWorkflowStep {
  phase: CalibrationPhase;
  label: string;
  description: string;
}

export const CALIBRATION_WORKFLOW: CalibrationWorkflowStep[] = [
  {
    phase: "empty_room_start",
    label: "Start empty-room baseline",
    description: "Confirm the controlled room is empty before recording baseline samples.",
  },
  {
    phase: "empty_room_sample",
    label: "Capture empty-room samples",
    description: "Collect permitted WiFi, network, and motion observations for the baseline.",
  },
  {
    phase: "empty_room_complete",
    label: "Complete empty-room baseline",
    description: "Mark baseline capture complete and send final calibration state.",
  },
  {
    phase: "zone_start",
    label: "Start zone fingerprint",
    description: "Select a zone and confirm authorized test conditions.",
  },
  {
    phase: "zone_sample",
    label: "Capture zone samples",
    description: "Record zone observations while keeping outputs probabilistic.",
  },
  {
    phase: "zone_complete",
    label: "Complete zone fingerprint",
    description: "Close the zone calibration step for backend analysis.",
  },
];
