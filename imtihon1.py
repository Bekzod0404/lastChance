import asyncio
import os
import httpx


class FileManager:
    def __init__(self, file_path, mode):
        self.file_path = file_path
        self.mode = mode

    def __enter__(self):
        self.file = open(file=self.file_path, mode=self.mode)
        return self.file

    def __exit__(self, *args, **kwargs):
        self.file.close()

    def __next__(self):
        line = self.file.readline()
        if not line:
            self.file.close()
            raise StopIteration
        return line.strip()

    def __iter__(self):
        self.file = open(file=self.file_path, mode=self.mode)
        return self


async def send_request(url, data):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        return response.status_code

if __name__ == '__main__':
    url = 'http://164.92.64.76/desc/'
    fruits = []

    for file_name in os.listdir("descriptions"):
        file_path = f"descriptions/{file_name}"

        with FileManager(file_path, "r") as file:
            file_data = [line.strip() for line in file]

        data = {
            "name": file_data[0],
            "price": int(file_data[1].split()[0]),
            "text": file_data[2]
        }
        fruits.append(data)

    with FileManager("Response {file_name}.txt", "w") as f:
        for fruit in fruits:
            status_code = asyncio.run(send_request(url, fruit))
            f.write(f"Response {file_name} {status_code}\n")

