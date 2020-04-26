def calculate_skill_index(row):
    set_row = set(row.split(','))
    set_user = set(skill_user)
    set_match = set_row.intersection(set_user)
    #count the lenght of the set_match
    number_skills_match = len(set_match)
    #count the lenght of the set_ad
    number_skills_ad = len(set_row)
    #create the skills fullfilment, i.e, skills_match divided by skills_ads
    percentage_index = number_skills_match/number_skills_ad
    return percentage_index

class TestStringMethods(unittest.TestCase):

    def test_skill_index(self):
        """ ADD DESCRIPTION """
        german_sentence = "Ich bin ein Berliner und ich liebe Python"
        language_detected = detect_lang(german_sentence)
        self.assertEqual(language_detected, 'de')
