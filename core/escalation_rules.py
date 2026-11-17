from .models import ClinicianEscalation, DailyCheckIn

# Prototype thresholds. A qualified clinician must approve these
# before real-world use.
HIGH_STRESS_LEVEL = 3     # stress at or above this counts as high
HIGH_STRESS_COUNT = 3      # consecutive high-stress check-ins needed
LOW_MOOD_LEVEL = 3         # mood at or below this counts as low
LOW_MOOD_COUNT = 3         # consecutive low-mood check-ins needed
MOOD_DROP = 1              # drop in average mood between two blocks
MOOD_BLOCK = 3             # check-ins per block for the trend rule

STRESS_SUBJECT = "MindBloom: Repeated high stress reported"
LOW_MOOD_SUBJECT = "MindBloom: Repeated low mood reported"
TREND_SUBJECT = "MindBloom: Change in recent mood reports"


def _last_escalation_time(user, subject):
    """Time of the last non-failed escalation for this rule, or None."""
    return (
        ClinicianEscalation.objects.filter(user=user, subject=subject)
        .exclude(status="failed")
        .order_by("-created_at")
        .values_list("created_at", flat=True)
        .first()
    )


def _all_new(checkins, since):
    """True if every check-in was submitted after the last escalation."""
    return since is None or all(c.created_at > since for c in checkins)


def assess_escalation(user):
    """
    Identify check-in patterns that may warrant clinician review.

    Rules are based on the number of check-ins, not on days. After a
    rule has triggered an email, it needs a fresh run of new check-ins
    before it can trigger another.

    These are prototype rules, not clinically validated risk criteria.
    """
    needed = max(HIGH_STRESS_COUNT, LOW_MOOD_COUNT, MOOD_BLOCK * 2)
    checkins = list(
        DailyCheckIn.objects.filter(user=user).order_by("-created_at")[:needed]
    )

    if not checkins:
        return []

    reasons = []

    # Rule 1: consecutive high-stress check-ins.
    latest = checkins[:HIGH_STRESS_COUNT]
    if len(latest) == HIGH_STRESS_COUNT and all(
        c.stress_level >= HIGH_STRESS_LEVEL for c in latest
    ):
        since = _last_escalation_time(user, STRESS_SUBJECT)
        if _all_new(latest, since):
            reasons.append({
                "reason": "high_risk",
                "subject": STRESS_SUBJECT,
                "message": (
                    f"The user's {HIGH_STRESS_COUNT} latest check-ins report "
                    "high stress. Please review the available information "
                    "and determine whether follow-up is appropriate."
                ),
            })

    # Rule 2: consecutive low-mood check-ins.
    latest = checkins[:LOW_MOOD_COUNT]
    if len(latest) == LOW_MOOD_COUNT and all(
        c.mood_level <= LOW_MOOD_LEVEL for c in latest
    ):
        since = _last_escalation_time(user, LOW_MOOD_SUBJECT)
        if _all_new(latest, since):
            reasons.append({
                "reason": "high_risk",
                "subject": LOW_MOOD_SUBJECT,
                "message": (
                    f"The user's {LOW_MOOD_COUNT} latest check-ins report "
                    "low mood. Please review the available information "
                    "and determine whether follow-up is appropriate."
                ),
            })

    # Rule 3: mood decline between two blocks of check-ins.
    block = MOOD_BLOCK * 2
    latest = checkins[:block]
    if len(latest) == block:
        recent = sum(c.mood_level for c in latest[:MOOD_BLOCK]) / MOOD_BLOCK
        previous = sum(c.mood_level for c in latest[MOOD_BLOCK:]) / MOOD_BLOCK

        if recent <= previous - MOOD_DROP:
            since = _last_escalation_time(user, TREND_SUBJECT)
            if _all_new(latest, since):
                reasons.append({
                    "reason": "worsening_condition",
                    "subject": TREND_SUBJECT,
                    "message": (
                        f"The average mood across the {MOOD_BLOCK} latest "
                        f"check-ins is at least {MOOD_DROP} point lower than "
                        f"the preceding {MOOD_BLOCK}. Please review the trend "
                        "and decide whether follow-up is appropriate."
                    ),
                })

    return reasons