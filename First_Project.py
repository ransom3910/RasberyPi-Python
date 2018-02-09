import time  # Needed for timers
import gpiozero  # Needed to control GPIO pins
import threading  # Needed so that both objects can run their light test at the same time and
                # allow the menu to run while the lights are running

# GPIO PIN Assignments for each LED
s1_g = 8
s1_y = 7
s1_r = 25
s2_g = 11
s2_y = 9
s2_r = 10
begin_status = True
end_program = False
choice = ""


class Stoplight(threading.Thread):
    """Class Object that represents a stoplight"""

    def __init__(self, red, yellow, green):
        """Assign GPIO pins to color objects and run through light test """
        self.red = gpiozero.LED(red)
        self.yellow = gpiozero.LED(yellow)
        self.green = gpiozero.LED(green)

    def xmus_tree(self):
        """Lights up all the lights on the stop light for testing"""
        self.red.on()
        self.green.on()
        self.yellow.on()
        time.sleep(5)
        self.red.off()
        self.green.off()
        self.yellow.off()

    def red_light(self):
        """Turn red light on while turning off yellow and green"""
        self.green.off()
        self.yellow.off()
        self.red.on()

    def green_light(self):
        """Turn red light off after short delay, then turn green light on"""
        self.red.on()
        time.sleep(1)
        self.red.off()
        self.yellow.off()
        self.green.on()

    def yellow_light(self):
        """Turn yellow light on while turning green and red off"""
        self.green.off()
        self.red.off()
        self.yellow.on()

    def flash_yellow(self):
        """Turns off red and gree and flashes yellow"""
        self.green.off()
        self.red.off()
        self.yellow.blink(1, 1, 10)

    def flash_red(self):
        """Turns off green and yellow then flashes red"""
        self.green.off()
        self.yellow.off()
        self.red.blink(1, 1, 10)

    def all_off(self):
        """Turns off all lights"""
        self.green.off()
        self.red.off()
        self.yellow.off()


def begin(street1, street2):
    """Runs the stop light"""
    global begin_status
    print("Starting the stop light")
    while begin_status:  # Run until menu function changes begin_status to False
        count = 0
        while count < 2 and begin_status:  # Run through normal traffic light patten for number of times specified
            if begin_status:
                street1.red_light()
                street2.green_light()
                time.sleep(5)
            if begin_status:
                street2.yellow_light()
                time.sleep(2)
            if begin_status:
                street2.red_light()
                street1.green_light()
                time.sleep(5)
            if begin_status:
                street1.yellow_light()
                time.sleep(2)
                count += 1

        # Start late night flashing
        if begin_status:
            street1.flash_red()
            street2.flash_yellow()
            time.sleep(10)


def menu():
    """Pressing enter will call exit which will cause all threads to stop and turn off the light"""
    global begin_status
    global end_program
    global choice
    print("(1) Turn on the stop light")
    print("(2) Turn off the stop light ")
    print("(3) Exit")
    choice = input("Enter (1), (2), or (3): ")
    if choice == "1":
        pass
    elif choice == "2":
        begin_status = False

    elif choice == "3":
        begin_status = False
        end_program = True
    else:
        print("Please choose 1,2, or 3")


def main():
    """This Program simulates a traffic light with a breadboard, LEDs controlled by the GPIO pins on the Pi"""

    street1 = Stoplight(s1_r, s1_y, s1_g)  # Street 1 top light
    street2 = Stoplight(s2_r, s2_y, s2_g)  # Street 2 stop light
    while end_program == False:
        t = threading.Thread(target=menu)
        t.start()
        t.join()

        if choice == "1":
            global begin_status
            t = threading.Thread(target=street1.xmus_tree)
            print("Testing the stop light")
            t.start()
            t = threading.Thread(target=street2.xmus_tree)
            t.start()
            t.join()
            begin_status = True
            t = threading.Thread(target=begin, name='StopLight', args=(street1, street2))
            t.daemon = True
            t.start()

        if choice == "2":
            street1.all_off()
            street2.all_off()


if __name__ == '__main__':
    main()































