# Generated by Django 4.2.14 on 2024-08-07 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("label", "0001_initial"),
        ("contactbook", "0003_alter_contactlabel_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactbook",
            name="labels",
            field=models.ManyToManyField(
                related_name="labeled_contact",
                through="contactbook.ContactLabel",
                to="label.label",
            ),
        ),
        migrations.AlterField(
            model_name="contactlabel",
            name="contact",
            field=models.ForeignKey(
                db_comment="주소록",
                on_delete=django.db.models.deletion.CASCADE,
                to="contactbook.contactbook",
            ),
        ),
        migrations.AlterField(
            model_name="contactlabel",
            name="label",
            field=models.ForeignKey(
                db_comment="라벨",
                on_delete=django.db.models.deletion.CASCADE,
                to="label.label",
            ),
        ),
    ]
