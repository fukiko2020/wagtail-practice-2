from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel


class TopPage(Page):
    # cover_image = models.ForeignKey(
    #     'wagtailimags.Image',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+',
    # )
    intro = models.CharField(max_length=255)
    main_body = RichTextField(blank=True)
    # side_image = models.ForeignKey(
    #     'wagtailimages.Image',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+',
    # )
    side_title = models.CharField(blank=True, max_length=255)
    side_body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('main_body', classname="full"),
        FieldPanel('side_title'),
        FieldPanel('side_body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class TopPageGalleryImage(Orderable):
    page = ParentalKey(TopPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+',
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


