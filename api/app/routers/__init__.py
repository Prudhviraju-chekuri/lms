from app.routers import healthchecks, courses

# Expose all routers in one place
all_routers = [
    ("/", healthchecks.router),
    ("/courses", courses.router),
]
