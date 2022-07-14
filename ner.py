from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics._models import RecognizeEntitiesResult as RER
from azure.core.credentials import AzureKeyCredential
from joblib import dump, load

key = "d4891fdc2cfb480a9b7b8faab9dea137"
endpoint = "https://westus.api.cognitive.microsoft.com/"


def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential)
    return text_analytics_client


client = authenticate_client()


# Example function for recognizing entities from text
def entity_recognition_example(client):
    try:
        job_desc_file = open("sample_job_desc.txt", encoding='utf8')
        job_desc = job_desc_file.read()
        job_desc_file.close()
        resume_file = open("sample_resume.txt", encoding='utf8')
        resume_text = resume_file.read()
        resume_file.close()
        # documents = ["I had a wonderful trip to Seattle last week."]
        documents = [resume_text]
        result = client.recognize_entities(documents=documents)[0]

        dump(result, "ner_result.joblib")
        print("Named Entities:\n")
        for entity in result.entities:
            print("\tText: \t", entity.text, "\tCategory: \t", entity.category, "\tSubCategory: \t", entity.subcategory,
                  "\n\tConfidence Score: \t", round(entity.confidence_score, 2), "\tLength: \t", entity.length,
                  "\tOffset: \t", entity.offset, "\n")

    except Exception as err:
        print("Encountered exception. {}".format(err))


entity_recognition_example(client)


def get_skills(results):
    """Given a result, extract all entities labeled as Skill or Product """
    skills = set()
    for entity in results.entities:
        if entity.confidence_score >= 0.8 and entity.category in ('Skill', 'Product'):
            skills.add(entity.text)

    return skills
