from enum import Enum


class SearchBy(Enum):
    TITLE = "title"
    TAGS = "tags"


class SortBy(Enum):
    TAGS = "tags"
    CREATED_AT = "created_at"
    MODIFIED_AT = "modified_at"


class SortOrder(Enum):
    ASC = "ascending"
    DESC = "descending"
