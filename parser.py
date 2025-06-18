import argparse
import sys

def create_argument_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(description='Script to hide messages in PDFs')
    
    # Add arguments
    parser.add_argument('--i', '--input', 
                       required=True,
                       help='Input PDF file')
    
    parser.add_argument('--o', '--output', 
                       required=True,
                       help='Output PDF file')
    
    parser.add_argument('--m', '--mode',
                       choices=['t', 'text', 'f', 'file'],
                       required=True,
                       help='Mode: t/text for text, f/file for file')
    
    parser.add_argument('--t', '--text', 
                       help='Message to hide in PDF (required if mode=text)')
    
    parser.add_argument('--f', '--file',
                       help='File to hide in PDF (required if mode=file)')
    
    parser.add_argument('--e', '--encryption',
                       help='Encryption key (optional)')
    
    return parser

def validate_args(args):
    """Validate arguments based on selected mode"""
    mode = getattr(args, 'mode', None) or getattr(args, 'm', None)
    # Normalize mode values
    if mode in ['t', 'text']:
        if not (getattr(args, 'text', None) or getattr(args, 't', None)):
            raise argparse.ArgumentTypeError("--message/-m is required when mode is 'text' or 't'")
    elif mode in ['f', 'file']:
        if not (getattr(args, 'file', None) or getattr(args, 'f', None)):
            raise argparse.ArgumentTypeError("--file/--f is required when mode is 'file' or 'f'")
    
    return args



def create_arguments_extract():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(description='Script to hide messages in PDFs')
    
    # Add arguments
    parser.add_argument('--i', '--input', 
                       required=True,
                       help='Input PDF file')
    
    parser.add_argument('--m', '--mode',
                       choices=['t', 'text', 'f', 'file'],
                       required=True,
                       help='Mode: t/text for text, f/file for file')
    
    parser.add_argument('--e', '--encryption',
                       help='Encryption key (optional)')
    
    return parser
