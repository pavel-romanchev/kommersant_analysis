from json import load

class Article:
    """Represents a newspaper article"""
    parent_issue: Issue  # link to an Issue object, which represents a singular issue of the newspaper
    parent_section: Section  # link to a Section object, which represents a large thematic section of the newspaper, such as "News", "Culture" etc
    parent_page: Page  # link to a Page object, which represents a singular page of the newspaper Issue

    rubric: str  # name of a rubric, which this article belongs to
    volume: int  # amount of symbols in the article.
    heading: str  # article's heading
    author: None|str  # article's author
    is_column: True|False  # whether the article is an author's column or not

    def __init__(self, issue, section, page, rubric, volume, heading, author=None, is_column=False):
        self.parent_issue = issue
        self.parent_section = section
        self.parent_page = page

        self.rubric = rubric

        self.volume = volume
        self.heading = heading
        author = author
        is_column = is_column


class Page:
    """Represents a page of a newspaper issue"""
    # Links to parent objects
    parent_issue: Issue
    parent_thematic_section: Section

    # Private data
    page_number: int

    # Contains
    articles_on_page: list[Article]

    def __init__(self, parent_issue: Issue, parent_thematic_section: Section, page_number: int, articles_on_page: list[Article]):
        self.parent_issue = parent_issue
        self.parent_thematic_section = parent_thematic_section

        self.number = int(page_number)
        self.articles_on_page = articles_on_page

    def __str__(self):
        return str(f"Страница {self.number}")

    def __repr__(self):
        return f"Page({self.number})"

class Section:
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
        return f"Section({self.name}, {self.pages})"

    def __repr__(self):
        return f"Section({self.name}, {self.pages})"

    def __getitem__(self, key: int):
        for page in self.pages:
            if page.number == key:
                return page

    def __iter__(self):
        return iter(self.pages)

class Issue:
    filename: str
    thematic_sections: list[Section[Page]]

    def __init__(self, filename: str):
        # Saving source filename
        self.filename = filename

        # Loading data from JSON
        issue_data = self.load_issue_data_from_json()

        # Defining thematic sections
        self.thematic_sections = []
        for thematic_section_name, pages in issue_data.items():
            thematic_section = Section(parent_issue=self, name=thematic_section_name)

            # Defining pages
            for page_number, rubrics in pages.items():
                page = Page(
                    parent_issue=self
                    parent_thematic_section=thematic_section, 
                    page_number=page_number,
                    articles_on_page=...
                )

                thematic_section.append(page)

            self.thematic_sections.append(thematic_section)

    def __repr__(self):
        return f"Issue({self.filename})"

    def __getitem__(self, key: str|int) -> Section|Page: 
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

    def count_rubric_occurences(structure: dict[dict[str:list]]) -> dict[str:int]:
        """Counts how many times each rubric occurs within the entire paper"""

        pages: dict[list]  # keys are page numbers, values are rubrics lists
        rubrics_count: dict[str: int] = {}  # result

        for page in structure.values():
            
            rubrics: list

            for rubrics in page.values():

                for rubric in rubrics:
                    if rubric in rubrics_count:
                        rubrics_count[rubric] += 1
                    else:
                        rubrics_count[rubric] = 1

        return rubrics_count

    def load_issue_data_from_json(self) -> dict[str:dict[str:list]]:
            with open(self.filename, "r", encoding="utf-8") as file:
                issue_structure = load(file)
            return issue_structure

    def get_wandering_rubrics(rubric_occurences: dict):
        """Returns only those rubrics that wander from page to page"""
        wandering_rubrics = []
        for rubric, count in rubric_occurences.items():
            if count > 1:
                wandering_rubrics.append(rubric)
        print(f"Wandering_rubrics: {wandering_rubrics}")
        return wandering_rubrics