import subprocess
import datetime
import os

def download_file(url, download_path, log_file):
    """
    Downloads a file from the given URL to the specified path and logs the download details.

    Args:
        url (str): The URL of the file to download.
        download_path (str): The directory where the file will be downloaded.
        log_file (str): The file where download details will be logged.
    """
    # Ensure the download path exists
    os.makedirs(download_path, exist_ok=True)

    # Extract the file name from the URL
    output_file = os.path.join(download_path, os.path.basename(url))

    # Download the file using wget
    command = ["wget", "-P", download_path, url]
    subprocess.run(command, check=True)

    # Get the current date and time
    download_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log the date and version information
    with open(log_file, "a") as log:
        log.write(f"Download Date: {download_date}\n")
        log.write(f"Downloaded File: {output_file}\n")
        log.write("-" * 40 + "\n")

    print(f"Download completed and logged successfully: {output_file}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python dl_ref_genome.py <url> <download_path> <log_file>")
        sys.exit(1)

    url = sys.argv[1]
    download_path = sys.argv[2]
    log_file = sys.argv[3]

    download_file(url, download_path, log_file)

