from django.core.mail import send_mail
from django.utils import timezone

from .escalation_rules import assess_escalation
from .models import ClinicianEscalation

def send_clinician_escalation(user, reason, subject, message):
    """
    Record an escalation and email the clinician address the user
    provided on their profile (clinician_email). Falls back to an
    assigned clinician profile if one exists.

    This service does not determine clinical risk itself.
    """

    profile = getattr(user, "teenager_profile", None)

    if not profile:
        return None

    clinician = getattr(profile, "assigned_clinician", None)

    recipient = (getattr(profile, "clinician_email", "") or "").strip()

    if not recipient and clinician and clinician.is_active:
        recipient = (clinician.email or "").strip()

    if not recipient:
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
        "MindBloom clinician notification\n\n"
        f"Reason: {escalation.get_reason_display()}\n"
        f"User: {user.username}\n"
        f"Date: {timezone.localtime(escalation.created_at)}\n\n"
        f"Message:\n{message}\n\n"
        "Please review this notification according to your established "
        "care and escalation procedures."
    )

    try:
        send_mail(
            subject=subject,
            message=email_message,
            from_email=None,
            recipient_list=[recipient],
            fail_silently=False,
        )

        escalation.status = "sent"
        escalation.email_sent_at = timezone.now()
        escalation.save(update_fields=["status", "email_sent_at"])

    except Exception:
        escalation.status = "failed"
        escalation.save(update_fields=["status"])

    return escalation

def process_user_escalations(user):
    """
    Evaluate the user's check-ins and send eligible clinician
    notifications. Repeat emails are prevented by the rules themselves,
    which need new check-ins after each escalation.
    """
    results = []

    for item in assess_escalation(user):
        escalation = send_clinician_escalation(
            user=user,
            reason=item["reason"],
            subject=item["subject"],
            message=item["message"],
        )

        if escalation:
            results.append(escalation)

    return results