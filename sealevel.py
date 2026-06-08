import json
from pathlib import Path

from projects.common import Project

PEOPLE_UNDER = Path(__file__).parent / "static" / "people_under.json"


class SeaLevel(Project):
    def __init__(self, id, name, description, **kwargs):
        super().__init__(id, name, description, **kwargs)

        def process(rec):
            key, val = rec
            if key.startswith("-"):
                ext = ""
                label = "Current state"
            else:
                ext = "_" + str(key)
                label = "+ %s m - %s million below" % (max(int(key), 0), int(val))

            return {
                "depth": max(int(key), 0),
                "at_risk": float(val),
                "path": "/static/projects/sealevel/elevation%s.png" % ext,
                "thumb": "/static/projects/sealevel/elevation_thumb%s.jpg" % ext,
                "label": label,
            }

        self.people_under = sorted(
            (process(rec) for rec in json.load(open(PEOPLE_UNDER)).items()),
            key=lambda r: r["depth"],
        )

    def fill_dict(self, request, d):
        d["people_under"] = self.people_under
