import time


def current_time():
    return int(round(time.time() * 1000))


while True:
    start = input('start logging?\n')
    if start in ('y', 'Y'):
        start_time = current_time()
        eye_arr = []
        serial_nunmber = []
        iterator = 0
        print('Initiating logger\n')
        while True:
            iterator += 1
            movement = input()
            if movement in ('p', 'P'):
                a = []
                a.append(iterator)
                a.append('Prolonged')
                a.append(current_time())
                a.append(current_time() - start_time)
                eye_arr.append(a)
            elif movement in ('r', 'R'):
                a = []
                a.append(iterator)
                a.append('Right gaze')
                a.append(current_time())
                a.append(current_time() - start_time)
                eye_arr.append(a)
            elif movement in ('l', 'L'):
                a = []
                a.append(iterator)
                a.append('Left gaze')
                a.append(current_time())
                a.append(current_time() - start_time)
                eye_arr.append(a)
            elif movement in ('u', 'U'):
                a = []
                a.append(iterator)
                a.append('Upward gaze')
                a.append(current_time())
                a.append(current_time() - start_time)
                eye_arr.append(a)
            elif movement in ('d', 'D'):
                a = []
                a.append(iterator)
                a.append('Down gaze')
                a.append(current_time())
                a.append(current_time() - start_time)
                eye_arr.append(a)
            else:
                if movement in ('q', 'Q'):
                    print('start time:')
                    print(start_time)
                    print()
                    print('Logger output:')
                    print('Sr. No.','\t','eye movement','\t','time of occurence (ms)','\t','time elapsed since start of logging')
                    for i in eye_arr:
                        print(*i, sep='\t')
                    # print(eye_arr)
                    print()
                    break
                else:
                    print('Please enter valid eye movements')

    elif start in ('n', 'N'):
        break
    else:
        print('Please enter valid response to begin\n')
        continue
