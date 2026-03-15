# --------------------------------------------------
# AI Slide Content Generator
# --------------------------------------------------

def generate_slide_content(llm, answer):

    prompt = f"""
You are creating a professional presentation.

Convert the following explanation into a presentation.

Rules:
- Create exactly 6 slides
- Each slide must contain:
    Slide Title
    3-5 bullet points
- Bullet points should be short and clear
- Use simple educational language

Format EXACTLY like this:

Slide 1: Title
- bullet point
- bullet point
- bullet point

Slide 2: Title
- bullet point
- bullet point
- bullet point

Slide 3: Title
- bullet point
- bullet point
- bullet point

Content:
{answer}
"""

    response = llm.invoke(prompt)

    return response


# --------------------------------------------------
# Parse LLM Slide Text into Dictionary
# --------------------------------------------------

def parse_slides(slide_text):

    slides = {}
    lines = slide_text.split("\n")

    current_title = None
    points = []

    for line in lines:

        line = line.strip()

        # Detect slide titles
        if line.lower().startswith("slide"):

            if current_title:
                slides[current_title] = points

            current_title = line
            points = []

        # Detect bullet points
        elif line.startswith("-"):

            points.append(line.replace("-", "").strip())

    if current_title:
        slides[current_title] = points

    return slides