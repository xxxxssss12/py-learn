# -*- coding: UTF-8 -*-
"""
1、有一群鸡和一群兔，它们的只数相同，它们的脚数都是三位数，且这两个三位数的数字分别是0，1，2，3，4，5。问鸡和兔的只数各是多少?它们的脚数各是多少?
"""
for chickens in range(50,500):
    chickjiao = chickens * 2
    rabbitjiao = chickens * 4
    if chickjiao > 999 or rabbitjiao > 999:
        print(chickjiao, rabbitjiao)
        break
    jgw=(chickens*2)%10
    jsw = (chickens * 2)//10%10
    jbw=(chickens*2)//100
    rgw = (chickens * 4) % 10
    rsw = (chickens * 4) // 10 % 10
    rbw = (chickens * 4) // 100
    arr=[0,0,0,0,0,0,0,0,0,0]
    arr[jgw] = 1
    arr[jsw] = 1
    arr[jbw] = 1
    arr[rgw] = 1
    arr[rsw] = 1
    arr[rbw] = 1
    print (chickjiao, rabbitjiao)
    print(arr)
    success = True
    for i in range(0,6):
        if arr[i] == 0:
            success = False
            break
    if success:
        print("chicken jiao=", chickens*2, "rabbit jiao=", chickens * 4)

"""
2、有一个三位数，个位数字比百位数字大，而百位数字又比十位数字大，并且各位数字之和等于各位数字相乘之积，求此三位数。
3、蜘蛛有8条腿，蜻蜓有6条腿和2对翅，蝉有6条腿和1对翅。三种虫子共18共，共有118条腿和20对翅。问每种虫子各几只？
4、甲、乙两数的和为168，甲数的八分之一与乙数的四分之三的和为76，求甲、乙两数各是多少？
5、我国古代数学问题：1兔换2鸡，2兔换3鸭，5兔换7鹅。某人用20只兔换得鸡、鸭、鹅共30只，问其中鸡、鸭、鹅各几只？
6.某年级的同学集体去公园划船，如果每只船坐10人，那么多出2个座位；如果每只船多坐2人，那么可少租1只船，这样，共需要租几只船？
7.松鼠妈妈采松果，晴天每天可采20个，雨天每天可采12个。它一连几天采了112个松果，平均每天采14个。问这些天中有几天下雨？
8.一辆汽车共载客 50人，其中一部分人买 A种票，每张 0.80元；另一部分人买 B种票，每张 0.30元。售票员最后统计出：所卖的 A种票比卖 B种票多收入 18元。买 A种票的有多少人？
9.设计一个程序，将1～9这九个数字组成的三个三位的平方数，要求每个数字只准使用一次。
10、有36块砖，有36个人，男的每次可搬4块，女的每次可搬3块，2个小孩可以每次抬1块。请问：36块砖如果要一次搬完，需要多少男的、女的和小孩？
11、把一元钞票换成一分、二分、五分硬币（每种至少一枚），有多少种换法？
"""