# Generated by Django 4.2.1 on 2023-05-27 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketball_blog', '0004_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
