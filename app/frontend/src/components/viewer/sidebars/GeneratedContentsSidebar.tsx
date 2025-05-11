import React, { useState, useEffect } from 'react';
import { useAgentProcessor } from '../../../hooks/useAgentProcessor'; // Adjusted path
import { ChatInterface } from './ChatInterface'; // Import the new ChatInterface
import './GeneratedContentsSidebar.css';

interface GeneratedContentsSidebarProps {
  // Props that Viewer.tsx was passing, if still needed after refactor
  getScreenshot?: () => string | null; // This will likely be handled by the hook now
  onClearScreenshot?: () => void;    // This will also be handled by the hook or internally
  // We might need a prop from Viewer.tsx to inform this component about a new screenshot if 
  // useAgentProcessor is not sufficient or if Viewer.tsx still manages the raw screenshot capture event.
  // For now, let's assume handleScreenshotCaptured from the hook is the primary way.
  initialScreenshot?: string | null; // If Viewer needs to pass an initial screenshot
}

export const GeneratedContentsSidebar: React.FC<GeneratedContentsSidebarProps> = (props) => {
  const {
    capturedImageDataUrl,    // From useAgentProcessor, replaces props.getScreenshot()
    handleScreenshotCaptured, // From useAgentProcessor
    resetAgentState,         // From useAgentProcessor, can be used for onClearScreenshot
    agentStatus,        // Get these from the hook
    chatMessages,       // Get these from the hook
    startAgentProcessing, // Get these from the hook
    statusMessage,
    errorMessage
  } = useAgentProcessor();

  const [activeItem, setActiveItem] = useState<string | null>('Video Explanations'); // Default to Video Explanations
  // The menu items from the original vanilla JS
  const menuItems = ['Images', 'Keywords', 'Notes', 'Mindmaps', 'Summaries', 'Video Explanations'];

  // Effect to handle new screenshots coming from props (e.g. from Viewer.tsx)
  // This acts like the old `(sidebar as any).updateScreenshot` method
  useEffect(() => {
    if (props.initialScreenshot && props.initialScreenshot !== capturedImageDataUrl) {
      handleScreenshotCaptured(props.initialScreenshot);
    }
    // If Viewer.tsx manages clearing, we might need a prop to trigger resetAgentState too.
  }, [props.initialScreenshot, handleScreenshotCaptured, capturedImageDataUrl]);
  
  // This effect can be used if Viewer.tsx still directly calls an update function for new screenshots
  // For example, if Viewer.tsx passes a new screenshot explicitly each time.
  // useEffect(() => {
  //   if (props.getScreenshot) {
  //     const ss = props.getScreenshot();
  //     if (ss && ss !== capturedImageDataUrl) {
  //        handleScreenshotCaptured(ss);
  //     }
  //   }
  // }, [props.getScreenshot, handleScreenshotCaptured, capturedImageDataUrl]);

  const handleClearScreenshot = () => {
    resetAgentState(); // This clears everything including capturedImageDataUrl and chat
    // If onClearScreenshot prop from Viewer is still relevant for Viewer's own state:
    if (props.onClearScreenshot) {
        props.onClearScreenshot();
    }
  };

  return (
    <div className="generated-contents-sidebar">
      <div className="sidebar-menu">
        {menuItems.map(item => (
          <button
            key={item}
            className={`menu-button ${activeItem === item ? 'active' : ''}`}
            onClick={() => setActiveItem(item)}
          >
            {item}
          </button>
        ))}
      </div>
      <div className="sidebar-content">
        {activeItem === 'Video Explanations' ? (
          <div className="video-explanations-content">
            {capturedImageDataUrl ? (
              <div className="screenshot-display">
                <img 
                  src={capturedImageDataUrl} 
                  alt="Screenshot" 
                  style={{ maxWidth: '100%', display: 'block', margin: '16px auto' }} 
                />
                <button onClick={handleClearScreenshot} className="clear-screenshot-btn">
                  Clear Screenshot
                </button>
              </div>
            ) : (
              <div className="placeholder-text" style={{ color: '#888', textAlign: 'center', marginBottom: '8px'}}>
                Make a selection by dragging and dropping to select the area.
                <div style={{ textAlign: 'center'}} dangerouslySetInnerHTML={{ __html: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#888" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>' }} />
              </div>
            )}
            {/* Render ChatInterface only when Video Explanations is active */}
            <ChatInterface 
              agentStatus={agentStatus}
              chatMessages={chatMessages}
              startAgentProcessing={startAgentProcessing}
              capturedImageDataUrl={capturedImageDataUrl}
              statusMessage={statusMessage}
              errorMessage={errorMessage}
            />
          </div>
        ) : (
          <div className="placeholder-text" style={{padding: '20px', textAlign: 'center'}}>
            Content for {activeItem} will be shown here. (Coming Soon)
          </div>
        )}
      </div>
      {/* Resizer logic would need to be re-implemented in React if still needed */}
      {/* <div className="sidebar-resizer"></div> */}
    </div>
  );
}; 