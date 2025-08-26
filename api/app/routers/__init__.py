from . import healthchecks
from . import courses

all_routers = [
    ("", healthchecks.router),
    ("/courses", courses.router),
]
