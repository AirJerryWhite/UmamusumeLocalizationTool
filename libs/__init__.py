import json
import os
import shutil


def mkDir(root: str, relativePath: str):
    DIRS = relativePath.split('/')
    for DIR in DIRS:
        if os.path.exists(os.path.join(root, DIR)):
            os.mkdir(os.path.join(root, DIR))
            root = os.path.join(root, DIR)


def spawnDict(originPath: str, translatePath: str):
    savaPath = os.path.abspath('resource/dict')

    if os.path.exists(savaPath):
        if os.path.exists(os.path.join(savaPath, 'bak')):
            shutil.rmtree(os.path.join(savaPath, 'bak'))
        os.mkdir(os.path.join(savaPath, 'bak'))
        pathList = []
        for root, _, files in os.walk(originPath):
            for file in files:
                pathList.append(os.path.join(root, file))
        for file in pathList:
            relatedPath = file.replace(originPath, '')
            shutil.move(file, os.path.join(savaPath, 'bak', relatedPath))

    pathList = []
    for root, _, files in os.walk(originPath):
        for file in files:
            pathList.append(os.path.join(root, file))
    for langFile in pathList:
        relativePath = os.path.splitext(langFile)[0].replace(originPath, '')[1:]
        filename = os.path.splitext(os.path.split(langFile)[1])[0]

        mkDir(savaPath, relativePath)

        compareDict = {}
        with open(langFile, 'r', encoding='utf-8') as fp:
            originData = json.load(fp)
        try:
            with open(os.path.join(translatePath, relativePath, f'{filename}.json'), 'r', encoding='utf-8') as fp:
                translateData = json.load(fp)
        except FileNotFoundError:
            continue
        for textID, text in originData.items():
            if text != translateData[textID]:
                compareDict[text] = translateData[textID]
        with open(os.path.join(savaPath, relativePath, f'{filename}.json'), 'w', encoding='utf-8') as fp:
            json.dump(compareDict, fp, ensure_ascii=False, indent=4)


def translate(folderPath: str, outputPath: str):
    compareDictPath = os.path.abspath('resource/dict')
    needTranslatePath = os.path.abspath('resource/output')

    if os.path.exists(needTranslatePath):
        shutil.rmtree(needTranslatePath)
    os.mkdir(needTranslatePath)

    langFilePathList = []
    for root, _, files in os.walk(folderPath):
        for file in files:
            langFilePathList.append(os.path.join(root, file))
    for langFile in langFilePathList:
        relativePath = os.path.splitext(langFile)[0].replace(folderPath, '')[1:]
        filename = os.path.splitext(os.path.split(langFile)[1])[0]

        needTranslate = {}
        with open(langFile) as fp:
            lang = json.load(fp)
        try:
            with open(os.path.join(compareDictPath, relativePath, f'{filename}.json')) as fp:
                compareDict = json.load(fp)
        except FileNotFoundError:
            for text in lang.values():
                needTranslate[text] = ""

        else:
            for textID, text in lang.items():
                if text in compareDict.keys():
                    lang[textID] = compareDict[text]
                else:
                    needTranslate[text] = ""
        with open(os.path.join(outputPath, relativePath, f'{filename}.json')) as fp:
            json.dump(lang, fp, ensure_ascii=False, indent=4)
        with open(os.path.join(needTranslatePath, relativePath, f'{filename}_needTranslate.json')) as fp:
            json.dump(needTranslate, fp, ensure_ascii=False, indent=4)
