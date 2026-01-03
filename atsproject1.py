from flask import Flask, request, render_template
import PyPDF2
from google import genai

app = Flask(__name__)

# ✅ Configure Gemini API
client = genai.Client(api_key="your api key")


def extract_text_from_pdf(pdf_file):
    extracted_text = ""
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text

    return extracted_text


@app.route("/", methods=["GET", "POST"])
def index():
    rating = ""
    if request.method == "POST":
        pdf = request.files.get("resume")

        if pdf:
            resume_text = extract_text_from_pdf(pdf)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
Here is my resume content:
{resume_text}

Question:
Give a rating out of 10 for this resume and short feedback.
"""
            )

            rating = response.text

    return render_template("index.html", rating=rating)


if __name__ == "__main__":
    app.run(debug=True)
