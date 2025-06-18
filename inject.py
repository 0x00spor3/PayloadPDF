from injector.injector import PDFHiddenObjectInjector
from logger.logger import OutputManager
from converter.converter import PDFTraditionalConverter
from parser import create_argument_parser, validate_args
from pathlib import Path
import argparse

if __name__ == "__main__":
    logger = OutputManager()
    logger.print_banner()

    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        args = validate_args(args)

        input_file = getattr(args, 'input', None) or getattr(args, 'i', None)
        output_file = getattr(args, 'output', None) or getattr(args, 'o', None)
        mode = getattr(args, 'mode', None) or getattr(args, 'm', None)
        message = getattr(args, 'text', None) or getattr(args, 't', None)
        file_path = getattr(args, 'file', None) or getattr(args, 'f', None)
        encryption_key = getattr(args, 'encryption', None) or getattr(args, 'e', None)
        has_encryption = bool(encryption_key)

        tmp = "temp.pdf"
        converter = PDFTraditionalConverter()
        if converter.convert_pdf(input_file, tmp):
            inj = PDFHiddenObjectInjector()

            if mode in ['t', 'text']:
                inj.inject_hidden_object(tmp, output_file, message, has_encryption, encryption_key) 
            if mode in ['f', 'file']:
                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
                    inj.inject_hidden_object_file(tmp, output_file, file_bytes, Path(file_path).name, has_encryption, encryption_key) 

    except argparse.ArgumentTypeError as e:
        parser.error(str(e))
        parser.print_help()
