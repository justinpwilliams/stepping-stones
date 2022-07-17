from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics._models import RecognizeEntitiesResult as RER
from azure.core.credentials import AzureKeyCredential
from joblib import dump, load

from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import graph
from config import MSFT_COGNITIVE_KEY

model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

endpoint = "https://westus.api.cognitive.microsoft.com/"


def authenticate_client():
    ta_credential = AzureKeyCredential(MSFT_COGNITIVE_KEY)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential)
    return text_analytics_client


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


def get_skills(results):
    """Given a result, extract all entities labeled as Skill or Product """
    skills = set()
    for entity in results.entities:
        if entity.confidence_score >= 0.8 and entity.category in ('Skill', 'Product'):
            skills.add(entity.text)

    return skills


def embed(sentences):
    """Get sentence embeddings"""
    # TODO Stem and Lemmatize
    return model.encode(sentences)


def ranked_related_concepts(skills):
    """Given a list of skills, use cosine similarity to find the most closely related concepts"""
    concepts = graph.load_topics('../LectureBank-master/LB-Paper/208topics.csv')
    concept_embeddings = embed(concepts['Name'])
    skill_embeddings = embed(skills)
    relation = cosine_similarity(skill_embeddings, concept_embeddings)

    maxes = np.max(relation, axis=0)
    max_sort = np.argsort(-maxes)  # Sort in descending order of cosine similarity
    ranked_concepts = concepts.iloc[max_sort]

    return ranked_concepts


if __name__ == '__main__':
    # client = authenticate_client()
    # entity_recognition_example(client)

    # Embeddings test
    keyword = ["markov decision process"]
    tests = ["markov decision process", "partial order markov decision process", "this is a sandwich"]
    # keyword_embedding = model.encode(keyword)
    # embeddings = model.encode(tests)
    # cos_sim = cosine_similarity(keyword_embedding, embeddings)

    print(ranked_related_concepts(tests)['Name'])
