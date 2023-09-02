# 中文
## 用于应对更新版本导致static发生变化的工具
- 未来将支持可视化程序的语言文件。


### 使用方法
1、解压并打开 interface.exe 。
2、在右上角的菜单中选择 生成字典文件 ，需要旧版本未翻译的原文本与译本，生成的字典文件会位于 ./source_file/dict 。
3、生成完成后选择 翻译原始语言文件 ，选择当前版本的原文本，生成的新文本位于 ./source_file/output 。

### 备注
1、生成字典文件 中，会优先以未翻译的原文本生成字典的文件名，即原文件名为 static.json 则会生成 static_dict.json。
2、翻译原始语言文件 中，请保证原文件名与旧版本的原文件名相同（程序会自动查询）。
3、生成的新语言文件中，文件名与原文件名相同的为已翻译词条的集合，前缀为 neededTranslate_ 的为未翻译词条的集合。后缀为 _all 的为两者的集合但是按照原文件的顺序进行排序。

# English
## A tool used to deal with static changes caused by updated versions
- Language files for visualization programs will be supported in the future.


### Instructions
1. Unzip and open interface.exe.
2. Select Generate Dictionary File from the menu in the upper right corner. The untranslated original text and translation of the old version are required. The generated dictionary file will be located in ./source_file/dict .
3. After the generation is complete, select Translate Original Language File , select the original text of the current version, and the generated new text is located in ./source_file/output .

### Remark
1. When generating a dictionary file, the file name of the dictionary will be generated with the untranslated original text first, that is, if the original file name is static.json, static_dict.json will be generated.
2. When translating the original language file, please ensure that the original file name is the same as the original file name of the old version (the program will automatically query).
3. Among the generated new language files, those whose file name is the same as the original file name are a collection of translated entries, and those whose prefix is neededTranslate_ are a collection of untranslated entries. The suffix _all is a collection of both but sorted according to the order of the original file.
