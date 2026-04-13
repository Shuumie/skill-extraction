from ollama import Client
import ollama as ol_base
import json
import unittest
import os
import redis

from SkillExtraction import skill_extraction

class OllamaSkillExtraction(skill_extraction):
    def __init__(self):
        self.client = Client(host=os.environ.get("OLLAMA_HOST"))

    def extract_skills(self, text, pull_if_unavailable = True):
        ollama = self.client
        ollama_message = 'Extract all technologies, programming languages, frameworks, tools and platforms mentioned. Normalize them to their most common canonical names (e.g., "k8s" -> "kubernetes", "tf" -> "tensorflow"). Return ONLY a JSON array of unique technology names in lowercase. Omit any introduction or suffix in your answer. Add no commentary. Do not assume (e.g. reading "microservices on cloud" do not assume "kubernetes". Add "cloud" to the result instead). Text: '
        message = f'""" {ollama_message}\n {text} """'

        try:
            response = ollama.chat(
                model="llama3",
                messages=[
                    {"role": "user", "content": message}
                ]
            )
        except ol_base.ResponseError:
            if pull_if_unavailable:
                ollama.pull("llama3")
                return self.extract_skills(text, pull_if_unavailable=False)
            raise

        return self.__result_to_array__(response)

    def __result_to_array__(self, ollama_result):
        return json.loads(ollama_result['message']['content'])

class RedisCommunicator:
    def __init__(self):
        self.client = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), db=0)

    def add_skill(self, value):
        print(f"adding skill {value}")
        self.client.rpush("skills", value)

    def list_skills(self):
        skills = self.client.lrange("skills", 0, -1)
        list(print(skill) for skill in skills)

class ollama_skill_extraction_tests(OllamaSkillExtraction, unittest.TestCase):
    def test(self):
        test_requirements = ''' """Wir suchen einen erfahrenen Senior Backend Engineer zur Unterstützung der Modernisierung unserer geschäftskritischen Backend-Landschaft von monolithischen Anwendungen hin zu Cloud-fähigen Microservices.
    Aufgaben und Kenntnisse:
    ·Java- und Spring-Boot-Backend-Entwicklung
    '''
        print("Test started")

        self.assertCountEqual(self.extract_skills(test_requirements), ["java", "springboot", "cloud"])

        print("Test finished successfully")

print("-----START-----")
skills = ["spring", "spring", "java"]
redisComm = RedisCommunicator()
list(redisComm.add_skill(skill) for skill in skills)
redisComm.list_skills()