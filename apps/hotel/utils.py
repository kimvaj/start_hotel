# from fpdf import FPDF
# from io import BytesIO

# from apps.hotel.models import Payment


# def generate_payment_pdf(payment):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     pdf.cell(200, 10, txt="Payment Receipt", ln=True, align='C')

#     pdf.cell(200, 10, txt=f"Payment ID: {payment.id}", ln=True)
#     pdf.cell(200, 10, txt=f"Booking ID: {payment.booking.id}", ln=True)
#     pdf.cell(200, 10, txt=f"Guest: {payment.booking.guest.first_name} {payment.booking.guest.last_name}", ln=True)
#     pdf.cell(200, 10, txt=f"Room Number: {payment.booking.room.room_number}", ln=True)
#     pdf.cell(200, 10, txt=f"Payment Date: {payment.payment_date}", ln=True)
#     pdf.cell(200, 10, txt=f"Amount: {payment.amount}", ln=True)
#     pdf.cell(200, 10, txt=f"Payment Method: {dict(Payment.PAYMENT_METHOD_CHOICES).get(payment.payment_method)}", ln=True)

#     pdf_content = BytesIO()
#     pdf.output(pdf_content)
#     pdf_content.seek(0)

#     return pdf_content.getvalue()
