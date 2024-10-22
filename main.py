from tkinter import *
from datetime import * 
from tkcalendar import Calendar, DateEntry
import tkinter.ttk
from tkinter import font
import csv

# CSV 파일 경로를 지정
CSV_FILE = "todo_list.csv"

#퍼센트 계산용 변수

total_tasks = 0
deleted_tasks = 0

# CSV 파일에서 기존 할 일 데이터를 로드
def load_csv_data():
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # 비어있지 않은 행만 처리.
                    todo_list.insert('', 'end', values=row)
    except FileNotFoundError:
        # 파일이 없으면 새로 파일이 생성될 것이기 때문에 pass
        pass

def count_tasks_in_csv():
    count = 0
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # 비어있지 않은 행만 처리
                    count += 1
    except FileNotFoundError:
        # 파일이 없으면 0을 반환
        pass
    return count


def add_work():
    global total_tasks
    total_tasks += 1
    work_name = work_entry.get()
    member = name_entry.get()
    deadline = due_date
    
    # 입력받은 데이터를 CSV 파일에 저장
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([work_name, member, deadline])

    # Entry에 입력된 내용 delete(시작인덱스, 끝인덱스)
    work_entry.delete(0, len(work_entry.get()))
    name_entry.delete(0, len(name_entry.get()))

    # 테스트코드
    print(f"추가됨 {work_name}, {member}, {deadline}")
    todo_list.insert('', 'end', values=(work_name, member, deadline))
    
    update_status_page()
    
def delete_work():
    global deleted_tasks
    deleted_tasks += 1
    selected_item = todo_list.selection()
    for item in selected_item:
        
        # Treeview에서 선택된 항목의 값을 가져옴
        work_name, member, deadline = todo_list.item(item, 'values')

        # CSV 파일에서 해당 항목을 삭제
        rows = []
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row != [work_name, member, deadline]:
                    rows.append(row)

        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        
        
        # 취소선 스타일로 변경
        todo_list.item(item, tags=('deleted',))
        todo_list.tag_configure('deleted', foreground='#c1c1c1', font=('맑은고딕', 13, 'overstrike'))
    
    update_status_page()



    # 리스트에서 선택된 내용을 딕셔너리 형태로 반환해서 출력하는 코드
    # info = todo_list.focus()
    # print(todo_list.set(info))

    # 리스트 전체 내용을 딕셔너리 형태로 반환해서 출력하는 코드
    # infos = todo_list.get_children()
    # for i in infos:
    #     print(todo_list.set(i))

    # {'text': '', 'image': '', 'values': ['role3', 'name3', '2024-09-01'], 'open': 0, 'tags': ''}
    #print(todo_list.item(info))

def printdate(event):
    # get_date() -> <class 'datetime.date'>
    global due_date
    due_date = cal.get_date()
    
def count_remaining_task():# 사람별 남은 할 일의 수를 세는 함수
    
    task_count = {}
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                name = row[1]
                if name in task_count:
                    task_count[name] += 1
                else:
                    task_count[name] = 1
    return task_count

def update_status_page():
    # 두 번째 페이지의 기존 레이블을 제거하는 코드
    for widget in frame2.winfo_children(): # frame2의 모든 자식 위젯을 리스트 형태로 반환
        # isinstance로 현재 위젯이 Label 타입인지 확인 
        if isinstance(widget, Label):
            widget.destroy()
        elif isinstance(widget,Listbox):
            widget.destroy()

    # 사람별 남은 할 일의 수를 가져와서 표시
    tasks_count = count_remaining_task()
    listbox = Listbox(frame2,selectmode='extended',width = 50,font = ('Arial', 20) ,fg="blue",yscrollcommand = scrollbar.set )

    for name, count in tasks_count.items():
        '''
        label_text = f"{name} : {count} 개"
        label = Label(frame2, text=label_text, fg="red", font=('Arial', 20))
        label.pack(anchor=W, padx=30, pady=10)
        '''
        listbox.insert(END,f"{name} : {count} 개")
    listbox.pack(side="left")

def set_color(persent):
    
    l = ["#FF0A0A","#F44336","#FFD700","#ADD46A","#4AC9DB","#8adce8"]
    if persent <= 100:
        return l[persent//20]
    else:
        return "#8adce8"
    update_status_page()
    

def circle(canvas, cx, cy, r,c):
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r,fill = c)
    

def work_persent():
    
    global total_tasks
    print(f"토탈태스크값: {total_tasks}")
    try:
        p = deleted_tasks / total_tasks * 100
        print(int(p))
        return int(p)
    except ZeroDivisionError:
        return 0
    

win = Tk()
win.title("project1")
win.geometry("800x600")

today = date.today()
# 사용자 정의 폰트 설정
custom_font = ('Arial', 12, 'bold')

notebook = tkinter.ttk.Notebook(win,width = 800,height = 600)
notebook.pack()

# 첫 번째 페이지
frame1=Frame(win)
notebook.add(frame1, text="등록")

work_label=Label(frame1, text="Role")
work_label.pack()

work_entry = Entry(frame1)
work_entry.pack()

name_label = Label(frame1,text="Name" )
name_label.pack()

name_entry = Entry(frame1)
name_entry.pack()


deadline_label = Label(frame1,text="Deadline" )
deadline_label.pack()

cal = DateEntry(frame1, selectmode='day', date_pattern = 'yyyy-MM-dd', showweeknumbers=False, firstweekday='sunday', background='darkblue', foreground='white')
cal.pack(pady=20)
cal.bind("<<DateEntrySelected>>", printdate )

add_btn = Button(frame1, text="추가", command = add_work)
add_btn.pack()


delete_btn = Button(frame1, text="삭제", command = delete_work)
delete_btn.pack()

todo_list = tkinter.ttk.Treeview(frame1, columns=("할 일", "이름", "기한"), show="headings")
todo_list.heading("할 일", text="할 일")
todo_list.heading("이름", text="이름")
todo_list.heading("기한", text="기한")



todo_list.pack()

total_tasks = count_tasks_in_csv()

# 프로그램 시작 시 CSV 파일에서 데이터를 로드
load_csv_data()


# 두 번째 페이지
frame2=Frame(win)
notebook.add(frame2, text="현황")
canvas = Canvas(frame2, width=300, height=300)
canvas.pack()

circle(canvas,150,100,85,set_color(int(work_persent())))
circle(canvas, 150, 100, 80,"WHite")

scrollbar = Scrollbar(frame2)
scrollbar.pack(side = 'left',fill = 'y')

update_status_page()
win.mainloop()