import argparse
import hadoopy_utils
import sys


def _parse():
    parser = argparse.ArgumentParser(description='Hadoopy Utils')
    parser.add_argument('cmd', type=str,
                        help='Input command (e.g., dir2seqtb)')
    args = parser.parse_args(sys.argv[1:2])
    return args.cmd
    
if __name__ == '__main__':
    cmd = _parse()
    print('---------------')
    print(sys.argv[2:])
    if cmd == 'dir2seqtb':
        hadoopy_utils.dir2seqtb.main(sys.argv[2:])
