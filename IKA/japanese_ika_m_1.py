class DammHalfRotor:
    def __init__(self, alphabet, offset=0):
        self.alphabet = alphabet
        self.offset = offset
        
        # Determine longest alphabet element
        self.max_element_length = 0
        for a in alphabet:
            if len(a) > self.max_element_length:
                self.max_element_length = len(a)

    def SetAbsoluteOffset(self, offset):
        self.offset = offset
        
    def IncrementOffset(self, increment):
        self.offset = (self.offset + increment) % len(self.alphabet)
        
    def Decipher(self, element):
        #print('self.offset=%d' % (self.offset)) #debug
        index1 = self.alphabet.index(element)
        #print('index1=%d' % (index1)) #debug
        index2 = (index1 + self.offset) % len(self.alphabet)
        #print('index2=%d' % (index2)) #debug
        return self.alphabet[index2]
        
    def Dump(self, desc, verbose):
        print('Dumping Damm half rotor: %s' % (desc))
        for a in self.alphabet:
            print(a.ljust(self.max_element_length) + ' ', end='')
        print()
        
        for i in range(len(self.alphabet)):
            offset = (self.offset + i) % len(self.alphabet)
            print(self.alphabet[offset].ljust(self.max_element_length) + ' ', end='')
            
        print()

class BreakWheel:
    def __init__(self, total_num_pins, inactive_pins):
        self.total_num_pins = total_num_pins
        self.inactive_pins = inactive_pins
        self.pin_number = 1
        
    def SetPinNumber(self, pin_number):
        n = pin_number % (self.total_num_pins + 1)
        if n == 0:
            n = 1
        self.pin_number = n
        
    def ComputePinNumber(self, pin_number, increment):
        pin_number = (pin_number + increment) % (self.total_num_pins + 1)
        if pin_number == 0:
            pin_number = 1
        return pin_number
        
    def ReturnSlide(self):
        slide = 0
        while True:
            if not (self.pin_number + 1) in self.inactive_pins:
                break
            slide = slide + 1
            self.pin_number = (self.pin_number + 1) % self.total_num_pins
            if self.pin_number == 0:
                self_pin_number = 1
                
        self.pin_number = self.ComputePinNumber(self.pin_number, 1)
        return slide+1
        
    def ReturnCurrentPin(self):
        return self.pin_number

    def FormatBreakWheelPinNumber(self, pin_number):
        if pin_number in self.inactive_pins:
            s = str(pin_number)
            #s = '_' * len(s)
            s = '_'
        else:
            s = str(pin_number)
        if pin_number == self.pin_number:
            s = '[' + s + ']'
            
        return s
        
    def Dump(self, desc, verbose):
        print('Dumping break wheel: %s' % (desc))
        if verbose:
            for i in range (1, self.total_num_pins+1):
                if (i > 1):
                    print(' ', end='')
                self.FormatBreakWheelPinNumber(i)
                print(self.FormatBreakWheelPinNumber(i), end='')
        else:
            # Dump abridged version of break wheel
            i = self.pin_number
            print(self.FormatBreakWheelPinNumber(i), end='')
            while True:
                i = self.ComputePinNumber(i, 1)
                print(' ' + self.FormatBreakWheelPinNumber(i), end='')
                if not i in self.inactive_pins:
                    break

        print()
        print()
        
class MonoalphabeticMapping:
    def __init__(self, mono_map):
        self.mono_map = mono_map
        
    def IsInMap(self, element):
        return (element in self.mono_map)
        
    def ReturnSubstitution(self, element):
        if self.IsInMap(element):
            return self.mono_map[element]
        else:
            return None

class IkaMachine:
    def __init__(self, major_alphabet, starting_offset, minor_alphabet, num_of_pins, inactive_pin_list, **kwargs):
        self.trace = kwargs['trace']

        self.major_alphabet = major_alphabet
        self.starting_offset = starting_offset
        self.minor_alphabet = minor_alphabet
        self.num_of_pins = num_of_pins
        self.inactive_pin_list = inactive_pin_list
        
        self.half_rotor = DammHalfRotor(self.major_alphabet, self.starting_offset)
        self.mono_map = MonoalphabeticMapping(self.minor_alphabet)
        self.break_wheel = BreakWheel(self.num_of_pins, self.inactive_pin_list)
        
        if (self.trace):
            self.TraceComponents('Initial setup state', verbose=True)

    def TraceComponents(self, desc, **kwargs):
        verbose = False
        if 'verbose' in kwargs:
            verbose = kwargs['verbose']
        self.break_wheel.Dump(desc, verbose)
        self.half_rotor.Dump(desc, verbose)
        
    def decipher(self, ct):
        complete_pt = ''
        count = 0
        for e in ct:
            print('-----------------------------------------')
            sub = self.mono_map.ReturnSubstitution(e)
            if (sub == None):
                # Not found in minor alphabet, decipher with major alphabet
                pt = self.half_rotor.Decipher(e)
                print('%d: %s -> %s' % (count, e, pt))  #debug
                complete_pt = complete_pt + pt + ' '
            else:
                # Found in minor alphabet
                complete_pt = complete_pt + sub + ' '
                print('%d: %s -> %s' % (count, e, sub))  #debug

            count = count + 1
            slide = self.break_wheel.ReturnSlide()
            self.half_rotor.IncrementOffset(slide);
            print('slide=%d' % (slide)) #debug

            if (self.trace):
                self.TraceComponents('After deciphering')

        return complete_pt

def unit_test_01():
    # (1) Break wheel
    number_of_pins = 47
    inactive_pin_list = [5, 8, 11, 17, 22, 25, 26, 29, 34, 37, 41, 44, 46]
    break_wheel = BreakWheel(number_of_pins, inactive_pin_list)
    expected_slides = [1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1]

    starting_pin = break_wheel.ReturnCurrentPin()

    expected_slide_offset = 0
    while True:
        current_pin = break_wheel.ReturnCurrentPin()
        #print('(1) current_pin=%d' % (break_wheel.ReturnCurrentPin()))    #debug
        slide = break_wheel.ReturnSlide()
        #print('(2) current_pin=%d' % (break_wheel.ReturnCurrentPin()))    #debug
        if expected_slides[expected_slide_offset] != slide:
            # Error
            print('unit_test_01: Failure: When sliding from pin %d, expected slide of %d, got %d' % (current_pin, expected_slides[expected_slide_offset], slide))
            return
        if break_wheel.ReturnCurrentPin() == starting_pin:
            break
        expected_slide_offset = (expected_slide_offset + 1) % len(expected_slides)

    print('unit_test_01: Success')

def unit_test_02():
    # Verify slide computation wraps correctly at end of pin list
    # Break wheel
    number_of_pins = 47
    inactive_pin_list = [47]
    break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

    # 
    break_wheel.SetPinNumber(46)
    slide = break_wheel.ReturnSlide()
    if slide != 2:
        print('unit_test_02: Failure: Expected slide of 2, received %d instead' % (slide))
        return

    print('unit_test_02: Success')

def unit_test_03():
    # Verify slide computation wraps correctly at end of pin list
    # Break wheel
    number_of_pins = 47
    inactive_pin_list = [1, 2, 47]
    break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

    # 
    break_wheel.SetPinNumber(1)
    slide = break_wheel.ReturnSlide()
    if slide != 2:
        print('unit_test_03: Failure: Expected slide of 2, received %d instead' % (slide))
        return

    # 
    break_wheel.SetPinNumber(46)
    slide = break_wheel.ReturnSlide()
    if slide != 4:
        print('unit_test_03: Failure: Expected slide of 4, received %d instead' % (slide))
        return

    print('unit_test_03: Success')

def unit_test_04():
    # Verify slide computation wraps correctly at end of pin list
    # Break wheel
    number_of_pins = 10
    inactive_pin_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

    # 
    break_wheel.SetPinNumber(1)
    slide = break_wheel.ReturnSlide()
    if slide != 10:
        print('unit_test_04: Failure: Expected slide of 10, received %d instead' % (slide))
        return

    print('unit_test_04: Success')
    
def main():
    # Perform unit tests
    unit_test_01()
    unit_test_02()
    unit_test_03()
    unit_test_04()
    
if __name__ == "__main__":
    main()
    