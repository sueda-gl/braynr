import React, { useState, useEffect, useRef } from 'react';
// import { useAgentProcessor } from '../../../hooks/useAgentProcessor'; // No longer call the hook directly
import './ChatInterface.css'; // We will create this CSS file later

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
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  agentStatus,
  chatMessages,
  startAgentProcessing,
  capturedImageDataUrl,
  // statusMessage, // included for completeness, can be used in UI
  // errorMessage
}) => {
  // Logs are good for seeing what props are received
  console.log('--- ChatInterface Props ---');
  console.log('capturedImageDataUrl:', capturedImageDataUrl?.substring(0, 50) + '...');
  console.log('chatMessages:', JSON.stringify(chatMessages, null, 2));
  console.log('agentStatus:', agentStatus);
  // console.log('statusMessage:', statusMessage);
  // console.log('errorMessage:', errorMessage);

  const [currentMessage, setCurrentMessage] = useState('');
  const chatBodyRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = () => {
    if (currentMessage.trim() && capturedImageDataUrl) {
      startAgentProcessing(currentMessage.trim());
      setCurrentMessage('');
    } else if (!capturedImageDataUrl) {
      // TODO: Optionally notify user they need to capture a screenshot first
      console.warn('ChatInterface: No screenshot captured. Cannot send message.');
      // alert('Please capture a screenshot before sending a message.');
    }
  };

  useEffect(() => {
    // Scroll to bottom of chat when new messages arrive
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [chatMessages]);

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
        {isProcessing && chatMessages.length > 0 && (
          <div className="chat-message agent typing-indicator">
             <div className="chat-message-bubble">
                Agent is thinking...
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