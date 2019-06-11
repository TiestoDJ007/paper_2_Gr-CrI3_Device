import numpy as np
import scipy.io as sciio
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    # 各个原子的DOS
    data_dos = sciio.loadmat('data_dos.mat')
    dos_upper = data_dos['data_dos'][:, 0, :]
    dos_under = data_dos['data_dos'][:, 1, :]
    # 各个原子的位置
    atom_file = open('scf.input', 'r')
    atom_line = []
    line = atom_file.readline()
    while line:
        atom_line.append(line)
        line = atom_file.readline()
    atom_file.close()
    atom_position = []
    for i in range(57, len(atom_line) - 1, 1):
        position_line = atom_line[i].split()
        position_atom = [position_line[0], np.array((position_line[2], position_line[3], position_line[4]))]
        atom_position.append(position_atom)
    # 画图数据,并将画图数据排序
    plot_data_up = []
    for i in range(len(atom_position)):
        plot_data_up.append([atom_position[i][1][0], dos_upper[i]])
    plot_data_up = np.array(plot_data_up)
    data_up_sort = plot_data_up[np.argsort(plot_data_up[:, 0], kind='mergesort')].tolist()
    #排序数组并将第一列相同的数对应的数据进行加和，将第一个遇到的数变成num_start,向下对比此位，当数不同的时候记录其序号为num_end,
    #再将num_start和num_end设置为加和的头和尾，进行加和。
    data_dos_up = []
    num_same = 0
    num_start = 0
    num_check = []
    for i in range(len(data_up_sort)):
        atom_total = data_up_sort[num_start][1]
        if i != len(data_up_sort) - 1:
            if data_up_sort[i][0] == data_up_sort[i + 1][0]:
                num_same = num_same + 1
            elif data_up_sort[i][0] != data_up_sort[i + 1][0]:
                num_end = num_same
                num_check.append(num_end)
                for j in range(num_start + 1, num_end + 1):
                    atom_total += data_up_sort[j][1]
                data_dos_up.append([data_up_sort[num_start][0], atom_total])
                num_start = num_same + 1
                num_same = num_start
        else:
            if data_up_sort[i][0] == data_up_sort[i - 1][0]:
                num_same = num_same + 1
                num_end = num_same
                num_check.append(num_end)
                for j in range(num_start + 1, num_same):
                    atom_total += data_up_sort[j][1]
                data_dos_up.append([data_up_sort[num_start][0], atom_total])
            else:
                data_dos_up.append([data_up_sort[i][0], data_up_sort[i][1]])

    # plot_data_down = []
    # for i in range(len(atom_position)):
    #    plot_data_down.append([atom_position[i][1][0], dos_under[i]])

    # data_plot = np.reshape(data_plot_up[:,2],(401,200))
    # ax=sns.heatmap(data_plot)
    # plt.show()
