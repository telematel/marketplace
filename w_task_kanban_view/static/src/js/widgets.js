odoo.define('w_task_kanban_view.BooleanFA', function (require) {
    "use strict";

    var field_registry = require('web.field_registry');
    var FieldToggleBoolean = require('web.basic_fields').FieldToggleBoolean;
    var AbstractField = require('web.AbstractField');
    var core = require('web.core')
    var _t = core._t;

    var WToggleBoolean = FieldToggleBoolean.extend({
        events: {
            'click': function (e) {
                e.stopPropagation();
            }
        },
        init: function () {
            this._super.apply(this, arguments);
        },
        /**
         * @override
         * @private
         */
        _render: function () {
            this.$('i').removeClass('fa-circle');
            this.$el.addClass('float-right');
            if (this.value) {
                this.$('i').addClass('fa-warning');
                this.$('i').attr('style', 'font-size: 1.5rem;color: #00A09D');
            } else {
                this.$('i').addClass('fa-check-circle hidden');
                this.$('i').attr('style', 'display: none;');
            }
            this.$('i').toggleClass('text-muted', !this.value);
            var title = this.value ? this.attrs.options.active : this.attrs.options.inactive;
            this.$el.attr('title', title);
            this.$el.attr('aria-pressed', this.value);
        },
    });

    var FieldMany2oneKanban = AbstractField.extend({
        events: {
            'click': '_onToggleButton'
        },
        supportedFieldTypes: ['many2one'],
        /**
         * Toggle the button
         *
         * @private
         * @param {MouseEvent} event
         */
        _onToggleButton: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: this.field.relation,
                method: 'get_formview_action',
                args: [[this.value.res_id]],
                context: this.record.getContext(this.recordParams),
            }).then(function (action) {
                self.trigger_up('do_action', {action: action});
            });
        },
        /**
         * Display button
         * @override
         * @private
         */
        _render: function () {
            var value = this._formatValue(this.value);
            this.$el.html(_.str.sprintf('<a><strong>%s</strong></a>', value));
            if (this.value) {
                this.$('a').attr('href', '#');
                this.$('a').addClass('o_form_uri');
            }
        },
    });

    field_registry.add('w_toggle_boolean', WToggleBoolean);
    field_registry.add('w_kanban_clickable', FieldMany2oneKanban);

});
