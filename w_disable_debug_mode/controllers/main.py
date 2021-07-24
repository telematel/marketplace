# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2019 Wedoo - http://www.wedoo.tech/
# All Rights Reserved.
#
# Developer(s): Randy La Rosa Alvarez
#               (randi.larosa@telematel.com)
########################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################
from odoo import http
from odoo.http import request
import werkzeug
from odoo.addons.web.controllers.main import Home


class HomeDebugModeEnable(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        debug = kw.get('debug', False) if 'debug' in kw.keys() else False
        user_id = request.context.get('uid', False)
        if debug or debug == '':
            if user_id:
                user = request.env['res.users'].sudo().browse(user_id)
                if not user.has_group('w_disable_debug_mode.group_debug_mode_enable'):
                    return werkzeug.utils.redirect('/web/login?error=access')
        return super(HomeDebugModeEnable, self).web_client(s_action=s_action, **kw)
