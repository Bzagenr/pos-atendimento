import os
import io
import requests
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from dotenv import load_dotenv

load_dotenv()

TOKEN   = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL")

# Estados da conversa
LGPD, CPF, DATA_NASCIMENTO, ESCOLHA_CONSULTA, RECEITA = range(5)

TERMO_LGPD = (
    "📄 *Termo de Consentimento (LGPD)*\n\n"
    "Para acessar suas informações de consulta, precisamos do seu consentimento "
    "para tratar seus dados pessoais e de saúde conforme a Lei Geral de Proteção "
    "de Dados (Lei 13.709/2018).\n\n"
    "Seus dados serão utilizados exclusivamente para fins de acompanhamento médico "
    "e não serão compartilhados com terceiros sem sua autorização.\n\n"
    "Você consente com o uso dos seus dados?"
)


def gerar_pdf_receita(data: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4

    # Cabeçalho
    c.setFillColor(colors.HexColor("#2C5F8A"))
    c.rect(0, H-80, W, 80, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, H-45, "Receita Médica")
    c.setFont("Helvetica", 10)
    c.drawString(40, H-62, "Sistema de Pós-Atendimento em Saúde")

    # Dados da consulta
    consulta   = data["consulta"]
    paciente   = data["paciente"]
    receita    = data["receita"]

    y = H - 110
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Dados do Paciente")
    c.setLineWidth(0.5)
    c.setStrokeColor(colors.HexColor("#2C5F8A"))
    c.line(40, y-4, W-40, y-4)

    y -= 22
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Paciente: {paciente['nome']}")
    y -= 18
    c.drawString(40, y, f"Data da Consulta: {consulta['data']}")
    y -= 18
    c.drawString(40, y, f"Médico: {consulta['medico']}")
    y -= 18
    c.drawString(40, y, f"Local: {consulta['local']}")

    # Medicamentos
    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Medicamentos Prescritos")
    c.line(40, y-4, W-40, y-4)
    y -= 22

    for i, med in enumerate(receita["medicamentos"]):
        c.setFillColor(colors.HexColor("#EEF3F8") if i % 2 == 0 else colors.white)
        c.rect(38, y-14, W-76, 58, fill=1, stroke=0)
        c.setFillColor(colors.black)

        c.setFont("Helvetica-Bold", 10)
        c.drawString(44, y, f"▪ {med['nome']}")
        y -= 16
        c.setFont("Helvetica", 10)
        if med.get("dosagem"):
            c.drawString(54, y, f"Dosagem: {med['dosagem']}")
            y -= 14
        if med.get("frequencia"):
            c.drawString(54, y, f"Frequência: {med['frequencia']}")
            y -= 14
        if med.get("duracaoDias"):
            c.drawString(54, y, f"Duração: {med['duracaoDias']} dias")
            y -= 14
        if med.get("observacao"):
            c.drawString(54, y, f"Obs: {med['observacao']}")
            y -= 14
        y -= 10

    # Rodapé
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica", 8)
    c.drawString(40, 30, f"Documento gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    c.drawRightString(W-40, 30, "Sistema de Pós-Atendimento em Saúde")

    c.save()
    buffer.seek(0)
    return buffer


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    try:
        resp = requests.get(
            f"{API_URL}/pacientes/telegram/{chat_id}/verificar-consentimento",
            timeout=60
        )
        if resp.status_code == 200 and resp.json().get("consentiu"):
            context.user_data["consentiu_lgpd"] = True
            await update.message.reply_text(
                "👋 Bem-vindo de volta!\n\n"
                "Por favor, informe seu *CPF*:\n"
                "_(Apenas números ou no formato 000.000.000-00)_",
                parse_mode="Markdown"
            )
            return CPF
    except Exception:
        pass

    markup = ReplyKeyboardMarkup(
        [["✅ Sim, concordo"], ["❌ Não concordo"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await update.message.reply_text(TERMO_LGPD, parse_mode="Markdown", reply_markup=markup)
    return LGPD


async def receber_lgpd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text.strip()

    if "Sim" not in resposta:
        await update.message.reply_text(
            "❌ Sem o consentimento não é possível acessar suas informações.\n\n"
            "Se mudar de ideia, digite /start.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    context.user_data["consentiu_lgpd"] = True
    await update.message.reply_text(
        "✅ Consentimento registrado!\n\n"
        "Por favor, informe seu *CPF*:\n"
        "_(Apenas números ou no formato 000.000.000-00)_",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return CPF


async def receber_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpf = update.message.text.strip()
    context.user_data["cpf"] = cpf
    await update.message.reply_text(
        "📅 Agora informe sua *data de nascimento* no formato *DD/MM/AAAA*:",
        parse_mode="Markdown"
    )
    return DATA_NASCIMENTO


async def receber_data_nascimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    cpf   = context.user_data.get("cpf")

    try:
        data_nasc = datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        await update.message.reply_text(
            "❌ Formato inválido. Informe a data no formato *DD/MM/AAAA*:",
            parse_mode="Markdown"
        )
        return DATA_NASCIMENTO

    await update.message.reply_text("🔍 Verificando seus dados...")

    try:
        response = requests.get(
            f"{API_URL}/paciente/{cpf}/ultima-consulta",
            params={"dataNascimento": data_nasc.isoformat()},
            timeout=60
        )

        if response.status_code == 404:
            detail = response.json().get("detail", "")
            if "não encontrado" in detail.lower():
                await update.message.reply_text(
                    "❌ CPF não encontrado no sistema.\n"
                    "Verifique o número e tente novamente com /start."
                )
            elif "não conferem" in detail.lower():
                await update.message.reply_text(
                    "❌ Data de nascimento incorreta.\n"
                    "Verifique e tente novamente com /start."
                )
            else:
                await update.message.reply_text(
                    "ℹ️ Nenhuma consulta finalizada encontrada.\n"
                    "Em caso de dúvidas, fale com a recepção."
                )
            return ConversationHandler.END

        # Registra consentimento LGPD e chat_id
        requests.patch(
            f"{API_URL}/pacientes/cpf/{cpf}/consentimento",
            json={"telegramChatId": update.effective_chat.id},
            timeout=10
        )

        data = response.json()

        if data.get("multiplas_consultas"):
            consultas = data["consultas"]
            context.user_data["consultas"] = consultas
            opcoes = [[f"{c['data']} — {c['medico']}"] for c in consultas]
            markup = ReplyKeyboardMarkup(opcoes, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "📋 Encontrei mais de uma consulta. Qual deseja consultar?",
                reply_markup=markup
            )
            return ESCOLHA_CONSULTA

        context.user_data["consulta_data"] = data
        await exibir_consulta(update, data)

        # Pergunta sobre receita se houver
        if data["receita"]["possui_receita"] and data["receita"]["medicamentos"]:
            markup = ReplyKeyboardMarkup(
                [["✅ Sim, quero a receita"], ["❌ Não, obrigado"]],
                one_time_keyboard=True,
                resize_keyboard=True
            )
            await update.message.reply_text(
                "💊 Foi encontrada uma receita para esta consulta.\n"
                "Deseja recebê-la em PDF?",
                reply_markup=markup
            )
            return RECEITA

        return ConversationHandler.END

    except requests.exceptions.Timeout:
        await update.message.reply_text("⏳ O servidor demorou. Tente novamente com /start")
        return ConversationHandler.END
    except Exception:
        await update.message.reply_text("⚠️ Ocorreu um erro. Tente novamente com /start")
        return ConversationHandler.END


async def receber_escolha_receita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    escolha = update.message.text.strip()
    data    = context.user_data.get("consulta_data")

    if "Sim" in escolha and data:
        await update.message.reply_text(
            "📄 Gerando sua receita em PDF...",
            reply_markup=ReplyKeyboardRemove()
        )
        try:
            pdf_buffer = gerar_pdf_receita(data)
            await update.message.reply_document(
                document=pdf_buffer,
                filename=f"receita_{data['consulta']['data'].replace('/', '-')}.pdf",
                caption="🏥 Receita médica gerada pelo Sistema de Pós-Atendimento."
            )
        except Exception as e:
            await update.message.reply_text("⚠️ Erro ao gerar o PDF. Tente novamente com /start")
    else:
        await update.message.reply_text(
            "Tudo bem! Se precisar, é só acessar novamente.",
            reply_markup=ReplyKeyboardRemove()
        )

    await update.message.reply_text(
        "❓ Para outras dúvidas, entre em contato com a recepção.\n\n"
        "Digite /start para consultar novamente."
    )
    return ConversationHandler.END


async def escolher_consulta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    escolha   = update.message.text.strip()
    cpf       = context.user_data.get("cpf")
    consultas = context.user_data.get("consultas", [])

    consulta_escolhida = next(
        (c for c in consultas if escolha.startswith(c["data"])), None
    )

    if not consulta_escolhida:
        await update.message.reply_text(
            "❌ Opção inválida. Tente novamente com /start",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    await update.message.reply_text("🔍 Buscando informações...", reply_markup=ReplyKeyboardRemove())

    try:
        response = requests.get(
            f"{API_URL}/paciente/{cpf}/consulta/{consulta_escolhida['idConsulta']}",
            timeout=60
        )
        data = response.json()
        context.user_data["consulta_data"] = data
        await exibir_consulta(update, data)

        if data["receita"]["possui_receita"] and data["receita"]["medicamentos"]:
            markup = ReplyKeyboardMarkup(
                [["✅ Sim, quero a receita"], ["❌ Não, obrigado"]],
                one_time_keyboard=True,
                resize_keyboard=True
            )
            await update.message.reply_text(
                "💊 Foi encontrada uma receita para esta consulta.\n"
                "Deseja recebê-la em PDF?",
                reply_markup=markup
            )
            return RECEITA

    except Exception:
        await update.message.reply_text("⚠️ Ocorreu um erro. Tente novamente com /start")

    return ConversationHandler.END


async def exibir_consulta(update: Update, data: dict):
    paciente   = data["paciente"]
    consulta   = data["consulta"]
    orientacao = data["orientacao"]

    await update.message.reply_text(
        f"✅ *Informações da sua consulta*\n\n"
        f"👤 *Paciente:* {paciente['nome']}\n"
        f"📅 *Data:* {consulta['data']}\n"
        f"👨‍⚕️ *Médico:* {consulta['medico']}\n"
        f"🏥 *Local:* {consulta['local']}",
        parse_mode="Markdown"
    )

    if orientacao["descricao"]:
        texto = f"📋 *Orientações médicas:*\n\n{orientacao['descricao']}"
        if orientacao["dataRetorno"]:
            texto += f"\n\n🔄 *Retorno previsto:* {orientacao['dataRetorno']}"
        await update.message.reply_text(texto, parse_mode="Markdown")


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Atendimento encerrado. Digite /start para começar novamente.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LGPD:             [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_lgpd)],
            CPF:              [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_cpf)],
            DATA_NASCIMENTO:  [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_data_nascimento)],
            ESCOLHA_CONSULTA: [MessageHandler(filters.TEXT & ~filters.COMMAND, escolher_consulta)],
            RECEITA:          [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_escolha_receita)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    app.add_handler(conv_handler)

    print("Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()
