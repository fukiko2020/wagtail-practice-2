from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RawHTMLBlock, RichTextBlock, StreamBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtailcolumnblocks.blocks import ColumnsBlock


class TopPage(Page):
    intro = models.CharField(max_length=255)
    main_body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('main_body', classname="full"),
        InlinePanel('top_images', label="Gallery images"),
    ]


class TopPageGalleryImage(Orderable):
    page = ParentalKey(TopPage, on_delete=models.CASCADE, related_name='top_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+',
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class IndexPage(Page):
    body = RichTextField(max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('index_images', label='Index images')
    ]


class IndexImages(Orderable):
    page = ParentalKey(IndexPage, on_delete=models.CASCADE, related_name='index_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(max_length=1000, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class ContentsPage(Page):
    body = StreamField([
        ('rich_text', RichTextBlock(icon='doc_full', label='Rich Text', required=False)),
        ('html', RawHTMLBlock(icon='code', label='Raw HTML', required=False)),
        ('image', ImageChooserBlock(label='Image', required=False)),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        InlinePanel('contents_images', label='Contents images'),
    ]


class ContentsImages(Orderable):
    page = ParentalKey(ContentsPage, on_delete=models.CASCADE, related_name='contents_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')

    panels = [
        ImageChooserPanel('image'),
    ]


class MyContentBlocks(StreamBlock):
    image = ImageChooserBlock()
    richtext = RichTextBlock()


class ThreeColumnBlocks(StreamBlock):
    column_1_1_1 = ColumnsBlock(
        MyContentBlocks(),
        ratios=(1, 1, 1),
        group="Columns",
        template='cms/blocks/three_column_block.html',
    )


class TwoColumnBlocks(StreamBlock):
    column_1_1 = ColumnsBlock(
        MyContentBlocks(),
        ratios=(1, 1),
        group="Columns",
        template='cms/blocks/two_column_block.html',
    )


class MyColumnPage(Page):
    body = StreamField([
        ('two_column', TwoColumnBlocks(label='two column', required=False)),
        ('three_column', ThreeColumnBlocks(label='three column', required=False)),
    ])

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('body'),
    ]
