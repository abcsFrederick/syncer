import os
import asyncore
import pyinotify

from girder import plugin
from . import rest
from girder import events
from girder.utility import setting_utilities
# from girder.settings import SettingDefault

from .constants import PluginSettings

# from girder.models.assetstore import Assetstore as AssetstoreModel
# from girder.utility.model_importer import ModelImporter
# from girder.models.folder import Folder
# from girder.models.item import Item
# from girder.models.file import File
# from girder.models.user import User
# from girder.constants import AccessType
# from girder.models.setting import Setting

@setting_utilities.validator({
    PluginSettings.ASSETSTORE_ID,
    PluginSettings.MONITOR_PARTITION,
    PluginSettings.DESTINATION_TYPE,
    PluginSettings.DESTINATION_ID,
    PluginSettings.MONITOR
})
def validateString(doc):
    pass

# SettingDefault.defaults.update({
#     PluginSettings.ASSETSTORE_ID: '', # hostname
#     PluginSettings.MONITOR_PARTITION: '', # hostname
#     PluginSettings.DESTINATION_TYPE: '',
#     PluginSettings.DESTINATION_ID: '',
#     PluginSettings.MONITOR: ''
# })
# settings = Setting()
# partition = settings.get(PluginSettings.MONITOR_PARTITION)
# assetstoreId = settings.get(PluginSettings.ASSETSTORE_ID)
# assetstore = AssetstoreModel().load(assetstoreId)
# print(partition)
# def importFile(item, path, user, name=None, mimeType=None, **kwargs):
#         # logger.debug('Importing file %s to item %s on filesystem assetstore %s',
#         #              path, item['_id'], self.assetstore['_id'])
#         stat = os.stat(path)
#         name = name or os.path.basename(path)
#         file = File().createFile(
#             name=name, creator=user, item=item, reuseExisting=True, assetstore=assetstore,
#             mimeType=mimeType, size=stat.st_size, saveFile=False)
#         file['path'] = os.path.abspath(os.path.expanduser(path))
#         file['mtime'] = stat.st_mtime
#         file['imported'] = True
#         file = File().save(file)
#         # logger.debug('Imported file %s to item %s on filesystem assetstore %s',
#         #              path, item['_id'], self.assetstore['_id'])
#         return file

# def _importFileToFolder(name, user, parent, parentType, path):
#     if parentType != 'folder':
#         raise ('Files cannot be imported directly underneath a %s.' % parentType)

#     item = Item().createItem(name=name, creator=user, folder=parent, reuseExisting=True)
#     importFile(item, path, user, name=name)

# def importData(parent, parentType, path, user, leafFoldersAsItems):
#     importPath = path
#     name = os.path.basename(importPath)

#     folder = Folder().createFolder(
#         parent=parent, name=name, parentType=parentType,
#         creator=user, reuseExisting=True)
#     folder['path'] = os.path.abspath(os.path.expanduser(path))
#     folder['imported'] = True
#     Folder().save(folder)
# class EventHandler(pyinotify.ProcessEvent):
#     def process_IN_CREATE(self, event):
#         print ("Creating:", event.pathname)
#         user = User().authenticate('admin', 'password')
#         leafFoldersAsItems = False
#         params = {
#             'fileIncludeRegex': False,
#             'fileExcludeRegex': False,
#             'importPath': partition,
#         }
#         destinationType = 'collection'
#         destinationId = '5fa97afd654d5434743bfc39'
#         collection = ModelImporter.model(destinationType).load(
#             destinationId, user=user, level=AccessType.WRITE, exc=True)
#         if(os.path.isfile(event.pathname)):
#             hierarchy = os.path.relpath(event.pathname, partition)
#             prefix = partition
#             hierarchyList = hierarchy.split('/')
#             print(hierarchyList)
#             for index, folder in enumerate(hierarchyList):
#                 currentPath = os.path.join(prefix, folder)
#                 # check if parent folder exist
#                 q = {'imported': True, 'path': prefix}
#                 existfolder = list(Folder().find(q))
#                 if index != len(hierarchyList) - 1:
#                     if len(existfolder) == 0:
#                         importData(collection, destinationType, currentPath, user, leafFoldersAsItems)
#                     else:
#                         importData(existfolder[0], 'folder', currentPath, user, leafFoldersAsItems)
#                 else:
#                     name = os.path.basename(currentPath)
#                     _importFileToFolder(name, user, existfolder[0], 'folder', currentPath)
#                 prefix = currentPath
#     def process_IN_DELETE(self, event):
#         print ("Removing:", event.pathname)
#         q = {'imported': True, 'path': event.pathname}
#         existFolder = list(Folder().find(q))
#         if len(existFolder) != 0:
#             Folder().remove(existFolder[0])
#         q = {'imported': True, 'path': event.pathname}
#         existFile = list(File().find(q))
#         if len(existFile) != 0:
#             File().remove(existFile[0])
#     def process_IN_MODIFY(self, event):
#         print ("Modify:", event.pathname)
#         q = {'imported': True, 'path': event.pathname}
#         exist = list(File().find(q))
#         if len(exist) != 0:
#             stat = os.stat(event.pathname)
#             exist[0]['size'] = stat.st_size
#             exist[0]['mtime'] = stat.st_mtime
#             File().updateFile(exist[0])

class SyncerPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Syncer'
    CLIENT_SOURCE_PATH = 'web_client'
    def load(self, info):
        info['apiRoot'].syncer = rest.Syncer()

        # wm = pyinotify.WatchManager()  # Watch Manager
        # mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        
        # notifier = pyinotify.ThreadedNotifier(wm, EventHandler())

        # wdd = wm.add_watch(partition, mask, rec=True, auto_add=True)

        # # asyncore.loop()
        # notifier.start()