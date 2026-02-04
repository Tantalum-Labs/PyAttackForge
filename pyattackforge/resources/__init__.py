"""Resource modules."""

from .assets import AssetsResource
from .projects import ProjectsResource
from .groups import GroupsResource
from .findings import FindingsResource
from .writeups import WriteupsResource
from .testcases import TestcasesResource
from .testsuites import TestsuitesResource
from .notes import NotesResource
from .users import UsersResource
from .reports import ReportsResource

__all__ = [
    "AssetsResource",
    "ProjectsResource",
    "GroupsResource",
    "FindingsResource",
    "WriteupsResource",
    "TestcasesResource",
    "TestsuitesResource",
    "NotesResource",
    "UsersResource",
    "ReportsResource",
]
