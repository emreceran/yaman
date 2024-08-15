# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

from odoo.addons.web_editor.tools import get_video_embed_code, get_video_thumbnail


class ProjectImage(models.Model):
    _name = 'project.image'
    _description = "Project Image"
    _inherit = ['image.mixin']
    _order = 'sequence, id'

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10)

    image_1920 = fields.Image()

    project_tmpl_id = fields.Many2one('project.project', "Project Gorsel ", index=True, ondelete='cascade')


