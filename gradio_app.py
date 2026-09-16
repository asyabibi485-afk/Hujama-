"""
Optional Gradio frontend for testing the same appointment backend.

Run:
    python gradio_app.py

The main deployed application is app.py (Streamlit).
"""

import gradio as gr
from backend import submit_booking, get_ai_response

def book(name, gender, phone, preferred_date, preferred_time, notes):
    if not name or not phone or not preferred_date:
        return "❌ Name, phone, and preferred date are required."
    practitioner = "Muhammad Isreal" if gender == "Male" else "Shamim Akhtar"
    try:
        result = submit_booking(
            name=name,
            gender=gender,
            phone=phone,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            practitioner=practitioner,
            notes=notes or "",
        )
        return (
            "✅ Appointment request received!\n\n"
            f"Booking ID: {result['booking_id']}\n"
            f"Practitioner: {practitioner}\n"
            "Status: Pending"
        )
    except Exception as e:
        return f"❌ Could not save booking: {e}"

def ai(question):
    if not question:
        return "Please enter a question."
    return get_ai_response(question)

with gr.Blocks(title="Hijama Appointment") as demo:
    gr.Markdown("# 🩸 Hijama Wellness Center")
    gr.Markdown("### Book an Appointment")

    with gr.Row():
        with gr.Column():
            name = gr.Textbox(label="Full name")
            gender = gr.Dropdown(["Male", "Female"], value="Male", label="Gender")
            phone = gr.Textbox(label="Phone number")
        with gr.Column():
            preferred_date = gr.Textbox(
                label="Preferred date",
                placeholder="YYYY-MM-DD",
            )
            preferred_time = gr.Dropdown(
                ["Morning", "Afternoon", "Evening", "Flexible"],
                value="Flexible",
                label="Preferred time",
            )
            notes = gr.Textbox(label="Symptoms / notes", lines=5)

    submit = gr.Button("📩 Submit Appointment Request", variant="primary")
    result = gr.Textbox(label="Booking result", lines=5)
    submit.click(
        book,
        inputs=[name, gender, phone, preferred_date, preferred_time, notes],
        outputs=result,
    )

    gr.Markdown("---")
    gr.Markdown("## 🤖 Gemini Information Assistant")
    question = gr.Textbox(label="Question")
    ask = gr.Button("Ask Gemini")
    answer = gr.Markdown()
    ask.click(ai, inputs=question, outputs=answer)

if __name__ == "__main__":
    demo.launch()
