from apps.contactbook.models import ContactLabel
from apps.label.models import Label


class ContactBookService:
    @staticmethod
    def add_label(instance, labels: list[int], bulk=False):
        exist_labels = (
            Label.objects.owner(instance.owner)
            .filter(id__in=labels)
            .values_list("id", flat=True)
        )
        already_labels = instance.labels.values_list("id", flat=True)
        add_labels = set(exist_labels) - set(already_labels)
        add_items = [
            ContactLabel(contact=instance, label_id=label_id)
            for label_id in add_labels
        ]
        if add_items:
            ContactLabel.objects.bulk_create(add_items)
            instance.refresh_from_db()

    @staticmethod
    def get_labels(
        request_labels: list[dict],
    ) -> list[int]:
        results = []
        for request_label in request_labels:
            if not request_label:
                continue
            results.append(request_label["id"])
        return results


contact_book_service = ContactBookService()
