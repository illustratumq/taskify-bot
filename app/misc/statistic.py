import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_charts(overdue, close_deadline, far_deadline, tasks_done, tasks_remaining):
    colors = ['#FF5555', '#FFC168', '#63C887']
    labels = ['Прострочено', 'Близькі до дедлайну', 'Далекі від дедлайну']
    sizes = [overdue, close_deadline, far_deadline]
    explode = (0.1, 0.1, 0.1)

    fig = plt.figure(figsize=(6, 8))

    tasks_values = [tasks_done, tasks_remaining]

    ax1 = fig.add_subplot(211)
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    ax1.set_title('Статистика дедлайнів')

    ax2 = fig.add_subplot(212, projection='3d')
    ax2.bar3d([0.4], [0], [0], [1.2], [1], [sum(tasks_values)], color='lightgray', alpha=0.3)
    ax2.bar3d([0.4], [0], [0], [1.2], [1], [tasks_done], color='#5dcc', alpha=1)
    ax2.set_xticks([0.9])
    ax2.set_xticklabels(['Завдання'])
    ax2.set_yticks([])
    ax2.set_zlabel('Кількість')
    ax2.set_title('Статистика завдань')

    plt.tight_layout()
    plt.savefig('name.png')
    plt.show()


create_charts(3, 5, 8, 10, 15)
