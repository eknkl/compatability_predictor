import json

'''Convert input of team and applicant information in JSON into a Python dict'''
def convert_to_dict(json_input):
    x = json.loads(json_input)
    team = x["team"]
    apps = x["applicants"]
    return team, apps

'''Calculate the average score of each attribute for members of the team'''
def calculate_avg_team_scores(team):
    atts = list(team[0]["attributes"].keys())
    att_values = {att : 0 for att in atts}
    for att in atts:
        for person in team:
            att_values[att] = att_values[att] + person["attributes"][att]
        att_values[att] = (att_values[att])/(len(team))
    return att_values
    
'''Score applicants based on how their attributes compare to average team attributes'''
def score_apps(applicant_info, avg_team_scores):
    applicant_names = [app["name"] for app in applicant_info]
    scored_applicants = {app : 0 for app in applicant_names}
    for app in applicant_info:
        sum_score = 0
        for att_name, value in app["attributes"].items():
            diff = abs(avg_team_scores[att_name] - value)
            sum_score += 1 - (diff/avg_team_scores[att_name])
        score = sum_score / len(avg_team_scores)
        scored_applicants[app["name"]] = round(score, 1)
    return scored_applicants

'''Convert applicant scores into JSON from a Python dict'''
def process_scores(raw_scores):
    scored_apps = { "scoredApplicants" : [ {"name" : x, "score" : y} for x, y in raw_scores.items()]}
    scored_apps_json = json.dumps(scored_apps)
    return scored_apps_json


if __name__ == "__main__":
    json_file = input("Please input the JSON filename (e.g. input.json): ")
    with open(json_file, "r") as user_file:
        contents = user_file.read()
        team, apps = convert_to_dict(contents)
    
    avg_team_scores = calculate_avg_team_scores(team)
    raw_scores = score_apps(apps, avg_team_scores)
    json_scores = process_scores(raw_scores)

    with open("json_output.json", "w") as json_output:
        json_output.write(json_scores)