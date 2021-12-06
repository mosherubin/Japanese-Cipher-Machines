# --------------------------------------
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
# --------------------------------------
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
        if not self.alphabet:
            raise Exception('DammHalfRotor: Alphabet is empty')

        if self.offset < 0:
            raise Exception('DammHalfRotor: Offset is < 0')

        if self.offset >= len(self.alphabet):
            raise Exception('DammHalfRotor: Offset exceeds alphabet size')

        # Make sure there are no duplicate or empty string elements in self.alphabet
        element_set = set()
        for e in self.alphabet:
            if e in element_set:
                raise Exception('DammHalfRotor: Duplicate element "%s" encountered' % (e))
            if not e:
                raise Exception('DammHalfRotor: Empty string element encountered')
            element_set.add(e)

        return True

    # --------------------------------------
    # Function Name: SetAbsoluteOffset
    # Purpose: Set the offset of self.alphabet against itself
    # Parameter: offset  The offset of self.alphabet against itself
    # --------------------------------------
    def SetAbsoluteOffset(self, offset):
        self.offset = offset

    # --------------------------------------
    # Function Name: IncrementOffset
    # Purpose: Increment the current offset value
    # Parameter: increment  The delta by which to increment self.offset
    # --------------------------------------
    def IncrementOffset(self, increment):
        self.offset = (self.offset + increment) % len(self.alphabet)

    # --------------------------------------
    # Function Name: Encipher
    # Purpose: Encipher a given plaintext <element>, given the current
    #          state of the IKA machine
    # Parameter: element  The plaintext element to be enciphered
    # Returns: The enciphered element (i.e., the ciphertext element)
    # --------------------------------------
    def Encipher(self, element):
        index1 = self.alphabet.index(element.upper())
        if index1 < 0:
            raise Exception('Encipher: Element "%s"" not found in Damm half rotor' % (element))
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
        if index1 < 0:
            raise Exception('Decipher: Element "%s"" not found in Damm half rotor' % (element))
        index2 = (index1 + self.offset) % len(self.alphabet)
        return self.alphabet[index2]

    # --------------------------------------
    # Function Name: Dump
    # Purpose: A debugging function for tracing the state of this class
    # Parameter: desc  A descriptive string printed in the trace dump
    # --------------------------------------
    def Dump(self, desc):
        print('\nDumping Damm half rotor: %s' % (desc))
        for a in self.alphabet:
            print(a.ljust(self.max_element_length) + ' ', end='')
        print()

        for i in range(len(self.alphabet)):
            offset = (self.offset + i) % len(self.alphabet)
            print(self.alphabet[offset].ljust(self.max_element_length) + ' ', end='')
        print()
