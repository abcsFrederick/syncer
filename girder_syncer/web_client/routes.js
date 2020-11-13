
import events from '@girder/core/events';
import router from '@girder/core/router';
import { exposePluginConfig } from '@girder/core/utilities/PluginUtils';

import ConfigView from './views/configuration/configView';

exposePluginConfig('syncer', 'plugins/syncer/config');
router.route('plugins/syncer/config', 'syncerConfig', function () {
    events.trigger('g:navigateTo', ConfigView);
});