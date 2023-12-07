import tkinter
import time

VICT_COLOR = "red"
TARG_COLOR = "green"
COMP_COLOR = "blue"

SWAP_INTERVAL = 0.08
COMP_INTERVAL = 0.02
WIDTH = 720
HEIGHT = 480

root = tkinter.Tk()
root.title("Sorting Visualizer")
root.geometry("{}x{}+100+100".format(WIDTH, HEIGHT))

class SVData:
    def __init__(self, data):
        self.data = data
        self.color = ["white"] * self.__len__()

    def __len__(self):
        return len(self.data)

    def reset_color(self):
        self.color = ["white"] * self.__len__()

def drawData(svdata):
    data_canvas.delete("all")

    height = data_canvas.winfo_height()

    for index, value in enumerate(svdata.data):
        x0 = 15 * index + 10
        y0 = height - 5 - value

        x1 = 15 * index + 20
        y1 = height - 5

        data_canvas.create_rectangle(x0, y0, x1, y1, fill=svdata.color[index])

    root.update()

def bubble_sort(svdata):
    data = svdata.data

    size = len(data)
    for i in range(0, size):
        for j in range(i, size):

            svdata.color[i] = "red"
            svdata.color[j] = "blue"

            if data[i] > data[j]:
                svdata.color[i] = "green"
                svdata.color[j] = "green"
                drawData(svdata)

                data[i], data[j] = data[j], data[i]

                time.sleep(SWAP_INTERVAL)

            drawData(svdata)

            time.sleep(COMP_INTERVAL)
            svdata.reset_color()

    svdata.reset_color()
    drawData(svdata)



def insertion_sort(svdata):
    data = svdata.data

    size = len(data)
    for i in range(1, size):
        key = data[i]
        j = i - 1

        while j >= 0 and key < data[j]:

            svdata.color[i] = VICT_COLOR
            svdata.color[j] = TARG_COLOR
            drawData(svdata)
            time.sleep(SWAP_INTERVAL)

            data[j + 1] = data[j]
            j -= 1

            svdata.color[i] = VICT_COLOR
            svdata.color[j] = TARG_COLOR
            time.sleep(SWAP_INTERVAL)

            drawData(svdata)
            svdata.reset_color()

        data[j + 1] = key

    svdata.reset_color()
    drawData(svdata)



def selection_sort(svdata):
    data = svdata.data

    size = len(data)
    for i in range(0, size - 1):
        min_index = i
        for j in range(i + 1, size):

            svdata.color[i] = VICT_COLOR
            if i != min_index:
                svdata.color[min_index] = TARG_COLOR
            svdata.color[j] = COMP_COLOR

            if data[min_index] > data[j]:
                min_index = j

            drawData(svdata)
            time.sleep(COMP_INTERVAL)
            svdata.reset_color()

        svdata.color[i] = VICT_COLOR
        svdata.color[min_index] = TARG_COLOR
        drawData(svdata)
        time.sleep(0.2)

        data[i], data[min_index] = data[min_index], data[i]

        svdata.color[i] = TARG_COLOR
        svdata.color[min_index] = VICT_COLOR
        drawData(svdata)
        time.sleep(0.5)

    svdata.reset_color()
    drawData(svdata)



def merge_sort(svdata):

    _merge_sort(svdata, 0, len(svdata.data) - 1)

    drawData(svdata)

def _merge_sort(svdata, left, right):
    if left >= right:
        return

    mid = (left + right) // 2

    _merge_sort(svdata, left, mid)
    _merge_sort(svdata, mid + 1, right)

    _merge(svdata, left, mid, right)

def _merge(svdata, left, mid, right):
    data = svdata.data

    drawData(svdata)
    time.sleep(0.5)

    left_data = data[left:mid + 1]
    right_data = data[mid + 1:right + 1]

    i, j = 0, 0
    for k in range(left, right + 1):

        if i < len(left_data) and j < len(right_data):

            svdata.color[k] = VICT_COLOR

            if left_data[i] <= right_data[j]:
                svdata.color[i] = TARG_COLOR
                data[k] = left_data[i]
                i += 1
            else:
                svdata.color[mid + j] = TARG_COLOR
                data[k] = right_data[j]
                j += 1

        elif i < len(left_data):
            svdata.color[k] = VICT_COLOR
            svdata.color[i] = TARG_COLOR
            data[k] = left_data[i]
            i += 1

        else:
            svdata.color[k] = VICT_COLOR
            svdata.color[mid + j] = TARG_COLOR
            data[k] = right_data[j]
            j += 1

        drawData(svdata)
        time.sleep(0.2)

        svdata.reset_color()



def heap_sort(svdata):
    global count
    data = svdata.data

    size = len(data)
    for i in range((size // 2) - 1, -1, -1):
        _heap_sort(svdata, size, i)

    for i in range(size - 1, 0, -1):

        svdata.color[0] = VICT_COLOR
        svdata.color[i] = TARG_COLOR
        drawData(svdata)
        time.sleep(0.2)

        data[i], data[0] = data[0], data[i]

        svdata.color[0] = TARG_COLOR
        svdata.color[i] = VICT_COLOR
        drawData(svdata)
        time.sleep(0.2)

        svdata.reset_color()

        _heap_sort(svdata, i, 0)

    drawData(svdata, 0, False)

def _heap_sort(svdata, size, i):
    global count
    data = svdata.data

    parent = i
    left = 2 * i
    right = 2 * i + 1

    svdata.color[parent] = VICT_COLOR
    if left < size:
        svdata.color[left] = COMP_COLOR
    if right < size:
        svdata.color[right] = COMP_COLOR

    drawData(svdata)
    time.sleep(0.25)
    svdata.reset_color()

    if left < size and data[parent] < data[left]:
        if data[left] > data[right]:
            parent = left

            svdata.color[i] = VICT_COLOR
            svdata.color[parent] = TARG_COLOR
            drawData(svdata)
            time.sleep(0.25)
            svdata.reset_color()

    if right < size and data[parent] < data[right]:
        parent = right

        svdata.color[i] = VICT_COLOR
        svdata.color[parent] = TARG_COLOR
        drawData(svdata)
        time.sleep(0.25)
        svdata.reset_color()

    if parent != i:
        data[i], data[parent] = data[parent], data[i]

        svdata.color[i] = TARG_COLOR
        svdata.color[parent] = VICT_COLOR
        drawData(svdata)
        time.sleep(0.25)
        svdata.reset_color()

        _heap_sort(svdata, size, parent)



def quick_sort(svdata):
    global count
    _quick_sort(svdata, 0, len(svdata.data) - 1)

    drawData(svdata)

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

        drawData(svdata)
        time.sleep(0.02)

        if data[j] <= pivot:

            i += 1

            svdata.color[i] = VICT_COLOR
            svdata.color[j] = COMP_COLOR
            svdata.color[right] = "purple"
            drawData(svdata)
            time.sleep(0.02)

            svdata.color[i] = TARG_COLOR
            svdata.color[j] = TARG_COLOR
            drawData(svdata)
            time.sleep(0.02)

            data[i], data[j] = data[j], data[i]

            drawData(svdata)
            time.sleep(0.02)

        svdata.reset_color()

    data[i + 1], data[right] = data[right], data[i + 1]

    return i + 1


if __name__ == "__main__":

    arr = [280, 220, 110, 30, 100, 200, 150, 300, 20, 10, 50, 90, 80,
           70, 60, 130, 230, 250, 20, 10, 50, 90, 80, 70, 60, 130, 230, 250,
           10, 100, 20, 200, 30, 300, 40]
    arr = SVData(arr)

    data_canvas = tkinter.Canvas(root, bg='grey')
    data_canvas.place(relx=0.5, rely=0.3, relwidth=0.98, relheight=0.69, anchor='n')
    data_canvas.update()

    frame_control = tkinter.Frame(root, bg='grey', relief="groove")
    frame_control.place(relx=0.5, rely=0.01, relwidth=0.98, relheight=0.2, anchor='n')

    btn1 = tkinter.Button(frame_control, text="버블 정렬", width=8, command=lambda: bubble_sort(arr))
    btn1.place(relx="0.01", y="5")
    
    btn2 = tkinter.Button(frame_control, text="삽입 정렬", width=8, command=lambda: insertion_sort(arr))
    btn2.place(relx="0.01", y="35")
    
    btn3 = tkinter.Button(frame_control, text="선택 정렬", width=8, command=lambda: selection_sort(arr))
    btn3.place(relx="0.01", y="65")
    
    btn4 = tkinter.Button(frame_control, text="병합 정렬", width=8, command=lambda: merge_sort(arr))
    btn4.place(relx="0.11", y="5")
    
    btn5 = tkinter.Button(frame_control, text="힙 정렬", width=8, command=lambda: heap_sort(arr))
    btn5.place(relx="0.11", y="35")
    
    btn6 = tkinter.Button(frame_control, text="퀵 정렬", width=8, command=lambda: quick_sort(arr))
    btn6.place(relx="0.11", y="65")
    
    drawData(arr)

    root.mainloop()
