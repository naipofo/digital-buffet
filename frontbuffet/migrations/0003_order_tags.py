# Generated by Django 4.2.5 on 2023-09-14 07:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frontbuffet", "0002_add_orders"),
    ]

    operations = [
        migrations.CreateModel(
            name="FoodTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name="foodoffer",
            name="tags",
            field=models.ManyToManyField(to="frontbuffet.foodtag"),
        ),
    ]
