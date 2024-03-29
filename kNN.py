from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
from os import listdir


def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels


def classify0(inX,dataSet,labels,k):  #inX是需要分类的向量，可以是list或者tuple，dataSet是训练数据集特征向量，labels是标签向量，最后的参数k表示用于选择最近邻居的数目
    dataSetSize = dataSet.shape[0]  #array的长度，即有多少行
    diffMat = tile(inX, (dataSetSize,1)) - dataSet  #tile() 复制inX延y轴方向复制dataSetSize倍,减 dataSet array 
    #输入向量的列和训练集的列一样多，行不一样多，于是此处需要复制inX复制成和训练数据集向量一样那么多
    sqDiffMat = diffMat ** 2 #相当于各求(x-inputX)和(y-inputY)的平方
    sqDistances = sqDiffMat.sum(axis=1)  #将上述平方两两相加 sum()中，参数axis=1表示按行相加 , axis=0表示按列相加
    distances = sqDistances ** 0.5 #开根号
    sortedDistIndicies = distances.argsort()  #argsort() 升序排列后返回原array的对应索引值
    classCount = {}
    for i in range(k):  #将sortedDistIndicies前k个的label记录下来
        voteIlabel = labels[sortedDistIndicies[i]]  
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1   #get方法，前者是需要在字典中寻找的参数，后者是若找不到赋值的参数；找到后进行+1操作，找不到先赋值0再进行+1操作
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse=True)  #key = operator.itemgetter(1)--按字典的第二个元素排列，对出现的label按出现次数降序排序
    return sortedClassCount[0][0]  #返回降序排序第一位的值，即出现最多次的label的值 
"""
classify0()步骤：
1. 允许输入值：需要进行分类的向量，可以是list或者tuple；训练数据集特征向量；训练数据集标签向量，最近邻居的数目（参数k）
2. 计算训练数据集特征向量的长度
3. 计算 （需要进行分类的向量 分别减 每行训练数据集特征向量）x,y各自平方后相加 再开根号，得到 需要进行分类的向量 距离 训练数据集特征向量 中每个点的距离。
4. 按距离（从小到大）升序排列后，返回对应原array的索引值
5. 取出排列后的向量对应的标签向量
6. 计算每个标签向量出现的次数
7. 返回出现次数最多的标签向量
"""

#group, labels = createDataSet()
#classify0([0,0], group, labels, 3)


def file2matrix(filename): #读文件 返回其特征向量和标签向量
    with open(filename) as fr:
        arrayOlines = fr.readlines() #以换行符分隔，数据类型：list
        numberOfLines = len(arrayOlines) #被分成多少行
        returnMat = zeros((numberOfLines,3))  #建立行，列数量分别为numberOfLines，3的全为零的array
        classLabelVector = []
        index = 0
        for line in arrayOlines:
            line = line.strip()
            listFromLine = line.split("\t") #以tab符分隔特征，数据类型：list
            returnMat[index,:] = listFromLine[0:3]  #array[:,:]，逗号前表示y,逗号后表示x，a:b即从第a项到第b项。这里指第index行的所有值=listFromLine[0:3]这个list
            classLabelVector.append(int(listFromLine[-1]))
            index += 1

    return returnMat, classLabelVector
"""
file2matrix()步骤：
1. 读文件，获取文件行数
2. 建立一个全为零的array，行与文件行数量一致，列数量为特征数
3. 遍历文章行，以tab符分隔，前三项是特征，后一项是分类，分别存入两个list中
4. 返回按序排列的特征和分类
"""

#datingDataMat, datingLabels = file2matrix("datingTestSet2.txt")


def autoNorm(dataSet): #归一化
    minVals = dataSet.min(0) #min(0)：取列的最小值，min(1)：取行的最小值；此处是获得每一列的最小值   type(minVals)=numpy.ndarray
    maxVals = dataSet.max(0) #最大值
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet)) #以dataSet的shape创建一个都为0的normDataSet
    m = dataSet.shape[0]  #获取dataSet的行
    normDataSet = dataSet - tile(minVals,(m,1))   #tile:复制minVals延y轴方向复制m倍，矩阵相减，减最小值得到该值到最小值的距离
    normDataSet = normDataSet/tile(ranges,(m,1))  #tile:复制ranges延y轴方向复制m倍，矩阵相除，除以范围，得到该点到最小值除以范围的值，作归一化
    return normDataSet, ranges, minVals

"""
autoNorm()步骤：
1. 输入dataSet，取dataSet每一列的最大值和最小值，相减，获得范围
2. 创建和dataSet相同shape（即行列数量一致）的normDataSet
3. 计算每一行的值到最小值的距离/范围，使得结果落到(0,1)之间，获得归一化的结果
4. 返回此归一化后的结果，范围和最小值
"""

def datingClassTest():
    hoRatio = 0.10 #测试集百分比
    dataingDataMat, dataingLabels = file2matrix("datingTestSet2.txt") #读取文件，获得训练集的特征和分类
    normMat, ranges, minVals = autoNorm(datingDataMat) #对数据进行归一化处理
    m = normMat.shape[0] #获取数据的行数
    numTestVecs = int(m*hoRatio) #确定测试集数量
    errorCount = 0.0
    for i in range(numTestVecs):  #循环测试集的数量
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)  
        #分类归一化后的第i行数据，训练样本集（从numTestVecs到m行的数据） normMat[numTestVecs:m,:] 后900行为训练集，前100行为测试集
        #print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]):errorCount += 1.0
    #print("the total error rate is: %f" % (errorCount/float(numTestVecs)))
    errorRate = errorCount/float(numTestVecs)
    #accuracy = 1 - errorRate
    #print(accuracy)
    return errorRate
"""
datingClassTest()步骤：
1. 读取文件，获得训练集的特征和分类
2. 对训练集的特征进行归一化处理
3. 根据百分比确定测试集数量
4. 循环对测试集进行分类（输入需测试的向量、训练集特征&标签及k值）
5. 对比测试集使用算法进行分类的结果和真正的分类的区别，计算错误率
6. 返回错误率
"""


def classifyPerson():
    resultList = ['not at all','in small doses', 'in large doses']
    percentTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat) #对训练集特征进行归一化处理
    inArr = array([ffMiles,percentTats,iceCream]) #将用户输入的转成array
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3) #(inArr-minVals)/ranges 归一化
    print("You will probably like this person: ",resultList[classifierResult - 1])


"""
classifyPerson()步骤：
1. 让用户在console输入三个特征数值
2. 获得训练集的特征&标签
3. 对训练集特征进行归一化处理
4. 将用户输入的转成array形式
5. 对用户输入进行归一化处理后进行分类
6. 打印分类结果的自然语言形式
"""

def img2vector(filename):  #文件是一个32x32的二进制图像矩阵，要转换为1x1024的向量
    returnVect = zeros((1,1024)) #构建shape为（1,1024）的全为零的array
    #fr = open(filename)
    with open(filename) as fr:
        for i in range(32):
            lineStr = fr.readline() #一个循环读文件的一行
            for j in range(32): 
                returnVect[0,32*i+j] = int(lineStr[j])  #一个循环赋值给returnVect，第1行的第32*i+j个位置是文件i+1行的j+1位数字
    return returnVect
"""
img2vector()步骤：  
1. 新建一个1*1024的全为零的array
2. 按行读取32*32的二进制图像矩阵，并将其数值按顺序赋值给步骤1中新建的array
3. 返回该array
"""
def handwritingClassTest(): #测试算法，计算错误率
    hwLabels = []
    trainingFileList = listdir('trainingDigits') #获取目录内容，即是文件名的list
    m = len(trainingFileList)
    trainingMat = zeros((m,1024)) #文件名有m个 构建m行，1024列的全为零的array
    for i in range(m):
        fileNameStr = trainingFileList[i] #获取文件名
        fileStr = fileNameStr.split('.')[0] #将文件名和后缀以“.”分隔，取名，去后缀，[0]表示是第一个分隔开的字符
        classNumStr = int(fileStr.split('_')[0]) #将文件名中数字摘出 所表示的数字是以“_”分隔的，，int(),将他变为整数
        hwLabels.append(classNumStr) #将Label存入list中
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr) #给出filename，用函数将img转为vector，放入第i行中
    testFileList = listdir('testDigits')  #测试集做同样操作
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat,hwLabels,3)  #knn只需在测试的时候，输入测试的【单条】数据，使用训练集作为训练矩阵来判断其准确率
        print("the classifier came back with: %d, the real answer is: %d"%(classifierResult,classNumStr))
        if (classifierResult != classNumStr):errorCount += 1.0 #单行if的写法，条件加括号
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: {}".format(errorCount/float(mTest)))
"""
handwritingClassTest()步骤：
1. 获取目录下的所有文件名，计算文件数量，记为m
2. 构建m行，1024列的全为零的array
3. 获取训练集文件名中表示该二进制图像所示的数字，记为classNumStr
4. 读取训练集文件，传到img2vector()函数，获取1*1024的array
5. 对测试集进行与步骤3,4相同的操作
6. 使用classify0()函数对测试集中的每项二进制图像进行分类
7. 若分类错误，记录错误次数。
8. 计算并打印错误率
"""
