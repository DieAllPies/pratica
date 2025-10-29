from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, ValidationError
from app.utils.sheets_service import append_to_sheet

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


class MessageForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    message: str


# 👇 ADD THIS
@router.get("/sobre")
async def sobre_page(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})


@router.post("/send-message")
async def send_message(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    try:
        form = MessageForm(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message,
        )
    except ValidationError:
        return templates.TemplateResponse(
            "sobre.html",
            {"request": request, "error": "Por favor insira um e-mail válido."},
        )

    success = await append_to_sheet(
        form.first_name, form.last_name, form.email, form.message
    )

    if success:
        return RedirectResponse(url="/sobre?sent=1", status_code=303)
    else:
        return templates.TemplateResponse(
            "sobre.html",
            {"request": request, "error": "Erro ao enviar a mensagem. Tente novamente."},
        )
