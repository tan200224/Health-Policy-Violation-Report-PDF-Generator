from flask import Flask, request, jsonify, render_template
import os
import openai
from dotenv import load_dotenv, find_dotenv
from pdfrw import PdfDict, PdfObject

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.getenv('OPENAI_API_KEY')


app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/classify", methods=["POST"])
def classify():
    # get the input from the form
    inputWords = request.form['input']

    #respond = get_openai_response(inputWords)

    messages =  [
                    {'role':'system', 'content':'You are a compliance officer conducting an investagation on an employee who broke a policy'},
                    {'role':'assistant', 'content': "You are givn with a context that is about an employee that violated a policy in healthcare"},
                    {'role':'user', 'content':' Archie accessed patient information that he did not have job-related reasons to access'},
                    {'role':'user', 'content':'Who was the employee who broke the policy'},
                    {'role':'assistant', 'content':'Detetrmine the empolyee name'},
                    {'role':'user', 'content':'What level of violation was deemed at the conclusion of the investigation'},
                    {'role':'assistant', 'content': 'There are three policies, determine which level the violation falls under'},
                    {'role':'user', 'content':'Who is their Human Resources business partner name?'},
                    {'role':'assistant', 'content':'Determine the discipline'},
                    {'role':'user', 'content':'What type of PHI (Protected Health Information) did the employee access '},
                    {'role':'assistant', 'content':'Determine if there is a PHI compromise and if it needs to be reported to the OCR'}
                ]

    #return render_template('index1.html', input = respond)
    return get_completion_from_messages(messages, temperature=1)




def populate_pdf(input_pdf_path, output_pdf_path, data_dict):
    """
    Populates a PDF form with data from a dictionary

    Args:
        input_pdf_path (str): The input PDF form to populate
        output_pdf_path (str): The output PDF to save the data to
        data_dict (dict): A dictionary of data to map into the PDF form

    Returns:
        None
    """

    ## Read the PDF template
    template = pdfrw.PdfReader(input_pdf_path)

    ## Populate the PDF with the data
    for page in template.pages:
        print("page")
        ## Get the annotations
        annotations = page.get('/Annots')  # Using .get() to avoid KeyError
        if annotations is None:
            continue

        ## Loop over the annotations
        for annotation in annotations:

            ## Get the annotation name/object ID
            field_key = annotation.get('/T')

       


    ## Save the PDF with the data
    template.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))
    pdfrw.PdfWriter().write(output_pdf_path, template)






def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]



def main():


    INPUT_PDF_PATH = "D:\dukeHack\POLICY_TEMPLATE_modified.pdf"
    OUTPUT_PDF_PATH = "D:\dukeHack"
    populate_pdf(INPUT_PDF_PATH, OUTPUT_PDF_PATH, row)
    print(f"[INFO] Generated PDF: {row['Full name']}")



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5500, debug=True)
    main()















# def get_openai_response(user_input, model="gpt-3.5-turbo", temperature=0):
#     # Define the prompt you want to send to the OpenAI API
#     prompt = f'User: {user_input}\nAI: '

#     # Call the OpenAI API
#     response = openai.Completion.create(
#         engine="davinci",  # Use the davinci engine
#         prompt=prompt,
#         max_tokens=50,  # Set the maximum number of tokens in the response
#         n=1,  # Number of completions to generate
#         stop=None,  # Set a stopping criterion if needed
#         temperature=0.6,  # Higher values make output more random, lower values make it more deterministic
#     )

#     # Extract the response from the API call
#     ai_response = response.choices[0].text.strip()[:response.choices[0].text.strip().index(".")+1]

#     return ai_response