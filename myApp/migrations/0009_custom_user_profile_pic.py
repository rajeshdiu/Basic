# Generated by Django 4.2.4 on 2023-12-20 18:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0008_alter_jobseekerprofile_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="custom_user",
            name="profile_pic",
            field=models.ImageField(null=True, upload_to="media/profile_pic"),
        ),
    ]