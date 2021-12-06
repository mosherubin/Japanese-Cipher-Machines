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
        # Verify that no value is used multiple times in <encipher_mono_map>
        value_set = set()
        for key, value in self.encipher_mono_map.items():
            if value in value_set:
                # Duplicate value
                raise Exception('MonoalphabeticMapping: Duplicate value ("%s") encountered in encipher_mono_map' % (value))
            value_set.add(value)

        # Verify no key is the empty string
        if '' in self.encipher_mono_map:
            raise Exception('MonoalphabeticMapping: Key of empty string encountered in encipher_mono_map')

        # Verify that no key is the empty string
        for key, value in self.encipher_mono_map.items():
            if not value:
                raise Exception('MonoalphabeticMapping: Key "%s" has value of empty string' % (key))

        return True

    #--------------------------------------
    # Function Name: Decipher
    # Purpose: Return decipherment of <element>
    # Parameter: element  The ciphertext element to decipher
    # Returns: The deciphered element (i.e., plaintext element) if exists,
    #          else None
    #--------------------------------------
    def Decipher(self, element):
        if element.upper() in self.decipher_mono_map:
            return self.decipher_mono_map[element.upper()]
        else:
            return None

    #--------------------------------------
    # Function Name: Encipher
    # Purpose: Return encipherment of <element>
    # Parameter: element  The plaintext element to encipher
    # Returns: The enciphered element (i.e., ciphertext element) if exists,
    #          else None
    #--------------------------------------
    def Encipher(self, element):
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
