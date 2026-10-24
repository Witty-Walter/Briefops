import fitz  # PyMuPDF
import os

def generate_test_pdf(output_path: str):
    doc = fitz.open()
    
    # Standard A4 size (595 x 842 points)
    width, height = 595, 842
    margin = 50
    content_width = width - (2 * margin)
    
    contract_elements = [
        {
            "type": "title",
            "text": "MASTER SERVICES AND VENDOR AGREEMENT"
        },
        {
            "type": "subtitle",
            "text": "CONFIDENTIAL & PROPRIETARY | LEGAL CONTRACT FOR ENTERPRISE SERVICES"
        },
        {
            "type": "preamble",
            "text": "This Master Services Agreement (\"Agreement\") is entered into as of October 24, 2026, by and between:\n\n"
                    "PARTY A (CLIENT): TechNova Global Solutions Private Limited, a company incorporated under the Companies Act, 2013, "
                    "having its registered office at Koramangala Industrial Layout, Bengaluru, Karnataka 560034; and\n\n"
                    "PARTY B (SERVICE PROVIDER): AgileByte Enterprises LLP, a registered MSME entity under the Micro, Small and Medium "
                    "Enterprises Development (MSMED) Act, 2006, having its registered office at Hinjewadi Phase 1, Pune, Maharashtra 411057.\n\n"
                    "WHEREAS the Client desires to engage the Service Provider for custom enterprise software development and technology consulting, "
                    "and the Service Provider agrees to perform such services in accordance with the terms below:"
        },
        {
            "type": "clause",
            "text": "1. Scope of Services and Project Deliverables\n"
                    "The Service Provider shall design, develop, test, and deploy the enterprise logistics management module as described in Statement of Work (SOW) Schedule A. All deliverables must conform to agreed technical specifications, industry security standards, and acceptance criteria formally approved in writing by the Client."
        },
        {
            "type": "clause",
            "text": "2. Payment Terms and Statutory Taxes\n"
                    "The Client agrees to pay the Service Provider a total consideration of INR 12,50,000 against verified project milestones. All invoices submitted by the Service Provider shall be settled within ninety (90) days from the date of invoice receipt. The Client reserves the unilateral right to withhold payment at its sole discretion without incurring interest. All professional fees are inclusive of Goods and Services Tax (GST), and the Service Provider shall bear sole liability for any reverse charge obligations."
        },
        {
            "type": "clause",
            "text": "3. Limitation of Liability and Indemnification\n"
                    "In no event shall the total aggregate liability of the Client arising out of or related to this Agreement exceed INR 10,000, under any cause of action, whether in contract, tort, or negligence. Conversely, the Service Provider agrees to indemnify, defend, and hold harmless the Client against all third-party claims, data breaches, and liabilities without any monetary ceiling or financial cap whatsoever."
        },
        {
            "type": "clause",
            "text": "4. Non-Compete and Exclusivity Covenants\n"
                    "The Service Provider and its key engineering personnel agree not to directly or indirectly engage in, consult for, advise, or provide software engineering services to any competing logistics or supply chain company operating within the territory of India for a period of five (5) consecutive years following the termination or expiration of this Agreement."
        },
        {
            "type": "clause",
            "text": "5. Termination and Notice Period\n"
                    "The Client reserves the unilateral right to terminate this Agreement at any time, for convenience or without cause, immediately upon written email notice to the Service Provider, without penalty, severance obligation, or compensation for work-in-progress. The Service Provider may terminate this Agreement only upon providing one hundred and eighty (180) days advance written notice."
        },
        {
            "type": "clause",
            "text": "6. Dispute Resolution and Governing Law\n"
                    "Any dispute, controversy, or claim arising out of or relating to this Agreement shall be referred to and finally resolved by arbitration administered in London, United Kingdom, conducted in accordance with English Arbitration Law. The courts of London shall have exclusive jurisdiction, superseding any provisions of the Indian Arbitration and Conciliation Act, 1996."
        },
        {
            "type": "clause",
            "text": "7. Intellectual Property Rights Ownership\n"
                    "All intellectual property rights, source code repositories, technical documentation, and design assets authored or developed by the Service Provider shall vest immediately in the Client upon generation, regardless of whether corresponding milestone payments or invoices have been approved, cleared, or paid."
        },
        {
            "type": "sign",
            "text": "IN WITNESS WHEREOF, the duly authorized representatives of the Parties have executed this Agreement:\n\n"
                    "For TechNova Global Solutions Pvt. Ltd.          For AgileByte Enterprises LLP\n\n"
                    "Signature: __________________________            Signature: __________________________\n"
                    "Name: Rahul Sharma                               Name: Vikram Deshmukh\n"
                    "Title: Director                                  Title: Designated Partner\n"
                    "Date: 24 October 2026                            Date: 24 October 2026"
        }
    ]
    
    page = doc.new_page(width=width, height=height)
    y_pos = margin
    
    def check_page_break(needed_space):
        nonlocal page, y_pos
        if y_pos + needed_space > (height - margin - 20):
            page.insert_text(fitz.Point(width / 2 - 15, height - 25), f"Page {len(doc)}", fontname="helv", fontsize=8.5, color=(0.45, 0.45, 0.45))
            page = doc.new_page(width=width, height=height)
            y_pos = margin
            
    for item in contract_elements:
        itype = item["type"]
        
        if itype == "title":
            rect = fitz.Rect(margin, y_pos, width - margin, y_pos + 26)
            page.insert_textbox(rect, item["text"], fontsize=14, fontname="hebo", color=(0.08, 0.22, 0.42), align=1)
            y_pos += 26
            
        elif itype == "subtitle":
            rect = fitz.Rect(margin, y_pos, width - margin, y_pos + 18)
            page.insert_textbox(rect, item["text"], fontsize=8.5, fontname="hebo", color=(0.4, 0.4, 0.4), align=1)
            y_pos += 20
            # Decorative horizontal line
            page.draw_line(fitz.Point(margin, y_pos), fitz.Point(width - margin, y_pos), color=(0.75, 0.8, 0.88), width=1)
            y_pos += 14
            
        elif itype == "preamble":
            text = item["text"]
            lines = text.count("\n") + len(text) // 75 + 2
            needed = lines * 13 + 10
            check_page_break(needed)
            rect = fitz.Rect(margin, y_pos, width - margin, y_pos + needed)
            page.insert_textbox(rect, text, fontsize=9.5, fontname="helv", color=(0.2, 0.2, 0.2), lineheight=1.22)
            y_pos += needed + 8
            
        elif itype == "clause":
            text = item["text"]
            lines = text.count("\n") + len(text) // 72 + 2
            needed = lines * 13 + 12
            check_page_break(needed)
            
            rect = fitz.Rect(margin, y_pos, width - margin, y_pos + needed)
            page.insert_textbox(rect, text, fontsize=9.5, fontname="helv", color=(0.15, 0.15, 0.15), lineheight=1.25)
            y_pos += needed + 6
            
        elif itype == "sign":
            text = item["text"]
            lines = text.count("\n") + 4
            needed = lines * 14 + 16
            check_page_break(needed)
            page.draw_line(fitz.Point(margin, y_pos), fitz.Point(width - margin, y_pos), color=(0.75, 0.8, 0.88), width=0.8)
            y_pos += 12
            rect = fitz.Rect(margin, y_pos, width - margin, y_pos + needed)
            page.insert_textbox(rect, text, fontsize=9, fontname="helv", color=(0.15, 0.15, 0.15), lineheight=1.2)
            y_pos += needed
            
    # Page number for final page
    page.insert_text(fitz.Point(width / 2 - 15, height - 25), f"Page {len(doc)}", fontname="helv", fontsize=8.5, color=(0.45, 0.45, 0.45))
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    doc.close()
    print(f"Successfully generated dummy contract: {output_path}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "data/test_contract_msme.pdf"
    generate_test_pdf(out)
