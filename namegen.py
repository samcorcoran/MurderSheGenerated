import random

maleFirstNames = ['Albert', 'Bancroft', 'Frederick', 'Garrett', 'Hale', 'Johnson', 'Kipling', 'Landon', 'Mathis', 'Neville', 'Oswald', 'Quinn', 'Rodger', 'Sutherland', 'Thurston', 'Hugo', 'Reginald', 'Walter', 'Tarquin', 'Terrence', 'Tobias', 'Gideon', 'Errol', 'Perry']
femaleFirstNames = ['Ansley', 'Bernadine', 'Florence', 'Gertrude', 'Grace', 'Katelyn', 'Lilith', 'Margot', 'Odelia', 'Ophelia', 'Victoria', 'Violet', 'Cecilia', 'Claudia', 'Felicity', 'Vera', 'Tabitha', 'Henrietta', 'Vivian', 'Elaine', 'Prudence', 'Norah']
surnames = ['Annesley', 'Asquith', 'Bankes', 'Buxton', 'Cadogan', 'Calvert', 'Cootes', 'Duncombe', 'Egerton', 'Fortescue', 'Guinness', 'Harley', 'Lambton', 'Mortimer', 'Osborne', 'Paget', 'Phipps', 'Runciman', 'Stopford', 'Talbot', 'Vane-Tempest', 'Walpole']

maleFirstNames.sort()
femaleFirstNames.sort()
surnames.sort()

def generateFirstName(gender):
    nameChoices = None
    if gender == "m":
        nameChoices = maleFirstNames
    else:
        nameChoices = femaleFirstNames
    return nameChoices.pop()

def generateSurname():
    surname = surnames.pop()
    return surname

companyAdjectives = ["Red", "Blue", "Frosty", "Docile", "Quiet", "Rampant", "Mischievious", "Quixotic"]
companyNouns = ["Solutions", "Enterprises", "Explorations", "Horses", "Vehicles", "Bridges", "Spaceflight", "Trains", "Manufacturing", "Tar"]
companyPostfixes = ["Limited", "Incorporated", "International", "Services", "Investigators", "Savants", "PLC"]

companyAdjectives.sort()
companyNouns.sort()
companyPostfixes.sort()

def generateCompanyName():
    adj = companyAdjectives.pop()
    noun = companyNouns.pop()
    postfix = companyPostfixes.pop()
    return ', '.join([adj, noun, postfix])

socialPrefixes = ["", "The"]
socialNouns = ["Cotswalds", "Billingate", "Haringey", "Chorley", "Old Boy's", "First Jesuit", "Darlington", "Royal"]
socialActivities = ["Bowls", "Debating", "Baking", "Dancing", "Gossip", "Politicking", "Gerrymandering", "Yoga", "Climbing", "Worship", "Gesticulation", "Upholstering"]
socialPostfixes = ["Club", "Group", "Society", "Gang", "Fellowship", "League"]

socialPrefixes.sort()
socialNouns.sort()
socialActivities.sort()
socialPostfixes.sort()

def generateSocialClubName():
    prefix = random.choice(socialPrefixes)
    noun = socialNouns.pop()
    activity = socialActivities.pop()
    postfix = random.choice(socialPostfixes)
    return ' '.join([prefix, noun, activity, postfix])