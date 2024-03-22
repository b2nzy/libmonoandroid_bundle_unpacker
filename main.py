import argparse
from elftools.elf.elffile import ELFFile
from io import BytesIO
import gzip
import os

def decompress_data(input_file, output_directory):
    with open(input_file, 'rb') as file:
        data = file.read()

    f = BytesIO(data)
    elffile = ELFFile(f)
    section = elffile.get_section_by_name('.dynsym')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for symbol in section.iter_symbols():
        if symbol['st_shndx'] != 'SHN_UNDEF' and symbol.name.startswith('assembly_data_'):
            print(symbol.name)
            dll_data = data[symbol['st_value']:symbol['st_value']+symbol['st_size']]
            dll_data = gzip.decompress(dll_data)
            with open(os.path.join(output_directory, symbol.name[14:].replace('_dll', '.dll')), 'wb') as outfile:
                outfile.write(dll_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decompress data from .so file')
    parser.add_argument('-i', '--input', help='Input .so file path', required=True)
    parser.add_argument('-o', '--output', help='Output directory path', required=True)
    args = parser.parse_args()

    decompress_data(args.input, args.output)
