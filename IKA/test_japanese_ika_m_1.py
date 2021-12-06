import unittest
import japanese_ika_m_1 as ika

# The following global variables (all prefixed by "christensen_")
# were taken from Chris Christensen's article entitled
# "The Imperial Japanese navy IKA Cipher Machine" in "Proceedings
# of the 4th International Conference on Historical Cryptology,
# HistoCrypt 2021" (https://ecp.ep.liu.se/index.php/histocrypt/article/view/155).

christensen_major_alphabet = [
    'KI', 'HI', 'WO', 'MI', 'KE', 'TO', 'SA', 'KO', 'SE', 'HO',
    'MU', 'NO', 'YO', 'RU', 'KA', 'FU', 'RE', 'RA', 'YA', 'SI',
    'HA', 'TU', 'N', 'U', 'A', 'I', 'MA', 'TE', 'WA', 'MO',
    'ME', 'KU', 'E', 'NA', 'TA', 'NI', 'YU', 'TI', 'RI', 'NE',
    'HE', 'SU']

christensen_minor_alphabet_encipher = {
    'parenthesis': 'RO',
    'RO': 'WI',
    'Nigori': 'SO',
    'Hannigori': 'NU',
    'SO': 'O',
    'NU': 'WE',
    'Stop': 'X'}

christensen_ct = [
    'SA', 'NO', 'TI', 'NO', 'SE', 'RE', 'KE', 'KI', 'WO', 'RU',
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

christensen_pt = [
    'RE', 'N', 'KO', 'A', 'U', 'E', 'N', 'SI', 'U', 'NI', 'KA',
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

christensen_total_number_pins = 47
christensen_inactive_pin_list = [5, 8, 11, 17, 22, 25, 26, 29, 34, 37, 41, 44, 46]

# --------------------------------------
#   Unit tests
# --------------------------------------

class TestIka(unittest.TestCase):

    # --------------------------------------
    # Name: test_decipher_01
    # Purpose: Sanity test for deciphering, major alphabet and ciphertext are all
    #          uppercase.
    # --------------------------------------
    def test_decipher_01(self):
        ikaMachine = ika.IkaMachine(
            christensen_major_alphabet,
            10,
            christensen_minor_alphabet_encipher,
            christensen_total_number_pins,
            christensen_inactive_pin_list,
            trace=False)
        pt_string = ikaMachine.Decipher(christensen_ct)
        pt = pt_string.split()
        self.assertEqual(len(pt), len(christensen_ct))

        expected_pt_start = ['RE', 'N', 'KO', 'A', 'U', 'E', 'N', 'SI']
        expected_pt_end = ['A', 'TA', 'YO', 'RI']

        for i in range(len(expected_pt_start)):
            self.assertEqual(pt[i], expected_pt_start[i])

        for i in range(len(expected_pt_end)):
            ind = len(pt) - len(expected_pt_end) + i
            self.assertEqual(pt[ind], expected_pt_end[i])

    # --------------------------------------
    # Name: test_decipher_02
    # Purpose: Sanity test for deciphering, major alphabet, minor encipherment
    #          mapping, and ciphertext all contain both uppercase and lowercase
    #          characters.
    # --------------------------------------
    def test_decipher_02(self):
        major_alphabet = ['ki', 'hi', 'wo', 'mi', 'ke', 'to', 'sa', 'ko', 'se', 'ho',
                          'MU', 'NO', 'YO', 'RU', 'KA', 'FU', 'RE', 'RA', 'YA', 'SI',
                          'ha', 'tu', 'n', 'u', 'a', 'i', 'ma', 'te', 'wa', 'mo',
                          'ME', 'KU', 'E', 'NA', 'TA', 'NI', 'YU', 'TI', 'RI', 'NE',
                          'he', 'su']
        minor_alphabet_encipher = {'parenthesis': 'RO', 'RO': 'WI', 'nigori': 'SO', 'Hannigori': 'NU',
                                   'so': 'o', 'nu': 'we', 'stop': 'x'}
        ct = ['SA', 'NO', 'Ti', 'NO', 'SE', 're', 'KE', 'KI', 'WO', 'rU',
              'NA', 'he', 'RE', 'WA', 'e', 'ta', 'MA', 'TA', 'Ku', 'sA']
        ikaMachine = ika.IkaMachine(
            major_alphabet,
            10,
            minor_alphabet_encipher,
            christensen_total_number_pins,
            christensen_inactive_pin_list,
            trace=False)
        pt_string = ikaMachine.Decipher(ct)
        pt = pt_string.split()
        self.assertEqual(len(pt), len(ct))

        expected_pt_start = ['RE', 'N', 'KO', 'A', 'U', 'E', 'N', 'SI']
        expected_pt_end = ['KA', 'A', 'N', 'KI']

        for i in range(len(expected_pt_start)):
            self.assertEqual(pt[i], expected_pt_start[i])

        for i in range(len(expected_pt_end)):
            ind = len(pt) - len(expected_pt_end) + i
            self.assertEqual(pt[ind], expected_pt_end[i])

    # --------------------------------------
    # Name: test_encipher_01
    # Purpose: Sanity test for enciphering, major alphabet and ciphertext are
    #          all in uppercase.
    # --------------------------------------
    def test_encipher_01(self):
        try:
            ikaMachine = ika.IkaMachine(
                christensen_major_alphabet,
                10,
                christensen_minor_alphabet_encipher,
                christensen_total_number_pins,
                christensen_inactive_pin_list,
                trace=False)
        except:
            print('test_encipher_01: Exception caught, check output')
            return
        ct_string = ikaMachine.Encipher(christensen_pt)
        ct = ct_string.split()
        self.assertEqual(len(christensen_pt), len(ct))

        expected_ct_start = ['SA', 'NO', 'TI', 'NO', 'SE', 'RE', 'KE', 'KI']
        expected_ct_end = ['YA', 'YO', 'TU', 'NE', 'N']

        for i in range(len(expected_ct_start)):
            self.assertEqual(ct[i], expected_ct_start[i])

        for i in range(len(expected_ct_end)):
            ind = len(ct) - len(expected_ct_end) + i
            self.assertEqual(ct[ind], expected_ct_end[i])

if __name__ == "__main__":
    unittest.main()