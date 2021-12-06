# --------------------------------------
# Class Name: BreakWheel
# Purpose: Simulate a Japanese cipher machine break (or pin) wheel, a
#          common component in IKA, RED, and other cipher machines
# Field: total_num_pins  The total number of pins defined for the break wheel
# Field: inactive_pins  A list of integers denoting the inactive pins (the
#        numbers are 1-based, not 0-based)
# Field: pin_number  The current pin position of the break wheel.  It should
#        always be in the range of 1 to <total_num_pins>.
# Note: As mentioned above, the pin numbers are 1-based indexes, not
#       0-based offsets.  This was done because the cryptographer historically
#       refers to the pins starting with 1.
# --------------------------------------
class BreakWheel:
    def __init__(self, total_num_pins, inactive_pins):
        self.total_num_pins = total_num_pins
        self.inactive_pins = inactive_pins
        self.pin_number = 1

        self.Verify()

    # --------------------------------------
    # Function Name: Verify
    # Purpose: Validate the data definitions passed to the constructor
    # --------------------------------------
    def Verify(self):
        for i in self.inactive_pins:
            if not isinstance(i, int):
                raise Exception('Non-integer inactive pin (%d) encountered' % i)

        if self.total_num_pins < 1:
            raise Exception('BreakWheel has invalid number of pins (%d)' % self.total_num_pins)

        if len(self.inactive_pins) > self.total_num_pins:
            raise Exception('BreakWheel has more inactive pins (%d) than total pins (%d)' %
                            (len(self.inactive_pins), self.total_num_pins))

        # Inactive pin numbers must be in range of 1 - self.total_num_pins
        for i in self.inactive_pins:
            if (i < 0) or (i > self.total_num_pins):
                raise Exception(
                    'BreakWheel: Inactive pin number (%d) in out of range (should be 1-%d' % (self.total_num_pins))

        # Make sure there are no duplicate elements in self.inactive_pins
        inactive_pin_set = set()
        for i in self.inactive_pins:
            if i in inactive_pin_set:
                raise Exception('BreakWheel: Duplicate inactive pin "%d" encountered' % (i))
            inactive_pin_set.add(i)

        # Verify there is at least one (1) active pin
        if self.total_num_pins - len(inactive_pin_set) == 0:
            raise Exception('BreakWheel: There are no active pins')

    # --------------------------------------
    # Function Name: SetPinNumber
    # Purpose: Set the value of <self.pin_number>
    # Parameter: pin_number  The pin number to be assigned to self.pin_number
    # --------------------------------------
    def SetPinNumber(self, pin_number):
        n = pin_number % (self.total_num_pins + 1)
        if n == 0:
            n = 1
        self.pin_number = n

    # --------------------------------------
    # Function Name: ComputePinNumber
    # Purpose: Normalize a pin number, keeping the result 1-based and in
    #          the correct range
    # Parameter: pin_number  The possibly non-normalized pin_number
    # Returns: The normalized pin number
    # --------------------------------------
    def ComputePinNumber(self, pin_number):
        normalized_pin_number = pin_number % (self.total_num_pins + 1)
        if normalized_pin_number == 0:
            normalized_pin_number = 1
        return normalized_pin_number

    # --------------------------------------
    # Function Name: ReturnSlide
    # Purpose: Compute the next break wheel slide factor (i.e.,
    #          how much the wheel advances at the next step), and
    #          change the break wheel's current offset accordingly.
    # Returns: The slide factor
    # --------------------------------------
    def ReturnSlide(self):
        slide = 0
        while True:
            if not (self.pin_number + 1) in self.inactive_pins:
                break
            slide = slide + 1
            self.pin_number = (self.pin_number + 1) % self.total_num_pins
            if self.pin_number == 0:
                self_pin_number = 1

        self.pin_number = self.ComputePinNumber(self.pin_number + 1)
        return slide + 1

    # --------------------------------------
    # Function Name: ReturnCurrentPin
    # Returns: Return the current offset of the break wheel
    # --------------------------------------
    def ReturnCurrentPin(self):
        return self.pin_number

    # --------------------------------------
    # Function Name: FormatBreakWheelPinNumber
    # Purpose: Return a string denoting a given pin number, formatting
    #          it depending on it is an an active pin (e.g., '25'), and
    #          inactive pin ('_'), and if it is the current pin ('[25]').
    # Returns: The formatted pin number as a string
    # --------------------------------------
    def FormatBreakWheelPinNumber(self, pin_number):
        if pin_number in self.inactive_pins:
            s = str(pin_number)
            s = '_'
        else:
            s = str(pin_number)
        if pin_number == self.pin_number:
            s = '[' + s + ']'

        return s

    # --------------------------------------
    # Function Name: Dump
    # Purpose: A debugging function for tracing the state of this class
    # Parameter: desc  A descriptive string printed in the trace dump
    # --------------------------------------
    def Dump(self, desc, verbose):
        print('\nDumping break wheel: %s' % (desc))
        if verbose:
            for i in range(1, self.total_num_pins + 1):
                if (i > 1):
                    print(' ', end='')
                self.FormatBreakWheelPinNumber(i)
                print(self.FormatBreakWheelPinNumber(i), end='')
        else:
            # Dump abridged version of break wheel
            i = self.pin_number
            print(self.FormatBreakWheelPinNumber(i), end='')
            while True:
                i = self.ComputePinNumber(i + 1)
                print(' ' + self.FormatBreakWheelPinNumber(i), end='')
                if not i in self.inactive_pins:
                    break
        print()
