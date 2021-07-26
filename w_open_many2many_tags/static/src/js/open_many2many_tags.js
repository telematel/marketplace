odoo.define('w_open_many2many_tags.open_many2many_tags', function(require) {
    "use strict";

    var dialogs = require('web.view_dialogs');
    var relationalFields = require('web.relational_fields');
    var FieldsRegistry = require('web.field_registry');

    var OpenMany2many_tags = relationalFields.FieldMany2ManyTags.extend({
        events: _.extend({}, relationalFields.FieldMany2ManyTags.prototype.events, {
           'click .badge': '_onClickTag'
        }),

        _onClickTag: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var self = this;
            var record_id = this.get_badge_id(event.target);
            new dialogs.FormViewDialog(self, {
                res_model: self.field.relation,
                res_id: record_id,
                title: event.target.innerText,
                context: self.record.context,
                readonly: true
            }).on('write_completed', self, function () {
                self.dataset.cache[record_id].from_read = {};
                self.dataset.evict_record(record_id);
                self.render_value();
            }).open();
        },

        get_badge_id: function(el){
            if ($(el).hasClass('badge')) return $(el).data('id');
            return $(el).closest('.badge').data('id');
        },
    });

   FieldsRegistry.add('open_many2many_tags', OpenMany2many_tags);
    return OpenMany2many_tags;

});
