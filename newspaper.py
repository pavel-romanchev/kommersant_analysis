from json import load
from copy import deepcopy

class Article:
    """Represents a newspaper article"""
    # Links to parent objects
    parent_issue: Issue  # link to an Issue object, which represents a singular issue of the newspaper
    parent_section: Section  # link to a Section object, which represents a large thematic section of the newspaper, such as "News", "Culture" etc
    parent_page: Page  # link to a Page object, which represents a singular page of the newspaper Issue

    # Local data
    rubric: str  # name of a rubric, which this article belongs to
    volume: int  # amount of symbols in the article.
    heading: str  # article's heading
    author: None|str  # article's author
    is_column: bool  # whether the article is an author's column or not

    def __init__(self, parent_issue, parent_section, parent_page, rubric, volume=None, heading=None, author=None, is_column=None):
        self.parent_issue = parent_issue
        self.parent_section = parent_section
        self.parent_page = parent_page

        self.rubric = rubric

        self.volume = volume
        self.heading = heading
        author = author
        is_column = is_column

    def __repr__(self):   
        representative_data = self.heading
        if self.heading is None:
            representative_data = self.rubric
        return f'Article({representative_data})'


class Page:
    """Represents a page of a newspaper issue"""

    # Links to parent objects
    parent_issue: Issue
    parent_thematic_section: Section

    # Local data
    number: int
    articles_on_page: list[Article]

    def __init__(self, parent_issue: Issue, parent_thematic_section: Section, page_number: int, articles_on_page: list[Article]):
        self.parent_issue = parent_issue
        self.parent_thematic_section = parent_thematic_section

        self.number = int(page_number)

        # Defining articles on page
        self.articles_on_page = []
        for rubric in articles_on_page:
            self.articles_on_page.append(Article(parent_issue, parent_thematic_section, self, rubric=rubric))

    def __repr__(self):
        return f"Page({self.number})"

    def __getitem__(self, article_index):
        return self.articles_on_page[article_index]

    def get_article(self, article_index: int = None):
        if article_index is None:
            return self.articles_on_page
        return self.articles_on_page[article_index]


class Section:
    # Links to parent objects
    parent_issue: Issue

    # Local data
    name: str
    pages_in_section = list[Page] | list

    def __init__(self, parent_issue: Issue, name: str, pages_in_section: list[Page] | list):
        self.parent_issue = parent_issue
        self.name = name

        if pages_in_section:
            # Adding pages to section
            self.pages_in_section = []
            for page_number, articles_on_page in pages_in_section:
                self.pages_in_section.append(Page(parent_issue, self, page_number, articles_on_page))

    def append(self, page: Page):
        self.pages.append(page)

    def __str__(self):
        return f"Section({self.name}, {self.pages_in_section})"

    def __repr__(self):
        return f'Section("{self.name}")'

    def __getitem__(self, page_index: int = None):
        if page_index is None:
            return self.pages_in_section
        elif isinstance(page_index, int):
            return self.pages_in_section[page_index]
        raise TypeError("Page index must be int")

    def __iter__(self):
        return iter(self.pages_in_section)

    def get_page(self, page_number: int = None) -> Page:
        if page_number is None:
            return self.pages_in_section
        elif isinstance(page_number, int):
            for page in self.pages_in_section:
                if page.number == page_number:
                    return page
        raise KeyError("No page with this number. Might try search with index via page[index: int]")

class Issue:
    _source_file_name: str | None
    _sections: list[Section[Page]] | list

    def __init__(self, source_file_name: str = None):
        self._sections = []
        self._source_file_name = source_file_name
        
        if source_file_name is not None:
            # Loading data from JSON
            issue_data: dict[str:dict[str:list]] = self.from_json(self._source_file_name)

            # Defining child thematic section
            for section_name, pages_in_section in issue_data.items():
                self._sections.append(Section(self, section_name, pages_in_section))

    def from_json(self, filename) -> dict[str:dict[str:list]]:
        with open(filename, "r", encoding="utf-8") as file:
            issue_data = load(file)

        return issue_data

    def append_article(self, article: Article):
        if article.parent_section not in self._sections:  
            self._sections.append(article.parent_section)

    def append_section(self, section: Section):
        self._sections.append(section)

    def __repr__(self):
        if self._source_file_name is not None:
            return f'Issue("{self._source_file_name}")'
        return f'Issue({self._sections})'

    def __getitem__(self, key: str|int) -> Section|Page: 
        if isinstance(key, str):
            for section in self._sections:
                if section.name == key: 
                    return section
            raise KeyError("There is no sections with such name")
        
        elif isinstance(key, int):
            for section in self._sections:
                for page in section:
                    if page.number == key:
                        return page
            raise KeyError("There is no section with this number")
        
        raise TypeError("A section id must be str or int")

    def __iter__(self):
        return iter(self._sections)

    def get_section(self, section_name: str = None) -> list[Section]:
        if section_name is None:
            return self._sections
        return self[section_name]

    def get_pages(self) -> list[Page]:
        pages = []
        for section in self._sections: 
            pages.extend(section.pages_in_section)
        return pages

    def get_articles(self) -> list[Article]:
        articles = []
        for page in self.get_pages():
            articles.extend(page.articles_on_page)
        return articles

    def get_rubric_occurences(self):
        articles: list[Article] = self.get_articles()

        rubric_occurences: dict[str: set[Page]] = dict()

        for article in articles:
            if article.rubric not in rubric_occurences:
                rubric_occurences[article.rubric] = set()
            rubric_occurences[article.rubric].add(article.parent_page)

        return rubric_occurences

    def get_wandering_rubrics(self) -> list[str]:
        rubric_occurences = self.get_rubric_occurences()
        wandering_rubrics = []
        for rubric in rubric_occurences:
            if len(rubric_occurences[rubric]) > 1:
                wandering_rubrics.append(rubric)
        return wandering_rubrics

    def without_wandering_rubrics(self) -> Issue:
        # wandering_rubrics = self.get_wandering_rubrics()

        # new_issue = Issue()

        # for section in self._sections:
        #     new_section = Section(
        #         parent_issue=new_issue,

        #         name=section.name,
        #         pages_in_section=[]
        #     )

        #     for page in section:
        #         new_page = Page(
        #             parent_issue=new_issue,
        #             parent_thematic_section=new_section,

        #             page_number=page.page_number,
        #             articles_on_page=[]
        #         )

        #         for article in page:
        #             if article.rubric not in wandering_rubrics:
        #                 new_article = Article(
        #                     parent_issue=new_issue,
        #                     parent_section=new_section,
        #                     parent_page=new_page,

        #                     rubric=article.rubric,
        #                     volume=article.volume,
        #                     heading=article.heading,
        #                     author=article.author,
        #                     is_column=article.is_column
        #                 )


        # return new_issue

        new_issue = deepcopy(self)

        return new_issue

        
        
        
