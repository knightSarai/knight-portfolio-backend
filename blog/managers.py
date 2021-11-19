from django.db.models import Manager


class PublishedManager(Manager):

    def get_queryset(self):
        return (
            super(PublishedManager, self)
            .get_queryset()
            .filter(status='published')
        )
