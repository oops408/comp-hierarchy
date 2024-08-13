import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Storing data for each user in dataframe.
# Each user can represent an employee from a company standpoint.
data = {
    'User_ID': [],
    'User_Name': [],
    'Group_ID': [],
    'Group_Name': [],
    'Role': []
}

df = pd.DataFrame(data)

def add_user(user_id, user_name, group_id, role, df):
    """
    Adding a user to dataframe.
    
    Parameters:
    - user_id: Unique identification for each user
    - user_name: Name of each user.
    - group_id: ID of group the user belongs to.
    - role: Role of user within group.
    - df: Dataframe to add user to.
    
    Output:
    - Updating dataframe with new user added.
    """

    # Format for new user entry
    new_user = pd.DataFrame({
        'User_ID': [user_id],
        'User_Name': [user_name],
        'Group_ID': [group_id],
        'Group_Name': [None],  # update later
        'Role': [role]
    })
    
    # concat with existing dataframe
    df = pd.concat([df, new_user], ignore_index=True)
    
    return df

def remove_user(user_id, df):
    """
    Removing a user from dataframe.
    
    Parameters:
    - user_id: Identify which user to remove.
    - df: Dataframe to remove user from.
    
    Output:
    - Updating dataframe with existing user removed.
    """
    df = df[df['User_ID'] != user_id]
    return df

def add_group(group_id, group_name, df):
    """
    Adds group to the dataframe / updating group name for existing users.
    
    Parameters:
    - group_id: Unique identifier for the group.
    - group_name: Name of the group.
    - df: DataFrame in which the group will be added.
    
    Output:
    - Updating dataframe with new group added.
    """
    # Updating group name for users in group
    df.loc[df['Group_ID'] == group_id, 'Group_Name'] = group_name
    
    return df

def remove_group(group_id, df):
    """
    Removes group / all users in group from dataframe.
    
    Parameters:
    - group_id: Identify which group to remove.
    - df: Dataframe to remove group from.
    
    Output:
    - Updating dataframe with existing group removed.
    """
    df = df[df['Group_ID'] != group_id]
    return df

def display_hierarchy(df):
    """
    Show company hierarchy (Terminal).

    Parameters:
    - df: Dataframe to display.

    Output:
    - Displays all users by group.
    """
    # group based on group name -> user name, reset index after grouping
    hierarchy = df.groupby(['Group_Name', 'User_Name'], as_index=False)['Role'].apply(lambda x: x).reset_index(drop=True)
    print(hierarchy)


def update_user_role(user_id, new_role, df):
    """
    Updating user's role in dataframe.
    
    Parameters:
    - user_id: Identify which user to update.
    - new_role: Role to assign to user.
    - df: Dataframe to update.
    
    Output:
    - Updating dataframe with new user role.
    """
    df.loc[df['User_ID'] == user_id, 'Role'] = new_role
    return df

def search_by_role(role, df):
    """
    Searching for users by role.
    
    Parameters:
    - role: The role to search for.
    - df: Dataframe to search.
    
    Output:
    - Dataframe with users matching role.
    """
    return df[df['Role'] == role]

def search_by_group(group_name, df):
    """
    Searching for users by group.
    
    Parameters:
    - group_name: The group to search for.
    - df: Dataframe to search.
    
    Output:
    - Dataframe with users matching group.
    """
    return df[df['Group_Name'] == group_name]

def export_hierarchy(df, filename):
    """
    Exporting dataframe to CSV.
    
    Parameters:
    - df: Dataframe to export.
    - filename: Name of exported file.

    Output:
    - CSV file with exported data.
    """
    df.to_csv(filename, index=False)

def import_hierarchy(filename):
    """
    Importing dataframe from CSV.
    
    Parameters:
    - filename: Name of file to import from.
    
    Output:
    - Dataframe with imported data.
    """
    df = pd.read_csv(filename)
    return df

def visualize_hierarchy(df):
    """
    Allows you to visualize the company hierarchy.
    
    Parameters:
    - df: Dataframe to pull data from.

    Output:
    - Graph of the company hierarchy split between groups.
    """
    G = nx.DiGraph()

    # create nodes
    for _, row in df.iterrows():
        group = row['Group_Name']
        user = row['User_Name']
        role = row['Role']

        if group not in G:
            G.add_node(group, size=3000)  # define group nodes (larger)
        G.add_node(user, size=1000, label=role)  # define user nodes (smaller)
        G.add_edge(group, user)
    
    # Seperating by groups
    pos = {}
    num_groups = df['Group_Name'].nunique()
    angle_step = 360 / num_groups
    radius = 5  # distance from center

    # Position groups in a circular fashion for ease of use
    group_positions = {}
    for i, group in enumerate(df['Group_Name'].unique()):
        angle = i * angle_step
        x = radius * np.cos(np.radians(angle))
        y = radius * np.sin(np.radians(angle))
        group_positions[group] = (x, y)
        pos[group] = (x, y)

    # Position users around groups.
    for group in df['Group_Name'].unique():
        users = df[df['Group_Name'] == group]['User_Name'].unique()
        angle_step_user = 360 / len(users) if len(users) > 1 else 0
        for j, user in enumerate(users):
            angle = j * angle_step_user
            x = group_positions[group][0] + 1.5 * np.cos(np.radians(angle))
            y = group_positions[group][1] + 1.5 * np.sin(np.radians(angle))
            pos[user] = (x, y)

    # Node sizes
    sizes = [G.nodes[node]['size'] for node in G.nodes]

    # Drawing graph with NetworkX
    nx.draw(G, pos, with_labels=True, node_size=sizes, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    
    # setting zoom/pan
    plt.margins(0.2)
    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.gca().autoscale_view()
    plt.show()

# Adding users.
all_users = [
    (1, 'User1', 102, 'Intern'),
    (2, 'User2', 103, 'Tester'),
    (3, 'User3', 104, 'Analyst'),
    (4, 'User4', 104, 'Intern'),
    (5, 'User5', 104, 'Manager'),
    (6, 'User6', 103, 'Tester'),
    (7, 'User7', 102, 'Tester'),
    (8, 'User8', 101, 'Analyst'),
    (9, 'User9', 102, 'Developer'),
    (10, 'User10', 105, 'Analyst'),
    (11, 'User11', 101, 'Tester'),
    (12, 'User12', 103, 'Manager'),
    (13, 'User13', 106, 'Intern'),
    (14, 'User14', 106, 'Intern'),
    (15, 'User15', 101, 'Analyst'),
    (16, 'User16', 107, 'Developer'),
    (17, 'User17', 105, 'Developer'),
    (18, 'User18', 101, 'Intern'),
    (19, 'User19', 102, 'Intern'),
    (20, 'User20', 104, 'Analyst'),
    (21, 'User21', 106, 'Developer'),
    (22, 'User22', 101, 'Analyst'),
    (23, 'User23', 103, 'Analyst'),
    (24, 'User24', 103, 'Tester'),
    (25, 'User25', 105, 'Analyst'),
    (26, 'User26', 102, 'Tester'),
    (27, 'User27', 106, 'Tester'),
    (28, 'User28', 105, 'Developer'),
    (29, 'User29', 102, 'Manager'),
    (30, 'User30', 106, 'Tester'),
    (31, 'User31', 105, 'Developer'),
    (32, 'User32', 102, 'Analyst'),
    (33, 'User33', 103, 'Developer'),
    (34, 'User34', 106, 'Developer'),
    (35, 'User35', 107, 'Analyst'),
    (36, 'User36', 107, 'Developer'),
    (37, 'User37', 107, 'Tester'),
    (38, 'User38', 105, 'Manager'),
    (39, 'User39', 102, 'Tester'),
    (40, 'User40', 106, 'Tester'),
    (41, 'User41', 101, 'Tester'),
    (42, 'User42', 103, 'Manager'),
    (43, 'User43', 106, 'Intern'),
    (44, 'User44', 106, 'Tester'),
    (45, 'User45', 104, 'Intern'),
    (46, 'User46', 107, 'Analyst'),
    (47, 'User47', 105, 'Tester'),
    (48, 'User48', 102, 'Manager'),
    (49, 'User49', 101, 'Analyst'),
    (50, 'User50', 107, 'Intern'),
]

for user_id, user_name, group_id, role in all_users:
    df = add_user(user_id, user_name, group_id, role, df)

# Adding groups.
all_groups = [
    (101, 'Engineering'),
    (102, 'Management'),
    (103, 'Human Resources'),
    (104, 'Finance'),
    (105, 'Marketing'),
    (106, 'Sales'),
    (107, 'IT Support')
]

for group_id, group_name in all_groups:
    df = add_group(group_id, group_name, df)

# Display hierarchy.
display_hierarchy(df)

# Updating user role.
df = update_user_role(1, 'Lead Developer', df)

# Searching by role.
developers = search_by_role('Developer', df)
print(developers)

# Searching by group.
engineering_team = search_by_group('Engineering', df)
print(engineering_team)

# Visualizing group hierarchy.
visualize_hierarchy(df)
