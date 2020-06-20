import random
import tkinter as tk
import copy

table = []


def generate():
    global table
    for i in range(81):
        table.append('.')
    for i in range(11):
        i = random.randint(0, 80)
        exclude = {table[j] for j in range(81) if same_row(i, j) or same_col(i, j) or same_block(i, j)}
        avail = set('123456789') - exclude
        table[i] = random.choice(tuple(avail))


def same_row(i, j): return (i // 9 == j // 9)


def same_col(i, j): return (i - j) % 9 == 0


def same_block(i, j): return (i // 27 == j // 27 and i % 9 // 3 == j % 9 // 3)


flag = False
Template = []


def solveSudoku(table):
    global flag
    global Template
    ans = []
    idx = table.index('.') if '.' in table else -1
    if idx == -1:
        flag = True
        Template = table
        for i in range(9):
            for j in range(9):
                print(Template[i * 9 + j], end=' ')
            print('\n')
        print("--------------------------")
        return [table]
    exclude = {table[j] for j in range(81) if same_row(idx, j) or same_col(idx, j) or same_block(idx, j)}
    for m in set('123456789') - exclude:
        ans += solveSudoku(table[:idx] + [m] + table[idx + 1:])
        if flag == True:
            return ans
    return ans


def checkUniqueness(table):
    idx = table.index('.') if '.' in table else -1
    global flag
    if idx == -1:
        if not flag:
            flag = True
            return True
        else:
            return False
    exclude = {table[j] for j in range(81) if same_row(idx, j) or same_col(idx, j) or same_block(idx, j)}
    candidates = set('123456789') - exclude
    for m in candidates:
        if not checkUniqueness(table[:idx] + [m] + table[idx + 1:]):
            return False
    return True


def set_ques(table):
    result = copy.deepcopy(table)
    for i in range(40):
        x = random.randint(0, 80)
        while result[x] == '.':
            x = random.randint(0, 80)
        result[x] = '.'
    return result


def judge(table, var1):
    for i in range(81):
        if Template[i] == '.':
            table[i] = blank[i].get()
    for i in range(81):
        if table[i] == '':
            var1.set('Please finish')
            return
    for i in range(81):
        exclude = {table[j] for j in range(81)
                   if i != j if same_row(i, j) or same_col(i, j) or same_block(i, j)}
        if table[i] in exclude:
            print("False")
            var1.set('Result:False')
            return
    print("True")
    var1.set('Result:True')


blank = []


def gui():
    global Template
    window = tk.Tk()
    window.configure(background='dimgray')
    window.title('Sudoku')
    table2 = Template.copy()
    var1 = tk.StringVar()
    var1.set('Result:')
    global blank
    for i in range(81):
        if Template[i] == '.':
            blank.append(tk.Entry(window, font=("Calibri", 20), width=5, justify='center', bg='springgreen', fg='red2'))
            blank[i].grid(row=i // 9, column=i % 9, ipady=10)
            if i % 9 < 3 or i % 9 > 5:
                if i // 9 >= 3 and i // 9 < 6:
                    blank[i].configure(background='lightskyblue1')
            else:
                if i // 9 < 3 or i // 9 > 5:
                    blank[i].configure(background='lightskyblue1')
        else:
            blank.append(tk.Label(window, font=("Calibri", 20), text=Template[i], bg='springgreen2'))
            blank[i].grid(row=i // 9, column=i % 9, ipadx=26, ipady=10, padx=5, pady=5)
            if i % 9 < 3 or i % 9 > 5:
                if i // 9 >= 3 and i // 9 < 6:
                    blank[i].configure(background='lightskyblue2')
            else:
                if i // 9 < 3 or i // 9 > 5:
                    blank[i].configure(background='lightskyblue2')
    label1 = tk.Label(window, textvariable=var1, bg='dimgray', font=("Calibri", 30)).grid(columnspan=9, rowspan=3)
    button1 = tk.Button(window, width=15, activebackground='lightgoldenrod', bg='goldenrod', font=("Calibri", 15),
                        text="Done", command=lambda: judge(table2, var1)).grid(columnspan=9, rowspan=3)
    boutton2 = tk.Button(window, width=15, activebackground='lightgoldenrod', bg='goldenrod', font=("Calibri", 15),
                         text="Restart", command=lambda: [window.destroy(), clear(), main()]).grid(columnspan=9,
                                                                                                   rowspan=3)
    window.mainloop()


def clear():
    global table
    global Template
    global blank
    global flag
    flag = False
    table.clear()
    Template.clear()
    blank.clear()


def main():
    global flag
    global Template
    generate()
    ans = solveSudoku(table)
    tmp = set_ques(Template)
    flag = False
    while not checkUniqueness(tmp):
        flag = False
        tmp = set_ques(Template)
    Template = copy.deepcopy(tmp)
    gui()


if __name__ == '__main__':
    main()
