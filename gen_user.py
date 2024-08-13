import random

# Function to generate random users (testing).
def generate_user_data(user_start, num_users):
    roles = ['Developer', 'Manager', 'Analyst', 'Tester', 'Intern'] # update if needed
    departments = [101, 102, 103, 104, 105, 106, 107] # update if needed
    users = []

    for i in range(user_start, user_start + num_users):
        name = f'User{i}'
        department = random.choice(departments)
        role = random.choice(roles)
        users.append((i, name, department, role))
    
    return users

new_users = generate_user_data(user_start = 1, num_users = 50) # update what user_id to start at and how many users to generate. All users are formatted correctly.
for i, user in enumerate(new_users):
    if i == len(new_users) - 1:
        print(f"{user}")
    else:
        print(f"{user},")