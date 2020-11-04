import PIL.ImageGrab
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import colors

def chooseColor(color):
    print(color)
    global color_1
    color_1 = color

def move_from(event):
    # Remember previous coordinates for scrolling with the mouse
    c1.scan_mark(event.x, event.y)
def move_to(event):
    # Drag (move) canvas to the new position
    c1.scan_dragto(event.x, event.y, gain=1)

def on_click(event):
    global dragging
    dragging = True
    on_move(event)

def on_move(event):
    global dragging
    if dragging:
        items = c1.find_closest(event.x, event.y)
        if items:
            rect_id = items[0]
            c1.itemconfigure(rect_id, fill=color_1, outline=color_1)

def on_release(event):
    global dragging
    dragging = False

def on_click3(event):
    global dragging
    dragging = True
    on_move3(event)

def on_move3(event):
    global dragging
    if dragging:
        items = c1.find_closest(event.x, event.y)
        if items:
            rect_id = items[0]
            c1.itemconfigure(rect_id, fill=color_2, outline='#d9d9d9')

def on_release3(event):
    global dragging
    dragging = False

def colorGrid():
    gridResolution = 100
    if canvasHeight > canvasWidth:
        print('Height Larger Than')
        for y in range(1, canvasHeight,int(canvasWidth/gridResolution)):
            for x in range(1,canvasWidth,int(canvasWidth/gridResolution)):
                pixel = c1.create_rectangle(x,y,x+int(canvasWidth/gridResolution),y+int(canvasWidth/gridResolution),fill='white',outline='#d9d9d9')
                rectList.append(pixel)
                c1.tag_bind(pixel, '<Button-1>', on_click)
                c1.tag_bind(pixel, '<B1-Motion>', on_move)
                c1.tag_bind(pixel, '<ButtonRelease-1>', on_release)
                c1.tag_bind(pixel, '<Button-3>', on_click3)
                c1.tag_bind(pixel, '<B3-Motion>', on_move3)
                c1.tag_bind(pixel, '<ButtonRelease-3>', on_release3)
    else:
        print('Width Larger Than')
        for y in range(1, canvasHeight,int(canvasHeight/gridResolution)):
            for x in range(1,canvasWidth,int(canvasHeight/gridResolution)):
                pixel = c1.create_rectangle(x,y,x+int(canvasHeight/gridResolution),y+int(canvasHeight/gridResolution),fill='white',outline='#d9d9d9')
                rectList.append(pixel)
                c1.tag_bind(pixel, '<Button-1>', on_click)
                c1.tag_bind(pixel, '<B1-Motion>', on_move)
                c1.tag_bind(pixel, '<ButtonRelease-1>', on_release)
                c1.tag_bind(pixel, '<Button-3>', on_click3)
                c1.tag_bind(pixel, '<B3-Motion>', on_move3)
                c1.tag_bind(pixel, '<ButtonRelease-3>', on_release3)

def genColorScheme():
    # Create color picker buttons
    try:
        for btn in btnList:
            btn.pack_forget()
            btn.destroy()
    except:
        print('No BTNs in list!')
    colorScheme1 = colors.monolumColorScheme()
    colorScheme2 = colors.complimentaryColor(colorScheme1)

    i = 0
    for color in colorScheme1:
        i += 1
        backgroundColor = colors.rgb_to_hex(color)
        btn1 = Button(color_frame, width=4, height=2, bg=backgroundColor,command=partial(chooseColor,backgroundColor))
        btnList.append(btn1)
        print(backgroundColor)
        btn1.grid(column=0,row=i,sticky='n',columnspan=1,rowspan=1)
        # grid_columnconfigure(btn1,uniform=True)

    d = 0
    for color in colorScheme2:
        d += 1
        backgroundColor = colors.rgb_to_hex(color)
        btn2 = Button(color_frame, width=4, height=2, bg=backgroundColor,command=partial(chooseColor,backgroundColor))
        btnList.append(btn2)
        print(backgroundColor)
        btn2.grid(column=1,row=d,sticky='n',columnspan=1,rowspan=1)
    print(btnList)

def entered(event):
    current = event.widget.find_withtag('current')
    item = current[0]
    c1.itemconfigure(item, fill=color_1, outline=color_1)
    print('Entered!')

def save():
    fileName = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics','*.png')])
    if fileName:
        x = window.winfo_rootx() + c1.winfo_x()
        y = window.winfo_rooty() + c1.winfo_y()
        x1 = x + c1.winfo_width()
        y1 = y + c1.winfo_height()
        PIL.ImageGrab.grab().crop((x,y,x1,y1)).save(fileName + '.png')

def clearAll():
    for rect in rectList:
        c1.itemconfigure(rect, fill=color_2, outline='#d9d9d9')

def drawToolCMD():
    pass

def fillToolCMD():
    pass


window = Tk()
window.geometry('1080x720')
window.title('Pixel Maker')

rectList = []
btnList = []
canvasHeight = 600
canvasWidth = 600
testH = 600
testW = 600

color_1 = '#8C15B9'
color_2 = '#ffffff'

main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)

color_frame = LabelFrame(main_frame, text='Colors', bd=5, relief=RIDGE, bg='white')
color_frame.place(x=0, y=0, width=140, height=245)

tools_frame = LabelFrame(main_frame, text='Tools', bd=5, relief=RIDGE, bg='white')
tools_frame.place(relx=1, rely=0,x=-86, width=86, height=245)

# Toolbar buttons
drawTool = Button(tools_frame, width=4, height=2, command=drawToolCMD)
drawTool.grid(column=0,row=1,sticky='n',columnspan=1,rowspan=1)

fillTool = Button(tools_frame, width=4, height=2, command=fillToolCMD)
fillTool.grid(column=1,row=1,sticky='n',columnspan=1,rowspan=1)

c1 = Canvas(main_frame, height=testH, width=testW, bg='grey')
c1.place(relx=0.5, rely=0.5, anchor=CENTER)

c1.pack()

colorGrid()

c1.bind('<ButtonPress-2>', move_from)
c1.bind('<B2-Motion>', move_to)

genColorSchemeBtn = Button(window, text='Generate Color Pallet', height=2, command=genColorScheme)
genColorSchemeBtn.place(x=0, y=244)

saveBtn = Button(window, text='Save', height=2, command=save)
saveBtn.place(x=0, y=286)

clearBtn = Button(window, text='Clear All', height=2, command=clearAll)
clearBtn.place(x=0, y=328)

print(rectList)

window.mainloop()