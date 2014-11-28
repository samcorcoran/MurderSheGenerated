import random

maleFirstNames = ['Albert', 'Bancroft', 'Frederick', 'Garrett', 'Hale', 'Johnson', 'Kipling', 'Landon', 'Mathis', 'Neville', 'Oswald', 'Quinn', 'Rodger', 'Sutherland', 'Thurston']

femaleFirstNames = ['Ansley', 'Bernadine', 'Florence', 'Gertrude', 'Grace', 'Katelyn', 'Lilith', 'Margot', 'Odelia', 'Ophelia', 'Victoria']

surnames = ['Annesley', 'Asquith', 'Bankes', 'Buxton', 'Cadogan', 'Calvert', 'Cootes', 'Duncombe', 'Egerton', 'Fortescue', 'Guinness', 'Harley', 'Lambton', 'Mortimer', 'Osborne', 'Paget', 'Phipps', 'Runciman', 'Stopford', 'Talbot', 'Vane-Tempest', 'Walpole']

def generateFirstName(gender):
    nameChoices = None
    if gender == "m":
        nameChoices = maleFirstNames
    else:
        nameChoices = femaleFirstNames
    name = random.choice(nameChoices)
    nameChoices.remove(name)
    return name

def generateSurname():
    surname = random.choice(surnames)
    surnames.remove(surname)
    return surname

companyAdjectives = ["Red", "Blue", "Frosty", "Docile", "Quiet", "Rampant", "Mischievious", "Quixotic"]
companyNouns = ["Solutions", "Enterprises", "Explorations", "Horses", "Vehicles", "Bridges", "Spaceflight", "Trains", "Manufacturing", "Tar"]
companyPostfixes = ["Limited", "Incorporated", "International", "Services", "Investigators", "Savants", "PLC"]

def generateCompanyName():
    adj = random.choice(companyAdjectives)
    noun = random.choice(companyNouns)
    postfix = random.choice(companyPostfixes)
    return adj + noun + postfix