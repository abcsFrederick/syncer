import View from '@girder/core/views/View';

import PluginConfigBreadcrumbWidget from
    '@girder/core/views/widgets/PluginConfigBreadcrumbWidget';
import { restRequest } from '@girder/core/rest';
import events from '@girder/core/events';

import ConfigViewTemplate from '../../templates/configuration/configView.pug';
import '../../stylesheets/configuration/configView.styl';

import SyncerModel from '../../models/SyncerModel';


var ConfigView = View.extend({
    events: {
        'submit #g-Syncer-settings-form': function (event) {
            event.preventDefault();
            this.$('#g-Syncer-settings-error-message').empty();
            this._saveSettings([{
                key: 'syncer.ASSETSTORE_ID',
                value: this.$('#g-Syncer-settings-ASSETSTORE-ID').val()
            }, {
                key: 'syncer.MONITOR_PARTITION',
                value: this.$('#g-Syncer-settings-MONITOR-PARTITION').val()
            }, {
                key: 'syncer.DESTINATION_TYPE',
                value: this.$('#g-Syncer-settings-DESTINATION-TYPE').val()
            }, {
                key: 'syncer.DESTINATION_ID',
                value: this.$('#g-Syncer-settings-DESTINATION-ID').val()
            }]);
        },
        'click #startMonitor': function (event) {
            this.syncerModel.start();
        },
        'click #stopMonitor': function (event) {
            this.syncerModel.stop();
        }
    },

    initialize: function () {
        this.syncerModel = new SyncerModel();
        this.syncerModel.on('startMonitoroing', function (e) {
            this.settings["syncer.MONITOR"] = true
            this.render();
        }, this);
        this.syncerModel.on('stopMonitoroing', function (e) {
            this.settings["syncer.MONITOR"] = false
            this.render();
        }, this);
        ConfigView.getSettings((settings) => {
            this.settings = settings;
            this.render();
        });
    },

    render: function () {
        this.$el.html(ConfigViewTemplate({
            settings: this.settings
        }));
        if (!this.breadcrumb) {
            this.breadcrumb = new PluginConfigBreadcrumbWidget({
                pluginName: 'Syncer',
                el: this.$('.g-config-breadcrumb-container'),
                parentView: this
            }).render();
        } else {
            this.breadcrumb.setElement(this.$('.g-config-breadcrumb-container')).render();
        }

        return this;
    },

    _saveSettings: function (settings) {
        /* Now save the settings */
        return restRequest({
            type: 'PUT',
            url: 'system/setting',
            data: {
                list: JSON.stringify(settings)
            },
            error: null
        }).done(() => {
            /* Clear the settings that may have been loaded. */
            ConfigView.clearSettings();
            events.trigger('g:alert', {
                icon: 'ok',
                text: 'Settings saved.',
                type: 'success',
                timeout: 4000
            });
        }).fail((resp) => {
            console.log(resp);
            this.$('#g-Syncer-settings-error-message').text(
                resp.responseJSON.message
            );
        });
    }
}, {
    /**
     * Get settings if we haven't yet done so.  Either way, call a callback
     * when we have settings.
     *
     * @param {function} callback a function to call after the settings are
     *      fetched.  If the settings are already present, this is called
     *      without any delay.
     */
    getSettings: function (callback) {
        if (!ConfigView.settings) {
            restRequest({
                type: 'GET',
                url: 'syncer/settings'
            }).done((resp) => {
                ConfigView.settings = resp;
                if (callback) {
                    callback(ConfigView.settings);
                }
            });
        } else {
            if (callback) {
                callback(ConfigView.settings);
            }
        }
    },

    /**
     * Clear the settings so that getSettings will refetch them.
     */
    clearSettings: function () {
        delete ConfigView.settings;
    }
});

export default ConfigView;