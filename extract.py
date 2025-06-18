from parser import create_arguments_extract
from logger.logger import OutputManager
from extractor.extractor import PDFHiddenMessageExtractor

if __name__ == "__main__":
    logger = OutputManager()
    logger.print_banner()

    parser = create_arguments_extract()
    args = parser.parse_args()


    input_file = getattr(args, 'input', None) or getattr(args, 'i', None)
    mode = getattr(args, 'mode', None) or getattr(args, 'm', None)
    encryption_key = getattr(args, 'encryption', None) or getattr(args, 'e', None)
    has_encryption = bool(encryption_key)

    ext = PDFHiddenMessageExtractor()
    if mode in ['t', 'text']:
        ext.extract_all_hidden_objects(input_file, has_encryption, encryption_key)
    if mode in ['f', 'file']:
        ext.extract_all_hidden_objects_file(input_file, has_encryption, encryption_key)

