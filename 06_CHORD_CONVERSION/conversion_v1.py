class Note:
    def __init__(self):
        self.x = []
        self.y = []
        self.musicpaper = 0

    def push(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def pop(self):
        return self.x.pop(), self.y.pop()

    def length(self):
        return len(self.x)

    def set_input(self):
        x = int(input())
        y = int(input())
        self.push(x, y)

    def print_xy(self, i):
        print(self.x[i], self.y[i])

    def output_xy(self, i):
        return self.x[i], self.y[i]

    def set_musicpaper(self, musicpaper):
        self.musicpaper = musicpaper

    def change_note(self, i, gap):
        self.y[i] = self.y[i] + gap * self.musicpaper


def change(base, step, musicPaper):  # 음표 y 위치, 기본 악보 코드와 변환 악보 코드의 차, 오선지 한칸 크기를 이용하여 음표 y 값 변환
    num = base + step * musicPaper
    return num


def transpose(org, ch):  # 기본 코드와 변하고 싶은 코드를 이용한 차이 return
    if org == 'C':
        base = 1
    elif org == 'D':
        base = 2
    elif org == 'E':
        base = 3
    elif org == 'F':
        base = 4
    elif org == 'G':
        base = 5
    elif org == 'A':
        base = 6
    elif org == 'B':
        base = 7
    else:
        print("잘못 입력 하셨습니다.")

    if ch == 'C':
        change = 1
    elif ch == 'D':
        change = 2
    elif ch == 'E':
        change = 3
    elif ch == 'F':
        change = 4
    elif ch == 'G':
        change = 5
    elif ch == 'A':
        change = 6
    elif ch == 'B':
        change = 7
    else:
        print("잘못 입력 하셨습니다.")
    gap = base - change
    return gap


# main
note = Note()
note.set_musicpaper(2)
org = input("기본 악보 코드(조) : ")
print(org)
ch = input("원하는 코드(조) : ")
print(ch)
gap = transpose(org, ch)
print(f"갭의 차이 : {gap}")
print("-------------------")
notenum = int(input("음표 개수 :"))
print(notenum)
print("-------------------")
i = 0
while i < notenum:  # 음표 삽입
    note.set_input()
    i = i + 1
i = 0
while i < notenum:  # 음표 출력
    note.print_xy(i)
    i = i + 1
print("-------------------")
i = 0
while i < notenum:  # 음표 변환
    note.change_note(i, gap)
    i = i + 1
i = 0
while i < notenum:  # 음표 출력
    note.print_xy(i)
    i = i + 1
print("-------------------")