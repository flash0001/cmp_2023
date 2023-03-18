from .database import get_races


class SharedContext:

    @property
    def races_table(self):
        return get_races()

    @property
    def races_table_data(self):
        data = self.races_table
        print(data)
        return [{
                "race_type": " ".join(rec["race_type"].split("_")),
                "drivers": rec["drivers"],
                "started_at": rec["started_at"].split(".")[0],
                "finished_at": rec["finished_at"].split(".")[0],
                "telemetry": rec["telemetry"][:40] + "...",
                } for rec in data]


shared_context = SharedContext()
