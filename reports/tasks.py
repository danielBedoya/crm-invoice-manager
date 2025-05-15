from django.core.mail import EmailMessage
from django.conf import settings
from django_rq import job

from .utils.file_generator import generate_excel, generate_csv
from dashboard.utils.search_utils import filter_data
import logging

logger = logging.getLogger("reports")


@job
def generate_and_send_report(user_email, selected_columns, data, format="xlsx"):

    logger.info(
        f"Generate and send report called with selected_columns: {selected_columns} and format: {format}"
    )

    try:
        filtered_data = filter_data(data, "")

        if format == "csv":
            file_stream, mime_type, filename = generate_csv(
                selected_columns, filtered_data
            )
        else:
            file_stream, mime_type, filename = generate_excel(
                selected_columns, filtered_data
            )

        logger.info(
            f"Sending email from {settings.DEFAULT_FROM_EMAIL} with filename: {filename}"
        )
        email = EmailMessage(
            subject="Tu reporte está listo",
            body="Adjunto encontrarás el reporte solicitado.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        file_stream.seek(0)
        email.attach(filename, file_stream.read(), mime_type)
        email.send()
    except Exception as e:
        logger.error(f"Failed to generate or send report to {user_email}: {str(e)}")
