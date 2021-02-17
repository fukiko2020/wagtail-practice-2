from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core import fields
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

# from wagtailcolumnblocks.blocks import ColumnsBlock


# class MyContentBlocks(blocks.StreamBlock):
#     image = ImageChooserBlock()
#     richtext = blocks.RichTextBlock()


# class ThreeColumnBlocks(blocks.StreamBlock):
#     column_1_1_1 = ColumnsBlock(
#         MyContentBlocks(),
#         ratios=(1, 1, 1),
#         group="Columns",
#         template='home/blocks/three_column_block.html',
#     )


# class TwoColumnBlocks(blocks.StreamBlock):
#     column_1_1 = ColumnsBlock(
#         MyContentBlocks(),
#         ratios=(1, 1),
#         group="Columns",
#         template='home/blocks/two_column_block.html',
#     )


# class MyColumnPage(Page):
#     body = fields.StreamField([
#         ('two_column', TwoColumnBlocks(label='two column', required=False)),
#         ('three_column', ThreeColumnBlocks(label='three column', required=False)),
#     ])

#     content_panels = [
#         FieldPanel('title'),
#         StreamFieldPanel('body'),
#     ]


class HomePage(Page):
    pass
