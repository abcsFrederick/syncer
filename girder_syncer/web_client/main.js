import './routes';

import { registerPluginNamespace } from '@girder/core/pluginUtils';

import * as syncer from './index';

registerPluginNamespace('syncer', syncer);