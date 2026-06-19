from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
        name,
        mbti,
        careers):

    filename = f"reports/{name}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            f"Career Report : {name}",
            styles['Title']
        )
    )

    elements.append(
        Paragraph(
            f"MBTI : {mbti}",
            styles['Normal']
        )
    )

    for role, salary in careers:

        elements.append(
            Paragraph(
                f"{role} - {salary}",
                styles['Normal']
            )
        )

    doc.build(elements)

    return filename