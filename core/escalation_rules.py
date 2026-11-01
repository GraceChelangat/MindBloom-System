from .models import DailyCheckIn


def assess_escalation(user):
    """
    Identify configured patterns that may warrant clinician review.

    These are prototype rules, not clinically validated risk criteria.
    A qualified clinician must approve the rules before real-world use.
    """
    checkins = list(
        DailyCheckIn.objects.filter(user=user).order_by("-created_at")[:7]
    )

    if not checkins:
        return []

    reasons = []

    # Prototype rule: high stress in the three latest check-ins.
    if len(checkins) >= 3 and all(
        item.stress_level >= 4 for item in checkins[:3]
    ):
        reasons.append({
            "reason": "high_risk",
            "subject": "MindBloom: Repeated high stress reported",
            "message": (
                "The user's three latest check-ins report high stress. "
                "Please review the available information and determine "
                "whether follow-up is appropriate."
            ),
        })

    # Prototype rule: a sustained decline in mood.
    if len(checkins) >= 6:
        recent_mood = sum(item.mood_level for item in checkins[:3]) / 3
        previous_mood = sum(item.mood_level for item in checkins[3:6]) / 3

        if recent_mood <= previous_mood - 1:
            reasons.append({
                "reason": "worsening_condition",
                "subject": "MindBloom: Change in recent mood reports",
                "message": (
                    "The average mood rating across the three latest "
                    "check-ins is at least one point lower than the "
                    "preceding three. Please review the trend and decide "
                    "whether follow-up is appropriate."
                ),
            })

    return reasons