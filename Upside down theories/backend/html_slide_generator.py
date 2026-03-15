import os

def create_html_slides(title, slides):

    os.makedirs("output", exist_ok=True)

    slide_html = ""

    for slide_title, points in slides.items():

        slide_html += f"<section>"
        slide_html += f"<h2>{slide_title}</h2>"
        slide_html += "<ul>"

        for p in points:
            slide_html += f'<li class="fragment fade-in">{p}</li>'

        slide_html += "</ul>"
        slide_html += "</section>"

    # Load template
    with open("templates/reveal_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Insert slides into template
    final_html = template.replace("{{slides}}", slide_html)

    output_path = "output/briefing.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    return output_path