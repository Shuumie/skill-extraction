import ollama
import json
import unittest

from SkillExtraction import skill_extraction

class OllamaSkillExtraction(skill_extraction):
    def extract_skills(self, text):
        ollama_message = 'Extract all technologies, programming languages, frameworks, tools and platforms mentioned. Normalize them to their most common canonical names (e.g., "k8s" -> "kubernetes", "tf" -> "tensorflow"). Return ONLY a JSON array of unique technology names in lowercase. Omit any introduction or suffix in your answer. Add no commentary. Do not assume (e.g. reading "microservices on cloud" do not assume "kubernetes". Add "cloud" to the result instead). Text: '
        message = f'""" {ollama_message}\n {text} """'

        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return self.__result_to_array__(response)

    def __result_to_array__(self, ollama_result):
        return json.loads(ollama_result['message']['content'])

class ollama_skill_extraction_tests(OllamaSkillExtraction, unittest.TestCase):
    def test(self):
        test_requirements = ''' """Wir suchen einen erfahrenen Senior Backend Engineer zur Unterstützung der Modernisierung unserer geschäftskritischen Backend-Landschaft von monolithischen Anwendungen hin zu Cloud-fähigen Microservices.
    Aufgaben und Kenntnisse:
    ·Java- und Spring-Boot-Backend-Entwicklung
    '''
        self.assertCountEqual(self.extract_skills(test_requirements), ["java", "springboot", "cloud"])

        print("Test finished successfully")

ollama.delete("llama3")
#ollama_skill_extraction_tests().test()