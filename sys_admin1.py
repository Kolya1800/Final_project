import os
import shutil
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def organize_files(directory):
    logging.info(f'Organizing files in {directory} by type')
    
    # Define file type directories
    file_types = {
        'text_files': ['.txt'],
        'log_files': ['.log'],
        'image_files': ['.jpg', '.jpeg', '.png'],
        'pdf_files': ['.pdf'],
    }

    # Create directories for each file type
    for folder, extensions in file_types.items():
        folder_path = os.path.join(directory, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Move files to the corresponding directory
        for filename in os.listdir(directory):
            if any(filename.endswith(ext) for ext in extensions):
                src_path = os.path.join(directory, filename)
                dest_path = os.path.join(folder_path, filename)
                shutil.move(src_path, dest_path)
                logging.info(f'Moved {filename} to {folder_path}')

    logging.info('Directory organization complete.')

def monitor_logs(log_file):
    logging.info(f'Monitoring {log_file} for critical messages')
    
    critical_messages = []
    with open(log_file, 'r') as file:
        for line in file:
            if "Error" in line or "Critical" in line:
                critical_messages.append(line.strip())
                logging.warning(f'Critical message found: "{line.strip()}"')

    # Log critical messages to a summary file
    if critical_messages:
        with open('error_summary.log', 'w') as summary_file:
            for message in critical_messages:
                summary_file.write(message + '\n')
        logging.info('Logged critical messages to error_summary.log.')

def main():
    parser = argparse.ArgumentParser(description='System Administration Script')
    subparsers = parser.add_subparsers(dest='command')

    # Directory organization command
    organize_parser = subparsers.add_parser('organize')
    organize_parser.add_argument('--dir', type=str, help='Directory to organize')
    organize_parser.add_argument('--log-monitor', type=str, help='Log file to monitor')

    args = parser.parse_args()

    if args.command == 'organize':
        if args.dir:
            organize_files(args.dir)
        if args.log_monitor:
            monitor_logs(args.log_monitor)

if __name__ == '__main__':
    main()