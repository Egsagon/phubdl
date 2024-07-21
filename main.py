import phub
from concurrent import futures
from rich.progress import Progress

INPUT = 'input.txt'
OUTPUT = './output'
THREADS = 4

with open(INPUT) as file:
    urls = file.read().split()

client = phub.Client()

with (
    Progress() as progress,
    futures.ThreadPoolExecutor(THREADS) as pool
):
    def download(url: str) -> None:
        
        video = client.get(url)
        task = progress.add_task(video.id)
        
        def display(cur: int, total: int):
            progress.update(task, completed = cur)
        
        video.download(
            path = f'{OUTPUT}/{video.id}.mp4',
            display = display
        )
        
        progress.remove_task(task)
    
    threads = [pool.submit(download, url) for url in urls]
    
    for thread in futures.as_completed(threads):
        thread.result()

print('Download completed.')

# EOF