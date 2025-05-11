import { useState, useRef, useCallback, useEffect } from 'react';
import type { 
    AgentWebSocketMessage, 
    WebSocketStatusUpdateMessage, 
    WebSocketPartialResultMessage, 
    WebSocketFinalResultMessage, 
    WebSocketErrorMessage,
    PartialResultType
} from '../types/websocketMessages'; // Adjust path if necessary

// Configuration - consider moving to .env or a config file
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';

// Define the API and WebSocket paths including the version prefix from backend settings
// Assuming backend uses /api/v1 as VERSIONED_API_PREFIX
const VERSIONED_API_PATH = '/api/v1'; // This should match settings.VERSIONED_API_PREFIX

export type AgentStatus = 'idle' | 'initiating' | 'connecting' | 'processing' | 'completed' | 'failed';

// Export ChatMessage interface
export interface ChatMessage {
  id: string; // For React keys
  sender: 'user' | 'agent';
  text: string;
  type?: 'status' | 'partial' | 'final' | 'error'; // Optional: for styling or specific handling
}

export interface AgentProcessorState {
    capturedImageDataUrl: string | null;
    jobId: string | null;
    agentStatus: AgentStatus;
    statusMessage: string;
    partialResults: Record<PartialResultType, string>;
    finalManimCode: string | null;
    videoUrl: string | null;
    manimError: string | null;
    errorMessage: string | null;
}

const initialPartialResults: Record<PartialResultType, string> = {
    explanation: '',
    concepts: '',
    storyboard: '',
    enhanced_storyboard: '',
    generated_code: '',
    review_comments: '',
};

export function useAgentProcessor() {
    const [capturedImageDataUrl, setCapturedImageDataUrl] = useState<string | null>(null);
    const [jobId, setJobId] = useState<string | null>(null);
    const [agentStatus, setAgentStatus] = useState<AgentStatus>('idle');
    const [statusMessage, setStatusMessage] = useState<string>('Ready to process.');
    const [partialResults, setPartialResults] = useState<Record<PartialResultType, string>>(initialPartialResults);
    const [finalManimCode, setFinalManimCode] = useState<string | null>(null);
    const [videoUrl, setVideoUrl] = useState<string | null>(null);
    const [manimError, setManimError] = useState<string | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);

    const webSocketRef = useRef<WebSocket | null>(null);

    // Effect to log state changes, useful for debugging UI reactivity
    useEffect(() => {
        console.log('[useAgentProcessor STATE UPDATE] AgentStatus:', agentStatus, 'JobId:', jobId, 'VideoUrl:', videoUrl, 'ManimError:', manimError);
    }, [agentStatus, jobId, videoUrl, manimError]);

    const resetStateForNewJob = useCallback(() => {
        setJobId(null);
        setAgentStatus('idle');
        setStatusMessage('Ready to process.');
        setPartialResults(initialPartialResults);
        setFinalManimCode(null);
        setVideoUrl(null);
        setManimError(null);
        setErrorMessage(null);
        setChatMessages([]);
        if (webSocketRef.current && webSocketRef.current.readyState === WebSocket.OPEN) {
            console.log('[WebSocket] Closing WebSocket from resetStateForNewJob.');
            webSocketRef.current.close(1000, "Client resetting job"); // Provide a code and reason
        }
        webSocketRef.current = null;
    }, []);
    
    const handleScreenshotCaptured = useCallback((dataUrl: string) => {
        console.log('Screenshot captured in hook:', dataUrl.substring(0,100) + '...');
        if (agentStatus !== 'idle' && agentStatus !== 'initiating') {
            resetStateForNewJob();
        }
        setCapturedImageDataUrl(dataUrl);
        setStatusMessage('Screenshot captured. Ready to start processing.');
    }, [agentStatus, resetStateForNewJob]);

    const disconnectAgentUpdates = useCallback((reason = "Client disconnecting") => {
        if (webSocketRef.current) {
            console.log(`[WebSocket] Closing WebSocket connection explicitly. Reason: ${reason}`);
            if (webSocketRef.current.readyState === WebSocket.OPEN || webSocketRef.current.readyState === WebSocket.CONNECTING) {
                webSocketRef.current.close(1000, reason);
            }
            webSocketRef.current = null; 
        }
    }, []);

    const connectToAgentUpdates = useCallback((currentJobId: string) => {
        if (!currentJobId) {
            console.error('No Job ID for WebSocket.'); setErrorMessage('No Job ID.'); setAgentStatus('failed'); return;
        }
        if (webSocketRef.current && webSocketRef.current.readyState === WebSocket.OPEN) {
            console.log('WebSocket already open for job:', currentJobId); return; 
        }

        const websocketUrl = `${WS_BASE_URL}${VERSIONED_API_PATH}/ws/agent_updates/${currentJobId}`;
        console.log('Connecting to WebSocket:', websocketUrl);
        setStatusMessage(`Connecting for job ${currentJobId}...`);
        setAgentStatus('connecting');

        console.log('[DEBUG] Creating WebSocket object for:', websocketUrl);
        const ws = new WebSocket(websocketUrl);
        webSocketRef.current = ws;
        console.log('[DEBUG] WebSocket object created.');

        ws.onopen = () => {
            console.log('!!! WebSocket ESTABLISHED for job:', currentJobId);
            setStatusMessage('Connected. Waiting for updates...');
            setAgentStatus('processing');
        };

        ws.onmessage = (event) => {
            try {
                const rawMessage = event.data;
                console.log('>>> WebSocket RAW message:', rawMessage);
                const message = JSON.parse(rawMessage as string) as AgentWebSocketMessage;
                console.log('>>> WebSocket PARSED message:', message);

                if (!jobId && message.job_id) setJobId(String(message.job_id));

                switch (message.type) {
                    case 'status_update':
                        const statusMsg = message as WebSocketStatusUpdateMessage;
                        console.log('Status Update:', statusMsg.message);
                        setStatusMessage(statusMsg.message || statusMsg.status);
                        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: statusMsg.message || statusMsg.status, type: 'status' }]);
                        break;
                    case 'partial_result':
                        const partial = message as WebSocketPartialResultMessage;
                        setPartialResults(prev => ({ ...prev, [partial.result_type]: partial.content }));
                        if (partial.result_type === 'explanation') { 
                            setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: partial.content, type: 'partial' }]);
                        }
                        break;
                    case 'final_result':
                        const final = message as WebSocketFinalResultMessage;
                        console.log('Final Result: Video URL:', final.video_url, 'Manim Error:', final.manim_error);
                        setFinalManimCode(final.refactored_code || null);
                        setVideoUrl(final.video_url || null); 
                        setManimError(final.manim_error || null); 
                        setStatusMessage(final.message || 'Processing complete!');
                        let finalChatMessageText = final.message || `Processing complete.`;
                        if (final.video_url) finalChatMessageText += ` Video is ready.`;
                        else if (final.manim_error) finalChatMessageText += ` Failed to generate video: ${final.manim_error}`;
                        else finalChatMessageText += ` Manim code generated (no video).`;
                        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: finalChatMessageText, type: 'final' }]);
                        setAgentStatus('completed');
                        // Do not call disconnectAgentUpdates() here immediately.
                        // Let the UI render the completed state. It can be closed by resetStateForNewJob or timeout.
                        break;
                    case 'error':
                        const err = message as WebSocketErrorMessage;
                        console.error('WebSocket error message:', err.error_message);
                        setErrorMessage(err.error_message);
                        setStatusMessage('An error occurred.');
                        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: `Error: ${err.error_message}`, type: 'error' }]);
                        setAgentStatus('failed');
                        disconnectAgentUpdates("Error received from backend");
                        break;
                    default: console.warn('Unknown WebSocket message type:', message);
                }
            } catch (error) {
                console.error('Error processing WebSocket message:', error, event.data);
                setErrorMessage('Error processing update.');
            }
        };

        ws.onerror = (error) => {
            console.error('!!! WebSocket error EVENT:', error);
            setErrorMessage('WebSocket connection error.');
            setStatusMessage('Connection error.');
            setAgentStatus('failed');
            webSocketRef.current = null; 
        };

        ws.onclose = (event) => {
            console.log(`!!! WebSocket CLOSED. Code: ${event.code}, Reason: '${event.reason}', Clean: ${event.wasClean}`);
            // Only set to idle if the process wasn't intentionally completed or failed already
            // and the close was not initiated by client's resetStateForNewJob (which sets status to idle itself)
            // This logic can be tricky. For now, let it be simple: if it closes and we are not in a terminal state, go to idle.
            // If it was closed with code 1000 by disconnectAgentUpdates, this is fine.
            if (agentStatus !== 'completed' && agentStatus !== 'failed') {
                 if (event.code !== 1000) { // Don't revert to idle if client explicitly closed it for reset
                    setStatusMessage('Disconnected from agent.');
                    setAgentStatus('idle'); 
                 }
            }
            webSocketRef.current = null; 
        };
    }, [jobId, agentStatus, disconnectAgentUpdates]); // Removed redundant dependencies

    const startAgentProcessing = useCallback(async (userPrompt: string) => {
        if (!capturedImageDataUrl) {
            setErrorMessage('No screenshot captured.'); return;
        }
        if (['initiating', 'processing', 'connecting'].includes(agentStatus)) {
            console.warn('Processing already in progress.'); return;
        }
        console.log('Starting agent processing with image and prompt:', userPrompt);
        const previousCapturedImage = capturedImageDataUrl; 
        resetStateForNewJob();
        setCapturedImageDataUrl(previousCapturedImage); 

        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'user', text: userPrompt }]);
        setAgentStatus('initiating');
        setStatusMessage('Initiating agent processing...');
        setErrorMessage(null);

        try {
            const response = await fetch(`${API_BASE_URL}${VERSIONED_API_PATH}/agent/jobs`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', },
                body: JSON.stringify({ image_data_url: capturedImageDataUrl, user_prompt: userPrompt }),
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown initiation error.' }));
                throw new Error(errorData.detail || `HTTP error ${response.status}`);
            }
            const result = await response.json();
            console.log('Agent job initiated. Job ID:', result.job_id);
            setJobId(String(result.job_id));
            setStatusMessage('Agent job created. Connecting...');
            connectToAgentUpdates(String(result.job_id));
        } catch (error) {
            const errMsg = error instanceof Error ? error.message : String(error);
            setErrorMessage(`Failed to initiate agent: ${errMsg}`);
            setStatusMessage('Failed to start agent.');
            setAgentStatus('failed');
        }
    }, [capturedImageDataUrl, agentStatus, resetStateForNewJob, connectToAgentUpdates]); // Removed setChatMessages, handled inside

    return {
        capturedImageDataUrl,
        jobId,
        agentStatus,
        statusMessage,
        partialResults,
        finalManimCode,
        videoUrl, 
        manimError, 
        errorMessage,
        chatMessages,
        handleScreenshotCaptured,
        startAgentProcessing,
        disconnectAgentUpdates,
        resetAgentState: () => {
            const previousCapturedImage = capturedImageDataUrl;
            resetStateForNewJob();
            // If you want to clear the image on full reset, uncomment next line
            // setCapturedImageDataUrl(null);
            // For now, keeping the image after reset if a user wants to retry with same image but new prompt
            setCapturedImageDataUrl(previousCapturedImage); 
        }
    };
} 