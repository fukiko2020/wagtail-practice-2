from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core import fields
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtailcolumnblocks.blocks import ColumnsBlock


class MyContentBlocks(blocks.StreamBlock):
    """
    The blocks you want to allow within each MyColumnBlocks column.
    """

    image = ImageChooserBlock()
    text = blocks.CharBlock()
    richtext = blocks.RichTextBlock()


class ThreeColumnBlocks(blocks.StreamBlock):
    column_1_1_1 = ColumnsBlock(
        MyContentBlocks(),
        ratios=(1, 1, 1),
        group="Columns",
        template='home/blocks/three_column_block.html',
    )


class ThreeColumnPage(Page):
    content = fields.StreamField(ThreeColumnBlocks)

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('content')
    ]


class TwoColumnBlocks(blocks.StreamBlock):
    column_1_1 = ColumnsBlock(
        MyContentBlocks(),
        ratios=(1, 1),
        group="Columns",
        template='home/blocks/two_column_block.html',
    )


class MyColumnPage(Page):
    two_column = fields.StreamField(TwoColumnBlocks)
    three_column = fields.StreamField(ThreeColumnBlocks)

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('two_column'),
        StreamFieldPanel('three_column'),
    ]


class HomePage(Page):
    pass
