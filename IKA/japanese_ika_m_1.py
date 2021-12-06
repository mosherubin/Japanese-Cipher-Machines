import os
import sys

# Add path to 'common' folder to enable importing components
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir + os.path.sep + 'common')))

from damm_half_rotor import DammHalfRotor
from break_wheel import BreakWheel
from monoalphabetic_mapping import MonoalphabeticMapping

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
            sub = self.mono_map.Encipher(e.upper())
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
            sub = self.mono_map.Decipher(e)
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
