#--------------------------------------
# Class Name: DammHalfRotor
# Purpose: Simulate a Damm half rotor
# Field: alphabet  An ordered list of strings comprising the
#        alphabet to be used
# Field: offset  The shift between the plaintext and ciphertext alphabets,
#        which consist of <alphabet> shifted against itself
# Field: max_element_length  The longest alphabet string defined
# Note: The alphabet used by this class consists of strings,
#       not single characters.  This is because the IKA cipher
#       machine enciphered/deciphered Romaji kana symbols, typically
#       consting of multiple characters (e.g., RO, KA, SE).
#--------------------------------------
class DammHalfRotor:
    def __init__(self, alphabet, offset=0):
        self.alphabet = alphabet
        self.offset = offset
        
        # Determine longest alphabet element
        self.max_element_length = 0
        for a in alphabet:
            if len(a) > self.max_element_length:
                self.max_element_length = len(a)

    #--------------------------------------
    # Function Name: SetAbsoluteOffset
    # Purpose: Set the offset of self.alphabet against itself
    # Parameter: offset  The offset of self.alphabet against itself
    #--------------------------------------
    def SetAbsoluteOffset(self, offset):
        self.offset = offset
        
    #--------------------------------------
    # Function Name: IncrementOffset
    # Purpose: Increment the current offset value
    # Parameter: increment  The delta by which to increment self.offset
    #--------------------------------------
    def IncrementOffset(self, increment):
        self.offset = (self.offset + increment) % len(self.alphabet)
        
    #--------------------------------------
    # Function Name: Decipher
    # Purpose: Decipher a given ciphertext <element>, given the current
    #          state of the IKA machine
    # Parameter: element  The ciphertext element to be deciphered
    # Returns: The deciphered element (i.e., the plaintext element)
    #--------------------------------------
    def Decipher(self, element):
        index1 = self.alphabet.index(element)
        index2 = (index1 + self.offset) % len(self.alphabet)
        return self.alphabet[index2]
        
    #--------------------------------------
    # Function Name: Dump
    # Purpose: A debugging function for tracing the state of this class
    # Parameter: desc  A descriptive string printed in the trace dump
    #--------------------------------------
    def Dump(self, desc):
        print('Dumping Damm half rotor: %s' % (desc))
        for a in self.alphabet:
            print(a.ljust(self.max_element_length) + ' ', end='')
        print()
        
        for i in range(len(self.alphabet)):
            offset = (self.offset + i) % len(self.alphabet)
            print(self.alphabet[offset].ljust(self.max_element_length) + ' ', end='')
        print()

#--------------------------------------
# Class Name: BreakWheel
# Purpose: Simulate a Japanese cipher machine break (or pin) wheel, a
#          common component in IKA, RED, and other cipher machines
# Field: total_num_pins  The total number of pins defined for the break wheel
# Field: inactive_pins  A list of integers denoting the inactive pins (the
#        numbers are 1-based, not 0-based)
# Field: pin_number  The current pin position of the break wheel.  It should
#        always be in the range of 1 to <total_num_pins>.
# Note: As mentioned above, the pin numbers are 1-based indexes, not
#       0-based offsets.
#--------------------------------------
class BreakWheel:
    def __init__(self, total_num_pins, inactive_pins):
        self.total_num_pins = total_num_pins
        self.inactive_pins = inactive_pins
        self.pin_number = 1
        
    #--------------------------------------
    # Function Name: SetPinNumber
    # Purpose: Set the value of <self.pin_number>
    # Parameter: pin_number  The pin number to be assigned to self.pin_number
    #--------------------------------------
    def SetPinNumber(self, pin_number):
        n = pin_number % (self.total_num_pins + 1)
        if n == 0:
            n = 1
        self.pin_number = n
        
    #--------------------------------------
    # Function Name: ComputePinNumber
    # Purpose: Normalize a pin number, keeping the result 1-based and in
    #          the correct range
    # Parameter: pin_number  The possibly non-normalized pin_number
    # Returns: The normalized pin number
    #--------------------------------------
    def ComputePinNumber(self, pin_number):
        normalized_pin_number = pin_number % (self.total_num_pins + 1)
        if normalized_pin_number == 0:
            normalized_pin_number = 1
        return normalized_pin_number
        
    #--------------------------------------
    # Function Name: ReturnSlide
    # Purpose: Compute the next break wheel slide factor (i.e.,
    #          how much the wheel advances at the next step), and
    #          change the break wheel's current offset accordingly.
    # Returns: The slide factor
    #--------------------------------------
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
        return slide+1
        
    #--------------------------------------
    # Function Name: ReturnCurrentPin
    # Returns: Return the current offset of the break wheel
    #--------------------------------------
    def ReturnCurrentPin(self):
        return self.pin_number

    #--------------------------------------
    # Function Name: FormatBreakWheelPinNumber
    # Purpose: Return a string denoting a given pin number, formatting
    #          it depending on it is an an active pin (e.g., '25'), and
    #          inactive pin ('_'), and if it is the current pin ('[25]').
    # Returns: The formatted pin number as a string
    #--------------------------------------
    def FormatBreakWheelPinNumber(self, pin_number):
        if pin_number in self.inactive_pins:
            s = str(pin_number)
            s = '_'
        else:
            s = str(pin_number)
        if pin_number == self.pin_number:
            s = '[' + s + ']'
            
        return s
        
    #--------------------------------------
    # Function Name: Dump
    # Purpose: A debugging function for tracing the state of this class
    # Parameter: desc  A descriptive string printed in the trace dump
    #--------------------------------------
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
                i = self.ComputePinNumber(i + 1)
                print(' ' + self.FormatBreakWheelPinNumber(i), end='')
                if not i in self.inactive_pins:
                    break

        print()
        print()
        
#--------------------------------------
# Class Name: ManoalphabeticMapping
# Purpose: Perform a monoalphabetic mapping of ciphertext strings to their plaintext phrases
# Field: mono_map  A dictionary mapping ciphertext to plaintext items
#--------------------------------------
class MonoalphabeticMapping:
    def __init__(self, mono_map):
        self.mono_map = mono_map
        
    #--------------------------------------
    # Function Name: IsInMap
    # Purpose: Determine if a ciphertext element exists in the mapping
    # Parameter: element  The ciphertext element to look for
    # Returns: True if <element> is a member of <mono_map>, False otherwise
    #--------------------------------------
    def IsInMap(self, element):
        return (element in self.mono_map)
        
    #--------------------------------------
    # Function Name: ReturnSubstitution
    # Purpose: Return decipherment of <element>
    # Parameter: element  The ciphertext element to decipher
    # Returns: The deciphered element (i.e., plaintext element) if exists,
    #          else None
    #--------------------------------------
    def ReturnSubstitution(self, element):
        if self.IsInMap(element):
            return self.mono_map[element]
        else:
            return None

#--------------------------------------
# Class Name: IkaMachine
# Purpose: Perform the deciphering operation of a Japanese IKA cipher machine
# Field: trace  True if the deciphering operation should produce debugging
#        traces during its steps
# Field: major_alphabet  An ordered list of alphabetic elements, used for 
#        populating the Damm half rotor
# Field: starting_offset  The initial offset of the Damm half rotor
# Field: minor_alphabet  A dictionary of ciphertext elements and their
#        plaintext counterparts
# Field: num_of_pins  The total number of pins defined for the break wheel
# Field: inactive_pins  A list of integers denoting the inactive pins (the
#        numbers are 1-based, not 0-based)
# Field: half_rotor  Instatiated Damm half rotor object
# Field: break_wheel  Instantiated break wheel object
#--------------------------------------
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

        if self.trace:        
            self.TraceComponents('Initial setup state')

    #--------------------------------------
    # Function Name: TraceComponents
    # Purpose: Output debugging traces of the break wheel and the half rotor
    # Parameter: desc  A descriptive string printed in the trace dump
    #--------------------------------------
    def TraceComponents(self, desc):
        self.break_wheel.Dump(desc, self.trace)
        self.half_rotor.Dump(desc)
        
    #--------------------------------------
    # Function Name: Decipher
    # Purpose: Decipher a list of ciphertext elements
    # Parameter: ct  A list of ciphertext elements, taken from the set of 
    #            the major and minor alphabet ciphertext elements
    #--------------------------------------
    def Decipher(self, ct):
        complete_pt = ''
        count = 0
        for e in ct:
            if self.trace:
                print('-----------------------------------------')
            sub = self.mono_map.ReturnSubstitution(e)
            if (sub == None):
                # Not found in minor alphabet, decipher with major alphabet
                pt = self.half_rotor.Decipher(e)
                if self.trace:
                    print('%d: %s -> %s' % (count, e, pt))  #debug
                complete_pt = complete_pt + pt + ' '
            else:
                # Found in minor alphabet
                complete_pt = complete_pt + sub + ' '
                if self.trace:
                    print('%d: %s -> %s' % (count, e, sub))  #debug

            count = count + 1
            slide = self.break_wheel.ReturnSlide()
            self.half_rotor.IncrementOffset(slide);
            if self.trace:
                print('slide=%d' % (slide)) #debug

            if (self.trace):
                self.TraceComponents('After deciphering')

        return complete_pt

#--------------------------------------
# Name: unit_test_01
# Purpose: Verify complete cycle of breakwheel slides
#--------------------------------------
def unit_test_01():
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

#--------------------------------------
# Name: unit_test_02
# Purpose: Verify break wheel slide computation wraps correctly at end of pin list
#          when the last pin is inactive.
#--------------------------------------
def unit_test_02():
    number_of_pins = 47
    inactive_pin_list = [47]
    break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

    break_wheel.SetPinNumber(46)
    slide = break_wheel.ReturnSlide()
    if slide != 2:
        print('unit_test_02: Failure: Expected slide of 2, received %d instead' % (slide))
        return

    print('unit_test_02: Success')

#--------------------------------------
# Name: unit_test_03
# Purpose: Verify break wheel slide computation wraps correctly at end of pin list when the
#          last and first two pins are all inactive.
#--------------------------------------
def unit_test_03():
    number_of_pins = 47
    inactive_pin_list = [1, 2, 47]
    break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

    break_wheel.SetPinNumber(1)
    slide = break_wheel.ReturnSlide()
    if slide != 2:
        print('unit_test_03: Failure: Expected slide of 2, received %d instead' % (slide))
        return

    break_wheel.SetPinNumber(46)
    slide = break_wheel.ReturnSlide()
    if slide != 4:
        print('unit_test_03: Failure: Expected slide of 4, received %d instead' % (slide))
        return

    print('unit_test_03: Success')

#--------------------------------------
# Name: unit_test_04
# Purpose: Verify break wheel slide computation is correct for many consecutive inactive pins
#--------------------------------------
def unit_test_04():
    number_of_pins = 10
    inactive_pin_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

    break_wheel.SetPinNumber(1)
    slide = break_wheel.ReturnSlide()
    if slide != 10:
        print('unit_test_04: Failure: Expected slide of 10, received %d instead' % (slide))
        return

    print('unit_test_04: Success')
    
#--------------------------------------
# Name: main
# Purpose: Perform unit tests
#--------------------------------------
def main():
    unit_test_01()
    unit_test_02()
    unit_test_03()
    unit_test_04()
    
if __name__ == "__main__":
    main()
    