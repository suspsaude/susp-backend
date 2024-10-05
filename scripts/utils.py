from datetime import datetime

def progress_bar(current: int, total: int, startedAt: datetime, prefix: str = "", suffix: str = "", length: int = 20, fill: str = "=", printEnd: str = "\r") -> None:
    """
    Print a progress bar to the console.

    Args:
    current (int): current progress
    total (int): total progress
    startedAt (datetime): start time
    prefix (str): prefix string
    suffix (str): suffix string
    length (int): character length of the progress bar
    fill (str): fill character
    printEnd (str): end character
    """
    percent = ("{0:.2f}").format(100 * (current / float(total)))
    filledLength = int(length * current // total)
    eta = int((datetime.now() - startedAt).seconds * (total - current) / current)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {eta}s {suffix}", end=printEnd)
    if current == total:
        print()