import React, { useState, useEffect, useRef } from 'react';
// import { useAgentProcessor } from '../../../hooks/useAgentProcessor'; // No longer call the hook directly
import './ChatInterface.css'; // We will create this CSS file later

// Define VIDEO_SRC_BASE_URL for constructing video URLs
const VIDEO_SRC_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// TODO: Move ChatMessage to a shared types file (e.g., src/types/chat.ts)
interface ChatMessage {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  type?: 'status' | 'partial' | 'final' | 'error';
}

// Define props for ChatInterface
interface ChatInterfaceProps {
  agentStatus: string; // Or the specific AgentStatus type if exported from hook
  chatMessages: ChatMessage[];
  startAgentProcessing: (userPrompt: string) => Promise<void>;
  capturedImageDataUrl: string | null;
  statusMessage: string;
  errorMessage: string | null;
  // Add new props for video display
  videoUrl?: string | null;
  manimError?: string | null;
  finalManimCode?: string | null;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  agentStatus,
  chatMessages,
  startAgentProcessing,
  capturedImageDataUrl,
  statusMessage, // Now we might want to use this for more detailed status
  errorMessage,  // And this for errors not coming from Manim
  // Destructure new props
  videoUrl,
  manimError,
  finalManimCode
}) => {
  // Logs are good for seeing what props are received
  console.log('--- Sidebar ChatInterface Props ---');
  console.log('Agent Status:', agentStatus);
  console.log('Video URL:', videoUrl);
  console.log('Manim Error:', manimError);
  console.log('Final Manim Code Present:', !!finalManimCode);

  const [currentMessage, setCurrentMessage] = useState('');
  const chatBodyRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = () => {
    if (currentMessage.trim() && capturedImageDataUrl) {
      startAgentProcessing(currentMessage.trim());
      setCurrentMessage('');
    } else if (!capturedImageDataUrl) {
      console.warn('ChatInterface: No screenshot captured. Cannot send message.');
      alert('Please capture a screenshot before sending a message.');
    }
  };

  useEffect(() => {
    // Scroll to bottom of chat when new messages arrive
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [chatMessages, agentStatus]); // Added agentStatus to scroll on status changes too

  const isProcessing = agentStatus === 'initiating' || agentStatus === 'connecting' || agentStatus === 'processing';

  return (
    <div className="chat-interface">
      <div className="chat-header">Video Explanations Chat</div>
      <div className="chat-body" ref={chatBodyRef}>
        {chatMessages.map((msg: ChatMessage) => (
          <div key={msg.id} className={`chat-message ${msg.sender} ${msg.type || ''}`}>
            <div className="chat-message-bubble">
              {/* Render text with line breaks preserved */}
              {msg.text.split('\n').map((line: string, index: number) => (
                <React.Fragment key={index}>
                  {line}
                  <br />
                </React.Fragment>
              ))}
            </div>
          </div>
        ))}

        {/* Display Agent Status during processing (can use statusMessage prop) */}
        {isProcessing && statusMessage && (
          <div className="chat-message agent status">
             <div className="chat-message-bubble">
                {statusMessage} {/* Or a spinner + statusMessage */}
             </div>
          </div>
        )}

        {/* Display Final Output: Video, Manim Error, or Fallback Code */}
        {agentStatus === 'completed' && (
            <div className="agent-final-output chat-message agent final">
                <div className="chat-message-bubble">
                    <p style={{ fontWeight: 'bold', marginBottom: '8px' }}>Agent Output:</p>
                    {videoUrl ? (
                        <div>
                            <p>Generated Video:</p>
                            <video 
                                key={videoUrl} 
                                controls 
                                src={`${VIDEO_SRC_BASE_URL}${videoUrl}`}
                                width="100%" 
                                style={{ maxWidth: '100%', display: 'block', borderRadius: '8px'}} // Adjusted for sidebar
                                onError={(e) => console.error('Video player error:', e)}
                            >
                                Your browser does not support the video tag. 
                                <a href={`${VIDEO_SRC_BASE_URL}${videoUrl}`} download>Download video</a>
                            </video>
                        </div>
                    ) : manimError ? (
                        <div>
                            <p style={{ color: 'red', fontWeight: 'bold' }}>Error generating video:</p>
                            <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', color: 'red' }}>{manimError}</pre>
                            {finalManimCode && (
                                <details style={{marginTop: '8px'}}>
                                    <summary style={{cursor: 'pointer', fontSize: '0.9em'}}>Show Manim Code (for debugging)</summary>
                                    <pre className="manim-code-display">{finalManimCode}</pre>
                                </details>
                            )}
                        </div>
                    ) : finalManimCode ? (
                        <div>
                            <p>Manim Code Generated (video not available):</p>
                            <pre className="manim-code-display">{finalManimCode}</pre>
                        </div>
                    ) : (
                        <p>Processing complete, but no specific output available.</p>
                    )}
                </div>
            </div>
        )}

        {/* Display general error messages from the hook if not a Manim error during completed state */}
        {errorMessage && agentStatus === 'failed' && (
             <div className="chat-message agent error">
                <div className="chat-message-bubble">
                    Error: {errorMessage}
                </div>
            </div>
        )}
      </div>
      <div className="chat-input-area">
        <textarea
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          placeholder={capturedImageDataUrl ? "Ask something about the screenshot..." : "Capture a screenshot to enable chat"}
          rows={3}
          disabled={!capturedImageDataUrl || isProcessing}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSendMessage();
            }
          }}
        />
        <button 
          onClick={handleSendMessage} 
          disabled={!capturedImageDataUrl || isProcessing || !currentMessage.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}; 