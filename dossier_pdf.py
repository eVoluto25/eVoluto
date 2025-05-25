import fitz  # PyMuPDF

def compila_dossier_pdf(template_path, output_path, blocchi_dict):
    doc = fitz.open(template_path)

    for page in doc:
        for tag, testo in blocchi_dict.items():
            placeholder = f"{{{{{tag}}}}}"  # esempio: {{contesto_economico}}
            aree = page.search_for(placeholder)
            for area in aree:
                page.add_redact_annot(area, fill=(1, 1, 1))  # copre il segnaposto
            page.apply_redactions()
            for area in aree:
                page.insert_textbox(
                    area,
                    testo,
                    fontsize=12,           # Grandezza del carattere
                    fontname="helv",       # Font Helvetica 
                    color=(0, 0, 0.4),      # Blu scuro in RGB normalizzato
                    wrap=True
            )
                
    doc.save(output_path)
    doc.close()
