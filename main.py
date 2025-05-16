from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
from xhtml2pdf import pisa
import io

app = FastAPI()

class PDFRequest(BaseModel):
    html: str

def convert_html_to_pdf(source_html: str) -> bytes:
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(source_html), dest=result)
    if pisa_status.err:
        raise Exception("Error while generating PDF")
    return result.getvalue()

@app.post("/generate-pdf/")
async def generate_pdf(data: PDFRequest):
    try:
        pdf_bytes = convert_html_to_pdf(data.html)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=output.pdf"}
        )
    except Exception as e:
        return {"error": str(e)}
