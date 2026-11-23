from newspaper import Issue

issue = Issue("structure.json")

# import json

# def get_paper_structure() -> dict[dict[str:list]]:
#     """Returns JSON file with the structure of the Kommersant newspaper"""

#     with open("structure.json", "r", encoding="utf-8") as file:
#             structure = json.load(file)

#     return structure

# def count_rubric_occurences(structure: dict[dict[str:list]]) -> dict[str:int]:
#     """Counts how many times each rubric occurs within the entire paper"""

#     pages: dict[list]  # keys are page numbers, values are rubrics lists
#     rubrics_count: dict[str: int] = {}  # result

#     for page in structure.values():
        
#         rubrics: list

#         for rubrics in page.values():

#             for rubric in rubrics:
#                 if rubric in rubrics_count:
#                     rubrics_count[rubric] += 1
#                 else:
#                     rubrics_count[rubric] = 1

#     return rubrics_count

# def get_wandering_rubrics(rubric_occurences: dict):
#     """Returns only those rubrics that wander from page to page"""
#     wandering_rubrics = []
#     for rubric, count in rubric_occurences.items():
#         if count > 1:
#             wandering_rubrics.append(rubric)
#     print(f"Wandering_rubrics: {wandering_rubrics}")
#     return wandering_rubrics

# def update_sctructure_exluding_wandering_rubrics(
#         structure: dict[dict[str:list]],
#         wandering_rubrics: list[str]
# ) -> dict[dict[str:list]]:
#     """Returns new dictionary that reflects paper structure with exluded wandering rubrics"""

#     updated_structure: dict[dict[str:list]] = {}

#     for theme, pages in structure.items():
#         updated_structure.setdefault(theme, {})

#         for page, rubrics in pages.items():
#             updated_structure[theme].setdefault(page, [])

#             for rubric in rubrics:
#                 if rubric in wandering_rubrics:
#                     continue

#                 updated_structure[theme][page].append(rubric)

#     return updated_structure

# def write_new_structure(new_structure):
#     """Writes new structure into new JSON"""

#     with open("new_structure.json", "w", encoding="utf-8") as file:
#         json.dump(new_structure, file, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
#     structure = get_paper_structure()
#     rubric_occurences = count_rubric_occurences(structure)
#     wandering_rubrics = get_wandering_rubrics(rubric_occurences)
#     new_structure = update_sctructure_exluding_wandering_rubrics(structure, wandering_rubrics)

#     write_new_structure(new_structure)