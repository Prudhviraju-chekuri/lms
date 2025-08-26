from app.routers import healthchecks
from app.routers import courses

all_routers = [
    ("", healthchecks.router),
    ("/courses", courses.router),
]
