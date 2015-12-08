import random

def popRandom(array):
    return array.pop(random.randint(0, len(array) - 1))

class NameGenerator:
    def __init__(self):
        self.maleFirstNames = ['Albert', 'Bancroft', 'Frederick', 'Garrett', 'Hale', 'Johnson', 'Kipling', 'Landon', 'Mathis', 'Neville', 'Oswald', 'Quinn', 'Rodger', 'Sutherland', 'Thurston', 'Hugo', 'Reginald', 'Walter', 'Tarquin', 'Terrence', 'Tobias', 'Gideon', 'Errol', 'Perry']
        self.femaleFirstNames = ['Ansley', 'Bernadine', 'Florence', 'Gertrude', 'Grace', 'Katelyn', 'Lilith', 'Margot', 'Odelia', 'Ophelia', 'Victoria', 'Violet', 'Cecilia', 'Claudia', 'Felicity', 'Vera', 'Tabitha', 'Henrietta', 'Vivian', 'Elaine', 'Prudence', 'Norah']
        self.surnames = ['Annesley', 'Asquith', 'Bankes', 'Buxton', 'Cadogan', 'Calvert', 'Cootes', 'Duncombe', 'Egerton', 'Fortescue', 'Guinness', 'Harley', 'Lambton', 'Mortimer', 'Osborne', 'Paget', 'Phipps', 'Runciman', 'Stopford', 'Talbot', 'Vane-Tempest', 'Walpole']
        self.companyAdjectives = ["Red", "Blue", "Frosty", "Docile", "Quiet", "Rampant", "Mischievious", "Quixotic"]
        self.companyNouns = ["Solutions", "Enterprises", "Explorations", "Horses", "Vehicles", "Bridges", "Spaceflight", "Trains", "Manufacturing", "Tar"]
        self.companyPostfixes = ["Limited", "Incorporated", "International", "Services", "Investigators", "Savants", "PLC"]
        self.socialPrefixes = ["", "The"]
        self.socialNouns = ["Cotswalds", "Billingate", "Haringey", "Chorley", "Old Boy's", "First Jesuit", "Darlington", "Royal"]
        self.socialActivities = ["Bowls", "Debating", "Baking", "Dancing", "Gossip", "Politicking", "Gerrymandering", "Yoga", "Climbing", "Worship", "Gesticulation", "Upholstering"]
        self.socialPostfixes = ["Club", "Group", "Society", "Gang", "Fellowship", "League"]

    def generateName(self, type):
        if type == "familial":
            return self.generateSurname()
        elif type == "professional":
            return self.generateCompanyName()
        elif type == "social":
            return self.generateSocialClubName()
        else:
            return type

    def generateFirstName(self, gender):
        nameChoices = None
        if gender.name == "male":
            nameChoices = self.maleFirstNames
        else:
            nameChoices = self.femaleFirstNames
        return popRandom(nameChoices)

    def generateSurname(self):
        surname = popRandom(self.surnames)
        return surname

    def generateCompanyName(self):
        return "%s %s, %s" % (
            popRandom(self.companyAdjectives),
            popRandom(self.companyNouns),
            popRandom(self.companyPostfixes)
            )

    def generateSocialClubName(self):
        prefix = random.choice(self.socialPrefixes)
        noun = popRandom(self.socialNouns)
        activity = popRandom(self.socialActivities)
        postfix = random.choice(self.socialPostfixes)
        return ' '.join([prefix, noun, activity, postfix])
