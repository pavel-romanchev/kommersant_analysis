from json import load

class Page:
    parent_thematic_section: ThematicSection
    number: int
    rubrics: list[str]

    def __init__(self, parent_thematic_section: ThematicSection, page_number: int, rubrics: list[str]):
        self.parent_thematic_section = parent_thematic_section
        self.number = int(page_number)
        self.rubrics = rubrics

    def __str__(self):
        return str(f"Страница {self.number}")

    def __repr__(self):
        return f"Page({self.number})"

class ThematicSection:
    parent_issue: Issue
    name: str
    pages = list[Page]

    def __init__(self, parent_issue: Issue, name: str, pages: list[Page] = None):
        self.parent_issue = parent_issue
        self.name = name
        if pages is None:
            self.pages = []
        else:
            self.pages = pages

    def append(self, page: Page):
        self.pages.append(page)

    def __str__(self):
        return f"ThematicSection({self.name}, {self.pages})"

    def __repr__(self):
        return f"ThematicSection({self.name}, {self.pages})"

    def __getitem__(self, key: int):
        for page in self.pages:
            if page.number == key:
                return page

    def __iter__(self):
        return iter(self.pages)

class Issue:
    filename: str
    thematic_sections: list[ThematicSection[Page]]
    load_issue_data_from_json: function

    def load_issue_data_from_json(self) -> dict[str:dict[str:list]]:
        with open(self.filename, "r", encoding="utf-8") as file:
            issue_structure = load(file)
        return issue_structure

    def __init__(self, filename: str):
        # Saving source filename
        self.filename = filename

        # Loading data from JSON
        issue_data = self.load_issue_data_from_json()

        # Defining thematic sections
        self.thematic_sections = []
        for thematic_section_name, pages in issue_data.items():
            thematic_section = ThematicSection(parent_issue=self, name=thematic_section_name)

            # Defining pages
            for page_number, rubrics in pages.items():
                page = Page(
                    parent_thematic_section=thematic_section, 
                    page_number=page_number,
                    rubrics=rubrics
                )

                thematic_section.append(page)

            self.thematic_sections.append(thematic_section)

    def __repr__(self):
        return f"Issue({self.filename})"

    def __getitem__(self, key: str|int) -> ThematicSection|Page: 
        if isinstance(key, str):
            for section in self.thematic_sections:
                if section.name == key: 
                    return section
            raise KeyError
        elif isinstance(key, int):
            for section in self.thematic_sections:
                for page in section:
                    if page.number == key:
                        return page
        raise TypeError