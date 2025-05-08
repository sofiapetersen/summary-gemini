from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required 
import os
import io
import google.generativeai as genai 
from PyPDF2 import PdfReader
from fpdf import FPDF


ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        reader = PdfReader(pdf_file)
        if reader.is_encrypted:
             print("Erro: PDF criptografado.")
             return None
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Erro inesperado ao extrair texto do PDF: {e}")
        return None
    return text

def generate_summary_with_gemini(text, model): 
    if not model:
        print("Erro: Tentativa de usar modelo Gemini não inicializado.")
        return "Erro: O serviço de processamento de IA não está disponível."

    MAX_TEXT_LENGTH = 30000

    if len(text) > MAX_TEXT_LENGTH:
         print(f"Aviso: Texto muito longo ({len(text)} chars). Truncando para {MAX_TEXT_LENGTH}.")
         text = text[:MAX_TEXT_LENGTH]

    prompt = f"Faça um resumo conciso e objetivo do texto abaixo, mantendo apenas as informações essenciais e principais ideias. O resumo deve ser claro, elegante, direto e preservar o significado original. O  resumo pode ser curto, médio ou com tópicos:\n\n{text}"

    try:
        response = model.generate_content(prompt)
        if not response.text:
             print(f"Aviso: Resposta da API Gemini vazia ou sem texto. Motivo: {response.prompt_feedback}")
             return "Erro: A IA não pôde gerar um resumo para este conteúdo."

        summary = response.text
        return summary
    except Exception as e:
        print(f"Erro ao chamar a API Gemini: {e}")
        return f"Erro ao gerar resumo pela IA: {e}"

def create_pdf_from_text(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_output = pdf.output(dest='S')
    return pdf_output


def register_summary_routes(app, jwt, model): # Passa as dependências
    # "Registra as rotas de resumo e upload 

    @app.route('/upload-and-summarize', methods=['POST'])
    @jwt_required() # Exige um token JWT válido 
    def upload_and_summarize():
        # Rota para receber um arquivo TXT/PDF, resumir com IA e retornar um PDF.

        if 'file' not in request.files:
            return jsonify({'message': 'Nenhum arquivo na requisição'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'Nenhum arquivo selecionado'}), 400

        # Verificar se o tipo de arquivo é permitido
        if file and allowed_file(file.filename):
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            extracted_text = None

            # Extrair texto do arquivo (TXT ou PDF)
            try:
                if file_extension == 'txt':
                     extracted_text = file.stream.read().decode('utf-8')
                elif file_extension == 'pdf':
                     file_content = io.BytesIO(file.stream.read())
                     extracted_text = extract_text_from_pdf(file_content) 
                     if extracted_text is None:
                          return jsonify({'message': 'Erro ao extrair texto do PDF ou PDF inválido/protegido'}), 400

            except Exception as e:
                 print(f"Erro inesperado ao ler/extrair arquivo: {e}")
                 return jsonify({'message': f'Erro inesperado ao ler ou extrair texto do arquivo: {e}'}), 500

            if not extracted_text or not extracted_text.strip():
                return jsonify({'message': 'Não foi possível extrair texto do arquivo ou o arquivo está vazio'}), 400

            # Gerar Resumo com Gemini
            print("Chamando API Gemini para gerar resumo...")
            summary = generate_summary_with_gemini(extracted_text, model) 

            if summary.startswith("Erro:"):
                return jsonify({'message': summary}), 500

            print("Resumo gerado com sucesso. Gerando PDF...")

            # Gerar PDF com o resumo
            try:
                 pdf_output = create_pdf_from_text(summary) 
            except Exception as e:
                print(f"Erro ao gerar PDF: {e}")
                return jsonify({'message': f'Erro ao gerar arquivo PDF com o resumo: {e}'}), 500

            print("PDF gerado com sucesso. Enviando resposta...")

            # Retornar o PDF como resposta para download
            headers = {
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'attachment; filename="resumo_gerado.pdf"'
            }
            return Response(bytes(pdf_output), status=200, headers=headers)

        else:
            return jsonify({'message': 'Tipo de arquivo não permitido. Use .txt ou .pdf.'}), 400
