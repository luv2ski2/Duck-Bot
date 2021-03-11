
# Basic class for users
class User:
    def __init__(self, name, ducks):
        self.name = name
        self.timesDucked = ducks
    def formatReturn(self):
        return f'{self.name}-{self.timesDucked}'

# Checks if there's a user with name in the supplied list, returns the index if it's there
# String if it's not there
def inUserList(name, list):
    for i in range(len(list)):
        if list[i].name == name:
            return i
    return "no user with that name"

# Returns a list of users from "ducks.txt"
def getInfo():
    f = open("ducks.txt", "r")
    returnUsers = []
    users = f.read().split("|")
    # print(users)
    # if len(users) > 0:
    if users != ['']:
        for person in users:
            attributes = person.split("-")
            returnUsers.append(User(attributes[0], attributes[1]))
    f.close()
    return returnUsers

# Writes a list of users in a formated way to the file "ducks.txt"
def writeInfo(users):
    f = open("ducks.txt", "w")
    returnUsers = ""
    for person in users:
        returnUsers = returnUsers + person.formatReturn()
        if person != users[len(users) - 1]:
            returnUsers = returnUsers + "|"

    f.write(returnUsers)
    f.close()

# Main, used for testing
if __name__ == "__main__":
    james = User("james", 0)

    ian = User("ian", 0)

    users = []
    users.append(james)
    users.append(ian)
    writeInfo(users)
    print(getInfo())

# Txt file structure:
# name-numberOfDucks|name-numberOfDucks