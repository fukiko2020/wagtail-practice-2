from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock, StreamBlock
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

    def get_context(self, request):
        context = super().get_context(request)

        articles = MyColumnPage.objects.live()
        tag = request.GET.get('tag')
        if tag:
            articles = articles.filter(tags__name=tag)

        context['articles'] = articles
        return context


class IndexImages(Orderable):
    page = ParentalKey(IndexPage, on_delete=models.CASCADE, related_name='index_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(max_length=1000, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


# カラムを2分割・3分割に自由に設定できるページ
class MyContentBlocks(StreamBlock):
    image = ImageChooserBlock()
    richtext = RichTextBlock()


class MyColumnBlocks(StreamBlock):
    two_columns = ColumnsBlock(
        MyContentBlocks(),
        ratios=(1, 1),
        group="Columns",
        template='cms/blocks/two_column_block.html',
    )
    three_columns = ColumnsBlock(
        MyContentBlocks(),
        ratios=(1, 1, 1),
        group="Columns",
        template='cms/blocks/three_column_block.html',
    )


# タグづけ
class MyColumnPageTag(TaggedItemBase):
    content_object = ParentalKey('MyColumnPage', on_delete=models.CASCADE, related_name='tagged_items')


class MyColumnPage(Page):
    body = StreamField(MyColumnBlocks)
    tags = ClusterTaggableManager(through=MyColumnPageTag, blank=True)

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

