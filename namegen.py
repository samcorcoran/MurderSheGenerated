import random

def popRandom(array):
    if array:
        return array.pop(random.randint(0, len(array) - 1))
    return "NAMEGEN ERROR"

class NameGenerator:
    def __init__(self):
        self.maleFirstNames = ['Albert', 'Bancroft', 'Frederick', 'Garrett', 'Hale', 'Johnson', 'Kipling', 'Landon', 'Mathis', 'Neville', 'Oswald', 'Quinn', 'Rodger', 'Sutherland', 'Thurston', 'Hugo', 'Reginald', 'Walter', 'Tarquin', 'Terrence', 'Tobias', 'Gideon', 'Errol', 'Perry']
        self.femaleFirstNames = ['Ansley', 'Bernadine', 'Florence', 'Gertrude', 'Grace', 'Katelyn', 'Lilith', 'Margot', 'Odelia', 'Ophelia', 'Victoria', 'Violet', 'Cecilia', 'Claudia', 'Felicity', 'Vera', 'Tabitha', 'Henrietta', 'Vivian', 'Elaine', 'Prudence', 'Norah']
        self.surnames = ['Annesley', 'Asquith', 'Bankes', 'Buxton', 'Cadogan', 'Calvert', 'Cootes', 'Duncombe', 'Egerton', 'Fortescue', 'Guinness', 'Harley', 'Lambton', 'Mortimer', 'Osborne', 'Paget', 'Phipps', 'Runciman', 'Stopford', 'Talbot', 'Vane-Tempest', 'Walpole']
        self.companyAdjectives = ["Red", "Blue", "Frosty", "Docile", "Quiet", "Rampant", "Mischievious", "Quixotic"]
        self.companyNouns = ["Solutions", "Enterprises", "Explorations", "Horses", "Vehicles", "Bridges", "Spaceflight", "Trains", "Manufacturing", "Tar"]
        self.companyPostfixes = ["Ltd.", "Inc.", "International", "Services", "Investigators", "Savants", "plc"]
        self.socialPrefixes = ["", "The"]
        self.socialNouns = ["Cotswalds", "Billingate", "Haringey", "Chorley", "Old Boy's", "First Jesuit", "Darlington", "Royal"]
        self.socialActivities = ["Bowls", "Debating", "Baking", "Dancing", "Gossip", "Politicking", "Gerrymandering", "Yoga", "Climbing", "Worship", "Gesticulation", "Upholstering"]
        self.socialPostfixes = ["Club", "Group", "Society", "Gang", "Fellowship", "League"]
        self.deathAdjectives = ["grizzly", "bloody", "unsettling", "hideous", "gruesome", "undignified", "scandalous", "unlikely", "terrible", "terrifying", "untimely"]
        self.deathNouns = ["death", "demise", "killing", "murder", "corpse", "execution", "homicide", "extermination", "slaying", "assassination", "end", "departure"]
        self.placeAdjectives = ["sleepy", "snooty", "exclusive", "conservative", "famous", "beautiful", "hidden", "mysterious"]
        self.placeNouns = ["village", "hamlet", "town", "community"]
        self.places = ["Chorley", "Goring", "Streatley", "Pangbourne", "Tilehurst", "Radley"]
        self.deathFlavourText = [", all covered in blood", ", splattered with gore", " surrounded by incriminating evidence of drug abuse", " with a pair of stockings wrapped tight around their neck", ", naked from head to toe", ", battered and bruised", ", completely untouched but for a single killing blow", " dressed in a gimp suit", ". Their corpse was riddled with holes", " bound tightly by rope", ". They were sat upright in an armchair with a peaceful look on their face and a hole in their head",  " (in rather more pieces than one would expect)"]
        self.transport = ["train from Paddington", "motorcar", "taxicab", "train from Waterloo", "train from Kings Cross", "limosine", "horse-drawn carriage", "hot-air balloon"]
        self.times = ["Last night", "Early this morning", "Yesterday evening", "Yesterday lunchtime", "In the dead of night", "The night before Christmas"]
        self.resolutions = ["to ferret out the truth", "for a good old-fashioned grilling", "for a quiet chat", "for intensive interrogations"]
        self.investigatorTitles = ["Detective", "Constable", "Sergant", "Chief Constable", "Detective Inspector"]
        self.investigatorDescriptor = ["sleuth", "investigator", "analyst", "inquisitor", "factfinder", "scrutineer"]
        self.extViewpoint = ["To all appearances", "Outwardly", "As seen by passers-by", "For all intents and purposes", "Seemingly"]
        self.extPlaceAdjective = ["charming", "homely", "quiet", "peaceful", "relaxed", "picturesque", "calm", "happy"]
        self.extPlaceUsage = ["that plays host to a number of clubs, local companies, and quiet romantic affairs", "with a rich culture, society, and industry", "home for boutique businesses and sophisticated societies"]
        self.intViewpoint = ["But behind closed doors", "Little could one know", "Yet for those who live there", "If one looks more closely"]
        self.intPlaceAdjective = ["scandal and secrets abound", "it is a wretched hive of scum and villany", "everyone is out to get you, or to get inside you.."]

    def generateTitle(self):
        return "%s %s" % (
            popRandom(self.deathAdjectives),
            popRandom(self.deathNouns)
            )
        return title

    def generateLocation(self):
        placeNoun = popRandom(self.placeNouns)
        placeAdj = popRandom(self.placeAdjectives)
        return {
            "name": "%s %s of %s" % (
                placeAdj,
                placeNoun,
                popRandom(self.places)
                ),
            "description": "%s, it is a %s %s %s. %s, %s." % (
                random.choice(self.extViewpoint),
                random.choice(self.extPlaceAdjective),
                placeNoun,
                random.choice(self.extPlaceUsage),
                random.choice(self.intViewpoint),
                random.choice(self.intPlaceAdjective)
                )
            }

    def generateScene(self, location, victim, investigator_title, investigator_surname, groups):
        return [
            "%s, %s was found dead at the %s%s." % (
                random.choice(self.times),
                victim.getFullName(),
                random.choice(groups).getLocation(),
                popRandom(self.deathFlavourText)
                ),
            "Scotland Yard dispatched their top %s, %s %s, to the %s via an express %s. The %s has already begun their investigation, and called some prime suspects to the %s %s..." % (
                random.choice(self.investigatorDescriptor),
                investigator_title,
                investigator_surname,
                location["name"],
                random.choice(self.transport),
                investigator_title,
                random.choice(groups).getLocation(),
                random.choice(self.resolutions)
            )
        ]

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
        return "%s %s %s" % (
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
