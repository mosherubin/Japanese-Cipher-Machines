import japanese_ika_m_1
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data',
                        help='JSON file containing IKA data'
                        )
    parser.add_argument('-t', '--trace',
                        action='store_true',
                        dest='trace',
                        help='Trace IKA components (for debugging purposes)'
                        )    
    args = parser.parse_args()

    # Opening JSON file
    f = open(args.data)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    ika = japanese_ika_m_1.IkaMachine(
        data['major_alphabet'],
        data['starting_offset'],
        data['minor_alphabet'],
        data['number_of_pins'],
        data['inactive_pin_list'],
        trace=args.trace)
    pt = ika.Decipher(data['ct'])
    print("\npt = '%s'" % (pt))

if __name__ == "__main__":
    main()
