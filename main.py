from newspaper import Issue

generalised_issue = Issue("generalised-structure.json")

new_issue = generalised_issue.get_wandering_rubrics()

print(generalised_issue, new_issue)


