# Generated by Django 4.0.3 on 2022-08-26 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0009_rename_recommendation1_recommendation_rec1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recommendation',
            old_name='rec1obj',
            new_name='age',
        ),
        migrations.RenameField(
            model_name='recommendation',
            old_name='rec2obj',
            new_name='rec1age',
        ),
        migrations.RenameField(
            model_name='recommendation',
            old_name='rec3obj',
            new_name='rec2age',
        ),
        migrations.RenameField(
            model_name='recommendation',
            old_name='rec4obj',
            new_name='rec3age',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='rec4age',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
