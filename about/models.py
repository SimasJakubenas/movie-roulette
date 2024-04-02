from django.db import models


class About(models.Model):
    """
    Modal for about page

    """
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title


class ContactFormModel(models.Model):
    """
    Modal for contact page
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact form from {self.name}"
