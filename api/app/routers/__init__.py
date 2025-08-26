from . import health_checks
from . import courses

all_routers = [
    ("/health", health_checks.router),
    ("/courses", courses.router),
]
