import re
import openai
import environ
import django.db
import pandas as pd
from django.http import JsonResponse

env = environ.Env()
environ.Env.read_env()

# openai api key
api_key = env("OPENAI_API_KEY")
openai.api_key = api_key


def getSkills(cursor, projects, col, db, name):
    # get Technologies of each project
    for i in projects:
        arr = []
        cursor.execute(
            f"SELECT `{col}`  FROM {db} WHERE `Project.Title` = %s",
            [i["title"]],
        )
        rows = cursor.fetchall()
        for row in rows:
            arr.append(row[0])
        i[name] = arr


def home(request):
    # connect to db
    conn = django.db.connection
    cursor = conn.cursor()

    # get all projects
    cursor.execute("SELECT DISTINCT `Project.Title`  FROM projTech")
    rows = cursor.fetchall()
    projects = []
    for i in rows:
        projects.append({"title": i[0]})

    # get all skills
    getSkills(cursor, projects, "Project.Technologies", "projTech", "tech")
    getSkills(cursor, projects, "Technical_Skillset.Backend", "skillBack", "back")
    getSkills(cursor, projects, "Technical_Skillset.Databases", "skillDb", "db")
    getSkills(cursor, projects, "Technical_Skillset.Frontend", "skillFront", "front")
    getSkills(
        cursor, projects, "Technical_Skillset.Infrastructre", "skillInfra", "infra"
    )
    conn.close()
    return JsonResponse(projects, safe=False)


def singleProject(request, projId):
    newProjId = "Project " + projId
    newProjId2 = "Project " + projId + " "
    # connect to db
    conn = django.db.connection
    cursor = conn.cursor()

    # get the project requested
    cursor.execute(
        "SELECT `Project.Title` FROM projTech WHERE `Project.Title` = %s OR `Project.Title` = %s",
        [newProjId, newProjId2],
    )
    rows = cursor.fetchone()
    oneProject = []
    oneProject.append({"title": rows[0]})

    # get all skills
    getSkills(cursor, oneProject, "Project.Technologies", "projTech", "tech")
    getSkills(cursor, oneProject, "Technical_Skillset.Backend", "skillBack", "back")
    getSkills(cursor, oneProject, "Technical_Skillset.Databases", "skillDb", "db")
    getSkills(cursor, oneProject, "Technical_Skillset.Frontend", "skillFront", "front")
    getSkills(
        cursor, oneProject, "Technical_Skillset.Infrastructre", "skillInfra", "infra"
    )

    return JsonResponse(oneProject, safe=False)


def get_relevant_projects(query, dataframe):
    # create a list of descriptions for the model
    descs = []
    for index, row in dataframe.iterrows():
        description = row["Combined"]
        descs.append(description)

    # Generate a relevance score using the GPT API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Take this python list: {descs} as input and rate the relevance of projects in descending order according to the query: '{query}'. 0 means not relevant at all and 10 means very relevant. Return only the index numbers of the projects that are relevant in descending order of relevance. Do not include any text other than the index numbers.",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    indexes = response["choices"][0]["text"]
    indexes = re.sub(r"\s+", "", indexes)
    indexes = indexes.replace("[", "")
    indexes = indexes.replace("]", "")
    indexes = indexes.split(",")

    projects = []
    # return a list of relevant projects
    for ind in indexes:
        newProjId = "Project " + ind
        newProjId2 = "Project " + ind + " "
        print(newProjId)
        # connect to db
        conn = django.db.connection
        cursor = conn.cursor()

        # get the project requested
        cursor.execute(
            "SELECT `Project.Title` FROM projTech WHERE `Project.Title` = %s OR `Project.Title` = %s",
            [newProjId, newProjId2],
        )
        rows = cursor.fetchone()
        if rows != None:
            projects.append({"title": rows[0]})

    # get all skills
    getSkills(cursor, projects, "Project.Technologies", "projTech", "tech")
    getSkills(cursor, projects, "Technical_Skillset.Backend", "skillBack", "back")
    getSkills(cursor, projects, "Technical_Skillset.Databases", "skillDb", "db")
    getSkills(cursor, projects, "Technical_Skillset.Frontend", "skillFront", "front")
    getSkills(
        cursor, projects, "Technical_Skillset.Infrastructre", "skillInfra", "infra"
    )
    conn.close()
    return projects


# Function to combine columns with column names in between
def combine_columns_with_names(row):
    # Join the values from each column with the column names in between
    return ". ".join(
        [f"{col.split('.')[1]} used: {value}" for col, value in row.items()]
    )


def search_projects(request, query):
    df = pd.read_excel("projects.xlsx")
    df.fillna("None", inplace=True)

    # Apply the function to each row in the DataFrame
    df["Combined"] = df.apply(combine_columns_with_names, axis=1)

    # Display the updated DataFrame
    df.drop(df.columns[[1, 2, 3, 4, 5]], axis=1, inplace=True)

    # Replace with the user's query
    relevant_projects = get_relevant_projects(query, df.head(65))
    return JsonResponse(relevant_projects, safe=False)
