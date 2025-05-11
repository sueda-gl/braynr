import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Box, TextField, Button, Paper, Typography, CircularProgress, Alert } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ScreenshotMonitor from './ScreenshotMonitor'; 
import ChatMessageBubble from './ChatMessageBubble'; 
// Use type-only import for ChatMessage if verbatimModuleSyntax is enabled
import { useAgentProcessor } from '../hooks/useAgentProcessor';
import type { ChatMessage } from '../hooks/useAgentProcessor';

const VIDEO_SRC_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const ChatInterface: React.FC = () => {
    const [userInput, setUserInput] = useState('');
    const {
        capturedImageDataUrl,
        agentStatus,
        statusMessage,
        finalManimCode,
        videoUrl,
        manimError,
        errorMessage,
        chatMessages, 
        handleScreenshotCaptured,
        startAgentProcessing,
        resetAgentState
    } = useAgentProcessor();

    const chatContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
        // console.log("--- ChatInterface Update ---"); // Basic log
        // More detailed logging can be added here if needed during specific debugging phases
    }, [chatMessages, agentStatus]); // Keep dependencies minimal for scroll effect

    // Separate useEffect for logging complex states if needed, to avoid re-running scroll logic unnecessarily
    useEffect(() => {
        console.log("--- ChatInterface Full State Log ---");
        console.log("Agent Status:", agentStatus);
        console.log("Video URL:", videoUrl);
        console.log("Manim Error:", manimError);
        console.log("Final Manim Code Present:", !!finalManimCode);
        console.log("Status Message:", statusMessage);
        console.log("Error Message:", errorMessage);
    }, [agentStatus, videoUrl, manimError, finalManimCode, statusMessage, errorMessage]);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUserInput(event.target.value);
    };

    const handleSubmit = async (event?: React.FormEvent<HTMLFormElement>) => {
        if (event) event.preventDefault();
        if (!capturedImageDataUrl) {
            alert("Please capture a screenshot before sending a prompt.");
            return;
        }
        if (!userInput.trim()) {
            alert("Please enter a prompt.");
            return;
        }
        startAgentProcessing(userInput.trim());
        setUserInput('');
    };

    const handleReset = () => {
        resetAgentState();
        setUserInput('');
    }

    // Log directly within the render function (before the return statement)
    console.log('[ChatInterface RENDER FN] agentStatus:', agentStatus, 'videoUrl:', videoUrl);

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', bgcolor: 'grey.100' }}>
            <ScreenshotMonitor onScreenshotCaptured={handleScreenshotCaptured} />
            
            <Typography variant="h5" sx={{ textAlign: 'center', py: 2, bgcolor: 'primary.main', color: 'white' }}>
                Content Explainer Agent
            </Typography>

            {capturedImageDataUrl && (
                <Box sx={{ textAlign: 'center', my: 1, p:1, border: '1px dashed grey', mx: 'auto', bgcolor: 'grey.50' }}>
                    <Typography variant="caption">Captured Image (Ready for Prompt):</Typography>
                    <img src={capturedImageDataUrl} alt="Captured Screenshot" style={{ maxWidth: '200px', maxHeight: '150px', display:'block', margin: '5px auto', border: '1px solid #ccc' }} />
                </Box>
            )}

            <Paper 
                ref={chatContainerRef}
                elevation={3} 
                sx={{ flexGrow: 1, overflowY: 'auto', p: 2, m: 2, bgcolor: 'white' }}
            >
                {chatMessages.map((msg) => (
                    <ChatMessageBubble key={msg.id} message={msg} />
                ))}

                {(agentStatus === 'initiating' || agentStatus === 'connecting' || agentStatus === 'processing') && statusMessage && (
                    <Box sx={{ display: 'flex', alignItems: 'center', my: 1, justifyContent: 'flex-start', p:1, bgcolor: 'info.light', borderRadius: '4px' }}>
                        <CircularProgress size={20} sx={{ mr: 1 }} />
                        <Typography variant="body2" color="text.primary">{statusMessage}</Typography>
                    </Box>
                )}

                {agentStatus === 'completed' && (
                    <Box className="agent-final-output" sx={{ mt: 2, p: 2, borderTop: '2px solid primary.main', bgcolor: 'grey.50'}}>
                        <Typography variant="h6" gutterBottom sx={{color: 'primary.dark'}}>Agent Output:</Typography>
                        {console.log("[Render Check] In 'completed' block. videoUrl:", videoUrl, "manimError:", manimError)}
                        {videoUrl ? (
                            <Box>
                                <Typography variant="subtitle1" gutterBottom>Generated Video:</Typography>
                                <video 
                                    key={videoUrl} 
                                    controls 
                                    src={`${VIDEO_SRC_BASE_URL}${videoUrl}`}
                                    width="100%" 
                                    style={{ maxWidth: '560px', display: 'block', margin: '10px auto', border: '1px solid #ddd'}}
                                    onError={(e) => console.error('Video player error:', e)}
                                    onCanPlay={() => console.log('Video can play - src:', `${VIDEO_SRC_BASE_URL}${videoUrl}`)}
                                    onLoadedData={() => console.log('Video data loaded')}
                                >
                                    Your browser does not support the video tag. 
                                    Download: <a href={`${VIDEO_SRC_BASE_URL}${videoUrl}`} download>video</a>
                                </video>
                            </Box>
                        ) : manimError ? (
                            <Box>
                                <Alert severity="error" sx={{mb: 1}}>Error generating video: {manimError}</Alert>
                                {finalManimCode && (
                                    <Box mt={1}>
                                        <Typography variant="caption">Generated Manim Code (for debugging):</Typography>
                                        <Paper component="pre" elevation={0} sx={{ maxHeight: '150px', overflowY: 'auto', background: '#efefef', border: '1px solid #ddd', p: 1, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
                                            <code>{finalManimCode}</code>
                                        </Paper>
                                    </Box>
                                )}
                            </Box>
                        ) : finalManimCode ? (
                            <Box>
                                <Typography variant="body2" gutterBottom>Manim Code Generated (video not available):</Typography>
                                <Paper component="pre" elevation={0} sx={{ maxHeight: '200px', overflowY: 'auto', background: '#efefef', border: '1px solid #ddd', p: 1, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
                                    <code>{finalManimCode}</code>
                                </Paper>
                            </Box>
                        ) : (
                            <Typography variant="body2">Processing complete, but no specific output available.</Typography>
                        )}
                    </Box>
                )}

                {errorMessage && (agentStatus === 'failed' || (agentStatus === 'completed' && !videoUrl && !finalManimCode)) && (
                     <Alert severity="error" sx={{mt: 1}}>{errorMessage}</Alert>
                )}
            </Paper>

            <Paper elevation={3} sx={{ p: 1.5, m: 2, mt: 0, bgcolor: 'white' }}>
                <form onSubmit={handleSubmit} style={{ display: 'flex', alignItems: 'center' }}>
                    <TextField
                        fullWidth
                        variant="outlined"
                        size="small"
                        placeholder={capturedImageDataUrl ? "Enter your prompt..." : "Capture a screenshot first..."}
                        value={userInput}
                        onChange={handleInputChange}
                        disabled={!capturedImageDataUrl || (agentStatus !== 'idle' && agentStatus !== 'completed' && agentStatus !== 'failed')}
                        sx={{ mr: 1 }}
                    />
                    <Button 
                        variant="contained" 
                        type="submit" 
                        endIcon={<SendIcon />} 
                        disabled={!capturedImageDataUrl || !userInput.trim() || (agentStatus !== 'idle' && agentStatus !== 'completed' && agentStatus !== 'failed')}
                    >
                        Send
                    </Button>
                    <Button 
                        variant="outlined"
                        color="secondary"
                        onClick={handleReset}
                        sx={{ ml: 1 }}
                        disabled={(agentStatus !== 'idle' && agentStatus !== 'completed' && agentStatus !== 'failed')}
                    >
                        Reset
                    </Button>
                </form>
            </Paper>
        </Box>
    );
};

export default ChatInterface; 