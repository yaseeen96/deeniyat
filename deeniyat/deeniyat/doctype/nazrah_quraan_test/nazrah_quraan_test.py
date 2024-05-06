# Copyright (c) 2024, yaseen and contributors
# For license information, please see license.txt

from datetime import date
import frappe
from frappe.model.document import Document
import pdfkit



def generate_pdf_and_send_email(html, recipient_email):
	# Configuration for pdfkit to ensure landscape orientation
	config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
	options = {
		'page-size': 'A4',
		'orientation': 'Landscape',
		'encoding': "UTF-8"
	}

	try:

	# Convert HTML to PDF
		pdf_data = pdfkit.from_string(html, False, options=options, configuration=config)

		# Send email with the PDF attachment
		frappe.sendmail(
			recipients=recipient_email,
			subject="Certificate of Completion",
			message="Congratulations on completing the course! Please find attached your certificate.",
			attachments=[{'fname': 'Certificate of Completion.pdf', 'fcontent': pdf_data}]
		)

		return "Email sent successfully with certificate."
	except Exception as e:
		return f"An error occurred while sending the email: {str(e)}"


def render_certificate_html(doc, certification):
    # Hardcoded HTML with placeholders replaced by actual data
    html = f"""
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="pdfkit-orientation" content="Landscape" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Certificate of Completion</title>
    <link
        href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@300;400&display=swap"
        rel="stylesheet">
    <style>
        .parent-container {{
            margin: 0;
			height: 100vh;
            padding: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #eae2b7;
            font-family: 'Open Sans', sans-serif;
        }}

        .certificate {{
            display: flex;
            justify-content: center;
            align-items: center;
   

            
            background: white;
            text-align: center;
            padding: 30px;
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.15);
            border-radius: 10px;
            position: relative;
            border: 5px solid #aacc00;
        }}

        .image {{
            flex-direction: row;
            justify-content: center;
        }}

        .content {{
            flex-direction: row;
        }}

        .logo {{
            width: 300px;
            top: 20px;
            left: 20px;
        }}

        h1 {{
            font-family: 'Merriweather', serif;
            color: #d00000;
            font-size: 28px;
            margin-bottom: 10px;
        }}

        p {{
            color: #005f73;
            font-size: 18px;
            margin: 5px 0;
        }}

        h2 {{
            color: #048b9a;
            font-size: 24px;
            margin: 20px 0;
        }}

        h3 {{
            color: #9a031e;
            font-size: 20px;
            margin-bottom: 20px;
        }}

        h4 {{
            color: #fb8b24;
            font-size: 16px;
            margin-bottom: 40px;
        }}

        .signature {{
            font-size: 16px;
            color: #444;
            margin-top: 20px;
        }}

        #sign {{
            height: 50px;
            margin-bottom: -25px;
        }}
    </style>
</head>

<body>
<div class="parent-container">
    <div class="certificate">
        <div class="image">
            <img src="https://shoaib.amlc.in/wp-content/uploads/2024/04/logo.jpeg" alt="Institution Logo" class="logo">
        </div>
        <div class="content">
            <h1>Certificate of Completion</h1>
            <p>This is to certify that</p>
            <h2>{doc.student or 'Student Name'}</h2>
            <p>has successfully completed the</p>
            <h3>{certification}</h3>
            <p>on</p>
            <h4>{doc.completion_date or 'Completion Date'}</h4>
            <div class="signature">
                <img src="https://shoaib.amlc.in/wp-content/uploads/2024/04/signature.png" alt="signature" id="sign">
                <p>___________________</p>
                <p>[Signature]</p>
            </div>
        </div>
    </div>
	</div>
</body>

</html>
    """
    return html



class NazrahQuraanTest(Document):
	def validate(self):
		# Dynamically get all check fields in the DocType
		check_fields = [f.fieldname for f in frappe.get_meta(self.doctype).fields if f.fieldtype == 'Check']

		# Check if all check fields are checked
		all_checked = all(self.get(field) == 1 for field in check_fields)

		# Set the completion date to the current date if all check fields are checked and completion date is not already set
		if all_checked and not self.completion_date:
			self.completion_date = date.today()
			html = render_certificate_html(self, "Nazrah Quraan Test")
			message = generate_pdf_and_send_email(html, "yaseen@standardtouch.com")
			frappe.msgprint(message)
			


