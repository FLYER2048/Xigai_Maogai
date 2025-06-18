import pandas as pd
import os
import random
import time

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
    print("\n".join([f"{i[0].split(']')[1]}\t{i[1]}题" for i in chp_cnt.items()]))
    print("题型\t题目数量\t")
    print("\n".join([f"{i[0].split(']')[1]}\t{i[1]}题" for i in types_cnt.items()]))
    print(f"总题数{len(chapters)}题")

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

# # 将数据存储到excel文件
# df.to_excel(folder_path + '\\24Q-习概总题库2.xlsx', index=False)
# stat(df)

# 将选项内容并入题干

ls = df.values.tolist()

def practice():
    '''
    无限刷题函数，无return
    '''
    cnt = 0 # 当前题数
    while True:
        q_num = random.randint(0, len(ls)-1)
        cnt += 1
        question_type, chapter, question, option, correct_answer = ls[q_num]
        
        question = question.replace("(", "（").replace(")", "）")
        option = [_[3:] for _ in option.split('\n')]
        correct_index = [ord(s[0])-65 for s in correct_answer.split('\n')]
        for i in range(4):
            if i in correct_index:
                option[i] = (option[i], True)
            else:
                option[i] = (option[i], False)

        random.shuffle(option)
        print('-'*30)
        print(f'{cnt}. [{question_type[3:]}]{question}')
        print('\n'.join([f'{chr(index + 65)}. {opt[0]}' for index, opt in enumerate(option)]))
        my_ans = input('请选择：')
        my_ans = ''.join(sorted(list(set(my_ans.upper()))))
        correct_order = ''.join([chr(index + 65) for index, opt in enumerate(option) if opt[1]])
        if my_ans == correct_order:
            print('回答正确')
            time.sleep(1)
        else:
            print('回答错误')
            print('正确答案：' + correct_order)
            # print('\n'.join([f'{chr(index + 65)}. {opt[0]}' for index, opt in enumerate(option) if opt[1]]))
            with open(folder_path+'\\错题本.txt', 'a', encoding='utf-8') as file:
                file.write(f'[{question_type[3:]}]{question}\n')
                file.write('\n'.join([f'{chr(index + 65)}. {opt[0]}' for index, opt in enumerate(option)]))
                file.write(f'\n正确答案：{correct_order}\n')
            time.sleep(3)
    
def newTK(isRandom=False):
    '''
    生成一套全新的练习题，无return
    '''
    
    if isRandom:
        random.shuffle(ls)
    ls.sort(key = lambda x: x[0])
    previous_question_type = ''
    if isRandom:
        FileSuffix = '（乱序版）'
    else:
        FileSuffix = '（顺序版）'
    
    for cnt, ls0 in enumerate(ls):
        question_type, chapter, question, option, correct_answer = ls0
        
        if previous_question_type != question_type:
            cnt = 0
            previous_question_type = question_type
            with open(f'{folder_path}\\25C-习概题库{FileSuffix}.txt', 'a', encoding='utf-8') as file:
                file.write(f'{question_type[3:]}\n')
            with open(f'{folder_path}\\25C-习概题库{FileSuffix}答案.txt', 'a', encoding='utf-8') as file:
                file.write(f'{question_type[3:]}\n')
            
        question = question.replace("(", "（").replace(")", "）")
        option = [_[3:] for _ in option.split('\n')]
        correct_index = [ord(s[0])-65 for s in correct_answer.split('\n')]
        for i in range(4):
            if i in correct_index:
                option[i] = (option[i], True)
            else:
                option[i] = (option[i], False)

        random.shuffle(option)
        correct_order = ''.join([chr(index + 65) for index, opt in enumerate(option) if opt[1]])


        with open(f'{folder_path}\\25C-习概题库{FileSuffix}.txt', 'a', encoding='utf-8') as file:
            file.write(f'{cnt+1}. {question}\n')
            if max([len(i[0]) for i in option]) <= 9: # 如果选项很短，就可以合并成两行
                file.write(f'A. {option[0][0]}\tB. {option[1][0]}\n')
                file.write(f'C. {option[2][0]}\tD. {option[3][0]}\n')
                file.write('\n')
            else:
                file.write('\n'.join([f'{chr(index + 65)}. {opt[0]}' for index, opt in enumerate(option)]))
                file.write('\n\n')
        with open(f'{folder_path}\\25C-习概题库{FileSuffix}答案.txt', 'a', encoding='utf-8') as file:
            file.write(f'{cnt+1}. {correct_order}\n')
    
def oriTK2():
    '''
    生成一套原始顺序的习题，无return
    '''
    ls.sort(key=lambda x: x[0]) # 按照题目类型的顺序排序
    for cnt, ls0 in enumerate(ls):
        question_type, chapter, question, option, correct_answer = ls0
            
        question = question.replace("(", "（").replace(")", "）")
        option = [_[3:] for _ in option.split('\n')]
        correct_index = [ord(s[0])-65 for s in correct_answer.split('\n')]
        for i in range(4):
            if i in correct_index:
                option[i] = (option[i], True)
            else:
                option[i] = (option[i], False)

        # random.shuffle(option)
        correct_order = ''.join([chr(index + 65) for index, opt in enumerate(option) if opt[1]])


        FileSuffix = '（顺序版）'
        with open(f'{folder_path}\\25C-习概题库{FileSuffix}.txt', 'a', encoding='utf-8') as file:
            file.write(f'{question}\n')
            if max([len(i[0]) for i in option]) <= 9: # 如果选项很短，就可以合并成两行
                file.write(f'A. {option[0][0]}\tB. {option[1][0]}\n')
                file.write(f'C. {option[2][0]}\tD. {option[3][0]}\n')
                file.write('\n')
            else:
                file.write('\n'.join([f'{chr(index + 65)}. {opt[0]}' for index, opt in enumerate(option)]))
                file.write('\n\n')
        with open(f'{folder_path}\\25C-习概题库{FileSuffix}答案.txt', 'a', encoding='utf-8') as file:
            file.write(f'{cnt+1}. {correct_order}\n')

def oriTK():
    '''
    输出按顺序排列的练习题，无return
    '''
    # random.shuffle(ls)
    ls.sort(key = lambda x: x[0])
    cnt = 0 # 当前题号-1
    previous_question_type = ''
    previous_chapter = ''
    for ls0 in ls:
        question_type, chapter, question, option, correct_answer = ls0
        
        if previous_question_type != question_type:
            cnt = 0
            previous_question_type = question_type
            with open(folder_path+'\\25春-习概题库（顺序版）.txt', 'a', encoding='utf-8') as file:
                file.write(f'{question_type[3:]}\n')
            with open(folder_path+'\\25春-习概题库（顺序版）答案.txt', 'a', encoding='utf-8') as file:
                file.write(f'\n{question_type[3:]}')

        if previous_chapter != chapter:
            cnt = 0
            previous_chapter = chapter
            with open(folder_path+'\\25春-习概题库（顺序版）.txt', 'a', encoding='utf-8') as file:
                file.write(f'【{chapter[4:]}】\n')
            with open(folder_path+'\\25春-习概题库（顺序版）答案.txt', 'a', encoding='utf-8') as file:
                file.write(f'\n{chapter[4:]}')

        question = question.replace("(", "（").replace(")", "）")
        option = [_[3:] for _ in option.split('\n')]
        correct_index = [ord(s[0])-65 for s in correct_answer.split('\n')]
        for i in range(len(option)):
            if i in correct_index:
                option[i] = (option[i], True)
            else:
                option[i] = (option[i], False)

        # random.shuffle(option)
        correct_order = ''.join([chr(index + 65) for index, opt in enumerate(option) if opt[1]])

        with open(folder_path+'\\25春-习概题库（顺序版）.txt', 'a', encoding='utf-8') as file:
            file.write(f'{cnt+1}. {question}\n')
            if max([len(i[0]) for i in option]) <= 9: # 如果选项很短，就可以合并成两行
                if len(option) == 4:
                    file.write(f'A. {option[0][0]}\tB. {option[1][0]}\n')
                    file.write(f'C. {option[2][0]}\tD. {option[3][0]}\n')
                    # file.write('\n')
                else:
                    # file.write(f'A. {option[0][0]}\tB. {option[1][0]}\n')
                    # file.write('\n')
                    pass
            else:
                file.write('\n'.join([f'{chr(index + 65)}. {opt[0]}' for index, opt in enumerate(option)]))
                # file.write('\n\n')
                file.write('\n')
        with open(folder_path+'\\25春-习概题库（顺序版）答案.txt', 'a', encoding='utf-8') as file:
            # file.write(f'{cnt+1}. {correct_order}\n')
            if cnt % 5 == 0:
                file.write(f'\n{cnt+1}-{cnt+5} {correct_order}')
            else:
                file.write(f' {correct_order}')
        
        cnt += 1

if __name__ == '__main__':
    print('请选择模式：1-无限刷题；2-输出乱序练习题；3-输出顺序版题库；4-输出顺序版题库(24C习概方法)')
    cmd = input()
    if cmd == '1':
        practice()
    elif cmd == '2':
        newTK(isRandom=True)
    elif cmd == '3':
        newTK(isRandom=False)
    elif cmd == '4':
        oriTK()