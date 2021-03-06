import japanese_ika_m_1
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--trace',
                        action='store_true',
                        dest='trace',
                        help='Trace IKA components (for debugging purposes)'
                        )    
    args = parser.parse_args()

    major_alphabet = ['KI', 'HI', 'WO', 'MI', 'KE', 'TO', 'SA', 'KO', 'SE', 'HO',
                      'MU', 'NO', 'YO', 'RU', 'KA', 'FU', 'RE', 'RA', 'YA', 'SI',
                      'HA', 'TU',  'N',  'U',  'A',  'I', 'MA', 'TE', 'WA', 'MO',
                      'ME', 'KU',  'E', 'NA', 'TA', 'NI', 'YU', 'TI', 'RI', 'NE',
                      'HE', 'SU']
    minor_alphabet = {'RO': 'parenthesis', 'WI': 'RO', 'SO': 'Nigori', 'NU': 'Hannigori', 
                      'O': 'SO', 'WE': 'NU', 'X': 'Stop'}
    ct = ['SA', 'NO', 'TI', 'NO', 'SE', 'RE', 'KE', 'KI', 'WO', 'RU',
          'NA', 'HE', 'RE', 'WA', 'E',  'TA', 'MA', 'TA', 'KU', 'SA', 
          'A',  'TE', 'KO', 'NE', 'SI', 'A',  'NI', 'FU', 'SU', 'A', 
          'MA', 'YU', 'YO', 'SE', 'KE', 'SE', 'SA', 'RA', 'TU', 'SI', 
          'HI', 'YA', 'MA', 'YO', 'FU', 'YA', 'YO', 'NA', 'HO', 'WA', 
          'MU', 'HO', 'MO', 'MU', 'KI', 'MU', 'WA', 'U',  'YA', 'TO', 
          'ME', 'TE', 'HE', 'NO', 'RU', 'SE', 'NE', 'MI', 'SO', 'SA', 
          'TA', 'I',  'KA', 'HI', 'NO', 'YU', 'ME', 'KU', 'RA', 'KE', 
          'WA', 'ME', 'ME', 'N',  'HI', 'X',  'KE', 'SI', 'X',  'TO', 
          'ME', 'NA', 'HO', 'YO', 'KO', 'SA', 'A',  'NU', 'KE', 'ME', 
          'TI', 'KU', 'ME', 'YU', 'NE', 'KI', 'TI', 'O',  'HA', 'NI', 
          'TE', 'MA', 'WA', 'MI', 'TI', 'KA', 'HA', 'RE', 'HI', 'MA', 
          'MO', 'TU', 'MO', 'SI', 'NO', 'SE', 'SU', 'KO', 'MU', 'TE', 
          'E',  'YU', 'HE', 'TA', 'KE', 'SA', 'SE', 'TA', 'NI', 'RA', 
          'A',  'SI', 'RA', 'SE', 'SA', 'MO', 'TA', 'KU', 'N',  'TO', 
          'HI', 'FU', 'KU', 'MU', 'YU', 'HO', 'YU', 'SA', 'MA', 'TE', 
          'TO', 'KA', 'RI', 'O',  'TE', 'YU', 'YA', 'YU', 'MA', 'ME', 
          'A',  'TI', 'KO', 'HO', 'SI', 'KA', 'YO', 'MU', 'SI', 'HA', 
          'WA', 'YO', 'MA', 'HO', 'YA', 'YO', 'TU', 'NE', 'N']
    inactive_pin_list = [5, 8, 11, 17, 22, 25, 26, 29, 34, 37, 41, 44, 46]
    ika = japanese_ika_m_1.IkaMachine(major_alphabet, 10, minor_alphabet, 47, inactive_pin_list, trace=args.trace)
    pt = ika.Decipher(ct)
    print("\npt = '%s'" % (pt))

if __name__ == "__main__":
    main()
