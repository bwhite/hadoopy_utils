import hadoopy
import os
import subprocess
import argparse


def _run(cmd, root_dir):
    read_fd, write_fd = os.pipe()
    read_fp = os.fdopen(read_fd, 'r')
    p = subprocess.Popen(cmd.split(), stdin=read_fp, close_fds=True)
    with hadoopy.TypedBytesFile(write_fd=write_fd) as tb_fp:
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                print(file_path)
                with open(file_path) as data_fp:
                    tb_fp.write((file_path, data_fp.read()))
        tb_fp.flush()
    p.wait()


def _parse(args):
    parser = argparse.ArgumentParser(description='Convert a directory of data into a sequence file of TypedBytes with key=file_path value=file_data')
    parser.add_argument('dir_in', type=str, 
                        help='Input directory')
    parser.add_argument('seq_out', type=str,
                        help='Output sequence file path')
    args = parser.parse_args(args)
    return args.dir_in, args.seq_out


def main(args):
    dir_in, seq_out = _parse(args)
    cmd = 'hadoop jar /home/brandyn/hadoop-0.20.2+320/contrib/streaming/hadoop-streaming-0.20.2-cdh3u0.jar loadtb %s' % seq_out
    _run(cmd, dir_in)


