from django.db import migrations
from django.apps import apps as global_apps


def forward(apps, _schema_editor):
    try:
        Redirect = apps.get_model("redirects", "Redirect")
    except LookupError:
        return

    BriefURL = apps.get_model("django_burl", "BriefURL")
    BriefURL.objects.bulk_create(
        BriefURL(
            id=redirect.id,
            url=redirect.url,
            burl=redirect.burl,
            description=redirect.description,
            created=redirect.created,
            updated=redirect.updated,
            enabled=redirect.enabled,
            user=redirect.user,
        )
        for redirect in Redirect.objects.all()
    )


class Migration(migrations.Migration):
    operations = [migrations.RunPython(forward, migrations.RunPython.noop)]
    dependencies = [
        ("django_burl", "0001_initial"),
        ("core", "0002_auto_20210508_1204"),
    ]

    if global_apps.is_installed("burl.redirects"):
        dependencies.append(("redirects", "0001_initial"))
