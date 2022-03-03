# Based on https://craiga.id.au/2020/05/26/rename-django-default-site

from django.db import migrations


def setup_default_site(apps, schema_editor):
    """
    Set up or rename the default example.com site created by Django.
    """
    Site = apps.get_model("sites", "Site")

    name = "CalibreWAN"
    domain = "CalibreWAN.yourdomain.com"

    try:
        site = Site.objects.get(domain="example.com")
        site.name = name
        site.domain = domain
        site.save()

    except Site.DoesNotExist:
        # No site with domain example.com exists.
        # Create a default site, but only if no sites exist.
        if Site.objects.count() == 0:
            Site.objects.create(name=name, domain=domain)


class Migration(migrations.Migration):
    dependencies = [
        ('library', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(setup_default_site, migrations.RunPython.noop),
    ]
