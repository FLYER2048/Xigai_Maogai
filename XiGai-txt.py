import pandas as pd
import os
import datetime

path = os.path.abspath(__file__)
folder_path = os.path.dirname(path)

ChapterNum = {
    '导论': '00',
    '第一章': '01', 
    '第二章': '02', 
    '第三章': '03', 
    '第四章': '04', 
    '第五章': '05', 
    '第六章': '06', 
    '第七章': '07', 
    '第八章': '08', 
    '第九章': '09', 
    '第十章': '10', 
    '第十一章': '11', 
    '第十二章': '12', 
    '第十三章': '13', 
    '第十四章': '14', 
    '第十五章': '15', 
    '第十六章': '16', 
    '第十七章': '17',
    '二十届三中全会': '99'
}

def isOption(ss):
    if ss in ['', '\n']:
        return False
    ls = ['【', 'Selected Answer:', 'Incorrect [None Given]', 'Answers:', 'Question ', ' out of ']
    for i in ls:
        if i in ss:
            return False
    return True


def stat(df):
    chapters = df['章节']
    types = df['题型']
    chp_cnt = {}
    types_cnt = {}
    for i in chapters:
        chp_cnt[i] = chp_cnt.get(i, 0) + 1
    for i in types:
        types_cnt[i] = types_cnt.get(i, 0) + 1
    
    print("章节号\t题目数量\t")
    print("\n".join([f"{_[0].split(']')[1]}\t{_[1]}题" for _ in chp_cnt.items()]))
    print("题型\t题目数量\t")
    print("\n".join([f"{_[0].split(']')[1]}\t{_[1]}题" for _ in types_cnt.items()]))
    print(f"总题数{len(chapters)}题")

def get_sep(answer_txt):
    '''
    返回一个合适的分隔符号。
    如果答案中没有点号，则使用顿号连接；
    如果含有顿号，则使用逗号；
    如果含有逗号，则使用分号。
    '''
    if '，' in answer_txt:
        return '；'
    elif '、' in answer_txt:
        return '，'
    else:
        return '、'

# 读取文件内容
with open(folder_path+'\\tk2.txt', 'r', encoding='utf-8') as file:
    content = file.readlines()

# 初始化存储数据的列表
chapters = []
questions = []
options = []
correct_answers = []

# 解析文件内容
current_question = "" # 现在题目题干
current_options = "" # 现在题目选项
current_correct_answer = "" # 现在题目正确选项
Ans_Flag = False
option_Cnt = 0 # 标记当前的选项是第几个

for line in content:
    # 找到题目
    if '【' in line:
        if current_question != "": # 如果有内容，就添加
            chapters.append(current_chapter)
            questions.append(current_question)
            options.append(current_options.strip())
            correct_answers.append(current_correct_answer.strip())
            current_chapter = ""
            current_question = ""
            current_options = ""
            current_correct_answer = ""
            option_Cnt = 0
            Ans_Flag = False
        # 获取题干
        current_question = line.strip().replace('Incorrect', '').replace('Correct ', '').replace('Correct', '').replace('"', '').replace(' ', '')#.split('Question ')[1].strip()
        current_chapter = current_question.split('】')[0][1:]
        current_chapter = "[" + str(ChapterNum[current_chapter]) + "]" + current_chapter
        current_question = current_question.split('】')[1]
    # 找到答案选项
    elif 'Answers:' in line and "Selected" not in line: # 找到正确答案区域的开始位置
        Ans_Flag = True
    elif Ans_Flag and isOption(line):
        option_Cnt += 1
        current_options += chr(option_Cnt + 64) + ". " + \
            line.strip().replace('Incorrect', '').replace('Correct ', '').replace('Correct', '') + "\n"
        # 找到正确答案
        if 'Correct' in line:
            current_correct_answer += chr(option_Cnt + 64) + ". " + \
                line.split('Correct')[1].strip() + "\n"



# 处理最后一个问题
chapters.append(current_chapter)
questions.append(current_question)
options.append(current_options.strip())
correct_answers.append(current_correct_answer.strip())

# 检测题目类型
question_types = []
for i in correct_answers:
    if '\n' in i:
        question_types.append("[3]多选题")
    elif 'A. True' in i or 'B. False' in i:
        question_types.append("[2]判断题")
    else:
        question_types.append("[1]单选题")

# 创建DataFrame
df = pd.DataFrame({'题型': question_types, '章节': chapters, '题干': questions, '选项': options, '正确答案': correct_answers})

# 按照章节升序排序并去重
df = df.sort_values(by='章节').drop_duplicates()

# 将数据存储到excel文件
df.to_excel(folder_path + '\\25C-习概总题库2.xlsx', index=False)
stat(df)

# 将选项内容并入题干
with open(folder_path + '\\25C-习概总题库2.md', 'w', encoding='utf-8') as file:
    ls = df.values.tolist()
    previous_chp = ''
    cnt = 1 # 章节内题号
    for i in ls:
        question_type, chapter, question, option, correct_answer = i
        
        if previous_chp != chapter: # 某一章节的第一题之前，输出章节名称
            file.write(f'## {chapter[4:]}\n\n')
            cnt = 1 # 章节内题号重置
        previous_chp = chapter
        
        question = question.replace("(", "（").replace(")", "）")
        correct_answers = [' **'+_[3:]+'** ' for _ in correct_answer.split('\n')]
        
        sep = get_sep(''.join(correct_answers)) # 获取适合的分隔符号

        if question.count('（）') == 1: # 只有一个空，所有答案用顿号连接，填入其中
            entry = question.replace("（）", sep.join(correct_answers))
        elif question.count('（）') == 0: # 没有空，则答案直接置于题干后
            entry = question + sep.join(correct_answers)
        else:
            # 有多个空的情况，依次填入
            q1 = question.split('（）') + [""] # 避免越界
            entry = ''
            for i in range(len(correct_answers)):
                entry += q1[i] + correct_answers[i]
            entry += q1[i + 1]
        
        file.write(f'{cnt}. {entry}\n\n')
        cnt += 1
    file.write(f'导出时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  总题数：{len(ls)}')
# 记录题目数量变化
with open(folder_path + '\\tk2_cnt.txt', 'a', encoding='utf-8') as file:
    file.write(str(len(ls)) + '\n')