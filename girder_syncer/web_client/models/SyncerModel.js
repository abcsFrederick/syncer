import _ from 'underscore';

import AccessControlledModel from '@girder/core/models/AccessControlledModel';
import { restRequest } from '@girder/core/rest';
import events from '@girder/core/events';

var SyncerModel = AccessControlledModel.extend({
    resourceName: 'syncer',

    start: function () {
        return restRequest({
            url: `${this.resourceName}/start`,
            method: 'POST'
        }).done((resp) => {
            events.trigger('g:alert', {
                icon: 'ok',
                text: 'Start monitor.',
                type: 'success',
                timeout: 4000
            });
            this.trigger('startMonitoroing');
        }).fail((err) => {
            this.trigger('g:error', err);
        });
    },

    stop: function () {
        return restRequest({
            url: `${this.resourceName}/stop`,
            method: 'POST'
        }).done((resp) => {
            events.trigger('g:alert', {
                icon: 'ok',
                text: 'Stop monitor.',
                type: 'success',
                timeout: 4000
            });
            this.trigger('stopMonitoroing');
        }).fail((err) => {
            this.trigger('g:error', err);
        });
    }
});

export default SyncerModel;
