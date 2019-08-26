import pyautogui
import random
import sys
import time


def craftingdict(durability):

    # returns a tuple containing macro button co-ordinates

    if durability == 80:
        return (1827, 980)
    elif durability == 40:
        return (1785, 980)
    else:
        return "ERROR"


def autocraft(durability, n_loops, collectable=False):

    # setup vars
    DURABILITY = durability
    if craftingdict(durability) == "ERROR":
        print('Invalid durability.')
        return
    FOOD_NECESSARY = False
    FOOD_DURATION = 1800
    MIN_CRAFT_TIME = 40
    MAX_CRAFT_VARIANCE = 5
    MIN_SELECTION_TIME = 3
    MAX_SELECTION_VARIANCE = 2
    SELECT_X = 1395  # synth button X
    SELECT_Y = 1300  # synth button Y
    CRAFT_X = craftingdict(DURABILITY)[0]  # macro X
    CRAFT_Y = craftingdict(DURABILITY)[1]  # macro Y
    SECOND_BUTTON = False
    SECOND_CRAFT_X = 0  # second button, if one is required
    SECOND_CRAFT_Y = 0  # second button, if one is required
    COLLECTABLE_X = 0  # collectable confirmation co-ordinates
    COLLECTABLE_Y = 0  # collectable confirmation co-ordinates
    COLLECTABLE_TIME = 5
    MAX_COLLECTABLE_VARIANCE = 2
    MAX_COORD_VARIANCE = 5
    LOOP_N = n_loops  # number of crafts
    PAUSE_TIME = 0.250
    RELOCATE_TIME = 5
    MIN_MOUSE_TIME = 0.50
    MAX_MOUSE_TIME = 2.50

    total_time = 0

    if LOOP_N == 0:
        print('No crafts to loop.')
        return

    crafts = {'x': [CRAFT_X], 'y': [CRAFT_Y]}

    if SECOND_BUTTON:
        crafts['x'].append(SECOND_CRAFT_X)
        crafts['y'].append(SECOND_CRAFT_Y)

    print('Get to your window within {0} seconds!'.format(RELOCATE_TIME))
    time.sleep(RELOCATE_TIME)

    for i in range(LOOP_N):

        print('Commencing loop {0} of {1}...'.format(i + 1, LOOP_N))
        pyautogui.moveTo(SELECT_X + getvariance(MAX_COORD_VARIANCE, True),
                         SELECT_Y + getvariance(MAX_COORD_VARIANCE, True),
                         random.uniform(MIN_MOUSE_TIME, MAX_MOUSE_TIME))
        time.sleep(PAUSE_TIME)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        sleep_time = MIN_SELECTION_TIME + getvariance(MAX_SELECTION_VARIANCE)
        total_time += sleep_time + PAUSE_TIME
        time.sleep(sleep_time)

        for j in range(len(crafts['x'])):  # arbitrary, can be either

            current_x = crafts['x'][j] + getvariance(MAX_COORD_VARIANCE, True)
            current_y = crafts['y'][j] + getvariance(MAX_COORD_VARIANCE, True)

            pyautogui.moveTo(current_x, current_y,
                             random.uniform(MIN_MOUSE_TIME, MAX_MOUSE_TIME))
            time.sleep(PAUSE_TIME)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            sleep_time = MIN_CRAFT_TIME + getvariance(MAX_CRAFT_VARIANCE)
            total_time += sleep_time + PAUSE_TIME
            time.sleep(sleep_time)

            if collectable:
                pyautogui.moveTo(COLLECTABLE_X, COLLECTABLE_Y,
                                 random.uniform(MIN_MOUSE_TIME, MAX_MOUSE_TIME))
                time.sleep(PAUSE_TIME)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                sleep_time = COLLECTABLE_TIME + getvariance(MAX_COLLECTABLE_VARIANCE)
                total_time += sleep_time + PAUSE_TIME
                time.sleep(sleep_time)

        if FOOD_NECESSARY:
            if total_time > FOOD_DURATION:
                print('Total time exceeds food time, terminating.')
                return

    print('Complete!')


def getvariance(max_variance, plusorminus=False):
    if plusorminus:
        plusorminus_decision = random.randint(0, 1)
        if plusorminus_decision == 0:
            return random.uniform(0, max_variance)
        else:
            return random.uniform(-1 * max_variance, 0)
    else:
        return random.uniform(0, max_variance)


if __name__ == '__main__':

    try:
        durability = int(input('Please select the durability of the craft.\n>'))
    except ValueError:
        print('Durability must be an integer.')
        sys.exit(1)

    collectable = input('Type Y to enable collectable mode.\n>')

    try:
        n_loops = int(input('Please select the number of loops.\n>'))
    except ValueError:
        print('The number of loops must be an integer.')
        sys.exit(1)

    if collectable == 'Y':
        autocraft(durability, n_loops, True)
    else:
        autocraft(durability, n_loops)