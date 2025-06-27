class Task:
    def __init__(self, id, title, description, priority, effort_hours, status, assigned_to, category=None, risk_analysis=None, risk_mitigation=None):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.effort_hours = effort_hours
        self.status = status
        self.assigned_to = assigned_to
        self.category = category
        self.risk_analysis = risk_analysis
        self.risk_mitigation = risk_mitigation

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": self.effort_hours,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "category": self.category,
            "risk_analysis": self.risk_analysis,
            "risk_mitigation": self.risk_mitigation
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["id"],
            data["title"],
            data["description"],
            data["priority"],
            data["effort_hours"],
            data["status"],
            data["assigned_to"],
            data.get("category"),
            data.get("risk_analysis"),
            data.get("risk_mitigation")
        )