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
    The blocks you want to allow within wach MyColumnBlocks column.
    """

    image = ImageChooserBlock()
    text = blocks.CharBlock()


class MyColumnBlocks(blocks.StreamBlock):
    """
    All the root level blocks  you can use
    """
    column_2_1 = ColumnsBlock(
        # Blocks you want to allow within each column
        MyContentBlocks(),
        # Two columns in admin, first twice as wide as the second
        ratios=(2, 1),
        # Used for grouping related fields in the streamfield field picker
        group="Columns",
        # 12 column frontend grid (this is the default, so can be omitted)
        grid_width=12,
        # Override the frontend template
        template='home/blocks/two_column_block.html',
    )


class SidebarPage(Page):
    content = fields.StreamField(MyColumnBlocks)

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('content'),
    ]


class HomePage(Page):
    pass
