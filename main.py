from math import floor
from tkinter import messagebox
from tkinter.ttk import Combobox
from copy import deepcopy
import matplotlib.pyplot as plt
from tkinter import *

import numpy as np


def Error_Msg(msg):
    messagebox.showerror('Failed', msg)


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


""" functions l first fit w best fit kan fehom 3'alta bas f 
    tare2et 7at l data fl dict_of_processes fa zabataha

    w zawedt kam satr f awelha 3ashan 2a2alel l parameters 
    ely bab3athalha w tet3amel ma3 l global parameters """

processes_counter = 0
holes_list = []
pre_allocated_list = []
dict_of_processes = {}
mem_size = None

main_root = Tk()
main_root.title('WELCOME')

""" Algorithm by: Monica """


def sort_holes_list(hole_list):  # step to make holes format    # with respect to start (adom 2 holes sawa)
    s = sorted(hole_list, key=lambda i: i['start'])
    return s


def holes_format(hole_list):
    x = int(0)
    # deh 3'ayartaha 3ashan kan feha moshkela enaha betzabat awel 2 holes wara ba3d bs
    while x < len(hole_list) - 1:
        if hole_list[x + 1]['start'] == hole_list[x]['size'] + hole_list[x]['start']:
            hole_list[x]['size'] = hole_list[x]['size'] + hole_list[x + 1]['size']
            del (hole_list[x + 1])
        else:
            x += 1


def sort_holes_list_bf(formated_holes):
    bf = sorted(formated_holes, key=lambda i: i['size'])
    return bf


def First_Fit(my_dict):
    global dict_of_processes, holes_list
    holes_list = sort_holes_list(holes_list)
    holes_format(holes_list)
    allocated = []
    const_formated_holes = deepcopy(holes_list)
    for i in range(len(my_dict)):
        for index in range(len(holes_list)):
            seg = 'Seg' + str(i)
            inner = my_dict['Seg' + str(i)]

            if holes_list[index]['size'] >= int(inner['size']):

                allocated.append(1)
                holes_list[index]['size'] -= int(inner['size'])
                my_dict[seg].update(start=holes_list[index]['start'])
                holes_list[index]['start'] = holes_list[index]['start'] + int(inner['size'])

                if holes_list[index]['size'] == 0:
                    del holes_list[index]
                break

    if len(allocated) == len(my_dict):
        dict_of_processes['p' + str(processes_counter)] = my_dict
        return True
    else:
        holes_list = deepcopy(const_formated_holes)
        return False


def Best_Fit(my_dict):
    global dict_of_processes, holes_list
    holes_list = sort_holes_list(holes_list)
    holes_format(holes_list)
    sorted_list_to_bf = sort_holes_list_bf(holes_list)
    allocated = []
    for i in range(len(my_dict)):
        sorted_list_to_bf = sort_holes_list_bf(sorted_list_to_bf)
        for index in range(0, len(sorted_list_to_bf)):
            seg = 'Seg' + str(i)
            inner = my_dict['Seg' + str(i)]
            if sorted_list_to_bf[index]['size'] >= int(inner['size']):

                allocated.append(1)
                sorted_list_to_bf[index]['size'] -= int(inner['size'])
                my_dict[seg].update(start=sorted_list_to_bf[index]['start'])
                sorted_list_to_bf[index]['start'] = sorted_list_to_bf[index]['start'] + int(inner['size'])

                if sorted_list_to_bf[index]['size'] == 0:
                    del sorted_list_to_bf[index]
                break

    if len(allocated) == len(my_dict):
        dict_of_processes['p' + str(processes_counter)] = my_dict
        holes_list = deepcopy(sort_holes_list(sorted_list_to_bf))
        return True

    else:
        return False


""" GUI by: Fady """


def On_Click(event):
    """
    Double click to Deallocate
    Single click to Show Segments table
    """

    if event.ydata is not None:
        val = floor(event.ydata)
        if event.button == 3:
            '''
            Deallocate part
            '''

            for i in range(len(pre_allocated_list)):
                if pre_allocated_list[i]['start'] <= val <= pre_allocated_list[i]['start'] + pre_allocated_list[i][
                    'size']:
                    holes_list.append(pre_allocated_list.pop(i))
                    plt.close('all')
                    Draw_Mem()
                    return

            for proc, segs in dict_of_processes.items():
                flag = False
                for seg in segs.values():
                    if seg['start'] <= val <= seg['start'] + seg['size']:
                        flag = True
                        break

                if flag:
                    for seg in segs.values():
                        holes_list.append(dict(start=seg['start'], size=seg['size']))

                    dict_of_processes.pop(proc)
                    plt.close('all')
                    Draw_Mem()
                    return
        elif event.button == 1:
            '''
            Show Segments Table
            '''
            for proc, segs in dict_of_processes.items():
                flag = False
                for seg in segs.values():
                    if seg['start'] <= val <= seg['start'] + seg['size']:
                        flag = True
                        break

                if flag:
                    data = []
                    for seg in segs.values():
                        data.append([seg['name'], seg['start'], seg['size']])

                    data = np.array(data)
                    figT = plt.figure('Segment Table')
                    try:
                        plt.close(figT)
                        figT = plt.figure('Segment Table')
                    except:
                        pass
                    plt.title(f'{proc.capitalize()} Segment Table')
                    collabel = ("Name", "Start", "Size")
                    plt.axis('off')
                    plt.table(cellText=data, colLabels=collabel, loc='center', cellLoc='center')
                    figT.set_size_inches(3, 4)
                    plt.show()
                    return


def Draw_Mem():
    """ Function that draws the memory figure """

    global holes_list
    fig = plt.figure('MEMORY')
    plt.title('Right click to Deallocate\nLeft click to Show Segments table\n')
    holes_list = sort_holes_list(holes_list)
    holes_format(holes_list)
    plt.xlim(0, 0)
    plt.ylim(0, mem_size)
    plt.xticks([0], ["Memory"])
    yticks = [mem_size]

    # Draw Holes
    for hole in holes_list:
        yticks.append(hole['start'])
        plt.bar(0, hole['size'], bottom=hole['start'], color='white', edgecolor='white')
        plt.text(0, (0.5 * hole['size'] + hole['start']), "Hole", horizontalalignment='center',
                 verticalalignment='center', fontsize=9)

    # Draw Pre_allocated
    for pre_all in pre_allocated_list:
        yticks.append(pre_all['start'])
        plt.bar(0, pre_all['size'], bottom=pre_all['start'], color='grey', edgecolor='white')
        plt.text(0, (0.5 * pre_all['size'] + pre_all['start']), "Pre_Allocated", horizontalalignment='center',
                 verticalalignment='center', fontsize=9)

    cmap = get_cmap(20)
    # Draw Entered Processes
    for proc, dct in dict_of_processes.items():
        for seg in dct.values():
            yticks.append(seg['start'])
            plt.bar(0, seg['size'], bottom=seg['start'], color=cmap((int(proc[1:]) - 1) % 20), edgecolor='white')
            plt.text(0, (0.5 * seg['size'] + seg['start']), f"{proc}\n{seg['name']}", horizontalalignment='center',
                     verticalalignment='center', fontsize=9)

    plt.yticks(yticks)
    # Connect the Click of mouse to function On_Click
    fig.canvas.mpl_connect('button_press_event', On_Click)
    fig.set_size_inches(3.2, 7.5)
    plt.show()


def Mem_Control():
    """ Window to get user's inputs about the
     number of segments and type of allocation"""

    global processes_counter
    options_root = Tk()
    options_root.title('OPTIONS')

    def Allocate():
        allocate_type = alloc_type_entry.get()
        seg_num = seg_num_entry.get()
        if not seg_num.isnumeric() or allocate_type not in ['First Fit', 'Best Fit']:
            Error_Msg('Please Enter VALID Entries!')
            return

        def Get_Segs():
            global processes_counter
            input_dict = {}
            for j in range(len(components[0])):
                if components[0][j]['text'] == 'Seg':
                    continue

                name = components[1][j].get()
                size = components[2][j].get()
                if not size.isnumeric():
                    Error_Msg('Invalid Value(s) Entered!')
                    return

                input_dict[components[0][j]['text']] = dict(name=name, size=int(size))
            processes_counter += 1

            seg_root.destroy()
            if allocate_type == 'First Fit':
                if not First_Fit(input_dict):
                    Error_Msg('No Enough Free Memory\nDeallocate Some Processes')
                    processes_counter -= 1
                    Mem_Control()
                else:
                    plt.close()
                    Mem_Control()
                    messagebox.showinfo('SUCCEEDED', 'Process allocated Successfully!')
                    Draw_Mem()
            else:
                if not Best_Fit(input_dict):
                    Error_Msg('No Enough Free Memory\nDeallocate Some Processes')
                    processes_counter -= 1
                    Mem_Control()
                else:
                    plt.close()
                    Mem_Control()
                    messagebox.showinfo('SUCCEEDED', 'Process allocated Successfully!')
                    Draw_Mem()

        seg_num = int(seg_num)
        options_root.destroy()
        seg_root = Tk()
        seg_root.title('SEGMENTS INFO')

        components = [[], [], []]
        for i in range(seg_num):
            if (i % 15) == 0:
                components[0].append(Label(seg_root, text="Seg"))
                components[1].append(Label(seg_root, text="Name"))
                components[2].append(Label(seg_root, text="Size"))

            components[0].append(Label(seg_root, text='Seg' + str(i)))
            components[1].append(Entry(seg_root, width=10))
            components[2].append(Entry(seg_root, width=10))

        for j in range(len(components[0])):
            components[0][j].grid(row=int(j % 16), column=0 + (int(j / 16) * 3), padx=5, pady=5)
            components[1][j].grid(row=int(j % 16), column=1 + (int(j / 16) * 3), padx=5, pady=5)
            components[2][j].grid(row=int(j % 16), column=2 + (int(j / 16) * 3), padx=5, pady=5)

        done_button = Button(seg_root, text='DONE', command=Get_Segs)
        done_button.grid(row=17, column=1, padx=10, pady=15)

        back_button = Button(seg_root, text="BACK", command=lambda: [seg_root.destroy(), Mem_Control()])
        back_button.grid(row=17, column=2, padx=10, pady=15)

    alloc_type_label = Label(options_root, text='Allocation Type :')
    alloc_type_label.grid(row=0, padx=10, pady=10)
    alloc_type_entry = Combobox(options_root, justify='center', value=['First Fit', 'Best Fit'], state='readonly')
    alloc_type_entry.grid(row=0, column=1, padx=10, pady=10)

    seg_num_label = Label(options_root, text='Number of Segments :')
    seg_num_label.grid(row=1, padx=10, pady=10)
    seg_num_entry = Entry(options_root)
    seg_num_entry.grid(row=1, column=1, padx=10, pady=10)

    allocate_button = Button(options_root, text='ALLOCATE', command=Allocate)
    allocate_button.grid(row=3, column=0, padx=20, pady=20)

    back_button = Button(options_root, text='BACK',
                         command=lambda: [main_root.deiconify(), options_root.destroy(), plt.close('all'),
                                          dict_of_processes.clear()])
    back_button.grid(row=3, column=1, padx=20, pady=20)

    exit_button = Button(options_root, text='EXIT',
                         command=lambda: [main_root.destroy(), options_root.destroy(), plt.close('all')])
    exit_button.grid(row=3, column=2, padx=20, pady=20)


def Get_Holes():
    """ Windows to get the Holes data from user
        then generates the pre_allocated List"""

    global mem_size, holes_list, pre_allocated_list, processes_counter
    processes_counter = 0
    mem_size = mem_size_entry.get()
    holes_num = holes_num_entry.get()
    if not mem_size.isnumeric() or not holes_num.isnumeric():
        Error_Msg('Please Enter VALID NUMERIC Entries!')
        return
    mem_size = int(mem_size)
    main_root.withdraw()
    holes_root = Tk()
    holes_root.title('HOLES INFO')

    def Get_Values():
        holes_list.clear()
        pre_allocated_list.clear()
        tp_list = []
        for j in range(len(components[0])):
            if components[0][j]['text'] == 'Hole':
                continue

            start = components[1][j].get()
            size = components[2][j].get()
            if not start.isnumeric() \
                    or not size.isnumeric() \
                    or int(start) + int(size) in tp_list \
                    or int(start) in tp_list \
                    or int(start) + int(size) > mem_size:
                Error_Msg('Invalid Start or Size Value(s) Entered!')
                return

            if int(size) == 0:
                continue
            tp_list.extend(list(range(int(start), int(start) + int(size))))
            holes_list.append(dict(start=int(start), size=int(size)))

        # sort holes in ascending order according to start value
        for i in range(len(holes_list) - 1):
            for j in range(len(holes_list) - 1 - i):
                if holes_list[j]['start'] > holes_list[j + 1]['start']:
                    tmp = holes_list[j]
                    holes_list[j] = holes_list[j + 1]
                    holes_list[j + 1] = tmp
        holes_format(holes_list)

        # fill the pre_allocated list
        for i in range(len(holes_list)):
            if holes_list[i] == holes_list[0] and holes_list[i]['start'] != 0:
                pre_allocated_list.append(dict(start=int(0), size=int(holes_list[i]['start'])))
            if holes_list[i] == holes_list[-1]:
                if mem_size - (holes_list[i]['start'] + holes_list[i]['size']) != 0:
                    pre_allocated_list.append(dict(start=int(holes_list[i]['start'] + holes_list[i]['size']),
                                                   size=int(
                                                       mem_size - (
                                                               holes_list[i]['start'] + holes_list[i]['size']))))
            else:
                if holes_list[i + 1]['start'] - (holes_list[i]['start'] + holes_list[i]['size']):
                    pre_allocated_list.append(dict(start=int(holes_list[i]['start'] + holes_list[i]['size']),
                                                   size=int(holes_list[i + 1]['start'] - (
                                                           holes_list[i]['start'] + holes_list[i]['size']))))
        if len(holes_list) == 0:
            pre_allocated_list.append(dict(start=int(0), size=mem_size))

        holes_root.destroy()
        Mem_Control()
        Draw_Mem()

    components = [[], [], []]
    for i in range(int(holes_num)):
        if (i % 15) == 0:
            components[0].append(Label(holes_root, text="Hole"))
            components[1].append(Label(holes_root, text="Start"))
            components[2].append(Label(holes_root, text="Size"))

        components[0].append(Label(holes_root, text='H' + str(i) + ' :'))
        components[1].append(Entry(holes_root, width=10))
        components[2].append(Entry(holes_root, width=10))

    for j in range(len(components[0])):
        components[0][j].grid(row=int(j % 16), column=0 + (int(j / 16) * 3), padx=5, pady=5)
        components[1][j].grid(row=int(j % 16), column=1 + (int(j / 16) * 3), padx=5, pady=5)
        components[2][j].grid(row=int(j % 16), column=2 + (int(j / 16) * 3), padx=5, pady=5)

    done_button = Button(holes_root, text='DONE', command=Get_Values)
    done_button.grid(row=17, column=1, padx=10, pady=15)

    back_button = Button(holes_root, text="BACK", command=lambda: [holes_root.destroy(), main_root.deiconify()])
    back_button.grid(row=17, column=2, padx=10, pady=15)


welcome_label = Label(main_root, text='______Welcome______\n. . . . .')
welcome_label.grid(row=0, columnspan=2, padx=30, pady=20)

mem_size_label = Label(main_root, text='Memory Size :')
mem_size_label.grid(row=1, padx=10, pady=10)
mem_size_entry = Entry(main_root)
mem_size_entry.grid(row=1, column=1, padx=10, pady=10)

holes_num_label = Label(main_root, text='Number of Holes :')
holes_num_label.grid(row=2, padx=10, pady=10)
holes_num_entry = Entry(main_root)
holes_num_entry.grid(row=2, column=1, padx=10, pady=10)

next_button = Button(main_root, text='NEXT', command=Get_Holes)
next_button.grid(row=3, columnspan=2, padx=30, pady=20)

main_root.mainloop()
