import tkinter
import tkinter.font
import time

VICT_COLOR = "indian red1"
TARG_COLOR = "lime green"
COMP_COLOR = "cyan"

SWAP_INTERVAL = 0.08
COMP_INTERVAL = 0.02
WIDTH = 925
HEIGHT = 600

root = tkinter.Tk()
root.title("Sorting Visualizer")
root.geometry(f"{WIDTH}x{HEIGHT}+100+100")
root.resizable(False, False)
root.config(background="light slate grey")

FONT = tkinter.font.Font(family="Consolas", size=10, weight="bold")

class SVData:
    def __init__(self, data):
        self.data = list(data)
        self._data = list(data)
        self.color = ["white"] * self.__len__()

    def __len__(self):
        return len(self.data)

    def reset_color(self):
        self.color = ["white"] * self.__len__()

    def reset_data(self):
        self.data = list(self._data)

def data_reset():
    global count
    count = 0
    count_text.set(f"비교 {count}회")
    arr.reset_data()
    showData(arr, 0, False)


""" =============== Create Data =============== """

import random

def data_create(size, intrv=1):
    minn = intrv
    maxn = (size + 1) * intrv

    arr = [i for i in range(minn, maxn, intrv)]
    random.shuffle(arr)

    return arr


""" =============== Show Data =============== """

def showData(svdata, t, reset):
    exec(data_type.get() + "(svdata)")
    time.sleep(t)
    if reset is True:
        svdata.reset_color()


""" =============== Show Data with Rectangle Shape =============== """

def drawData(svdata):
    data_canvas.delete("all")

    canvas_width = data_canvas.winfo_width()
    canvas_height = data_canvas.winfo_height()

    blank_space = 5
    rect_width = (canvas_width - blank_space) / (svdata.__len__())

    maxn = max(svdata.data)
    weight = (canvas_height - 10) / maxn

    for index, value in enumerate(svdata.data):
        x0 = rect_width * index + blank_space
        y0 = canvas_height - 5 - (value * weight)

        x1 = rect_width * (index + 1)
        y1 = canvas_height - 5

        data_canvas.create_rectangle(x0, y0, x1, y1, fill=svdata.color[index], outline=svdata.color[index])

    root.update()


""" =============== Show Data with Text =============== """

def printData(svdata):
    data_canvas.delete("all")

    w = 0
    height = 10
    for index, value in enumerate(svdata.data):

        data_canvas.create_rectangle((index - w) * 30 + 5, height - 5, (index - w + 1) * 30 + 5, height + 10, fill=svdata.color[index])
        data_canvas.create_text((index - w) * 30 + 20, height + 2, text=value, font=FONT, fill="black", width=30)

        if (index + 1) % 30 == 0:
            w = index + 1
            height += 20

    root.update()


""" =============== Bubble Sort =============== """

def bubble_sort(svdata):
    data = svdata.data

    count = 0
    size = len(data)
    for i in range(0, size):
        for j in range(i, size):
            count += 1
            count_text.set("비교 {}회".format(count))

            svdata.color[i] = "red"
            svdata.color[j] = "blue"

            if data[i] > data[j]:
                svdata.color[i] = "green"
                svdata.color[j] = "green"
                showData(svdata, SWAP_INTERVAL, False)

                data[i], data[j] = data[j], data[i]

            showData(svdata, COMP_INTERVAL, True)

    svdata.reset_color()
    showData(svdata, 0, False)


""" =============== Insertion Sort =============== """

def insertion_sort(svdata):
    data = svdata.data

    count = 0
    size = len(data)
    for i in range(1, size):
        key = data[i]
        j = i - 1

        while j >= 0 and key < data[j]:
            count += 1
            count_text.set("비교 {}회".format(count))

            svdata.color[i] = VICT_COLOR
            svdata.color[j] = TARG_COLOR
            showData(svdata, SWAP_INTERVAL, False)

            data[j + 1] = data[j]
            j -= 1

            svdata.color[i] = VICT_COLOR
            svdata.color[j] = TARG_COLOR

            showData(svdata, SWAP_INTERVAL, True)

        data[j + 1] = key

    svdata.reset_color()
    showData(svdata, 0, False)


""" =============== Selection Sort =============== """

def selection_sort(svdata):
    data = svdata.data

    count = 0
    size = len(data)
    for i in range(0, size - 1):
        min_index = i
        for j in range(i + 1, size):
            count += 1
            count_text.set("비교 {}회".format(count))

            svdata.color[i] = VICT_COLOR
            if i != min_index:
                svdata.color[min_index] = TARG_COLOR
            svdata.color[j] = COMP_COLOR

            if data[min_index] > data[j]:
                min_index = j

            showData(svdata, COMP_INTERVAL, True)

        svdata.color[i] = VICT_COLOR
        svdata.color[min_index] = TARG_COLOR
        showData(svdata, 0.2, False)

        data[i], data[min_index] = data[min_index], data[i]

        svdata.color[i] = TARG_COLOR
        svdata.color[min_index] = VICT_COLOR
        showData(svdata, 0.5, False)

    showData(svdata, 0, False)


""" =============== Merge Sort =============== """

def merge_sort(svdata):
    global count
    count = 0

    _merge_sort(svdata, 0, len(svdata.data) - 1)

    showData(svdata, 0, False)

def _merge_sort(svdata, left, right):
    if left >= right:
        return

    mid = (left + right) // 2

    _merge_sort(svdata, left, mid)
    _merge_sort(svdata, mid + 1, right)

    _merge(svdata, left, mid, right)

def _merge(svdata, left, mid, right):
    global count
    
    data = svdata.data

    for index in range(left, right + 1):
        svdata.color[index] = "light steel blue"
    showData(svdata, 0.2, False)

    left_data = data[left:mid + 1]
    right_data = data[mid + 1:right + 1]

    i, j = 0, 0
    for k in range(left, right + 1):

        count += 1
        count_text.set(f"비교 {count}회")

        for index in range(left, right + 1):
            if index < left + i + j:
                svdata.color[index] = "lime green"
            else:
                svdata.color[index] = "light steel blue"

        if i < len(left_data) and j < len(right_data):

            if left_data[i] <= right_data[j]:
                for l in range(left, right + 1):
                    if data[l] == left_data[i]:
                        if data[k] != data[l]:
                            targ = left_data[i]
                        else:
                            targ = -1

                        break

                i += 1
            else:
                for l in range(left, right + 1):
                    if data[l] == right_data[j]:
                        if data[k] != data[l]:
                            targ = right_data[j]
                        else:
                            targ = -1

                        break

                j += 1

        elif i < len(left_data):
            for l in range(left, right + 1):
                if data[l] == left_data[i]:
                    if data[k] != data[l]:
                        targ = left_data[i]
                    else:
                        targ = -1

                    break

            i += 1

        else:
            for l in range(left, right + 1):
                if data[l] == right_data[j]:
                    if data[k] != data[l]:
                        targ = right_data[j]
                    else:
                        targ = -1

                    break

            j += 1
        
        if targ != -1:
            svdata.color[k] = VICT_COLOR
            svdata.color[l] = COMP_COLOR
            showData(svdata, 0.1, False)

            data[l] = data[k]
            data[k] = targ

            svdata.color[k] = COMP_COLOR
            svdata.color[l] = VICT_COLOR
        else:
            svdata.color[k] = "lime green"
        
        showData(svdata, 0.1, True)


""" =============== Heap Sort =============== """

def heap_sort(svdata):
    global count
    data = svdata.data

    size = len(data)
    for i in range((size // 2) - 1, -1, -1):
        _heap_sort(svdata, size, i)

    for i in range(size - 1, 0, -1):

        svdata.color[0] = VICT_COLOR
        svdata.color[i] = TARG_COLOR
        showData(svdata, 0.2, False)

        data[i], data[0] = data[0], data[i]

        svdata.color[0] = TARG_COLOR
        svdata.color[i] = VICT_COLOR
        showData(svdata, 0.2, True)

        _heap_sort(svdata, i, 0)

    showData(svdata, 0, False)

def _heap_sort(svdata, size, i):
    global count
    data = svdata.data
 
    parent = i
    left = 2 * i
    right = 2 * i + 1

    svdata.color[parent] = VICT_COLOR
    if left < size:
        count += 1
        count_text.set(f"비교 {count}회")
        svdata.color[left] = COMP_COLOR
    if right < size:
        count += 1
        count_text.set(f"비교 {count}회")
        svdata.color[right] = COMP_COLOR

    showData(svdata, 0.25, True)

    if left < size and data[parent] < data[left]:
        if data[left] > data[right]:
            parent = left

            svdata.color[i] = VICT_COLOR
            svdata.color[parent] = TARG_COLOR
            showData(svdata, 0.25, True)

    if right < size and data[parent] < data[right]:
        parent = right

        svdata.color[i] = VICT_COLOR
        svdata.color[parent] = TARG_COLOR
        showData(svdata, 0.25, True)

    if parent != i:
        data[i], data[parent] = data[parent], data[i]

        svdata.color[i] = TARG_COLOR
        svdata.color[parent] = VICT_COLOR
        showData(svdata, 0.25, True)

        _heap_sort(svdata, size, parent)


""" =============== Quick Sort =============== """

def quick_sort(svdata):
    global count
    _quick_sort(svdata, 0, len(svdata.data) - 1)

    showData(svdata, 0, False)

def _quick_sort(svdata, left, right):
    global count
    if left < right:
        pivot = _partition(svdata, left, right)
        svdata.reset_color()
        _quick_sort(svdata, left, pivot - 1)
        _quick_sort(svdata, pivot + 1, right)

def _partition(svdata, left, right):
    global count
    data = svdata.data

    i = left - 1
    pivot = data[right]

    for j in range(left, right):

        for k in range(len(data)):
            if k == j:
                svdata.color[k] = COMP_COLOR
            elif k == right:
                svdata.color[k] = "purple"
            elif i < k < right:
                svdata.color[k] = "light grey"

        showData(svdata, 0.02, False)

        count += 1
        count_text.set(f"비교 {count}회")

        if data[j] <= pivot:

            i += 1

            svdata.color[i] = VICT_COLOR
            svdata.color[j] = COMP_COLOR
            svdata.color[right] = "purple"
            showData(svdata, 0.02, False)

            svdata.color[i] = TARG_COLOR
            svdata.color[j] = TARG_COLOR
            showData(svdata, 0.02, False)

            data[i], data[j] = data[j], data[i]

            showData(svdata, 0.02, False)

        svdata.reset_color()

    data[i + 1], data[right] = data[right], data[i + 1]

    return i + 1


""" =============== Main =============== """

if __name__ == "__main__":

    _arr = data_create(30)

    # _arr = [280, 220, 10, 50, 150, 300, 110, 30, 20, 70,
    #         210, 190, 100, 170, 80, 290, 40, 200, 120, 260,
    #         160, 140, 250, 60, 130, 240, 180, 270, 90, 230]
    arr = list(_arr)
    arr = SVData(arr)

    count = 0



    frame_control = tkinter.Frame(root, bg='slate grey', highlightbackground="white", highlightthickness=2)
    frame_control.place(relx=0.5, rely=0.01, relwidth=0.986, relheight=0.22, anchor='n')

    count_text = tkinter.StringVar()
    count_text.set("비교 0회")
    count_label = tkinter.Label(frame_control, textvariable=count_text, font=FONT)
    count_label.place(relx="0.45", y="65")

    btn_reset = tkinter.Button(frame_control, text="데이터 리셋", font=FONT, command=lambda: data_reset())
    btn_reset.place(relx="0.45", y="5")



    lframe_bigonn = tkinter.LabelFrame(frame_control, text=" O(n^2) ", font=FONT, bg="slate grey", padx=5, pady=2)
    lframe_bigonn.place(relx="0.01", rely="0.015")

    btn_bubble = tkinter.Button(lframe_bigonn, text="버블 정렬", font=FONT, width=8, bg="white", command=lambda: bubble_sort(arr))
    btn_bubble.grid(row=0, column=0, padx="2")

    btn_insertion = tkinter.Button(lframe_bigonn, text="삽입 정렬", font=FONT, width=8, bg="white", command=lambda: insertion_sort(arr))
    btn_insertion.grid(row=1, column=0, pady="5")

    btn_selection = tkinter.Button(lframe_bigonn, text="선택 정렬", font=FONT, width=8, bg="white", command=lambda: selection_sort(arr))
    btn_selection.grid(row=2, column=0)



    lframe_bigonlogn = tkinter.LabelFrame(frame_control, text=" O(n*logn) ", font=FONT, bg="slate grey", padx=5, pady=2)
    lframe_bigonlogn.place(relx="0.12", rely="0.015")

    btn_merge = tkinter.Button(lframe_bigonlogn, text="병합 정렬", font=FONT, width=8, bg="white", command=lambda: merge_sort(arr))
    btn_merge.grid(row=0, column=0, padx="2")

    btn_heap = tkinter.Button(lframe_bigonlogn, text="힙 정렬", font=FONT, width=8, bg="white", command=lambda: heap_sort(arr))
    btn_heap.grid(row=1, column=0, pady="5")

    btn_quick = tkinter.Button(lframe_bigonlogn, text="퀵 정렬", font=FONT, width=8, bg="white", command=lambda: quick_sort(arr))
    btn_quick.grid(row=2, column=0)



    data_type = tkinter.StringVar()
    rad1 = tkinter.Radiobutton(frame_control, text="그래프", font=FONT, value="drawData", variable=data_type, command=lambda: drawData(arr))
    rad1.place(relx="0.9", y="5")
    rad2 = tkinter.Radiobutton(frame_control, text="텍스트", font=FONT, value="printData", variable=data_type, command=lambda: printData(arr))
    rad2.place(relx="0.9", y="35")
    rad1.select()
    rad2.deselect()



    btn_close = tkinter.Button(root, text="프로그램 종료", font=FONT, bg="white", command=lambda: exit())
    btn_close.place(relx="0.885", rely="0.94")

    font_title = tkinter.font.Font(family="Consolas", size=15, weight="bold")
    label_title = tkinter.Label(root, text="Sorting Visualizer", font=font_title, foreground="white", bg="light slate grey")
    label_title.place(relx="0.01", rely="0.94")



    data_canvas = tkinter.Canvas(root, bg='slate grey')
    data_canvas.place(relx=0.4995, rely=0.24, relwidth=0.986, relheight=0.69, anchor='n')
    data_canvas.update()
    
    drawData(arr)

    root.mainloop()
