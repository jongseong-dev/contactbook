import pytest
from pytest_django.asserts import assertNumQueries

from apps.contactbook.models import ContactBook


@pytest.mark.django_db
def test_ContactBook_OWNER_N_PLUS_1_문제_해결(user_contact_book):
    with assertNumQueries(1):
        contactbooks = ContactBook.objects.select_related("owner").all()
        for contactbook in contactbooks:
            contactbook.owner


@pytest.mark.django_db
def test_ContactBook_OWNER_N_PLUS_1_문제_발생(user_contact_book):
    with assertNumQueries(2):
        contactbooks = ContactBook.objects.all()
        for contactbook in contactbooks:
            contactbook.owner


@pytest.mark.django_db
def test_ContactBook_LABELS_N_PLUS_1_문제_해결(contact_labels):
    with assertNumQueries(2):
        contactbooks = ContactBook.objects.prefetch_related("labels").all()
        for contactbook in contactbooks:
            list(contactbook.labels.all())


@pytest.mark.django_db
def test_ContactBook_LABELS_N_PLUS_1_문제_발생(contact_labels):
    with assertNumQueries(11):
        contactbooks = ContactBook.objects.all()
        for contactbook in contactbooks:
            list(contactbook.labels.all())
