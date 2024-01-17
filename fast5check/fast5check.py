import typer
from rich.console import Console
import h5py
import os

app = typer.Typer()
console = Console()

@app.command()
def check_fast5_files(directory: str, rename: bool = typer.Option(False, help="Enable renaming of corrupted files")):
    output_file = "fast5_truncation_check.txt"
    with open(output_file, 'w') as log, console.status("[bold green]Processing files...") as status:
        for filename in os.listdir(directory):
            if filename.endswith(".fast5"):
                file_path = os.path.join(directory, filename)
                try:
                    with h5py.File(file_path, 'r'):
                        log.write(f"{filename}: PASS\n")
                        console.print(f"{filename}: [bold green]PASS")
                except OSError:
                    log.write(f"{filename}: FAIL\n")
                    status_msg = f"{filename}: [bold red]FAIL"
                    if rename:
                        new_filename = filename + ".corrupted"
                        os.rename(file_path, os.path.join(directory, new_filename))
                        status_msg += f", renamed to {new_filename}"
                    console.print(status_msg)

if __name__ == "__main__":
    app()
