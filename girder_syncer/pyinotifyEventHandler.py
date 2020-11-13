import pyinotify
import os
from girder.models.assetstore import Assetstore as AssetstoreModel
from girder.utility.model_importer import ModelImporter
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.file import File
from girder.models.user import User
from girder.models.setting import Setting

def importFile(item, path, user, assetstore, name=None, mimeType=None, **kwargs):
    stat = os.stat(path)
    name = name or os.path.basename(path)
    file = File().createFile(
        name=name, creator=user, item=item, reuseExisting=True, assetstore=assetstore,
        mimeType=mimeType, size=stat.st_size, saveFile=False)
    file['path'] = os.path.abspath(os.path.expanduser(path))
    file['mtime'] = stat.st_mtime
    file['imported'] = True
    file = File().save(file)
    return file

def _importFileToFolder(name, user, parent, parentType, path, assetstore):
    if parentType != 'folder':
        raise ('Files cannot be imported directly underneath a %s.' % parentType)

    item = Item().createItem(name=name, creator=user, folder=parent, reuseExisting=True)
    importFile(item, path, user, assetstore, name=name)

def importData(parent, parentType, path, user, leafFoldersAsItems):
    importPath = path
    name = os.path.basename(importPath)

    folder = Folder().createFolder(
        parent=parent, name=name, parentType=parentType,
        creator=user, reuseExisting=True)
    folder['path'] = os.path.abspath(os.path.expanduser(path))
    folder['imported'] = True
    Folder().save(folder)

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, assetstore, destination, destinationType, partition):
        self.assetstore = assetstore
        self.destination = destination
        self.destinationType = destinationType
        self.partition = partition
    def process_IN_CREATE(self, event):
        print ("Creating:", event.pathname)
        user = User().authenticate('admin', 'password')
        leafFoldersAsItems = False
        params = {
            'fileIncludeRegex': False,
            'fileExcludeRegex': False,
            'importPath': self.partition,
        }
        if(os.path.isfile(event.pathname)):
            hierarchy = os.path.relpath(event.pathname, self.partition)
            prefix = self.partition
            hierarchyList = hierarchy.split('/')
            print(self.destination)
            for index, folder in enumerate(hierarchyList):
                currentPath = os.path.join(prefix, folder)
                # check if parent folder exist
                q = {'imported': True, 'path': prefix}
                existfolder = list(Folder().find(q))
                if index != len(hierarchyList) - 1:
                    if len(existfolder) == 0:
                        importData(self.destination, self.destinationType, currentPath, user, leafFoldersAsItems)
                    else:
                        importData(existfolder[0], 'folder', currentPath, user, leafFoldersAsItems)
                else:
                    name = os.path.basename(currentPath)
                    _importFileToFolder(name, user, existfolder[0], 'folder', currentPath, self.assetstore)
                prefix = currentPath
    def process_IN_DELETE(self, event):
        print ("Removing:", event.pathname)
        q = {'imported': True, 'path': event.pathname}
        existFolder = list(Folder().find(q))
        if len(existFolder) != 0:
            Folder().remove(existFolder[0])
        q = {'imported': True, 'path': event.pathname}
        existFile = list(File().find(q))
        if len(existFile) != 0:
            File().remove(existFile[0])
    def process_IN_MODIFY(self, event):
        print ("Modify:", event.pathname)
        q = {'imported': True, 'path': event.pathname}
        exist = list(File().find(q))
        if len(exist) != 0:
            stat = os.stat(event.pathname)
            exist[0]['size'] = stat.st_size
            exist[0]['mtime'] = stat.st_mtime
            File().updateFile(exist[0])