import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter

app = FastAPI(title="Docling API")

converter = DocumentConverter()


@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "Docling API"
    }


@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    try:
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = converter.convert(tmp_path)

        markdown = result.document.export_to_markdown()

        os.remove(tmp_path)

        return JSONResponse({
            "success": True,
            "markdown": markdown
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
