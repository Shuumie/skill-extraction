from datetime import datetime, timedelta
import random
from collections import defaultdict

class SkillReader:
    def read_skills(self):
        return self.populate_random_skills()
    
    def populate_random_skills(self, amount = 100, skills = ["spring", "kafka", "java", "javascript", "aws", "cloud", "keycloak"], max_age = timedelta(days=30)):
        result = []
        now = datetime.now()
        for i in range(amount):
            skill = random.choice(skills)
            occurance = now - timedelta(seconds=random.randint(0, int(max_age.total_seconds())))
            result.append({"skill": skill, "time": occurance})
        return result
    
class SkillWeighter:
    def __init__(self, max_age = timedelta(days=1)):
        self.max_age = max_age

    def weigh_skills(self, skills):
        now = datetime.now()
        result = []

        def __calculate_age__(from_time, to_time):
            return from_time - to_time;

        for skill_data in skills:
            skill_name = skill_data["skill"]
            skill_occurance = skill_data["time"]

            skill_age = __calculate_age__(now, skill_occurance)

            if self.max_age - skill_age < timedelta(0):
                continue

            skill_weight = (self.max_age - skill_age).total_seconds() / self.max_age.total_seconds()
            result.append({"skill": skill_name, "time":skill_occurance, "weight": skill_weight})

        return result
    
class SkillAnalyzer:
    def __init__(self, skill_name_dict_element = "skill", skill_weight_dict_element = "weight"):
        self.skill_name_dict_element = skill_name_dict_element
        self.skill_weight_dict_element = skill_weight_dict_element

    def group_skills(self, skills):
        result = defaultdict(float)
        max_skill = 0
        for skill in skills:
            result[skill[self.skill_name_dict_element]] += skill[self.skill_weight_dict_element]
            if result[skill[self.skill_name_dict_element]] > max_skill:
                max_skill = result[skill[self.skill_name_dict_element]]

        if max_skill > 1:
            for result_element in result:
                result[result_element] /= max_skill

        return result


    
skill_reader = SkillReader()
skills = skill_reader.read_skills()
skill_weighter = SkillWeighter()
skill_weight = skill_weighter.weigh_skills(skills)
skill_analyzer = SkillAnalyzer()
print(skill_analyzer.group_skills(skill_weight))