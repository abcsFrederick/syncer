import pyinotify
import os
from girder.api.rest import Resource
from girder.api import access
from girder.api.describe import Description, autoDescribeRoute
from girder.models.setting import Setting
from girder.models.assetstore import Assetstore as AssetstoreModel
from girder.utility.model_importer import ModelImporter
from girder.constants import AccessType
from girder.settings import SettingDefault

from .constants import PluginSettings
from .pyinotifyEventHandler import EventHandler

class Syncer(Resource):
    def __init__(self):
        super(Syncer, self).__init__()
        self.resourceName = 'syncer'
        self.user = self.getCurrentUser()
        self.token = self.getCurrentToken()

        self.route('GET', ('settings',), self.getSettings)
        self.route('POST', ('start',), self.startMonitor)
        self.route('POST', ('stop',), self.stopMonitor)

    @access.admin
    @autoDescribeRoute(
        Description('Getting Syncer settings.')
    )
    def getSettings(self):
        settings = Setting()
        return {
            PluginSettings.ASSETSTORE_ID:
                settings.get(PluginSettings.ASSETSTORE_ID) or '',
            PluginSettings.MONITOR_PARTITION:
                settings.get(PluginSettings.MONITOR_PARTITION) or '',
            PluginSettings.DESTINATION_TYPE:
                settings.get(PluginSettings.DESTINATION_TYPE) or '',
            PluginSettings.DESTINATION_ID:
                settings.get(PluginSettings.DESTINATION_ID) or '',
            PluginSettings.MONITOR:
                settings.get(PluginSettings.MONITOR) or ''
            }

    @access.admin
    @autoDescribeRoute(
        Description('Starting monitor.')
    )
    def startMonitor(self):
        settings = Setting()
        self.ASSETSTORE_ID = settings.get(PluginSettings.ASSETSTORE_ID)
        self.assetstore = AssetstoreModel().load(self.ASSETSTORE_ID)
        
        self.MONITOR_PARTITION = settings.get(PluginSettings.MONITOR_PARTITION)

        self.DESTINATION_TYPE = settings.get(PluginSettings.DESTINATION_TYPE)
        self.DESTINATION_ID = settings.get(PluginSettings.DESTINATION_ID)
        self.destination = ModelImporter.model(self.DESTINATION_TYPE).load(
            self.DESTINATION_ID, user=self.getCurrentUser(), level=AccessType.WRITE, exc=True)

        wm = pyinotify.WatchManager()  # Watch Manager
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        
        self.notifier = pyinotify.ThreadedNotifier(wm, EventHandler(self.assetstore,
                                                                self.destination, self.DESTINATION_TYPE, self.MONITOR_PARTITION))
        wdd = wm.add_watch(self.MONITOR_PARTITION, mask, rec=True, auto_add=True)
        self.notifier.start()
        SettingDefault.defaults.update({PluginSettings.MONITOR: True})
        return { PluginSettings.MONITOR: settings.get(PluginSettings.MONITOR) }
    @access.admin
    @autoDescribeRoute(
        Description('Getting Syncer settings.')
    )
    def stopMonitor(self):
        settings = Setting()
        self.notifier.stop()
        SettingDefault.defaults.update({ PluginSettings.MONITOR: False })
        return { PluginSettings.MONITOR: settings.get(PluginSettings.MONITOR) }