# Generated by Django 2.1.7 on 2019-06-12 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coordinates',
        ),
        migrations.RenameField(
            model_name='tagimage',
            old_name='tags_rectangles',
            new_name='tags_boxes',
        ),
    ]