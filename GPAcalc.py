#coding:utf-8
#计算GPA的工具

class GPAcalc:
    def __init__(self,scores):
        self.scores=scores
##        [
##            ["课程名",学分数,成绩("A-"),是否为Major(可不填，默认True)],
##            ["课程名",学分数,成绩("A-")],
##            ["课程名",学分数,成绩("A-")],
##            ...
##        ]
    def calc_rank(self,major=False):
        #计算以等第制(A,A-,B+,B,...)表示的成绩的GPA。major=True时不计算score中带有False标记的成绩
        #即major=True只计算主课的成绩。不是主课的在scores输入中用False标记
        score_sum=0
        credit_sum=0
        score_mapping={
            'A':4,
            'A-':3.7,
            'B+':3.3,
            'B':3,
            'B-':2.7,
            'C+':2.3,
            'C':2,
            'C-':1.7,
            'D':1.3,
            'D-':1,
            'F':0,
            #'P':raise,
            #'NP':raise,
            }
        if major:#只计算主课的成绩。不是主课的在scores输入中用False标记
            for item in self.scores:
                if (len(item)==3 or item[3]==True):    #是主课
                    score=item[2].upper()   #一门课的成绩
                    credit=int(item[1])
                    #下面检查输入成绩是否正常
                    if score in score_mapping:
                        score_sum+=score_mapping[score]*credit
                        credit_sum+=credit
                    else:
                        print('成绩为P/NP,或输入有误,已忽略:',item)
                else:   #不是主课
                    print('已忽略副课:',item)
        else:#计算所有课的成绩，不管是否被标记为主课
            for item in self.scores:
                #if len(item)==3 or item[3]==True:    #是主课
                    score=item[2].upper()   #一门课的成绩
                    credit=int(item[1])
                    #下面检查输入是否正常
                    if score in score_mapping:
                        score_sum+=score_mapping[score]*credit
                        credit_sum+=credit
                    else:
                        print('成绩为P/NP,或输入有误,已忽略:',item)
                #else:   #不是主课
                    #print('已忽略课程:',item)

        GPA=score_sum/credit_sum
        #print('GPA:',GPA)
        return GPA
            
    def calc_five(self,major=False):
        #计算五分制表示的成绩
        pass
    def calc_hundred(self,major=False):
        #计算百分制表示的成绩
        pass
if __name__=='__main__':
    scores=[
        ['工程数学',4,'A-'],
        ['数字逻辑基础',4,"A-"],
        ['电子系统设计',2,'A'],
        ['多媒体技术',2,'A'],
        ['科技英语',2,'A-'],
        ['概率、数理统计与随机过程',4,'B'],
        ['模拟电子线路',5,'A'],
        ['模拟电子学基础',4,'A'],
        ['形势与政策IV',0.5,'P'],
        ['形势与政策III',0.5,'P'],
        ['形势与政策II',0.5,'P'],
        ['形势与政策I',0.5,'P'],
        ['大学英语III',2,'P'],
        ['军事理论',1,'C',False],
        ['大学物理B(上)',4,'B+'],
        ['中国近现代史纲要',2,'A-',False],
        ['学术英语（管理科学）',2,'A-'],
        ['创伤与急救',2,'A-',False],
        ['环境与人群健康',2,'A',False],
    ]
    c=GPAcalc(scores)
    print('GPA:',c.calc_rank(major=True))
