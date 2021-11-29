import unittest

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

        try:
            self.Verify()
        except:
            raise Exception('MonoalphabeticMapping: verification failed')

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

        try:
            self.Verify()
        except:
            raise Exception('BreakWheel: verification failed')

    #--------------------------------------
    # Function Name: Verify
    # Purpose: Validate the data definitions passed to the constructor
    #--------------------------------------
    def Verify(self):
        return True

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
# Field: mono_map  A dictionary mapping ciphertext to plaintext items
#--------------------------------------
class MonoalphabeticMapping:
    def __init__(self, mono_map):
        self.decipher_mono_map = {}
        for key, value in mono_map.items():
            self.decipher_mono_map[key.upper()] = value.upper()

        try:
            self.Verify()
        except:
            raise Exception('MonoalphabeticMapping: verification failed')

        # Create mapping for enciphering
        self.encipher_mono_map = {}
        for key, value in mono_map.items():
            self.encipher_mono_map[value.upper()] = key.upper()

    #--------------------------------------
    # Function Name: Verify
    # Purpose: Validate the data definitions passed to the constructor
    #--------------------------------------
    def Verify(self):
        # Verify that no value is used multiple times
        value_set = set()
        for key, value in self.decipher_mono_map.items():
            if value in value_set:
                # Duplicate value
                print('MonoalphabeticMapping: The value "%s" occurs twice' % (value))
                raise Exception('MonoalphabeticMapping: Duplicate value encountered ("%s")' % (value))
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
# Field: half_rotor  Instatiated Damm half rotor object
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
                self.TraceComponents('After deciphering')

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

# --------------------------------------
#   Unit tests
# --------------------------------------

class TestIka(unittest.TestCase):

    # --------------------------------------
    # Name: test_breakwheel_01
    # Purpose: Verify complete cycle of breakwheel slides
    # --------------------------------------
    def test_breakwheel_01(self):
        number_of_pins = 47
        inactive_pin_list = [5, 8, 11, 17, 22, 25, 26, 29, 34, 37, 41, 44, 46]
        break_wheel = BreakWheel(number_of_pins, inactive_pin_list)
        expected_slides = [1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1,
                           2, 2, 1]

        starting_pin = break_wheel.ReturnCurrentPin()

        expected_slide_offset = 0
        while True:
            current_pin = break_wheel.ReturnCurrentPin()
            slide = break_wheel.ReturnSlide()
            self.assertEqual(expected_slides[expected_slide_offset], slide)
            if break_wheel.ReturnCurrentPin() == starting_pin:
                break
            expected_slide_offset = (expected_slide_offset + 1) % len(expected_slides)

    # --------------------------------------
    # Name: test_breakwheel_02
    # Purpose: Verify break wheel slide computation wraps correctly at end of pin list
    #          when the last pin is inactive.
    # --------------------------------------
    def test_breakwheel_02(self):
        number_of_pins = 47
        inactive_pin_list = [47]
        break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

        break_wheel.SetPinNumber(46)
        slide = break_wheel.ReturnSlide()
        self.assertEqual(slide, 2)

    # --------------------------------------
    # Name: test_breakwheel_03
    # Purpose: Verify break wheel slide computation wraps correctly at end of pin list when the
    #          last and first two pins are all inactive.
    # --------------------------------------
    def test_breakwheel_03(self):
        number_of_pins = 47
        inactive_pin_list = [1, 2, 47]
        break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

        break_wheel.SetPinNumber(1)
        slide = break_wheel.ReturnSlide()
        self.assertEqual(slide, 2)

        break_wheel.SetPinNumber(46)
        slide = break_wheel.ReturnSlide()
        self.assertEqual(slide, 4)

    # --------------------------------------
    # Name: test_breakwheel_04
    # Purpose: Verify break wheel slide computation is correct for many consecutive inactive pins
    # --------------------------------------
    def test_breakwheel_04(self):
        number_of_pins = 10
        inactive_pin_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        break_wheel = BreakWheel(number_of_pins, inactive_pin_list)

        break_wheel.SetPinNumber(1)
        slide = break_wheel.ReturnSlide()
        self.assertEqual(slide, 10)

    def test_decipher_01(self):
        major_alphabet = ['KI', 'HI', 'WO', 'MI', 'KE', 'TO', 'SA', 'KO', 'SE', 'HO',
                          'MU', 'NO', 'YO', 'RU', 'KA', 'FU', 'RE', 'RA', 'YA', 'SI',
                          'HA', 'TU', 'N', 'U', 'A', 'I', 'MA', 'TE', 'WA', 'MO',
                          'ME', 'KU', 'E', 'NA', 'TA', 'NI', 'YU', 'TI', 'RI', 'NE',
                          'HE', 'SU']
        minor_alphabet = {'RO': 'parenthesis', 'WI': 'RO', 'SO': 'Nigori', 'NU': 'Hannigori',
                          'O': 'SO', 'WE': 'NU', 'X': 'Stop'}
        ct = ['SA', 'NO', 'TI', 'NO', 'SE', 'RE', 'KE', 'KI', 'WO', 'RU',
              'NA', 'HE', 'RE', 'WA', 'E', 'TA', 'MA', 'TA', 'KU', 'SA',
              'A', 'TE', 'KO', 'NE', 'SI', 'A', 'NI', 'FU', 'SU', 'A',
              'MA', 'YU', 'YO', 'SE', 'KE', 'SE', 'SA', 'RA', 'TU', 'SI',
              'HI', 'YA', 'MA', 'YO', 'FU', 'YA', 'YO', 'NA', 'HO', 'WA',
              'MU', 'HO', 'MO', 'MU', 'KI', 'MU', 'WA', 'U', 'YA', 'TO',
              'ME', 'TE', 'HE', 'NO', 'RU', 'SE', 'NE', 'MI', 'SO', 'SA',
              'TA', 'I', 'KA', 'HI', 'NO', 'YU', 'ME', 'KU', 'RA', 'KE',
              'WA', 'ME', 'ME', 'N', 'HI', 'X', 'KE', 'SI', 'X', 'TO',
              'ME', 'NA', 'HO', 'YO', 'KO', 'SA', 'A', 'NU', 'KE', 'ME',
              'TI', 'KU', 'ME', 'YU', 'NE', 'KI', 'TI', 'O', 'HA', 'NI',
              'TE', 'MA', 'WA', 'MI', 'TI', 'KA', 'HA', 'RE', 'HI', 'MA',
              'MO', 'TU', 'MO', 'SI', 'NO', 'SE', 'SU', 'KO', 'MU', 'TE',
              'E', 'YU', 'HE', 'TA', 'KE', 'SA', 'SE', 'TA', 'NI', 'RA',
              'A', 'SI', 'RA', 'SE', 'SA', 'MO', 'TA', 'KU', 'N', 'TO',
              'HI', 'FU', 'KU', 'MU', 'YU', 'HO', 'YU', 'SA', 'MA', 'TE',
              'TO', 'KA', 'RI', 'O', 'TE', 'YU', 'YA', 'YU', 'MA', 'ME',
              'A', 'TI', 'KO', 'HO', 'SI', 'KA', 'YO', 'MU', 'SI', 'HA',
              'WA', 'YO', 'MA', 'HO', 'YA', 'YO', 'TU', 'NE', 'N']
        inactive_pin_list = [5, 8, 11, 17, 22, 25, 26, 29, 34, 37, 41, 44, 46]
        try:
            ika = IkaMachine(major_alphabet, 10, minor_alphabet, 47, inactive_pin_list, trace=False)
        except:
            print('Exception caught, check output')
            return
        pt_string = ika.Decipher(ct)
        pt = pt_string.split()
        self.assertEqual(len(pt), len(ct))

        expected_pt_start = ['RE', 'N', 'KO', 'A', 'U', 'E', 'N', 'SI']
        expected_pt_end = ['A', 'TA', 'YO', 'RI']

        for i in range(len(expected_pt_start)):
            self.assertEqual(pt[i], expected_pt_start[i])

        for i in range(len(expected_pt_end)):
            ind = len(pt) - len(expected_pt_end) + i
            self.assertEqual(pt[ind], expected_pt_end[i])

    def test_decipher_02(self):
        major_alphabet = ['ki', 'hi', 'wo', 'mi', 'ke', 'to', 'sa', 'ko', 'se', 'ho',
                          'MU', 'NO', 'YO', 'RU', 'KA', 'FU', 'RE', 'RA', 'YA', 'SI',
                          'ha', 'tu', 'n', 'u', 'a', 'i', 'ma', 'te', 'wa', 'mo',
                          'ME', 'KU', 'E', 'NA', 'TA', 'NI', 'YU', 'TI', 'RI', 'NE',
                          'he', 'su']
        minor_alphabet = {'RO': 'parenthesis', 'WI': 'RO', 'SO': 'nigori', 'NU': 'Hannigori',
                          'o': 'so', 'we': 'nu', 'x': 'stop'}
        ct = ['SA', 'NO', 'TI', 'NO', 'SE', 'RE', 'KE', 'KI', 'WO', 'RU',
              'NA', 'HE', 'RE', 'WA', 'E', 'TA', 'MA', 'TA', 'KU', 'SA']
        inactive_pin_list = [5, 8, 11, 17, 22, 25, 26, 29, 34, 37, 41, 44, 46]
        try:
            ika = IkaMachine(major_alphabet, 10, minor_alphabet, 47, inactive_pin_list, trace=False)
        except:
            print('Exception caught, check output')
            return
        pt_string = ika.Decipher(ct)
        pt = pt_string.split()
        self.assertEqual(len(pt), len(ct))

        expected_pt_start = ['RE', 'N', 'KO', 'A', 'U', 'E', 'N', 'SI']
        expected_pt_end = ['MA', 'TA', 'KU', 'SA']

        for i in range(len(expected_pt_start)):
            self.assertEqual(pt[i], expected_pt_start[i])

        for i in range(len(expected_pt_end)):
            ind = len(pt) - len(expected_pt_end) + i
            self.assertEqual(pt[ind], expected_pt_end[i])

    def test_encipher_01(self):
        major_alphabet = ['KI', 'HI', 'WO', 'MI', 'KE', 'TO', 'SA', 'KO', 'SE', 'HO',
                          'MU', 'NO', 'YO', 'RU', 'KA', 'FU', 'RE', 'RA', 'YA', 'SI',
                          'HA', 'TU', 'N', 'U', 'A', 'I', 'MA', 'TE', 'WA', 'MO',
                          'ME', 'KU', 'E', 'NA', 'TA', 'NI', 'YU', 'TI', 'RI', 'NE',
                          'HE', 'SU']
        minor_alphabet = {'RO': 'parenthesis', 'WI': 'RO', 'SO': 'Nigori', 'NU': 'Hannigori',
                          'O': 'SO', 'WE': 'NU', 'X': 'Stop'}
        pt = ['RE', 'N', 'KO', 'A', 'U', 'E', 'N', 'SI', 'U', 'NI', 'KA',
              'N', 'SU', 'RU', 'YA', 'TU', 'KA', 'A', 'N', 'KI', 'SI',
              'A', 'TO', 'RI', 'SI', 'MA', 'RI', 'HA', 'TO', 'KU', 'NI',
              'KE', 'A', 'N', 'SI', 'A', 'U', 'NI', 'SU', 'HE', 'A', 'KI',
              'MU', 'NE', 'HI', 'TO', 'KI', 'U', 'KI', 'HA', 'MI', 'KE',
              'I', 'HO', 'KI', 'YO', 'KU', 'TE', 'U', 'YO', 'RI', 'TI',
              'HO', 'U', 'TE', 'U', 'KA', 'N', 'Nigori', 'TE', 'KA', 'SA',
              'NE', 'TE', 'NE', 'U', 'SI', 'TU', 'SE', 'RI', 'TU', 'I',
              'MA', 'SI', 'SU', 'Stop', 'TO', 'U', 'Stop', 'YO', 'RI',
              'KI', 'SI', 'A', 'HA', 'TU', 'HE', 'Hannigori', 'U', 'SE',
              'RA', 'RU', 'RU', 'HA', 'A', 'WA', 'I', 'SO', 'NO', 'TE',
              'TU', 'TU', 'A', 'KI', 'NI', 'KA', 'TU', 'YA', 'KE', 'KU',
              'NI', 'ME', 'NE', 'KU', 'A', 'N', 'KA', 'A', 'WA', 'TO',
              'NO', 'RE', 'N', 'RA', 'KU', 'NI', 'RI', 'U', 'I', 'SE',
              'RA', 'RU', 'RU', 'TO', 'TO', 'MO', 'NI', 'NA', 'I', 'MU',
              'KO', 'N', 'NE', 'HA', 'TO', 'U', 'HO', 'U', 'WO', 'KE',
              'I', 'YU', 'SI', 'SO', 'NO', 'TU', 'TO', 'A', 'RE', 'N',
              'RA', 'KU', 'WO', 'TO', 'RA', 'RU', 'RU', 'YO', 'U', 'I',
              'TA', 'SI', 'TA', 'SI', 'MO', 'A', 'TA', 'YO', 'RI']
        inactive_pin_list = [5, 8, 11, 17, 22, 25, 26, 29, 34, 37, 41, 44, 46]

        try:
            ika = IkaMachine(major_alphabet, 10, minor_alphabet, 47, inactive_pin_list, trace=False)
        except:
            print('Exception caught, check output')
            return
        ct_string = ika.Encipher(pt)
        ct = ct_string.split()
        self.assertEqual(len(pt), len(ct))

        expected_ct_start = ['SA', 'NO', 'TI', 'NO', 'SE', 'RE', 'KE', 'KI']
        expected_ct_end = ['YA', 'YO', 'TU', 'NE', 'N']

        for i in range(len(expected_ct_start)):
            self.assertEqual(ct[i], expected_ct_start[i])

        for i in range(len(expected_ct_end)):
            ind = len(ct) - len(expected_ct_end) + i
            self.assertEqual(ct[ind], expected_ct_end[i])

if __name__ == "__main__":
    unittest.main()