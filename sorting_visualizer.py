import sys
import tkinter
import tkinter.font
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import random
import queue

VICT_COLOR = 'indian red'
COMP_COLOR = 'cyan'
TARG_COLOR = 'sea green'

# GUI 기본 설정
root = tkinter.Tk()
root.title("Sorting Visualizer")
root.geometry('925x600+100+100')
root.resizable(False, False)
root.config(bg='light slate grey')

DATA_SIZE = 30
DATA_INTRV = 1

running = queue.Queue()

# 프로그램 폰트
FONT = tkinter.font.Font(family="Consolas", size=10, weight='bold')

def SVReset():
    global cnt_bubble, cnt_insert, cnt_select, cnt_merge, cnt_heap, cnt_quick
    cnt_bubble, cnt_insert, cnt_select, cnt_merge, cnt_heap, cnt_quick = 0, 0, 0, 0, 0, 0
    count_bubble.set("비교 {0:04d}회".format(cnt_bubble))
    count_insert.set("비교 {0:04d}회".format(cnt_insert))
    count_select.set("비교 {0:04d}회".format(cnt_select))
    count_merge.set("비교 {0:04d}회".format(cnt_merge))
    count_heap.set("비교 {0:04d}회".format(cnt_heap))
    count_quick.set("비교 {0:04d}회".format(cnt_quick))

    _arr = data_create(DATA_SIZE, DATA_INTRV)
    arr.set(_arr)
    for i in range(len(svcanvas.svdata)):
        svcanvas.svdata[i].set(_arr)

    showAll()


def sort_bg(sort):
    bg = 'white'
    if sort == 'bubble_sort': bg = '#f5a8ca'
    if sort == 'insertion_sort': bg = '#f8963e'
    if sort == 'selection_sort': bg = '#b6d994'
    if sort == 'merge_sort': bg = '#92b5df'
    if sort == 'heap_sort': bg = 'medium purple'
    if sort == 'quick_sort': bg = '#6f5d03'

    return bg


""" =============== Data =============== """


class SVData:
    def __init__(self, data):
        self.data = list(data)
        self.data_backup = list(data)
        self.color = ['white'] * self.__len__()

    def __len__(self):
        return len(self.data)

    def set(self, data):
        self.data = list(data)
        self.data_backup = list(data)
        self.color = ['white'] * self.__len__()

    def copy(self):
        _new = SVData(self.data)
        return _new

    def reset_color(self):
        self.color = ['white'] * self.__len__()

    def reset_data(self):
        self.data = list(self.data_backup)


""" =============== Multi Canvas =============== """


class SVCanvas:
    def __init__(self):
        self.sort_type = []
        self.canvas_data = []
        self.svdata = []

        self.ax = []

    def contains(self, sort):
        return self.sort_type.__contains__(sort)

    def add(self, sort):
        bg = sort_bg(sort)
        canvas = tkinter.Canvas(frame_data, width=1, height=1, bg=bg)
        if data_type != 'cubicData':
            canvas.pack(fill='both', expand=True)
            canvas.update()

        self.sort_type.append(sort)
        self.canvas_data.append(canvas)
        self.svdata.append(arr.copy())

        self.ax = check_axes()

    def remove(self, sort):
        for i in range(len(self.sort_type)):
            if self.sort_type[i] == sort:
                self.delete(i)
                break

    def delete(self, index):
        self.sort_type.pop(index)
        self.canvas_data[index].destroy()
        self.canvas_data.pop(index)
        self.svdata.pop(index)

        self.ax = check_axes()

        if len(svcanvas.sort_type) == 0:
            canvas_cubic.get_tk_widget().pack_forget()

    def reset_data(self):
        for i in range(len(self.svdata)):
            self.svdata[i].reset_data()


""" =============== Create Data =============== """


def data_create(size, intrv=1):
    minn = intrv
    maxn = (size + 1) * intrv

    arr = [i for i in range(minn, maxn, intrv)]
    random.shuffle(arr)

    return arr


""" =============== Show Data =============== """


def showAll():
    if check_frame() != 'cubicData':
        for i in range(len(svcanvas.canvas_data)):
            showData(svcanvas.canvas_data[i], svcanvas.svdata[i], 0, False)
    else:
        for i in range(len(svcanvas.ax)):
            cubicData(svcanvas.ax[i], svcanvas.svdata[i])


def check_frame():
    global prev
    to = data_type.get()

    if len(svcanvas.sort_type) == 0:
        change_state('normal')
        return

    if len(svcanvas.sort_type) == 1:
        if to == 'cubicData':
            ctn_bubble.configure(state='disabled')
            ctn_insert.configure(state='disabled')
            ctn_select.configure(state='disabled')
            ctn_merge.configure(state='disabled')
            ctn_heap.configure(state='disabled')
            ctn_quick.configure(state='disabled')
            selected = svcanvas.sort_type[0]
            if 'bubble' in selected:
                ctn_bubble.configure(state='normal')
            elif 'insert' in selected:
                ctn_insert.configure(state='normal')
            elif 'select' in selected:
                ctn_select.configure(state='normal')
            elif 'merge' in selected:
                ctn_merge.configure(state='normal')
            elif 'heap' in selected:
                ctn_heap.configure(state='normal')
            elif 'quick' in selected:
                ctn_quick.configure(state='normal')
        elif prev == 'cubicData':
            change_state('normal')
        else:
            rad3.configure(state='normal')

    else:
        rad3.configure(state='disabled')

    if to == 'cubicData':
        for i in range(len(svcanvas.canvas_data)):
            svcanvas.canvas_data[i].pack_forget()
        canvas_cubic.get_tk_widget().pack(fill='both', expand=True)

    elif prev == 'cubicData':
        canvas_cubic.get_tk_widget().pack_forget()
        for i in range(len(svcanvas.canvas_data)):
            svcanvas.canvas_data[i].pack(fill='both', expand=True)

    root.update()
    prev = to
    return to


def check_axes():
    ax = []
    cnt = len(svcanvas.sort_type)

    svfig.clf()
    for i in range(0, cnt):
        _ax = svfig.add_subplot((cnt - 1) // 3 + 1, cnt if cnt < 3 else 3, i + 1, projection='3d')
        _ax.patch.set_facecolor(sort_bg(svcanvas.sort_type[i]).replace(' ', ''))
        _ax.patch.set_edgecolor('white')
        _ax.patch.set_linewidth(1)
        _ax.set_axis_off()

        ax.append(_ax)

    svfig.tight_layout()
    canvas_cubic.draw()

    return ax


def showData(canvas, svdata, t, reset):
    exec(data_type.get() + "(canvas, svdata)")
    time.sleep(t)
    if reset is True:
        svdata.reset_color()


def drawData(canvas, svdata):
    # 기존 canvas의 내용 삭제
    canvas.delete("all")

    # 각 데이터의 크기 설정
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    blank_space = 5
    rect_width = (width - blank_space) / (svdata.__len__())

    maxn = max(svdata.data)
    weight = (height - 10) / maxn

    # svdata 값을 시각화
    for index, value in enumerate(svdata.data):
        x0 = rect_width * index + blank_space
        y0 = height - 5 - (value * weight)

        x1 = rect_width * (index + 1)
        y1 = height - 5

        canvas.create_rectangle(x0, y0, x1, y1, fill=svdata.color[index], outline=svdata.color[index])


def printData(canvas, svdata):
    # 기존 canvas의 내용 삭제
    canvas.delete("all")

    # 각 데이터의 크기 설정
    w = 0
    height = 10

    # svdata 값을 시각화, 줄당 30개의 텍스트 데이터 표시
    for index, value in enumerate(svdata.data):
        canvas.create_rectangle((index - w) * 30 + 5, height - 5, (index - w + 1) * 30 + 5, height + 10,
                                fill=svdata.color[index])
        canvas.create_text((index - w) * 30 + 20, height + 2, text=value, font=FONT, fill="black", width=30)

        if (index + 1) % 30 == 0:
            w = index + 1
            height += 20


def cubicData(ax, svdata):
    for artist in ax.collections:
        artist.remove()

    for index, value in enumerate(svdata.data):
        ax.bar3d(index, index, 0, 1, 1, value, color=svdata.color[index].replace(' ', ''), edgecolor='black')

    canvas_cubic.draw()


""" =============== Start Sort =============== """


def start_sort():
    # 정렬을 시작한 후 데이터 제어가 불가능하도록 변경
    change_state('disabled')

    # 다중 정렬을 위해 여러 개의 스레드 사용
    for i in range(len(svcanvas.canvas_data)):
        if data_type.get() != 'cubicData':
            th = Thread(target=getattr(sys.modules[__name__], svcanvas.sort_type[i]),
                        args=(svcanvas.canvas_data[i], svcanvas.svdata[i]))
        else:
            th = Thread(target=getattr(sys.modules[__name__], svcanvas.sort_type[i]),
                        args=(svcanvas.ax[i], svcanvas.svdata[i]))
        th.daemon = True
        th.start()

        # 정렬 중임을 알림
        running.put(svcanvas.sort_type[i])

    # 모든 정렬이 끝났는지 0.2초 단위로 확인
    th = Thread(target=check_end)
    th.daemon = True
    th.start()


def check_end():
    if running.empty():
        # 모든 정렬이 끝나면 데이터 제어가 가능하도록 변경
        change_state('normal')
    else:
        # 모든 정렬이 끝났는지 0.2초 단위로 확인
        time.sleep(0.2)
        th = Thread(target=check_end)
        th.daemon = True
        th.start()


def change_state(state):
    ctn_bubble.configure(state=state)
    ctn_insert.configure(state=state)
    ctn_select.configure(state=state)
    ctn_merge.configure(state=state)
    ctn_heap.configure(state=state)
    ctn_quick.configure(state=state)
    btn_start.configure(state=state)
    btn_reset.configure(state=state)


""" =============== Check Sort Algos =============== """


def check_sort():
    if ctn_var_bubble.get() == 1 and not svcanvas.contains('bubble_sort'):
        svcanvas.add('bubble_sort')
    elif ctn_var_bubble.get() == 0:
        svcanvas.remove('bubble_sort')

    if ctn_var_insert.get() == 1 and not svcanvas.contains('insertion_sort'):
        svcanvas.add('insertion_sort')
    elif ctn_var_insert.get() == 0:
        svcanvas.remove('insertion_sort')

    if ctn_var_select.get() == 1 and not svcanvas.contains('selection_sort'):
        svcanvas.add('selection_sort')
    elif ctn_var_select.get() == 0:
        svcanvas.remove('selection_sort')

    if ctn_var_merge.get() == 1 and not svcanvas.contains('merge_sort'):
        svcanvas.add('merge_sort')
    elif ctn_var_merge.get() == 0:
        svcanvas.remove('merge_sort')

    if ctn_var_heap.get() == 1 and not svcanvas.contains('heap_sort'):
        svcanvas.add('heap_sort')
    elif ctn_var_heap.get() == 0:
        svcanvas.remove('heap_sort')

    if ctn_var_quick.get() == 1 and not svcanvas.contains('quick_sort'):
        svcanvas.add('quick_sort')
    elif ctn_var_quick.get() == 0:
        svcanvas.remove('quick_sort')

    showAll()


""" =============== Bubble Sort =============== """


def bubble_sort(canvas, svdata):
    # 기본 설정
    global cnt_bubble
    cnt_bubble = 0
    data = svdata.data

    # 버블 정렬
    size = len(data)
    for i in range(0, size):
        for j in range(0, size - i - 1):
            # 정렬이 된 데이터는 lime green, 기준 데이터는 VICT_COLOR, 비교 데이터는 COMP_COLOR 색으로 지정
            for k in range(size - i, size):
                svdata.color[k] = "lime green"
            svdata.color[j] = VICT_COLOR
            svdata.color[j + 1] = COMP_COLOR
            showData(canvas, svdata, 0.01, True)

            # 데이터 비교
            cnt_bubble += 1
            count_bubble.set("비교 {0:04d}회".format(cnt_bubble))
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]

                # 데이터 교환 후 데이터 시각화
                for k in range(size - i, size):
                    svdata.color[k] = "lime green"
                svdata.color[j] = COMP_COLOR
                svdata.color[j + 1] = VICT_COLOR
                showData(canvas, svdata, 0.01, True)

    # 정렬이 끝나고 데이터 시각화
    for i in range(0, size):
        svdata.color[i] = "lime green"
        showData(canvas, svdata, 0.01, False)
    svdata.reset_color()

    running.get()


""" =============== Insertion Sort =============== """


def insertion_sort(canvas, svdata):
    # 기본 설정
    global cnt_insert
    cnt_insert = 0
    data = svdata.data

    # 삽입 정렬
    size = len(data)
    for i in range(1, size):
        # 이전의 데이터와 한 번 비교
        j = i - 1
        cnt_insert += 1
        count_insert.set("비교 {0:04d}회".format(cnt_insert))
        while j >= 0 and data[j + 1] < data[j]:
            # 기준 데이터를 VICT_COLOR 색으로 시각화
            svdata.color[j + 1] = VICT_COLOR
            showData(canvas, svdata, 0.01, True)

            # 기준 데이터를 비교 데이터 위치에 삽입(데이터 시각화를 위해 삽입이 아닌 교환을 사용함)
            data[j + 1], data[j] = data[j], data[j + 1]
            j -= 1

            # 기준 데이터가 삽입되고 VICT_COLOR 색으로 시각화
            svdata.color[j + 1] = VICT_COLOR
            showData(canvas, svdata, 0.01, True)

            # 비교 데이터의 인덱스가 0 이상이면 한 번 더 비교
            if j > -1:
                cnt_insert += 1
                count_insert.set("비교 {0:04d}회".format(cnt_insert))

        # 기준 데이터의 삽입이 끝났음을 lime green 색으로 데이터 시각화
        svdata.color[j + 1] = "lime green"
        showData(canvas, svdata, 0.1, True)

    # 정렬이 끝나고 데이터 시각화
    for i in range(0, size):
        svdata.color[i] = "lime green"
        showData(canvas, svdata, 0.01, False)
    svdata.reset_color()

    running.get()


""" =============== Selection Sort =============== """


def selection_sort(canvas, svdata):
    # 기본 설정
    global cnt_select
    cnt_select = 0
    data = svdata.data

    # 선택 정렬
    size = len(data)
    for i in range(0, size - 1):
        min_index = i
        for j in range(i + 1, size):
            # 바꿀 데이터보다 비교 데이터가 작으면 인덱스 변경
            cnt_select += 1
            count_select.set("비교 {0:04d}회".format(cnt_select))
            if data[min_index] > data[j]:
                min_index = j

            # 기준 데이터는 VICT_COLOR, 바꿀 데이터는 TARG_COLOR, 비교 데이터는 COMP_COLOR 색으로 지정
            svdata.color[i] = VICT_COLOR
            svdata.color[j] = COMP_COLOR
            if i != min_index:
                svdata.color[min_index] = TARG_COLOR

            # 데이터 시각화
            showData(canvas, svdata, 0.01, True)

        # 데이터 교환 및 데이터 시각화
        data[i], data[min_index] = data[min_index], data[i]

        svdata.color[i] = TARG_COLOR
        svdata.color[min_index] = VICT_COLOR
        showData(canvas, svdata, 0.1, True)

    # 정렬이 끝나고 데이터 시각화
    for i in range(0, size):
        svdata.color[i] = "lime green"
        showData(canvas, svdata, 0.01, False)
    svdata.reset_color()

    running.get()


""" =============== Merge Sort =============== """


def merge_sort(canvas, svdata):
    # 기본 설정
    global cnt_merge
    cnt_merge = 0

    # 병합 정렬
    _merge_sort(canvas, svdata, 0, len(svdata.data) - 1)

    # 정렬이 끝나고 데이터 시각화
    for i in range(0, len(svdata.data)):
        svdata.color[i] = "lime green"
        showData(canvas, svdata, 0.01, False)
    svdata.reset_color()

    running.get()


def _merge_sort(canvas, svdata, left, right):
    # 분할된 데이터 위치 확인
    if left >= right:
        return

    # 데이터 분할(전체 데이터를 시각화하기 위해 전체 데이터와 분할될 데이터의 위치를 넘김)
    mid = (left + right) // 2
    _merge_sort(canvas, svdata, left, mid)
    _merge_sort(canvas, svdata, mid + 1, right)

    # 병합 정렬(전체 데이터를 시각화하기 위해 전체 데이터와 분할된 데이터의 위치를 넘김)
    _merge(canvas, svdata, left, mid, right)


def _merge(canvas, svdata, left, mid, right):
    # 기본 설정
    global cnt_merge
    data = svdata.data

    # 분할된 리스트를 light steel blue 색으로 데이터 시각화
    for index in range(left, right + 1):
        svdata.color[index] = "light steel blue"
    showData(canvas, svdata, 0.1, False)

    # 데이터 분할
    left_data = data[left:mid + 1]
    right_data = data[mid + 1:right + 1]

    # 병합 정렬(i는 왼쪽 데이터의 위치, j는 오른쪽 데이터의 위치, k는 데이터가 들어갈 위치)
    # 전체 데이터 시각화를 위해 분할된 데이터를 정렬해서 병합하는 것이 아닌 데이터 위치 교환 사용
    i, j = 0, 0
    for k in range(left, right + 1):
        # 분할된 데이터 중 정렬이 완료된 데이터는 lime green, 정렬할 데이터는 light steel blue 색으로 지정
        for index in range(left, right + 1):
            if index < left + i + j:
                svdata.color[index] = "lime green"
            else:
                svdata.color[index] = "light steel blue"

        # 양쪽 데이터가 남아있을 경우
        if i < len(left_data) and j < len(right_data):
            cnt_merge += 1
            count_merge.set("비교 {0:04d}회".format(cnt_merge))

            # 왼쪽 데이터가 작을 경우
            if left_data[i] <= right_data[j]:
                for min_index in range(left, right + 1):
                    if data[min_index] == left_data[i]:
                        targ = left_data[i] if data[k] != data[min_index] else -1
                        break
                i += 1

            # 오른쪽 데이터가 작을 경우
            else:
                for min_index in range(left, right + 1):
                    if data[min_index] == right_data[j]:
                        targ = right_data[j] if data[k] != data[min_index] else -1
                        break
                j += 1

        # 왼쪽 데이터만 남아있을 경우
        elif i < len(left_data):
            for min_index in range(left, right + 1):
                if data[min_index] == left_data[i]:
                    targ = left_data[i] if data[k] != data[min_index] else -1
                    break
            i += 1

        # 오른쪽 데이터만 남아있을 경우
        else:
            for min_index in range(left, right + 1):
                if data[min_index] == right_data[j]:
                    targ = right_data[j] if data[k] != data[min_index] else -1
                    break
            j += 1

        # 데이터 병합(데이터 시각화를 위해 데이터 위치 교환 사용)
        if targ != -1:
            # 데이터가 들어갈 위치는 VICT_COLOR, 들어갈 데이터는 COMP_COLOR 색으로 데이터 시각화
            svdata.color[k] = VICT_COLOR
            svdata.color[min_index] = COMP_COLOR
            showData(canvas, svdata, 0.05, False)

            # 데이터 위치 교환
            data[min_index] = data[k]
            data[k] = targ

            # 데이터가 들어간 위치는 COMP_COLOR, 기존 데이터는 VICT_COLOR 색으로 데이터 시각화
            svdata.color[k] = COMP_COLOR
            svdata.color[min_index] = VICT_COLOR
            showData(canvas, svdata, 0.05, True)
        # 이미 기존 데이터 위치에 들어갈 데이터가 있다면 lime green 색으로 데이터 시각화
        else:
            svdata.color[k] = "lime green"
            showData(canvas, svdata, 0.05, True)


""" =============== Heap Sort =============== """


def heap_sort(canvas, svdata):
    # 기본 설정
    global cnt_heap
    cnt_heap = 0
    data = svdata.data

    # 힙 트리로 만들기
    size = len(data)
    for i in range((size // 2) - 1, -1, -1):
        _heap_sort(canvas, svdata, size, i)

    # 힙 트리가 완성된 후 루트에 있는 데이터를 가장 뒤에서부터 채운 뒤 다시 힙 트리로 만듦
    for i in range(size - 1, 0, -1):
        # 루트 데이터는 VICT_COLOR, 교환할 데이터는 TARG_COLOR 색으로 데이터 시각화
        svdata.color[0] = VICT_COLOR
        svdata.color[i] = TARG_COLOR
        showData(canvas, svdata, 0.1, False)

        # 데이터 교환 및 데이터 시각화
        data[i], data[0] = data[0], data[i]

        svdata.color[0] = TARG_COLOR
        svdata.color[i] = VICT_COLOR
        showData(canvas, svdata, 0.1, True)

        # 데이터 교환 후 깨진 힙 트리를 다시 힙 트리로 만듦
        _heap_sort(canvas, svdata, i, 0)

    # 정렬이 끝나고 데이터 시각화
    for i in range(0, len(svdata.data)):
        svdata.color[i] = "lime green"
        showData(canvas, svdata, 0.01, False)
    svdata.reset_color()

    running.get()


def _heap_sort(canvas, svdata, size, i):
    # 기본 설정
    global cnt_heap
    data = svdata.data

    # 부모 위치 설정 및 VICT_COLOR 색으로 지정
    # 양쪽 자식 위치 설정 및 자식 노드가 존재 할 경우 COMP_COLOR 색으로 지정
    parent = i
    left = 2 * i
    right = 2 * i + 1

    svdata.color[parent] = VICT_COLOR
    if left < size:
        cnt_heap += 1
        count_heap.set("비교 {0:04d}회".format(cnt_heap))
        svdata.color[left] = COMP_COLOR
    if right < size:
        cnt_heap += 1
        count_heap.set("비교 {0:04d}회".format(cnt_heap))
        svdata.color[right] = COMP_COLOR

    # 데이터 시각화
    showData(canvas, svdata, 0.1, True)

    # 왼쪽 데이터가 부모 데이터와 오른쪽 데이터보다 클 경우
    if left < size and data[parent] < data[left]:
        if data[left] > data[right]:
            parent = left

            svdata.color[i] = VICT_COLOR
            svdata.color[parent] = TARG_COLOR
            showData(canvas, svdata, 0.05, True)

    # 오른쪽 데이터가 부모 데이터와 왼쪽 데이터보다 클 경우
    if right < size and data[parent] < data[right]:
        parent = right

        svdata.color[i] = VICT_COLOR
        svdata.color[parent] = TARG_COLOR
        showData(canvas, svdata, 0.05, True)

    # 부모 데이터보다 자식 데이터가 클 경우
    if parent != i:
        # 데이터 교환 및 데이터 시각화
        data[i], data[parent] = data[parent], data[i]

        svdata.color[i] = TARG_COLOR
        svdata.color[parent] = VICT_COLOR
        showData(canvas, svdata, 0.05, True)

        # 바뀐 데이터 위치를 기준으로 힙 트리로 만듦
        _heap_sort(canvas, svdata, size, parent)


""" =============== Quick Sort =============== """


def quick_sort(canvas, svdata):
    # 기본 설정
    global cnt_quick
    cnt_quick = 0

    # 퀵 정렬
    _quick_sort(canvas, svdata, 0, len(svdata.data) - 1)

    # 정렬이 끝나고 데이터 시각화
    for i in range(0, len(svdata.data)):
        svdata.color[i] = "lime green"
        showData(canvas, svdata, 0.01, False)
    svdata.reset_color()

    running.get()


def _quick_sort(canvas, svdata, left, right):
    if left < right:
        # right를 기준으로 퀵 정렬 및 얻은 pivot으로 좌우 퀵 정렬
        pivot = _partition(canvas, svdata, left, right)
        _quick_sort(canvas, svdata, left, pivot - 1)
        _quick_sort(canvas, svdata, pivot + 1, right)


def _partition(canvas, svdata, left, right):
    # 기본 설정
    global cnt_quick
    data = svdata.data

    # i는 데이터가 들어갈 위치, pivot은 기준 데이터, j는 비교할 데이터
    i = left - 1
    pivot = data[right]
    for j in range(left, right):
        # 들어갈 데이터의 위치는 VICT_COLOR, 비교할 데이터는 COMP_COLOR
        # 기준 데이터는 pale violet red, 비교해야 할 데이터는 light steel blue 색으로 데이터 시각화
        for k in range(len(data)):
            if i < k < right:
                svdata.color[k] = "light steel blue"
        svdata.color[i + 1] = TARG_COLOR
        if i != j:
            svdata.color[j] = COMP_COLOR
        svdata.color[right] = "pale violet red"

        showData(canvas, svdata, 0.05, True)

        # 기준 데이터와 비교 후 작으면 i 위치에서부터 채움
        cnt_quick += 1
        count_quick.set("비교 {0:04d}회".format(cnt_quick))
        if data[j] < pivot:
            # 들어갈 데이터의 위치 증가
            i += 1

            # 데이터 교환 후 데이터 시각화
            data[i], data[j] = data[j], data[i]

            for k in range(len(data)):
                if i < k < right:
                    svdata.color[k] = "light steel blue"
            svdata.color[right] = "pale violet red"
            if i != j:
                svdata.color[i] = COMP_COLOR
                svdata.color[j] = TARG_COLOR
                showData(canvas, svdata, 0.05, True)

        svdata.reset_color()

    # 기준 데이터와의 비교가 끝난 후 기준 데이터도 교환 및 데이터 시각화
    svdata.color[i + 1] = TARG_COLOR
    svdata.color[right] = "pale violet red"
    showData(canvas, svdata, 0.05, True)

    data[i + 1], data[right] = data[right], data[i + 1]

    if i + 1 != right:
        svdata.color[i + 1] = "pale violet red"
        svdata.color[right] = TARG_COLOR
        showData(canvas, svdata, 0.05, True)

    return i + 1


""" =============== Main =============== """

if __name__ == '__main__':
    _arr = data_create(DATA_SIZE, DATA_INTRV)
    arr = list(_arr)
    arr = SVData(arr)

    """ =============== Basic widget =============== """

    btn_close = tkinter.Button(root, text="프로그램 종료", font=FONT, bg='white', command=lambda: exit())
    btn_close.place(relx=0.885, rely=0.94)

    font_title = tkinter.font.Font(family="Consolas", size=15, weight='bold')
    label_title = tkinter.Label(root, text="Sorting Visualizer", font=font_title, fg='white', bg='light slate grey')
    label_title.place(relx=0.01, rely=0.94)

    """ =============== Control Frame =============== """

    frame_control = tkinter.Frame(root, bg='lightcyan3', highlightbackground='white', highlightthickness=2, highlightcolor='white')
    frame_control.place(relx=0.5, rely=0.01, relwidth=0.986, relheight=0.22, anchor='n')

    frame_font = FONT.copy()
    frame_font.configure(size=13)

    btn_start = tkinter.Button(frame_control, text="정렬\n시작", font=frame_font, width=8, command=lambda: start_sort())
    btn_start.place(x=800, y=8)

    btn_reset = tkinter.Button(frame_control, text="데이터\n초기화", font=frame_font, width=8, command=lambda: SVReset())
    btn_reset.place(x=800, y=67)

    frame_bubble = tkinter.Frame(frame_control, bg='#f5a8ca', width=124, height=78, highlightthickness=2)
    frame_bubble.place(x=5, y=5)
    ctn_var_bubble = tkinter.IntVar()
    ctn_bubble = tkinter.Checkbutton(frame_control, text="버블 정렬", fg='black', font=frame_font, width=10, bg='#f5a8ca',
                                     variable=ctn_var_bubble, command=check_sort)
    ctn_bubble.place(x=7, rely=0.1)
    cnt_bubble = 0
    count_bubble = tkinter.StringVar()
    count_bubble.set("비교 {0:04d}회".format(cnt_bubble))
    label_bubble = tkinter.Label(frame_control, textvariable=count_bubble, font=frame_font, width=10, bg='#f5a8ca')
    label_bubble.place(x=19, y=50)

    frame_insert = tkinter.Frame(frame_control, bg='#f8963e', width=124, height=78, highlightthickness=2)
    frame_insert.place(x=134, y=5)
    ctn_var_insert = tkinter.IntVar()
    ctn_insert = tkinter.Checkbutton(frame_control, text="삽입 정렬", fg='black', font=frame_font, width=10, bg='#f8963e',
                                     variable=ctn_var_insert, command=check_sort)
    ctn_insert.place(x=136, rely=0.1)
    cnt_insert = 0
    count_insert = tkinter.StringVar()
    count_insert.set("비교 {0:04d}회".format(cnt_insert))
    label_insert = tkinter.Label(frame_control, textvariable=count_insert, font=frame_font, width=10, bg='#f8963e')
    label_insert.place(x=148, y=50)

    frame_select = tkinter.Frame(frame_control, bg='#b6d994', width=124, height=78, highlightthickness=2)
    frame_select.place(x=263, y=5)
    ctn_var_select = tkinter.IntVar()
    ctn_select = tkinter.Checkbutton(frame_control, text="선택 정렬", fg='black', font=frame_font, width=10, bg='#b6d994',
                                     variable=ctn_var_select, command=check_sort)
    ctn_select.place(x=265, rely=0.1)
    cnt_select = 0
    count_select = tkinter.StringVar()
    count_select.set("비교 {0:04d}회".format(cnt_select))
    label_select = tkinter.Label(frame_control, textvariable=count_select, font=frame_font, width=10, bg='#b6d994')
    label_select.place(x=277, y=50)

    frame_merge = tkinter.Frame(frame_control, bg='#92b5df', width=124, height=78, highlightthickness=2)
    frame_merge.place(x=392, y=5)
    ctn_var_merge = tkinter.IntVar()
    ctn_merge = tkinter.Checkbutton(frame_control, text="병합 정렬", fg='black', font=frame_font, width=10, bg='#92b5df',
                                    variable=ctn_var_merge, command=check_sort)
    ctn_merge.place(x=394, rely=0.1)
    cnt_merge = 0
    count_merge = tkinter.StringVar()
    count_merge.set("비교 {0:04d}회".format(cnt_merge))
    label_merge = tkinter.Label(frame_control, textvariable=count_merge, font=frame_font, width=10, bg='#92b5df')
    label_merge.place(x=406, y=50)

    frame_heap = tkinter.Frame(frame_control, bg='medium purple', width=124, height=78, highlightthickness=2)
    frame_heap.place(x=521, y=5)
    ctn_var_heap = tkinter.IntVar()
    ctn_heap = tkinter.Checkbutton(frame_control, text=" 힙  정렬", fg='black', font=frame_font, width=10,
                                   bg='medium purple',
                                   variable=ctn_var_heap, command=check_sort)
    ctn_heap.place(x=523, rely=0.1)
    cnt_heap = 0
    count_heap = tkinter.StringVar()
    count_heap.set("비교 {0:04d}회".format(cnt_heap))
    label_heap = tkinter.Label(frame_control, textvariable=count_heap, font=frame_font, width=10, bg='medium purple')
    label_heap.place(x=535, y=50)

    frame_quick = tkinter.Frame(frame_control, bg='#6f5d03', width=124, height=78, highlightthickness=2)
    frame_quick.place(x=650, y=5)
    ctn_var_quick = tkinter.IntVar()
    ctn_quick = tkinter.Checkbutton(frame_control, text=" 퀵  정렬", fg='black', font=frame_font, width=10, bg='#6f5d03',
                                    variable=ctn_var_quick, command=check_sort)
    ctn_quick.place(x=652, rely=0.1)
    cnt_quick = 0
    count_quick = tkinter.StringVar()
    count_quick.set("비교 {0:04d}회".format(cnt_quick))
    label_quick = tkinter.Label(frame_control, textvariable=count_quick, font=frame_font, width=10, bg='#6f5d03')
    label_quick.place(x=664, y=50)

    frame_type = tkinter.Frame(frame_control, bg='lavender', width=253, height=35, highlightthickness=2)
    frame_type.place(x=5, y=88)
    data_type = tkinter.StringVar()
    rad1 = tkinter.Radiobutton(frame_control, text="그래프", font=frame_font, bg='lavender',
                               value="drawData", variable=data_type, command=lambda: showAll())
    rad1.place(x=26, y=90)
    rad2 = tkinter.Radiobutton(frame_control, text="텍스트", font=frame_font, bg='lavender',
                               value="printData", variable=data_type, command=lambda: showAll())
    rad2.place(x=155, y=90)

    frame_type2 = tkinter.Frame(frame_control, bg='lavender', width=124, height=35, highlightthickness=2)
    frame_type2.place(x=263, y=88)
    rad3 = tkinter.Radiobutton(frame_control, text="3D", font=frame_font, bg='lavender',
                               value="cubicData", variable=data_type, command=lambda: showAll())
    rad3.place(x=300, y=90)

    rad1.select()

    prev = data_type.get()

    """ =============== Data Frame =============== """

    frame_data = tkinter.Frame(root, bg='slate grey', highlightcolor='white', highlightbackground='white',
                               highlightthickness=2)
    frame_data.place(relx=0.5, rely=0.24, relwidth=0.986, relheight=0.69, anchor='n')

    label_inform = tkinter.Label(frame_data, text="보고자 하는 정렬 알고리즘을 좌측 상단에서 선택해주세요.", fg='white', font=FONT,
                                 bg='slate grey')
    label_inform.place(relx=0.5, rely=0.5, anchor='n')

    svcanvas = SVCanvas()

    svfig = plt.figure(frameon=False)
    canvas_cubic = FigureCanvasTkAgg(svfig, master=frame_data)
    canvas_cubic.get_tk_widget().configure(bg='slategrey')


    """ =============== Start Program =============== """

    root.mainloop()
