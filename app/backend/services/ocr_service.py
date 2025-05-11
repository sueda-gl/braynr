# app/backend/services/ocr_service.py
import base64
# from PIL import Image # Example import for a library like Pillow/Tesseract
# import io             # Example import for handling byte streams
import io
import easyocr

# Initialize the reader globally or manage its lifecycle appropriately
# For a hackathon, initializing per call is simpler but less efficient.
# For production, initialize once: reader = easyocr.Reader(['en'])
# We will initialize it inside the function for simplicity here.

async def extract_text_from_image(image_data_url: str) -> str:
    """
    Extracts text from an image provided as a Data URL.
    Uses EasyOCR for text recognition.
    """
    print(f"OCR Service: Received image data URL (first 100 chars): {image_data_url[:100]}...")
    
    try:
        header, encoded_data = image_data_url.split(",", 1)
    except ValueError:
        print("OCR Service: Invalid Data URL format. Couldn't split header and data.")
        return "Error: Invalid Data URL format"

    try:
        image_bytes = base64.b64decode(encoded_data)
        
        # Initialize EasyOCR reader
        # For mathematical formulas, 'en' should be sufficient.
        # You could add other languages if needed: ['en', 'ch_sim'], etc.
        reader = easyocr.Reader(['en'], gpu=False) # Specify gpu=False if not using GPU, True otherwise
        
        # Read text from image bytes
        # The result is a list of (bbox, text, prob) tuples
        results = reader.readtext(image_bytes)
        
        # Combine all detected text pieces
        extracted_text = " ".join([text for _, text, _ in results])
        
        print(f"OCR Service: Extracted text: '{extracted_text}'")
        return extracted_text
    except base64.binascii.Error as e:
        print(f"OCR Service: Base64 decoding error: {e}")
        return f"Error: Base64 decoding failed - {e}"
    except Exception as e:
        # Catching general exceptions from EasyOCR or other image processing steps
        print(f"OCR Service: Error during OCR processing: {e}")
        return f"Error: OCR processing failed - {e}" 