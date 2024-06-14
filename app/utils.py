from app.models import Contact, SpamReport
from sqlalchemy import or_


def search_by_name(query):
    results = []
    if query:
        contacts = Contact.query.filter(
            or_(Contact.name.like(f"{query}%"), Contact.name.like(f"%{query}%"))
        ).all()
        for contact in contacts:
            spam_reports = SpamReport.query.filter_by(
                phone_number=contact.phone_number
            ).count()
            results.append(
                {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_reports": spam_reports,
                }
            )
    return results


def search_by_phone(phone_number):
    results = []
    if phone_number:
        contacts = Contact.query.filter_by(phone_number=phone_number).all()
        for contact in contacts:
            spam_reports = SpamReport.query.filter_by(
                phone_number=contact.phone_number
            ).count()
            results.append(
                {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_reports": spam_reports,
                }
            )
    return results
