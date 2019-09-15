import os
import codecs  # 支持多国语言的编码解码
import chardet  # 自动判别侦听文件字符集类型

class FileUtil:
    """
    File Operation Tool
    -----------------------
        + api link
            + [Python File(文件) 方法 - 菜鸟教程](https://www.runoob.com/python/file-methods.html)
            + [Python 文件I/O - 菜鸟教程](https://www.runoob.com/python/python-files-io.html)
        + default encoding:utf-8
        + methods
            + writeFile(filePath,data,encoding='utf-8')
            + writeFileByCover(filePath,data,encoding='utf-8')
            + writeFileByAppend(filePath,data,encoding='utf-8')
            + fileSwitchEncode(filePath,oldEncodeCharset,newEncodeCharset='utf-8')
            + fileCharset(filePath)
            + readFileNBytes(filePath,startPosition=0,readByteSize=1000,encoding='utf-8')
            + readFileNLines(filePath,startLine=0,lineSize=10,encoding='utf-8')
            + readFile(filePath,encoding='utf-8')
            + getAlllFilesPathOfCurrentDirectory(file_dir=None) 获取当前路径下的所有文件
            + getAllSubDirsOfCurrentDirectory(file_dir=None) 获取当前路径下的所有子目录(一级子目录)
            + printAllFile(file_dir) 打印指定路径下的所有文件、目录
    """

    def writeFile(self, filePath, data, encoding='utf-8'):
        self.writeFileByCover(filePath, data, encoding);  # 默认覆盖
        pass;

    # 通过覆盖的方式写入新数据
    # + 打开一个文件用于读写。
    # + 如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。
    # + 如果该文件不存在，创建新文件。
    def writeFileByCover(self, filePath, data, encoding='utf-8'):
        with open(filePath, mode='w', encoding=encoding) as file:
            file.write(data);
            file.flush();  # 主动刷新文件内部缓冲，直接把内部缓冲区的数据立刻写入文件, 而不是被动的等待输出缓冲区写入。
            file.close();
        pass;

    # 如果文件存在，则通过从原文件结尾处添加新数据的方式写入
    # + 打开一个文件用于追加。
    # + 如果该文件已存在，文件指针将会放在文件的结尾。
    # + 也就是说，新的内容将会被写入到已有内容之后。
    # + 如果该文件不存在，创建新文件进行写入。
    def writeFileByAppend(self, filePath, data, encoding='utf-8'):
        with open(filePath, mode='a', encoding=encoding) as file:
            file.write(data);
            file.flush();  # 主动刷新文件内部缓冲，直接把内部缓冲区的数据立刻写入文件, 而不是被动的等待输出缓冲区写入。
            file.close();
        pass;

    # 文件编码转换
    ### path = r"C:\Users\千千寰宇\Desktop\text.txt";
    ### FileUtil.fileSwitchEncode(path,'gbk','utf-8');
    def fileSwitchEncode(self, filePath, oldEncodeCharset, newEncodeCharset='utf-8'):
        data = '';
        newData = '';
        newFileTmpPath = filePath + ".tmp";
        if os.path.exists(newFileTmpPath) == True:  # 存在：删除其内容
            os.remove(newFileTmpPath);  # 删除已存在的临时文件
            print("[fileSwitchEncode] Remove temporary file '", newFileTmpPath, "' successfully!");
            pass;
        newFile = codecs.open(newFileTmpPath, 'a', encoding=newEncodeCharset);  # a：文件末尾追加 + 写
        with codecs.open(self, filePath, "r", encoding=oldEncodeCharset) as file:
            data = file.readlines();
            for line in data:
                newFile.write(line.encode(newEncodeCharset).decode(newEncodeCharset));  # gbk,utf-8
                pass;
            file.close();
        newFile.close();
        # 删除 原file
        os.remove(filePath);
        os.rename(newFileTmpPath, filePath);  # os.rename(src,dist) #将临时文件路径命名为 原file的名字
        pass;

    def fileCharset(filePath):  # 获得文件的字符集类型
        tmpFile = open(filePath, 'rb');
        data = tmpFile.read(90)
        tmpFile.close()
        print(chardet.detect(data));
        return chardet.detect(data)["encoding"];  # 形如：gbk，utf-8
        pass;

    def readFileNBytes(self, filePath, startPosition=0, readByteSize=1000,
                       encoding='utf-8'):  # 读取从第startPosition字节处开始的readByteSize字节的文件数据
        data = '';
        if startPosition < 0:
            startPosition = 0;
            pass;
        if readByteSize < 1:
            readByteSize = 100;
            pass;
        with open(self, filePath, 'r', encoding=encoding) as f:
            f.seek(startPosition);  # startPosition即偏移字节位置
            data = f.read(readByteSize);
            f.close();
            pass;
        return data;
        pass;

    def readFileNLines(self, filePath, startLine=0, lineSize=10, encoding='utf-8'):  # 读取从第startLine行开始的lineSize行文件数据
        data = '';
        i = 0;  # 记录当前所处行数
        line = None;
        endLineSize = startLine + lineSize;
        with open(filePath, 'r', encoding=encoding) as f:
            print("[FileUtil.readFileNLines] file name: ", f.name)
            line = f.readline();
            while (line != None) and (i < startLine):
                line = None;
                line = f.readline();
                i += 1;
                pass;
            print("current line[", i, "] line:", line);  # test
            while (line != None) and (i < endLineSize):
                # print ("[FileUtil.readFileNLines] 第 %d 行 - %s" % (i+1, line)); # test
                data += line;
                line = None;
                line = f.readline();
                i += 1;
                pass;
            f.close();
        return data;
        pass;

    def readFile(self, filePath, encoding='utf-8'):
        # data = '';
        # try:
        # f = open(filePath, 'r',encoding='utf-8');
        ## print(f.read());
        # for line in f:
        #    #print(line);
        #    data +=line;
        #    pass;
        # finally:
        # if f:
        # f.close();
        # pass;
        # pass;
        with open(filePath, 'r', encoding=encoding) as file:
            data = file.read()
        return data;
        pass;

    def getAlllFilesPathOfCurrentDirectory(self, file_dir=None):  # 获取当前路径下的所有文件
        """
        获取当前路径下的所有文件
        ------------------------
        即 不包含子目录下的文件和子目录
        :file_dir：必须为存在的目录路径，不得为文件路径
        :return 文件名数组，形如：['DatabaseUtil.py', 'FileUtil.py', 'PageRank.py', 'poms.ipynb', 'Test.ipynb', 'textrank.ipynb', 'Untitled.ipynb']
        """
        L = [];
        for root, dirs, files in os.walk(file_dir):
            L.append(files);
            # print(files) #当前路径下所有非目录子文件
            pass
        # print(L); # test
        return L[0];

    def getAllSubDirsOfCurrentDirectory(self, file_dir=None):  # 获取当前路径下的所有子目录(一级子目录)
        """
        获取当前路径下的所有子目录(一级子目录)
        ------------------------
        即 不包含子目录下的文件和子目录
        :file_dir：必须为存在的目录路径，不得为文件路径
        :return 子目录数组，形如：['.ipynb_checkpoints', '__pycache__']
        """
        L = [];
        for root, dirs, files in os.walk(file_dir):
            L.append(dirs);
            # print(files) #当前路径下所有非目录子文件
            pass
        # print(L); # test
        return L[0];

    def printAllFile(self, file_dir):  # 打印指定路径下的所有文件、目录
        L = [];
        for root, dirs, files in os.walk(file_dir):
            print("root:", root)  # 当前目录路径
            print("dirs:", dirs)  # 当前路径下所有子目录
            print("files:", files)  # 当前路径下所有非目录子文件
            # for file in files:
            # if os.path.splitext(file)[1] == '.jpeg':   # 指定特定类型的文件
            # L.append(os.path.join(root, file))
            # pass;
            # pass;
            # return L;
        pass

    pass;  # end class