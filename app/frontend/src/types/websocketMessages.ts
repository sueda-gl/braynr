export interface WebSocketMessageBase {
    job_id: number;
    type: string;
    data?: Record<string, any>;
}

export interface WebSocketStatusUpdateMessage extends WebSocketMessageBase {
    type: "status_update";
    status: string; // e.g., "PENDING", "PROCESSING_EXPLANATION", "COMPLETED", "FAILED"
    message?: string;
}

export type PartialResultType = 
    | "explanation"
    | "concepts"
    | "storyboard"
    | "enhanced_storyboard"
    | "generated_code"
    | "review_comments";

export interface WebSocketPartialResultMessage extends WebSocketMessageBase {
    type: "partial_result";
    result_type: PartialResultType;
    content: string;
}

export interface WebSocketFinalResultMessage extends WebSocketMessageBase {
    type: "final_result";
    refactored_code?: string | null;
    video_url?: string | null;
    manim_error?: string | null;
    message?: string;
}

export interface WebSocketErrorMessage extends WebSocketMessageBase {
    type: "error";
    error_message: string;
}

export type AgentWebSocketMessage = 
    | WebSocketStatusUpdateMessage 
    | WebSocketPartialResultMessage 
    | WebSocketFinalResultMessage 
    | WebSocketErrorMessage; 