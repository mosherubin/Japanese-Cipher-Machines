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
        self.alphabet = [x.upper() for x in alphabet]
        self.offset = offset

        self.Verify()

        # Determine longest alphabet element
        self.max_element_length = 0
        for a in alphabet:
            if len(a) > self.max_element_length:
                self.max_element_length = len(a)

    # --------------------------------------
    # Function Name: Verify
    # Purpose: Validate the data definitions passed to the constructor
    # --------------------------------------
    def Verify(self):
        if self.offset < 0:
            print('Offset is < 0 for DammHalfRotor, throwing exception')
            raise Exception('DammHalfRotor: Offset is < 0')

        if self.offset >= len(self.alphabet):
            print('Offset exceeds alphabet size for DammHalfRotor, throwing exception')
            raise Exception('DammHalfRotor: Offset exceeds alphabet size')

        # Make sure there are no duplicate elements in self.alphabet
        element_set = set()
        for e in self.alphabet:
            if e in element_set:
                print('DammHalfRotor: Duplicate element "%s" encountered' % (e))
                raise Exception('DammHalfRotor: Duplicate element "%s" encountered' % (e))
            element_set.add(e)

        return True

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
    # Function Name: Encipher
    # Purpose: Encipher a given plaintext <element>, given the current
    #          state of the IKA machine
    # Parameter: element  The plaintext element to be enciphered
    # Returns: The enciphered element (i.e., the ciphertext element)
    #--------------------------------------
    def Encipher(self, element):
        index1 = self.alphabet.index(element.upper())
        index2 = (index1 - self.offset) % len(self.alphabet)
        return self.alphabet[index2]

    # --------------------------------------
    # Function Name: Decipher
    # Purpose: Decipher a given ciphertext <element>, given the current
    #          state of the IKA machine
    # Parameter: element  The ciphertext element to be deciphered
    # Returns: The deciphered element (i.e., the plaintext element)
    # --------------------------------------
    def Decipher(self, element):
        index1 = self.alphabet.index(element.upper())
        index2 = (index1 + self.offset) % len(self.alphabet)
        return self.alphabet[index2]

    #--------------------------------------
    # Function Name: Dump
    # Purpose: A debugging function for tracing the state of this class
    # Parameter: desc  A descriptive string printed in the trace dump
    #--------------------------------------
    def Dump(self, desc):
        print('\nDumping Damm half rotor: %s' % (desc))
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

        self.Verify()

    #--------------------------------------
    # Function Name: Verify
    # Purpose: Validate the data definitions passed to the constructor
    #--------------------------------------
    def Verify(self):
        if self.total_num_pins < 1:
            raise Exception('BreakWheel has invalid number of pins (%d)' % self.total_num_pins)

        if len(self.inactive_pins) > self.total_num_pins:
            raise Exception('BreakWheel has more inactive pins (%d) than total pins (%d)' %
                (len(self.inactive_pins), self.total_num_pins))

        # Make sure there are no duplicate elements in self.inactive_pins
        pin_set = set()
        for i in self.inactive_pins:
            if i in pin_set:
                raise Exception('BreakWheel: Duplicate inactive pin "%d" encountered' % (i))
            pin_set.add(i)

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
        print('\nDumping break wheel: %s' % (desc))
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

#--------------------------------------
# Class Name: MonoalphabeticMapping
# Purpose: Perform a monoalphabetic mapping of ciphertext strings to their plaintext phrases
# Field: mono_map  A dictionary mapping plaintext to ciphertext items
#--------------------------------------
class MonoalphabeticMapping:
    def __init__(self, encipher_mono_map):
        self.encipher_mono_map = {}
        for key, value in encipher_mono_map.items():
            self.encipher_mono_map[key.upper()] = value.upper()

        # Create mapping for deciphering
        self.decipher_mono_map = {}
        for key, value in encipher_mono_map.items():
            self.decipher_mono_map[value.upper()] = key.upper()

        self.Verify()

    #--------------------------------------
    # Function Name: Verify
    # Purpose: Validate the data definitions passed to the constructor
    #--------------------------------------
    def Verify(self):
        # Verify that no value is used multiple times in <decipher_mono_map>
        value_set = set()
        for key, value in self.encipher_mono_map.items():
            if value in value_set:
                # Duplicate value
                print('MonoalphabeticMapping: The value "%s" occurs twice in encipher_mono_map' % (value))
                raise Exception('MonoalphabeticMapping: Duplicate value encountered in encipher_mono_map ("%s")' % (value))
            value_set.add(value)

        # Verify that no value is used multiple times in <decipher_mono_map>
        value_set = set()
        for key, value in self.decipher_mono_map.items():
            if value in value_set:
                # Duplicate value
                print('MonoalphabeticMapping: The value "%s" occurs twice in encipher_mono_map' % (value))
                raise Exception('MonoalphabeticMapping: Duplicate value encountered in encipher_mono_map ("%s")' % (value))
            value_set.add(value)

        return True

    #--------------------------------------
    # Function Name: ReturnDecipheredValue
    # Purpose: Return decipherment of <element>
    # Parameter: element  The ciphertext element to decipher
    # Returns: The deciphered element (i.e., plaintext element) if exists,
    #          else None
    #--------------------------------------
    def ReturnDecipheredValue(self, element):
        if element.upper() in self.decipher_mono_map:
            return self.decipher_mono_map[element.upper()]
        else:
            return None

    #--------------------------------------
    # Function Name: ReturnEncipheredValue
    # Purpose: Return encipherment of <element>
    # Parameter: element  The plaintext element to encipher
    # Returns: The enciphered element (i.e., ciphertext element) if exists,
    #          else None
    #--------------------------------------
    def ReturnEncipheredValue(self, element):
        if element.upper() in self.encipher_mono_map:
            return self.encipher_mono_map[element.upper()]
        else:
            return None

    # --------------------------------------
    # Function Name: Dump
    # Purpose: A debugging function for tracing the state of this class
    # Parameter: desc  A descriptive string printed in the trace dump
    # --------------------------------------
    def Dump(self, desc):
        print('\nDumping monoalphabet map: %s' % (desc))

        print('\nDecipher mapping')
        for key, value in self.decipher_mono_map.items():
            print("%s -> %s" % (key, value))
        print()

        print('\nEncipher mapping')
        for key, value in self.encipher_mono_map.items():
            print("%s -> %s" % (key, value))
        print()

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
# Field: number_of_pins  The total number of pins defined for the break wheel
# Field: inactive_pins  A list of integers denoting the inactive pins (the
#        numbers are 1-based, not 0-based)
# Field: half_rotor  Instantiated Damm half rotor object
# Field: break_wheel  Instantiated break wheel object
#--------------------------------------
class IkaMachine:
    def __init__(self, major_alphabet, starting_offset, minor_alphabet, number_of_pins, inactive_pin_list, **kwargs):
        self.trace = kwargs['trace']

        self.major_alphabet = major_alphabet
        self.starting_offset = starting_offset
        self.minor_alphabet = minor_alphabet
        self.number_of_pins = number_of_pins
        self.inactive_pin_list = inactive_pin_list

        try:
            self.half_rotor = DammHalfRotor(self.major_alphabet, self.starting_offset)
            self.mono_map = MonoalphabeticMapping(self.minor_alphabet)
            self.break_wheel = BreakWheel(self.number_of_pins, self.inactive_pin_list)
        except:
            raise Exception('IkaMachine: constructor failed')

        if self.trace:
            desc = 'Initial setup state'
            self.TraceComponents(desc)
            self.mono_map.Dump(desc)
            print("starting_offset = %d" % self.starting_offset)
            print("number_of_pins = %d" % self.number_of_pins)
            print("inactive_pin_list = %s" % (str(self.inactive_pin_list)))

    #--------------------------------------
    # Function Name: TraceComponents
    # Purpose: Output debugging traces of the break wheel and the half rotor
    # Parameter: desc  A descriptive string printed in the dump
    #--------------------------------------
    def TraceComponents(self, desc):
        self.break_wheel.Dump(desc, self.trace)
        self.half_rotor.Dump(desc)

    #--------------------------------------
    # Function Name: Encipher
    # Purpose: Encipher a list of plaintext elements
    # Parameter: ct  A list of plaintext elements, taken from the set of
    #            the major and minor alphabet plaintext elements
    #--------------------------------------
    def Encipher(self, pt):
        complete_ct = ''
        count = 0
        for e in pt:
            if self.trace:
                print('-----------------------------------------')
            sub = self.mono_map.ReturnEncipheredValue(e.upper())
            if (sub == None):
                # Not found in minor alphabet, decipher with major alphabet
                ct = self.half_rotor.Encipher(e.upper())
                if self.trace:
                    print('%d: %s -> %s' % (count, e, ct))  #debug
                complete_ct = complete_ct + ct + ' '
            else:
                # Found in minor alphabet
                complete_ct = complete_ct + sub + ' '
                if self.trace:
                    print('%d: %s -> %s' % (count, e, sub))  #debug

            count = count + 1
            slide = self.break_wheel.ReturnSlide()
            self.half_rotor.IncrementOffset(slide);
            if self.trace:
                print('slide=%d' % (slide)) #debug

            if (self.trace):
                self.TraceComponents('After enciphering')

        return complete_ct

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
            sub = self.mono_map.ReturnDecipheredValue(e)
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
