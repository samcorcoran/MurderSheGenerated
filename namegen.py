import random

def popRandom(array):
    return array.pop(random.randint(0, len(array) - 1))

def generateFirstName(gender):
    maleFirstNames = ['Albert', 'Bancroft', 'Frederick', 'Garrett', 'Hale', 'Johnson', 'Kipling', 'Landon', 'Mathis', 'Neville', 'Oswald', 'Quinn', 'Rodger', 'Sutherland', 'Thurston', 'Hugo', 'Reginald', 'Walter', 'Tarquin', 'Terrence', 'Tobias', 'Gideon', 'Errol', 'Perry']
    femaleFirstNames = ['Ansley', 'Bernadine', 'Florence', 'Gertrude', 'Grace', 'Katelyn', 'Lilith', 'Margot', 'Odelia', 'Ophelia', 'Victoria', 'Violet', 'Cecilia', 'Claudia', 'Felicity', 'Vera', 'Tabitha', 'Henrietta', 'Vivian', 'Elaine', 'Prudence', 'Norah']
    nameChoices = None
    if gender == "m":
        nameChoices = maleFirstNames
    else:
        nameChoices = femaleFirstNames
    return popRandom(nameChoices)

def generateSurname():
    surnames = ['Annesley', 'Asquith', 'Bankes', 'Buxton', 'Cadogan', 'Calvert', 'Cootes', 'Duncombe', 'Egerton', 'Fortescue', 'Guinness', 'Harley', 'Lambton', 'Mortimer', 'Osborne', 'Paget', 'Phipps', 'Runciman', 'Stopford', 'Talbot', 'Vane-Tempest', 'Walpole']
    surname = popRandom(surnames)
    return surname

def generateCompanyName():
    companyAdjectives = ["Red", "Blue", "Frosty", "Docile", "Quiet", "Rampant", "Mischievious", "Quixotic"]
    companyNouns = ["Solutions", "Enterprises", "Explorations", "Horses", "Vehicles", "Bridges", "Spaceflight", "Trains", "Manufacturing", "Tar"]
    companyPostfixes = ["Limited", "Incorporated", "International", "Services", "Investigators", "Savants", "PLC"]
    adj = popRandom(companyAdjectives)
    noun = popRandom(companyNouns)
    postfix = popRandom(companyPostfixes)
    return ', '.join([adj, noun, postfix])

def generateSocialClubName():
    socialPrefixes = ["", "The"]
    socialNouns = ["Cotswalds", "Billingate", "Haringey", "Chorley", "Old Boy's", "First Jesuit", "Darlington", "Royal"]
    socialActivities = ["Bowls", "Debating", "Baking", "Dancing", "Gossip", "Politicking", "Gerrymandering", "Yoga", "Climbing", "Worship", "Gesticulation", "Upholstering"]
    socialPostfixes = ["Club", "Group", "Society", "Gang", "Fellowship", "League"]
    prefix = random.choice(socialPrefixes)
    noun = popRandom(socialNouns)
    activity = popRandom(socialActivities)
    postfix = random.choice(socialPostfixes)
    return ' '.join([prefix, noun, activity, postfix])
