import { useState, useRef, useCallback } from 'react';
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

export type AgentStatus = 'idle' | 'initiating' | 'connecting' | 'processing' | 'completed' | 'failed';

interface ChatMessage {
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
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);

    const webSocketRef = useRef<WebSocket | null>(null);

    const resetStateForNewJob = useCallback(() => {
        setJobId(null);
        setAgentStatus('idle');
        setStatusMessage('Ready to process.');
        setPartialResults(initialPartialResults);
        setFinalManimCode(null);
        setErrorMessage(null);
        setChatMessages([]);
        if (webSocketRef.current && webSocketRef.current.readyState === WebSocket.OPEN) {
            webSocketRef.current.close();
        }
        webSocketRef.current = null;
    }, []);
    
    const handleScreenshotCaptured = useCallback((dataUrl: string) => {
        console.log('Screenshot captured in hook:', dataUrl.substring(0,100) + '...');
        // If a previous job was running, or an error occurred, reset before starting a new one implicitly
        if (agentStatus !== 'idle' && agentStatus !== 'initiating') {
            resetStateForNewJob();
        }
        setCapturedImageDataUrl(dataUrl);
        setStatusMessage('Screenshot captured. Ready to start processing.');
    }, [agentStatus, resetStateForNewJob]);

    const disconnectAgentUpdates = useCallback(() => {
        if (webSocketRef.current) {
            console.log('Closing WebSocket connection.');
            webSocketRef.current.close();
            webSocketRef.current = null; // Ensure it's cleared after close
        }
    }, []);

    const connectToAgentUpdates = useCallback((currentJobId: string) => {
        if (!currentJobId) {
            console.error('No Job ID provided for WebSocket connection.');
            setErrorMessage('Failed to connect: No Job ID.');
            setAgentStatus('failed');
            return;
        }

        if (webSocketRef.current && webSocketRef.current.readyState === WebSocket.OPEN) {
            console.log('WebSocket already open for job:', currentJobId);
            //Potentially, if job ID changed, close old and open new, but startAgentProcessing should handle this.
            return; 
        }

        const websocketUrl = `${WS_BASE_URL}/ws/agent_updates/${currentJobId}`;
        console.log('Connecting to WebSocket:', websocketUrl);
        setStatusMessage(`Connecting to agent for job ${currentJobId}...`);
        setAgentStatus('connecting');

        const ws = new WebSocket(websocketUrl);
        webSocketRef.current = ws;

        ws.onopen = () => {
            console.log('WebSocket connection established for job:', currentJobId);
            setStatusMessage('Connected to agent. Waiting for updates...');
            setAgentStatus('processing'); // Or wait for first status update?
        };

        ws.onmessage = (event) => {
            try {
                const rawMessage = event.data;
                console.log('WebSocket message received:', rawMessage);
                const message = JSON.parse(rawMessage as string) as AgentWebSocketMessage;

                // Update job ID from message if not already set (though it should be)
                if (!jobId && message.job_id) setJobId(String(message.job_id));

                switch (message.type) {
                    case 'status_update':
                        const statusMsg = message as WebSocketStatusUpdateMessage;
                        console.log('Status Update:', statusMsg.message);
                        setStatusMessage(statusMsg.message || statusMsg.status);
                        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: statusMsg.message || statusMsg.status, type: 'status' }]);
                        // Optionally update a more granular agentStatus based on message.status if backend sends it
                        break;
                    case 'partial_result':
                        const partial = message as WebSocketPartialResultMessage;
                        console.log('Partial Result:', partial.result_type, partial.content.substring(0,100) + '...');
                        setPartialResults(prev => ({ ...prev, [partial.result_type]: partial.content }));
                        if (partial.result_type === 'explanation') { 
                            setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: partial.content, type: 'partial' }]);
                        }
                        break;
                    case 'final_result':
                        const final = message as WebSocketFinalResultMessage;
                        console.log('Final Result:', final.refactored_code?.substring(0,100) + '...');
                        setFinalManimCode(final.refactored_code || null);
                        setStatusMessage(final.message || 'Processing complete!');
                        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: final.message || `Processing complete. Final Manim code generated.`, type: 'final' }]);
                        setAgentStatus('completed');
                        disconnectAgentUpdates();
                        break;
                    case 'error':
                        const err = message as WebSocketErrorMessage;
                        console.error('WebSocket error message:', err.error_message);
                        setErrorMessage(err.error_message);
                        setStatusMessage('An error occurred.');
                        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'agent', text: `Error: ${err.error_message}`, type: 'error' }]);
                        setAgentStatus('failed');
                        disconnectAgentUpdates();
                        break;
                    default:
                        console.warn('Unknown WebSocket message type:', message);
                }
            } catch (error) {
                console.error('Error processing WebSocket message:', error, event.data);
                setErrorMessage('Error processing update from agent.');
                // Not setting to 'failed' here unless it's a critical parsing error often.
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            setErrorMessage('WebSocket connection error. Ensure the backend is running and accessible.');
            setStatusMessage('Connection error.');
            setAgentStatus('failed');
            webSocketRef.current = null; // Clear ref on error
        };

        ws.onclose = (event) => {
            console.log('WebSocket connection closed:', event.code, event.reason);
            // Only reset to idle if not already in a terminal state (completed/failed)
            if (agentStatus !== 'completed' && agentStatus !== 'failed') {
                setStatusMessage('Disconnected from agent.');
                setAgentStatus('idle'); 
            }
            webSocketRef.current = null; // Ensure ref is cleared
        };

    }, [jobId, agentStatus, disconnectAgentUpdates]); // Added agentStatus and jobId as dependencies

    const startAgentProcessing = useCallback(async (userPrompt: string) => {
        if (!capturedImageDataUrl) {
            setErrorMessage('No screenshot captured to process.');
            console.warn('startAgentProcessing called without capturedImageDataUrl.');
            return;
        }
        if (agentStatus === 'initiating' || agentStatus === 'processing' || agentStatus === 'connecting') {
            console.warn('Agent processing already in progress.');
            return;
        }

        console.log('Starting agent processing with image:', capturedImageDataUrl.substring(0,100) + '...', 'and prompt:', userPrompt);
        resetStateForNewJob(); // Reset state before new job, but keep captured image
        setCapturedImageDataUrl(capturedImageDataUrl); // Re-set it after reset

        // Add user's message to chat
        setChatMessages(prev => [...prev, { id: Date.now().toString(), sender: 'user', text: userPrompt }]);

        setAgentStatus('initiating');
        setStatusMessage('Initiating agent processing...');
        setErrorMessage(null);

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/agent/jobs`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image_data_url: capturedImageDataUrl, user_prompt: userPrompt }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred during initiation.' }));
                throw new Error(errorData.detail || `HTTP error ${response.status}`);
            }

            const result = await response.json();
            console.log('Agent job initiated. Job ID:', result.job_id);
            setJobId(String(result.job_id));
            setStatusMessage('Agent job created. Connecting for updates...');
            // connectToAgentUpdates will be called by useEffect when jobId changes, or call explicitly:
            connectToAgentUpdates(String(result.job_id));

        } catch (error) {
            console.error('Failed to start agent processing:', error);
            const errMsg = error instanceof Error ? error.message : String(error);
            setErrorMessage(`Failed to initiate agent: ${errMsg}`);
            setStatusMessage('Failed to start agent.');
            setAgentStatus('failed');
        }
    }, [capturedImageDataUrl, agentStatus, resetStateForNewJob, connectToAgentUpdates, setChatMessages]);

    return {
        capturedImageDataUrl,
        jobId,
        agentStatus,
        statusMessage,
        partialResults,
        finalManimCode,
        errorMessage,
        chatMessages,
        handleScreenshotCaptured,
        startAgentProcessing,
        disconnectAgentUpdates, // Expose if manual disconnect is needed from UI
        resetAgentState: () => { // Expose a full reset if needed
            resetStateForNewJob();
            setCapturedImageDataUrl(null);
        }
    };
} 