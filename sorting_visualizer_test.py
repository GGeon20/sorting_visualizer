import tkinter

window = tkinter.Tk()
window.title("Test")

data = [280, 220, 110, 30, 100, 200, 150, 300, 20, 10, 50, 90, 80, 70, 60, 130, 230, 250]

width = 640
height = 400
window.geometry("{}x{}+100+100".format(width, height))

b1 = tkinter.Button(window, text="정렬 시작")
b1.pack(side="bottom")

canvas = tkinter.Canvas(window, width=width, height=height-40, relief="solid", bd=2)

for i, value in enumerate(data):
    line = canvas.create_rectangle(15 * i + 10, 360 - value, 15 * i + 20, 400, fill="white")

canvas.pack()

index = 0

def refresh_window():
    global canvas
    global data
    global index
    global line

    for j, _ in enumerate(data):
        if data[index] > data[j]:
            tmp = data[index]
            data[index] = data[j]
            data[j] = tmp

    canvas.delete("all")
    # canvas = tkinter.Canvas(window, width=640, height=360, relief="solid", bd=2)
    for k, value in enumerate(data):
        line = canvas.create_rectangle(15 * k + 10, 360 - value, 15 * k + 20, 400, fill="white")

    if index < k:
        index += 1
    window.after(300, refresh_window)


refresh_window()

window.mainloop()