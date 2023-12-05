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
root.title = "Sorting Visualize"
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
    
    drawData(arr)

    root.mainloop()
