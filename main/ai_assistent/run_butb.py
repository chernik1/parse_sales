import asyncio
import replicate
import time

async def run_model(prompt, system_prompt):
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": prompt,
            "system_prompt": system_prompt,
        }
    )

    loop = asyncio.get_running_loop()
    iterator = await loop.run_in_executor(None, lambda: iter(output))

    for item in iterator:
        print(item, end="")

async def main():
    # Задаём 10 разных запросов
    tasks = [
        run_model(f"привет {i}", "Отвечай только нет нет нет")
        for i in range(50)
    ]
    await asyncio.gather(*tasks)
time_start = time.time()
# Запускаем асинхронную функцию main
asyncio.run(main())
time_end = time.time()
print(time_end - time_start)