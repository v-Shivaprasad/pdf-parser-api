from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
import io
import uvicorn

# --- FastAPI instance ---
app = FastAPI()

# --- Enable CORS for React frontend ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your React port
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Debug GET route ---
@app.get("/debug")
async def debug_route():
    return {"status": "Streamlit + FastAPI server is running!"}

# --- PDF upload POST route ---
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        reader = PdfReader(io.BytesIO(contents))
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        return {"text": full_text}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# # --- Streamlit UI (optional) ---
# st.title("Resume Parser Server")
# st.write("You can use this UI to test PDF uploads manually.")

# uploaded_file = st.file_uploader("Upload PDF", type="pdf")
# if uploaded_file:
#     reader = PdfReader(uploaded_file)
#     full_text = ""
#     for page in reader.pages:
#         text = page.extract_text()
#         if text:
#             full_text += text + "\n"
#     st.text_area("Extracted Text", full_text, height=400)

# --- Run FastAPI server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)
