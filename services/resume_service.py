import os
import json
from mongoengine import connect
from gridfs import GridFS
from io import BytesIO
from model.resume import PDFFile
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

connect(host=os.environ.get('MONGO_URI'))
# Create a GridFS instance
fs = GridFS(PDFFile._get_db())


def evaluate_service(file):
    pdf_file = PDFFile(filename=file.filename)
    pdf_file.save()
    extracted_text = extract_text_from_pdf(file)
    response = get_response(extracted_text)
    file_id = fs.put(file, filename=pdf_file.id)

    return response


def get_pdf(file_id):
    pdf_file = PDFFile.objects.get(id=file_id)
    file_obj = fs.get(pdf_file.id)
    return file_obj


def extract_text_from_pdf(file_obj):
    extracted_text = ""

    # Open the PDF file
    with BytesIO(file_obj.read()) as file_stream:
        reader = PdfReader(file_stream)

        # Get the number of pages
        num_pages = len(reader.pages)

        # Iterate through each page
        for i in range(num_pages):
            # Get the page
            page = reader.pages[i]

            # Extract text from the page
            text = page.extract_text()

            # Append the extracted text to the result
            extracted_text += text

    return extracted_text


def get_response(text):
    load_dotenv()
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": "You're an AI-powered CV parser capable of extracting relevant information "
                                          "from resumes. The system should accurately identify and categorize key "
                                          "details such as personal information, work experience, education, skills, "
                                          "and contact information. Consider implementing natural language processing "
                                          "(NLP) techniques to understand and extract contextual information "
                                          "accurately. Ensure the parser handles different CV layouts and formats "
                                          "efficiently.Only provide information for the provided CV_text."},
            {"role": "user",
             "content": "Please provide a JSON response, with the following structure," +
                        '{{''\\"skills''\\":\\"<all_skill_here_as_a_list>\\",\\"degree\\":\\"<degree>\\",'
                        '\\"name\\":\\"<name_surname>\\",'
                        '\\"university\\":\\"<university>\\",'
                        '\\"experience\\":\\"<experience>\\",'
                        '\\"title\\":\\"<title>\\",}},\\"……\\"]' +
                        'CV_text:' + text +
                        "Behave like an API REST entrypoint, giving only snake case JSON responses "
                        "formatted strictly"
                        "with no"
                        "deviations. I don't need any extra information, provide response strictly using structure "
                        "provided above. Get prompts like http requests from an API Client. Your response should be "
                        "JSON"
                        "parseable by a machine. Don’t give any polite introduction on your response, just JSON format"}
        ]


    )

    fn_client = OpenAI(
        api_key=os.environ.get("FINETUNE_API_KEY"),
    )
    ft_response = fn_client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::9BimcPvv",
        top_p=1,
        temperature=0,
        messages=[
            {"role": "system", "content": "I am assigning you the role of a system AI hiring assistant for an "
                                          "intelligent job matching platform. Your task involves reviewing resumes "
                                          "with two main objectives:\n\n1. Ensure consistency by identifying any "
                                          "instances of overlapping work experiences. A consistent resume should have "
                                          "distinct and non-overlapping work periods.\n2. Verify the presence of at "
                                          "least one programming language skill. This is a key requirement for "
                                          "consistency in our evaluation criteria.\n\nA resume is deemed consistent "
                                          "only if it meets both criteria: it has no overlapping work experience and "
                                          "includes at least one programming language in the skills section. Any "
                                          "deviation from these standards is considered inconsistent."},
            {"role": "user",
             "content": "Can you review this resume [RESUME] and tell me if it shows consistency in terms of "
                        "overlapping work experience and the presence of at least one programming language?"
                        "[RESUME]="+text}
        ]
    )
    processed = response.choices[0].message.content
    print(processed)

    processed_json = json.loads(processed)
    processed_json["consistency"] = ft_response.choices[0].message.content
    processed_with_consistent = json.dumps(processed_json, indent=4)
    return processed_with_consistent
