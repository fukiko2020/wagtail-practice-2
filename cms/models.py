from django import forms
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
from wagtail.snippets.models import register_snippet

from wagtailcolumnblocks.blocks import ColumnsBlock


class IndexPage(Page):
    body = RichTextField(max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('index_images', label='Index images')
    ]

    # タグ指定されたらそのタグを持つ記事だけ表示するため←不要
    # カテゴリーごとに表示できるようにする
    def get_context(self, request):
        context = super().get_context(request)

        context['category_1'] = MyColumnPage.objects.live().filter(category=1)
        context['category_2'] = MyColumnPage.objects.live().filter(category=2)
        context['category_3'] = MyColumnPage.objects.live().filter(category=3)
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


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=100)

    panels = [FieldPanel('name')]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'カテゴリー'


# タグづけ
class MyColumnPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'MyColumnPage',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class MyColumnPage(Page):
    body = StreamField(MyColumnBlocks)
    post_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='category',
        null=True
    )
    tags = ClusterTaggableManager(through=MyColumnPageTag, blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('category', widget=forms.Select),
        FieldPanel('tags'),
        StreamFieldPanel('body'),
    ]
