import japanese_ika_m_1
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data',
                        help='JSON file containing IKA data'
                        )
    parser.add_argument('--decipher',
                        action='store_true',
                        help='Decipher the ciphertext into plaintext'
                        )
    parser.add_argument('--encipher',
                        action='store_true',
                        help='Encipher the plaintext into ciphertext'
                        )
    parser.add_argument('-t', '--trace',
                        action='store_true',
                        dest='trace',
                        help='Trace IKA components (for debugging purposes)'
                        )    
    args = parser.parse_args()

    if args.decipher and args.encipher:
        print('Error: both --decipher and --encipher were specified')
        sys.exit(-1)

    if not args.decipher and not args.encipher:
        print('Error: neither --decipher nor --encipher were specified')
        sys.exit(-1)

    # Opening JSON file
    f = open(args.data)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    try:
        ika = japanese_ika_m_1.IkaMachine(
            data['major_alphabet'],
            data['starting_offset'],
            data['minor_alphabet_encipher'],
            data['number_of_pins'],
            data['inactive_pin_list'],
        trace=args.trace)
    except:
        print('Exception caught, exiting')
        sys.exit(-1)

    if args.decipher:
        pt = ika.Decipher(data['ct'])
        print("\npt = '%s'" % (pt))
    elif args.encipher:
        ct = ika.Encipher(data['pt'])
        print("\nct = '%s'" % (ct))

if __name__ == "__main__":
    main()
