export interface AIAnalysis {
  available?: boolean;
  provider?: string;
  model?: string | null;
  summary?: string;
  confidence?: number;
  confidence_explanation?: string;
  false_positive_risks?: string[];
  recommended_next_action?: string;
  observations?: string[];
  recommendations?: string[];
  limitations?: string[];
  metadata?: Record<string, unknown>;
}

export interface AIAnalysisEnvelope {
  status?: Record<string, unknown>;
  ai_analysis?: AIAnalysis;
}
