class AlredyApplied(Exception):
    def __str__(self):
        return "Project already Applied"


class ProjectNotActive(Exception):
    def __str__(self):
        return "Project Not active any more"
