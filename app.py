import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO

st.set_page_config(
    page_title="Document Formatter",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Document Formatter")
st.write("Upload a Word template, add your instructions, and download a formatted document.")

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    code = st.text_input("Enter admin code", type="password")

    if st.button("Unlock"):
        if code == st.secrets["edit_password"]:
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("Incorrect code")

else:
    st.success("Unlocked")

    prompt = st.text_area(
        "What do you want the document to say?",
        height=200,
        placeholder="Type the content or instructions here..."
    )

    uploaded_file = st.file_uploader(
        "Upload supporting file",
        type=["txt", "docx", "pdf"]
    )

    template_file = st.file_uploader(
        "Upload your Word template",
        type=["docx"]
    )

    if uploaded_file:
        st.info(f"Uploaded: {uploaded_file.name}")

    if st.button("Generate Document"):
        if not prompt:
            st.warning("Please type your instructions or content.")
        elif not template_file:
            st.warning("Please upload your Word template.")
        else:
            doc = DocxTemplate(template_file)

            context = {
                "title": "Formatted Document",
                "body": prompt,
                "uploaded_filename": uploaded_file.name if uploaded_file else ""
            }

            doc.render(context)

            output = BytesIO()
            doc.save(output)
            output.seek(0)

            st.download_button(
                label="Download Formatted Document",
                data=output,
                file_name="formatted_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    if st.button("Lock App"):
        st.session_state.unlocked = False
        st.rerun()
