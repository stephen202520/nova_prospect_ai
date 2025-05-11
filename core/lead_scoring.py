# core/lead_scoring.py

class LeadScorer:
    def __init__(self):
        pass

    def score_lead(self, lead):
        score = 0
        if lead.get("industry") in ["Technology", "Finance"]:
            score += 20
        if lead.get("position") in ["CEO", "CTO", "CFO"]:
            score += 30
        if lead.get("company_size", 0) > 100:
            score += 10
        return score