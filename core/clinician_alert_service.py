from django.core.mail import send_mail
from django.utils import timezone

from .models import ClinicianEscalation


def send_clinician_escalation(user, reason, subject, message):
    """
    Record an escalation and email the user's assigned clinician.

    This service sends notifications only when a clinician is assigned
    and active. It does not determine clinical risk itself.
    """

    profile = getattr(user, "teenager_profile", None)

    if not profile or not profile.assigned_clinician:
        return None

    clinician = profile.assigned_clinician

    if not clinician.is_active or not clinician.email:
        return None

    escalation = ClinicianEscalation.objects.create(
        user=user,
        clinician=clinician,
        reason=reason,
        subject=subject,
        message=message,
        status="pending",
    )

    email_message = (
        f"MindBloom clinician notification\n\n"
        f"Reason: {escalation.get_reason_display()}\n"
        f"User: {user.username}\n"
        f"Date: {timezone.localtime(escalation.created_at)}\n\n"
        f"Message:\n{message}\n\n"
        "Please sign in to the MindBloom system to review this notification "
        "according to your established care and escalation procedures."
    )

    try:
        send_mail(
            subject=subject,
            message=email_message,
            from_email=None,
            recipient_list=[clinician.email],
            fail_silently=False,
        )

        escalation.status = "sent"
        escalation.email_sent_at = timezone.now()
        escalation.save(update_fields=["status", "email_sent_at"])

    except Exception:
        escalation.status = "failed"
        escalation.save(update_fields=["status"])

    return escalation

from datetime import timedelta

from django.utils import timezone

from .escalation_rules import assess_escalation


def process_user_escalations(user):
    """
    Evaluate the user's recent check-ins and send eligible
    clinician notifications without duplicating recent alerts.
    """
    results = []

    for item in assess_escalation(user):
        already_exists = ClinicianEscalation.objects.filter(
            user=user,
            reason=item["reason"],
            created_at__gte=timezone.now() - timedelta(hours=24),
        ).exists()

        if already_exists:
            continue

        escalation = send_clinician_escalation(
            user=user,
            reason=item["reason"],
            subject=item["subject"],
            message=item["message"],
        )

        if escalation:
            results.append(escalation)

    return results