users = (
    {
        "username": "nsdc181",
        "name": "İzzet Can Karakuş",
        "email": "83716289362@armend.local",
    },
    {
        "username": "nsdc180",
        "name": "Bünyamin Aktaş",
        "email": "91827356416@armend.local",
    },
    {
        "username": "nsdc179",
        "name": "Emre Karagöz",
        "email": "72549182742@armend.local",
    },
)

print(type(users))
print(users)

for item in users:
    print(type(item))
    print(item)
    print(item["username"])
