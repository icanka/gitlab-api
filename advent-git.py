import time

import gitlab

import random_password_generator
from users import users

gl = gitlab.Gitlab(
    "https://gitlab", private_token="L-KCy7SXKCbKh6oef6Pa", ssl_verify=False
)
gl = gitlab.Gitlab(
    "https://gitlab",
    private_token="L-KCy7SXKCbKh6oef6Pa",
    user_agent="advent-agent",
    ssl_verify=False,
)
gl.auth()

# projects = gl.projects.list()
# for project in projects:
#    print(project)
#    print(type(project))

pg = random_password_generator.password_generator(password_length=8)
password = pg.generate()
# user_data = {'email': 'jen@foo.com', 'username': 'jen', 'name': 'Jen', 'reset_password': False, 'password': password}

print(
    "##################################################################################################################################################################"
)

start_time = time.time()
gl_users = gl.users.list()
for user in gl_users:
    print(user.username + ": " + str(user.is_admin))
# print(type(gl_users))
# print("--- %s seconds ---" % (time.time() - start_time))
# print(gl_users)
# for user in users:

# print(gl.users.delete(39))

# test = gl.users.list(username='nsdc181')
test = gl.users.list(admin=True)
print("ADMIN USERS:")
print(test)

for user_data in users:
    # print(user_data['username'])
    is_gl_user = gl.users.list(search=user_data["username"])
    if not is_gl_user:
        print(
            user_data["username"] + " is not registered in Gitlab. Generating user..."
        )

        user_data["password"] = pg.generate()
        created_user = gl.users.create(user_data)
        print(type(created_user))
        print(created_user.password)
    else:
        print(user_data["username"] + " is already a gitlab user.")
        print("User ID: " + str(is_gl_user[0].id))

print(
    "##################################################################################################################################################################"
)

for user_data in users:
    password = pg.generate()
    user_data["password"] = password
    user_data["can_create_group"] = False
    user_data["can_create_project"] = False
    user_data["projects_limit"] = 10
    # created_user = gl.users.create(user_data)
    # print(created_user)

# print(gl.projects.get_create_attrs())

# user = gl.users.create(user_data)
# print(user)
